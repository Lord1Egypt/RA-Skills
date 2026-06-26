#!/usr/bin/env python3
"""
Feishu Calendar 使用示例
"""

def example_1_list_events():
    """示例 1: 查看日程"""
    print("=" * 60)
    print("示例 1: 查看今日日程")
    print("=" * 60)
    print("使用：feishu_calendar_event --action list")
    print("--start_time 2026-03-16T00:00:00+08:00")
    print("--end_time 2026-03-16T23:59:59+08:00\n")

def example_2_create_event():
    """示例 2: 创建日程"""
    print("=" * 60)
    print("示例 2: 创建日程")
    print("=" * 60)
    print("使用：feishu_calendar_event --action create")
    print("--summary \"团队会议\"")
    print("--start_time \"2026-03-17T14:00:00+08:00\"")
    print("--end_time \"2026-03-17T15:00:00+08:00\"\n")

def example_3_check_freebusy():
    """示例 3: 查询忙闲"""
    print("=" * 60)
    print("示例 3: 查询忙闲")
    print("=" * 60)
    print("使用：feishu_calendar_freebusy --action list")
    print("--time_min \"2026-03-17T09:00:00+08:00\"")
    print("--time_max \"2026-03-17T18:00:00+08:00\"")
    print("--user_ids \"ou_xxx\"\n")

if __name__ == "__main__":
    example_1_list_events()
    example_2_create_event()
    example_3_check_freebusy()
    print("✅ 所有示例运行完成!")
