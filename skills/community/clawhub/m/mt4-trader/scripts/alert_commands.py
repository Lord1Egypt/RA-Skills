#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格预警管理工具 - 支持子命令的统一 CLI

用法:
  python alert_commands.py add <类型> <品种> <值> [消息]
  python alert_commands.py list
  python alert_commands.py clear

子命令:
  add     添加预警
  list    列出所有预警
  clear   清除所有预警

快捷子命令（默认品种 BTCUSD）:
  python alert_commands.py above <值>           # 突破预警
  python alert_commands.py below <值>           # 跌破预警
  python alert_commands.py profit <值>          # 盈利预警

完整示例:
  python alert_commands.py add above BTCUSD 77000 "BTC 突破 77000"
  python alert_commands.py add profit 20         # 持仓盈利 $20
  python alert_commands.py list
  python alert_commands.py clear
"""
import json
import os
import sys
import logging

logger = logging.getLogger("alert_commands")

_DIR = os.path.dirname(os.path.abspath(__file__))
_ALERT_FILE = os.path.join(_DIR, "alerts.json")


def _load_alerts():
    """加载预警列表。"""
    if os.path.exists(_ALERT_FILE):
        try:
            with open(_ALERT_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            logger.error("读取预警文件失败: %s", e)
            return []
    return []


def _save_alerts(alerts):
    """保存预警列表。"""
    try:
        with open(_ALERT_FILE, "w") as f:
            json.dump(alerts, f, ensure_ascii=False, indent=2)
    except OSError as e:
        logger.error("保存预警文件失败: %s", e)
        sys.exit(1)


def cmd_list():
    """列出所有预警。"""
    alerts = _load_alerts()
    if not alerts:
        print("暂无预警。")
        return

    print(f"预警数量: {len(alerts)}")
    for i, a in enumerate(alerts):
        cond = a.get("condition", "?")
        msg = a.get("message", "")
        if a.get("price") is not None:
            detail = f"价格: {a['price']}"
        elif a.get("profit") is not None:
            detail = f"盈利: ${a['profit']}"
        else:
            detail = ""
        print(f"  {i+1}. [{cond}] {msg} ({detail})")


def cmd_clear():
    """清除所有预警。"""
    _save_alerts([])
    print("已清除所有预警。")


def cmd_add(condition, symbol, value, message=None):
    """
    添加预警。

    Args:
        condition: "above" | "below" | "profit"
        symbol: 品种代码
        value: 阈值（float）
        message: 自定义消息（可选）
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        print(f"❌ 无效的阈值: {value}，请输入数字。")
        sys.exit(1)

    alerts = _load_alerts()
    alert = {"condition": condition, "symbol": symbol.upper()}

    if condition == "profit":
        alert["profit"] = value
        alert["message"] = message or f"持仓盈利超过 ${value}"
    else:
        alert["price"] = value
        alert["message"] = message or f"{symbol} {condition} ${value}"

    alerts.append(alert)
    _save_alerts(alerts)
    print(f"✅ 已添加预警: {alert['message']}")


def _parse_args():
    """
    手动解析参数（保持轻量级，避免额外依赖）。
    不适用 argparse 是因为子命令的参数结构差异较大。
    """
    if len(sys.argv) < 2:
        _print_help()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd in ("list", "clear"):
        return cmd, None

    if cmd == "add" and len(sys.argv) >= 5:
        # add <condition> <symbol> <value> [message]
        return ("add", {
            "condition": sys.argv[2],
            "symbol": sys.argv[3],
            "value": sys.argv[4],
            "message": sys.argv[5] if len(sys.argv) > 5 else None,
        })

    # 快捷命令: above/below/profit <value>
    if cmd in ("above", "below", "profit") and len(sys.argv) >= 3:
        return ("add", {
            "condition": cmd,
            "symbol": "BTCUSD",  # 快捷命令默认 BTCUSD
            "value": sys.argv[2],
            "message": sys.argv[3] if len(sys.argv) > 3 else None,
        })

    print(f"❌ 未知命令或参数不足: {' '.join(sys.argv[1:])}")
    _print_help()
    sys.exit(1)


def _print_help():
    print(__doc__)


def main():
    cmd, args = _parse_args()

    if cmd == "list":
        cmd_list()
    elif cmd == "clear":
        cmd_clear()
    elif cmd == "add":
        cmd_add(**args)
    else:
        _print_help()


if __name__ == "__main__":
    main()