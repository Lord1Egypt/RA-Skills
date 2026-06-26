#!/usr/bin/env python3
"""
AI 分析和下注决策 v2
- 使用 ai_model_v2 的新策略
- 用期望值（EV）决定是否下注，而不是固定阈值
"""
import sys
import json
from datetime import datetime, timezone

sys.path.insert(0, "/root/.openclaw/workspace/polymarket-arb-bot")

from ai_trader.ai_model_v2 import analyze_market
import subprocess


def log_decision(slug, coin, ptb, direction, confidence, up_odds, down_odds, details):
    """记录决策到统计文件"""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "coin": coin,
        "ptb": ptb,
        "direction": direction,
        "confidence": confidence,
        "up_odds": up_odds,
        "down_odds": down_odds,
        "ev": details.get("expected_value", 0),
        "price_diff_pct": details.get("price_diff_pct", 0),
        "diff_in_atr": details.get("diff_in_atr", 0),
        "current_price": details.get("current_price", 0),
        "total_score": details.get("total_score", 0),
    }

    with open("logs/decisions_v2.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")


def analyze_and_decide(coin, price_to_beat, up_odds, down_odds, slug):
    """
    执行 AI 分析并返回决策

    返回: (should_bet, direction, confidence, details)
    """
    direction, confidence, details = analyze_market(
        coin, price_to_beat, up_odds, down_odds
    )

    if not direction:
        return False, None, 0, details

    # 记录决策
    log_decision(slug, coin, price_to_beat, direction, confidence, up_odds, down_odds, details)

    # ── 下注条件（5分钟市场专用策略） ──
    # 无法止盈止损，必须高准确率
    # 1. 置信度 >= 85%（更高质量信号）
    # 2. EV > 0.6（更强期望值）
    # 3. 赔率 < 0.85（不买太贵的）
    target_odds = up_odds if direction == "UP" else down_odds
    ev = details.get("expected_value", 0)

    should_bet = (
        confidence >= 0.85
        and ev > 0.6
        and target_odds < 0.85
    )

    details["should_bet"] = should_bet
    details["bet_reason"] = (
        f"conf={confidence:.0%} ev={ev:+.3f} odds={target_odds:.3f}"
    )

    return should_bet, direction, confidence, details


def execute_bet(slug, direction, token_id, amount=None):
    """执行下注（通过 Polymarket CLI）
    
    Args:
        slug: 市场 slug（用于日志）
        direction: UP 或 DOWN
        token_id: 代币 ID
        amount: 下注金额（美元），None则自动计算为余额的2%
    """
    # 获取当前余额
    if amount is None:
        try:
            result = subprocess.run(
                ["polymarket", "clob", "balance", "--signature-type", "gnosis-safe", "--asset-type", "collateral"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                # 解析余额（格式：Balance: $5.05）
                import re
                match = re.search(r'Balance: \$([0-9.]+)', result.stdout)
                if match:
                    balance = float(match.group(1))
                    amount = max(1, int(balance * 0.01))  # 1%，最小$1（测试阶段）
                else:
                    amount = 1  # 默认$1
            else:
                amount = 1
        except:
            amount = 1
    
    # 获取当前价格
    try:
        import requests
        resp = requests.get(f"https://clob.polymarket.com/midpoint?token_id={token_id}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            price = float(data.get('mid', 0.5))
        else:
            price = 0.5  # 默认价格
    except:
        price = 0.5
    
    # 价格四舍五入到2位小数（Polymarket要求）
    price = round(price, 2)
    
    # 固定5份（Polymarket最小值），实盘测试阶段保持最小仓位
    size = 5
    
    cmd = [
        "polymarket", "clob", "create-order",
        "--signature-type", "gnosis-safe",
        "--token", token_id,
        "--side", "buy",
        "--price", str(price),
        "--size", str(size),
    ]

    print(f"  💸 下注命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    
    success = result.returncode == 0
    output = result.stdout if success else result.stderr
    
    # 记录下注结果
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "direction": direction,
        "token_id": token_id,
        "price": price,
        "size": size,
        "amount": price * size,
        "success": success,
        "output": output[:200],  # 截断输出
    }
    
    with open("logs/bets.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    # 如果下注成功，记录持仓
    if success:
        position = {
            "token_id": token_id,
            "slug": slug,
            "direction": direction,
            "entry_price": price,
            "size": size,
            "entry_time": datetime.now(timezone.utc).isoformat(),
            "closed": False
        }
        with open("logs/positions.jsonl", "a") as f:
            f.write(json.dumps(position) + "\n")
    
    return success, output


if __name__ == "__main__":
    if len(sys.argv) > 1:
        coin = sys.argv[1]
        ptb = float(sys.argv[2])
        up_odds = float(sys.argv[3])
        down_odds = float(sys.argv[4])

        should_bet, direction, confidence, details = analyze_and_decide(
            coin, ptb, up_odds, down_odds, "test"
        )

        print(f"Direction: {direction}")
        print(f"Confidence: {confidence*100:.1f}%")
        print(f"Should bet: {should_bet}")
        print(f"EV: {details.get('expected_value', 0):+.3f}")
        print(f"Details: {json.dumps(details, indent=2)}")
