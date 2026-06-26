#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""支撑压力位交易策略 - Python 编排脚本

功能:
1. 启用策略时与用户确认参数
2. 查看当前策略状态和持仓信息
3. 停止策略

用法:
  python sr_strategy.py --enable                    # 启用策略(交互式确认参数)
  python sr_strategy.py --status                    # 查看策略状态
  python sr_strategy.py --stop                      # 停止策略

注意: 本脚本不执行实际交易逻辑。策略由 MT4 端的 sr_strategy.mq4 EA 执行。
      Python 脚本仅负责参数管理和状态查询。
"""
import sys
import os
import json
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mt4_client import MT4Client

logger = logging.getLogger("sr_strategy")

# ---- 默认参数 ----
DEFAULT_CONFIG = {
    "max_loss_percent": 1.0,   # 最大亏损 %
    "entry_timeframe": "M15",  # 入场周期
    "breakout_thresh": 0.003,  # 突破阈值 0.3%
    "stop_thresh": 0.005,      # 止损阈值 0.5%
    "symbols": ["XAUUSD.s"],   # 交易品种
    "max_positions": 2,        # 每品种最大持仓
    "enabled": False           # 是否启用
}

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "sr_strategy_config.json")


def load_config():
    """加载配置，文件不存在则返回默认配置。"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error("读取配置失败: %s，使用默认配置", e)
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存配置。"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        logger.info("配置已保存到 %s", CONFIG_FILE)
    except OSError as e:
        logger.error("保存配置失败: %s", e)
        sys.exit(1)


def enable_strategy():
    """启用策略 — 交互式确认参数。"""
    config = load_config()

    print("\n" + "=" * 50)
    print("支撑压力位交易策略 - 参数确认")
    print("=" * 50)
    print(f"\n当前配置:")
    print(f"  1. 最大亏损%: {config['max_loss_percent']}%")
    print(f"  2. 入场周期: {config['entry_timeframe']}")
    print(f"  3. 突破阈值: {config['breakout_thresh'] * 100}%")
    print(f"  4. 止损阈值: {config['stop_thresh'] * 100}%")
    print(f"  5. 交易品种: {config['symbols']}")
    print(f"  6. 每品种最大持仓: {config['max_positions']}")

    print("\n按回车使用默认值，或输入新值:")

    try:
        val = input(f"1. 最大亏损% [{config['max_loss_percent']}]: ").strip()
        if val:
            config['max_loss_percent'] = float(val)

        val = input(f"2. 入场周期 [{config['entry_timeframe']}]: ").strip()
        if val:
            config['entry_timeframe'] = val.upper()

        val = input(f"3. 突破阈值% [{config['breakout_thresh'] * 100}]: ").strip()
        if val:
            config['breakout_thresh'] = float(val) / 100

        val = input(f"4. 止损阈值% [{config['stop_thresh'] * 100}]: ").strip()
        if val:
            config['stop_thresh'] = float(val) / 100

        val = input(f"5. 交易品种 [{','.join(config['symbols'])}]: ").strip()
        if val:
            config['symbols'] = [s.strip() for s in val.split(',')]

        val = input(f"6. 每品种最大持仓 [{config['max_positions']}]: ").strip()
        if val:
            config['max_positions'] = int(val)

    except KeyboardInterrupt:
        print("\n已取消")
        return
    except ValueError as e:
        print(f"❌ 输入格式错误: {e}")
        return

    config['enabled'] = True
    save_config(config)

    print("\n" + "=" * 50)
    print("✅ 策略已启用!")
    print("=" * 50)
    print(f"配置已保存到: {CONFIG_FILE}")
    print("\n策略将在 MT4 中自动运行。")
    print("请确保 sr_strategy.mq4 EA 已挂载到图表上。")


def show_status():
    """显示策略状态和当前持仓。"""
    config = load_config()

    print("\n" + "=" * 50)
    print("支撑压力位交易策略 - 状态")
    print("=" * 50)
    print(f"\n策略状态: {'✅ 已启用' if config.get('enabled') else '❌ 未启用'}")

    if not config.get('enabled'):
        return

    print(f"\n配置参数:")
    print(f"  最大亏损%: {config['max_loss_percent']}%")
    print(f"  入场周期: {config['entry_timeframe']}")
    print(f"  突破阈值: {config['breakout_thresh'] * 100}%")
    print(f"  止损阈值: {config['stop_thresh'] * 100}%")
    print(f"  交易品种: {config['symbols']}")
    print(f"  每品种最大持仓: {config['max_positions']}")

    c = MT4Client()

    # 查询当前持仓
    print(f"\n当前持仓:")
    try:
        r = c.get_positions()
        if r.get('count', 0) == 0:
            print("  无持仓")
        else:
            for p in r.get('positions', []):
                if p.get('symbol') in config.get('symbols', []):
                    print(f"  {p['symbol']} {p['type']} {p['lots']}手 @ {p['price']} "
                          f"P/L: ${p.get('profit', 0):.2f}")
    except Exception as e:
        print(f"  ⚠️ 获取持仓失败: {e}")

    # 查询 SR 位
    print(f"\n支撑压力位:")
    for sym in config.get('symbols', []):
        try:
            sr = c.get_sr_levels(symbol=sym)
            if sr.get('status') == 'ok':
                print(f"  {sym}:")
                print(f"    阻力: {sr.get('resistance', [])}")
                print(f"    支撑: {sr.get('support', [])}")
            else:
                print(f"  {sym}: 获取失败 ({sr.get('error', '未知错误')})")
        except Exception as e:
            print(f"  {sym}: 获取失败 - {e}")


def stop_strategy():
    """停止策略。"""
    config = load_config()
    config['enabled'] = False
    save_config(config)
    print("✅ 策略已停止")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="支撑压力位交易策略")
    parser.add_argument("--enable", action="store_true", help="启用策略")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--stop", action="store_true", help="停止策略")

    args = parser.parse_args()

    if args.enable:
        enable_strategy()
    elif args.status:
        show_status()
    elif args.stop:
        stop_strategy()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()