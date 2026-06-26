#!/usr/bin/env python3
"""
Odaily Skill 工具入口
用法: python run.py <tool_name> [json_args]
示例: python run.py get_today_watch '{"limit": 10}'
      python run.py get_crypto_market_analysis '{"focus": "overview"}'
"""

import sys
import json
import os

# 把 skill 目录加到 path，使 config/lib/tools 可以直接 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TOOLS = {
    # M1 今日必关注
    "get_today_watch": ("tools.odaily_news", "get_today_watch"),
    # M2 加密市场分析（含宏观）
    "get_crypto_market_analysis": ("tools.market_trend", "get_crypto_market_analysis"),
    # M3 明日关注
    "get_tomorrow_watch": ("tools.tomorrow_watch", "get_tomorrow_watch"),
    # M4 预测市场异动 + 巨鲸尾盘跟单
    "scan_whale_tail_trades": ("tools.whale_trades", "scan_whale_tail_trades"),
    # M5 API模块化调用
    "get_api_module": ("tools.api_module", "get_api_module"),
    # 向后兼容别名
    "get_odaily_headlines": ("tools.odaily_news", "get_odaily_headlines"),
    "get_market_trend_analysis": ("tools.market_trend", "get_market_trend_analysis"),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("可用工具:")
        for name in TOOLS:
            print(f"  {name}")
        print("\n用法: python run.py <tool_name> [json_args]")
        return

    tool_name = sys.argv[1]
    if tool_name not in TOOLS:
        print(f"错误: 未知工具 '{tool_name}'")
        print(f"可用工具: {', '.join(TOOLS.keys())}")
        sys.exit(1)

    args = {}
    if len(sys.argv) > 2:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(f"错误: JSON 参数解析失败 — {e}")
            sys.exit(1)

    module_path, func_name = TOOLS[tool_name]
    module = __import__(module_path, fromlist=[func_name])
    func = getattr(module, func_name)

    try:
        result = func(**args)
        print(result)
    except Exception as e:
        print(f"❌ 工具执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
