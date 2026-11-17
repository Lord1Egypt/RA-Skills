#!/usr/bin/env python3
"""
PaperTrade + ONDO Perps 中性对冲机器人 - 入口

使用方法:
  1. 复制 .env.example 为 .env，填入私钥和 API 凭证
  2. pip install -r requirements.txt
  3. python main.py

子命令:
  python main.py              # 运行对冲机器人
  python main.py status       # 查看两个平台的账户状态
  python main.py close-all    # 平掉所有持仓
  python main.py register     # 仅注册 PaperTrade Session Key
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

from paper_client import PaperTradeClient, INSTRUMENTS
from ondo_client import OndoClient, OndoConfig
from hedge_bot import HedgeBot, HedgeConfig


def load_config() -> tuple:
    load_dotenv()

    mode = os.getenv("HEDGE_MODE", "real").lower()  # real | mock
    paper_key = os.getenv("PAPER_WALLET_PRIVATE_KEY", "")

    if mode == "mock":
        # 模拟模式：使用固定测试钱包，不需要真实凭证
        from mock_clients import MockPaperTradeClient, MockOndoClient
        # 使用固定测试私钥（仅用于模拟，不会进行真实交易）
        mock_private_key = "0x6e9d21376d0c7a1d267aa3c04068b5c90c2eb621e2aa696c54a3f2636f48cf8b"
        paper = MockPaperTradeClient(wallet_private_key=mock_private_key)
        ondo = MockOndoClient()
        print("[模式] 模拟模式 (Mock) - 不会进行真实交易")
    else:
        # 真实模式：需要完整凭证
        if not paper_key or paper_key == "your_private_key_here":
            print("错误: 请在 .env 中设置 PAPER_WALLET_PRIVATE_KEY")
            sys.exit(1)

        paper_session_key = os.getenv("PAPER_SESSION_KEY", "") or None

        ondo_key_id = os.getenv("ONDO_KEY_ID", "")
        ondo_secret = os.getenv("ONDO_API_SECRET", "")
        if not ondo_key_id or not ondo_secret:
            print("错误: 请在 .env 中设置 ONDO_KEY_ID 和 ONDO_API_SECRET")
            sys.exit(1)

        paper = PaperTradeClient(
            wallet_private_key=paper_key,
            session_key=paper_session_key,
        )
        ondo = OndoClient(OndoConfig(key_id=ondo_key_id, api_secret=ondo_secret))
        print("[模式] 真实模式 (Real) - 将进行真实交易")

    config = HedgeConfig(
        symbol=os.getenv("HEDGE_SYMBOL", "BTC"),
        position_size_usd=float(os.getenv("HEDGE_POSITION_SIZE", "50")),
        paper_leverage=int(os.getenv("HEDGE_PAPER_LEVERAGE", "10")),
        ondo_leverage=int(os.getenv("HEDGE_ONDO_LEVERAGE", "10")),
        target_move_pct=float(os.getenv("HEDGE_TARGET_MOVE_PCT", "1.0")),
        max_hold_seconds=int(os.getenv("HEDGE_MAX_HOLD_SECONDS", "3600")),
        poll_interval=int(os.getenv("HEDGE_POLL_INTERVAL", "10")),
        max_cycles=int(os.getenv("HEDGE_MAX_CYCLES", "200")),
        direction=os.getenv("HEDGE_DIRECTION", "random"),
    )

    return paper, ondo, config


def cmd_status(paper: PaperTradeClient, ondo: OndoClient):
    print("=" * 50)
    print("账户状态")
    print("=" * 50)

    # PaperTrade
    try:
        paper_bal = paper.get_balance_usd()
        paper_positions = paper.get_positions()
        paper_paper = paper.get_paper_minted()
        print(f"\n[PaperTrade] 钱包: {paper.wallet_address}")
        print(f"  余额: ${paper_bal:.4f}")
        print(f"  持仓数: {len(paper_positions)}")
        print(f"  PAPER: {paper_paper:.2f}")
        for p in paper_positions:
            print(f"    - id={p['positionId']} {'多' if p['isLong'] else '空'} "
                  f"${p['marginUsd']:.2f} x{p['leverage']} @ ${p['entryPrice']:.2f}")
    except Exception as e:
        print(f"[PaperTrade] 查询失败: {e}")

    # ONDO
    try:
        ondo_bal = ondo.get_balance()
        ondo_positions = ondo.get_positions()
        print(f"\n[ONDO]")
        print(f"  余额: {ondo_bal}")
        print(f"  持仓数: {len(ondo_positions)}")
        for p in ondo_positions:
            print(f"    - {p.get('market')}: size={p.get('size')} "
                  f"entry=${p.get('entryPrice', '?')} pnl=${p.get('unrealizedPnl', '?')}")
    except Exception as e:
        print(f"[ONDO] 查询失败: {e}")


def cmd_close_all(paper: PaperTradeClient, ondo: OndoClient):
    print("平掉所有持仓...")
    try:
        paper.close_all()
    except Exception as e:
        print(f"PaperTrade 平仓失败: {e}")
    try:
        ondo.close_all()
    except Exception as e:
        print(f"ONDO 平仓失败: {e}")
    print("完成")


def cmd_register(paper: PaperTradeClient):
    print("注册 PaperTrade Session Key...")
    sess = paper.register_session_key()
    print(f"Session Key: {sess.session_address}")
    print(f"过期时间: {sess.expiry}")
    # 保存 session key 到 .env
    print("请将以下变量添加到 .env:")
    print(f"PAPER_SESSION_KEY={sess.session_key}")


def main():
    paper, ondo, config = load_config()
    is_mock = os.getenv("HEDGE_MODE", "real").lower() == "mock"

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            cmd_status(paper, ondo)
        elif cmd == "close-all":
            cmd_close_all(paper, ondo)
        elif cmd == "register" and not is_mock:
            cmd_register(paper)
        elif cmd == "register" and is_mock:
            print("[模拟模式] 不需要注册 Session Key")
        else:
            print(f"未知命令: {cmd}")
            print("可用命令: status, close-all, register")
        return

    # 注册 Session Key（如果不存在，且非 mock 模式）
    if not is_mock and not paper.session:
        print("未检测到 Session Key，正在注册...")
        paper.register_session_key()

    # 运行对冲机器人
    bot = HedgeBot(paper, ondo, config)
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\n用户中断，正在清理...")
        bot._emergency_close()
    finally:
        bot.export_stats()


if __name__ == "__main__":
    main()
