#!/usr/bin/env python3
"""
MiniMax Token Plan 用量查询脚本

用法:
    python3 query.py <API_KEY>
    python3 query.py  # 从环境变量 MINIMAX_API_KEY 读取

注意: current_interval_usage_count 字段表示剩余配额，不是已用量！
"""

import json
import sys
import datetime
import urllib.request
import urllib.error

ENDPOINT = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"


def query_quota(api_key: str) -> dict:
    """查询 MiniMax Token Plan 额度"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        ENDPOINT,
        headers=headers,
        method="GET"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        sys.exit(1)


def format_time_ms(ms: int) -> str:
    """毫秒时间戳转可读格式"""
    seconds = ms / 1000
    hours = seconds / 3600
    days = seconds / 86400
    return f"{hours:.0f} 小时后（约 {days:.0f} 天）"


def format_window(start_ms: int, end_ms: int) -> str:
    """格式化时间窗口"""
    start = datetime.datetime.fromtimestamp(start_ms / 1000)
    end = datetime.datetime.fromtimestamp(end_ms / 1000)
    return f"{start.strftime('%m-%d %H:%M')} ~ {end.strftime('%H:%M')}"


def print_quota(data: dict):
    """格式化打印额度信息"""
    models = data.get('model_remains', [])
    
    print("=" * 50)
    print(" MiniMax Token Plan 用量查询")
    print("（注意：usage_count = 剩余配额）")
    print("=" * 50)
    
    for m in models:
        name = m.get('model_name', 'Unknown')
        total = m.get('current_interval_total_count', 0)
        # ⚠️ 关键：usage_count 是剩余配额，不是已用量
        remaining = m.get('current_interval_usage_count', 0)
        used = total - remaining
        pct = used * 100 // total if total > 0 else 0
        
        weekly_total = m.get('current_weekly_total_count', 0)
        weekly_remaining = m.get('current_weekly_usage_count', 0)
        weekly_used = weekly_total - weekly_remaining
        weekly_pct = weekly_used * 100 // weekly_total if weekly_total > 0 else 0
        
        remains_time = m.get('remains_time', 0)
        window_start = m.get('start_time', 0)
        window_end = m.get('end_time', 0)
        
        print(f"\n【{name}】")
        print(f" 5小时窗口：已用 {used} / {total}（{pct}%）剩余 {remaining} 次")
        if weekly_total > 0:
            print(f" 本周：已用 {weekly_used} / {weekly_total}（{weekly_pct}%）剩余 {weekly_remaining} 次")
        print(f" 窗口：{format_window(window_start, window_end)}")
        print(f" 重置：约 {format_time_ms(remains_time)}")
    
    print("\n" + "=" * 50)


def main():
    # 获取 API Key
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    elif os.environ.get("MINIMAX_API_KEY"):
        api_key = os.environ["MINIMAX_API_KEY"]
    else:
        print("用法: python3 query.py <API_KEY>")
        print("或设置环境变量 MINIMAX_API_KEY")
        sys.exit(1)
    
    print("查询中...")
    data = query_quota(api_key)
    
    if data.get('base_resp', {}).get('status_code') != 0:
        error_msg = data.get('base_resp', {}).get('status_msg', 'Unknown error')
        print(f"查询失败: {error_msg}")
        sys.exit(1)
    
    print_quota(data)


if __name__ == "__main__":
    import os
    main()
