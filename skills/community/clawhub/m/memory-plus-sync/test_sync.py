#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书消息同步
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from collector import MultiChannelCollector
from memory_plus import MemoryPlus

def test_feishu_sync():
    """测试飞书消息同步"""
    print("🧪 开始测试飞书消息同步...")
    
    # 1. 采集飞书消息
    print("1️⃣ 采集最近1小时的飞书消息...")
    mcc = MultiChannelCollector()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    try:
        messages = mcc.collect_and_merge(
            channels=['feishu'],
            start_time=start_time,
            end_time=end_time
        )
        print(f"✅ 采集到 {len(messages)} 条飞书消息")
        
        if not messages:
            print("⚠️  没有采集到飞书消息，可能原因：")
            print("   - chat_history 目录不存在或为空")
            print("   - 最近1小时内没有飞书消息")
            return False
            
        # 显示前几条消息
        for i, msg in enumerate(messages[:3]):
            print(f"  消息 {i+1}: {msg.get('content', '无内容')[:80]}...")
        
        # 2. 同步到记忆系统
        print("\n2️⃣ 同步消息到记忆系统...")
        mp = MemoryPlus()
        if mp.connect():
            mp.sync_from_channel('feishu', messages)
            mp.close()
            print("✅ 同步完成！")
            return True
        else:
            print("❌ 数据库连接失败")
            return False
            
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_chat_history():
    """检查 chat_history 目录"""
    chat_history_dir = Path.home() / '.openclaw' / 'workspace' / 'chat_history'
    print(f"\n📁 检查 chat_history 目录: {chat_history_dir}")
    
    if not chat_history_dir.exists():
        print("❌ chat_history 目录不存在")
        return False
    
    files = list(chat_history_dir.glob('*.json'))
    print(f"✅ 找到 {len(files)} 个聊天记录文件")
    
    if files:
        for i, f in enumerate(files[:3]):
            print(f"  文件 {i+1}: {f.name} (修改时间: {datetime.fromtimestamp(f.stat().st_mtime)})")
    
    return True

if __name__ == "__main__":
    print("==========================================")
    print("Memory Plus Sync - 飞书消息同步测试")
    print("==========================================")
    
    # 检查环境
    check_chat_history()
    
    # 测试同步
    success = test_feishu_sync()
    
    print("\n" + "="*50)
    if success:
        print("🎉 测试成功！飞书消息已同步到记忆系统")
    else:
        print("⚠️  测试未完成，请检查配置和聊天记录")
    
    print("="*50)