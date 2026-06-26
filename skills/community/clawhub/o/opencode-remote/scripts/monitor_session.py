#!/usr/bin/env python3
"""
OpenCode Session 监控脚本 - 最佳实践版本
基于经验教训：不要只查单条消息，要综合 todo 列表和消息状态
"""

import json
import subprocess
import sys
import time
from datetime import datetime

def curl_get(url, proxy="socks5://127.0.0.1:1080"):
    """使用 curl 获取数据"""
    try:
        cmd = ['curl', '-s', '--socks5-hostname', proxy, '--max-time', '15', url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            print(f"curl 错误: {result.stderr}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def check_session_status(base_url, session_id):
    """
    正确的监控逻辑：
    1. 优先检查 todo 列表
    2. 检查多条消息
    3. 对比消息 ID
    """
    print(f"\n{'='*60}")
    print(f"检查 Session: {session_id[:25]}...")
    print(f"时间: {datetime.now().strftime('%H:%M:%S')}")
    print('='*60)
    
    # 1. 检查 todo 列表（最准确）
    print("\n📋 Todo 列表状态:")
    todos = curl_get(f"{base_url}/session/{session_id}/todo")
    if todos:
        status_counts = {}
        for todo in todos:
            status = todo.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        total = len(todos)
        completed = status_counts.get('completed', 0)
        in_progress = status_counts.get('in_progress', 0)
        pending = status_counts.get('pending', 0)
        cancelled = status_counts.get('cancelled', 0)
        
        print(f"  总计: {total}")
        print(f"  ✅ 已完成: {completed}")
        print(f"  🔄 进行中: {in_progress}")
        print(f"  ⏳ 待处理: {pending}")
        if cancelled:
            print(f"  ❌ 已取消: {cancelled}")
        
        # 判断任务是否完成
        if completed == total:
            print("\n🎉 所有待办已完成！")
            return True
        elif completed + cancelled == total:
            print("\n✅ 任务完成（含取消项）")
            return True
    else:
        print("  无法获取 todo 列表")
    
    # 2. 检查最近消息（查多条，不要只查一条）
    print("\n💬 最近消息状态:")
    messages = curl_get(f"{base_url}/session/{session_id}/message?limit=3")
    if messages and len(messages) > 0:
        for i, msg in enumerate(messages[:3]):
            msg_id = msg.get('info', {}).get('id', 'N/A')[:15]
            completed_time = msg.get('info', {}).get('time', {}).get('completed')
            parts_count = len(msg.get('parts', []))
            
            status = "✅ 完成" if completed_time else "🔄 进行中"
            print(f"  [{i+1}] {msg_id}... - {status} ({parts_count} parts)")
        
        # 检查最新消息是否完成
        latest = messages[0]
        if latest.get('info', {}).get('time', {}).get('completed'):
            print("\n✓ 最新消息已完成")
    else:
        print("  无法获取消息")
    
    # 3. 获取 session 基本信息
    print("\n📊 Session 基本信息:")
    session = curl_get(f"{base_url}/session/{session_id}")
    if session:
        print(f"  标题: {session.get('title', 'N/A')}")
        print(f"  更新: {session.get('time', {}).get('updated', 'N/A')}")
    
    print("\n" + "-"*60)
    return False

def monitor_session(base_url, session_id, interval=300):
    """持续监控 session 直到完成"""
    print(f"开始监控 session: {session_id}")
    print(f"服务器: {base_url}")
    print(f"检查间隔: {interval} 秒\n")
    
    check_count = 0
    try:
        while True:
            check_count += 1
            print(f"\n第 {check_count} 次检查:")
            
            is_done = check_session_status(base_url, session_id)
            if is_done:
                print("\n✅ 监控完成！任务已结束。")
                break
            
            print(f"\n⏳ 等待 {interval} 秒后下次检查...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n监控被用户中断")
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python3 monitor_session.py <base_url> <session_id> [interval_seconds]")
        print("示例: python3 monitor_session.py http://host:port ses_xxx 300")
        sys.exit(1)
    
    base_url = sys.argv[1]
    session_id = sys.argv[2]
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    
    monitor_session(base_url, session_id, interval)
