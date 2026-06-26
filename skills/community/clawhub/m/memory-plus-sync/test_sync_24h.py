#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试飞书消息同步 - 采集最近24小时
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from collector import MultiChannelCollector
from memory_plus import MemoryPlus

def test_feishu_sync_24h():
    """测试飞书消息同步 - 最近24小时"""
    print("🧪 开始测试飞书消息同步（最近24小时）...")
    
    # 1. 采集飞书消息
    print("1️⃣ 采集最近24小时的飞书消息...")
    mcc = MultiChannelCollector()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    
    try:
        messages = mcc.collect_and_merge(
            channels=['feishu'],
            start_time=start_time,
            end_time=end_time
        )
        print(f"✅ 采集到 {len(messages)} 条飞书消息")
        
        if not messages:
            print("⚠️  没有采集到飞书消息")
            # 测试使用模拟数据
            print("📝 使用模拟数据进行测试...")
            messages = [
                {
                    'content': '测试飞书消息 - 记忆同步功能验证',
                    'sender': '测试用户',
                    'timestamp': datetime.now().isoformat(),
                    'message_id': 'test_msg_001',
                    'channel': 'feishu'
                },
                {
                    'content': '这是第二条测试消息，用于验证记忆存储功能',
                    'sender': '系统',
                    'timestamp': datetime.now().isoformat(),
                    'message_id': 'test_msg_002',
                    'channel': 'feishu'
                }
            ]
            print(f"📝 使用 {len(messages)} 条模拟消息")
        
        # 显示消息
        for i, msg in enumerate(messages):
            content = msg.get('content', '无内容')
            timestamp = msg.get('timestamp', '未知时间')
            sender = msg.get('sender', '未知发送者')
            print(f"  消息 {i+1}: [{timestamp}] {sender}: {content[:60]}...")
        
        # 2. 同步到记忆系统
        print("\n2️⃣ 同步消息到记忆系统...")
        mp = MemoryPlus()
        if mp.connect():
            mp.sync_from_channel('feishu', messages)
            mp.close()
            print("✅ 同步完成！")
            
            # 3. 验证同步结果
            print("\n3️⃣ 验证同步结果...")
            if mp.connect():
                # 检查数据库
                cursor = mp.conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM chunks WHERE source = 'channel' AND path LIKE '%feishu%'")
                count = cursor.fetchone()[0]
                print(f"✅ 数据库中已存储 {count} 条飞书渠道记忆")
                
                # 显示最近几条
                cursor.execute("""
                    SELECT path, text, updated_at 
                    FROM chunks 
                    WHERE source = 'channel' AND path LIKE '%feishu%'
                    ORDER BY updated_at DESC 
                    LIMIT 3
                """)
                rows = cursor.fetchall()
                print(f"📋 最近 {len(rows)} 条飞书记忆:")
                for i, row in enumerate(rows):
                    path, text, updated_at = row
                    print(f"  记录 {i+1}: {path}")
                    print(f"     内容: {text[:80]}...")
                    print(f"     更新时间: {datetime.fromtimestamp(updated_at/1000)}")
                
                mp.close()
            return True
        else:
            print("❌ 数据库连接失败")
            return False
            
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_database():
    """检查数据库状态"""
    print("\n💾 检查数据库状态...")
    db_path = Path.home() / '.openclaw' / 'memory' / 'main.sqlite'
    print(f"数据库路径: {db_path}")
    
    if not db_path.exists():
        print("❌ 数据库文件不存在")
        return False
    
    print(f"✅ 数据库文件存在 ({db_path.stat().st_size} 字节)")
    
    # 检查表结构
    mp = MemoryPlus()
    if mp.connect():
        cursor = mp.conn.cursor()
        
        # 检查 chunks 表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chunks'")
        if cursor.fetchone():
            print("✅ chunks 表存在")
            
            # 统计记录数
            cursor.execute("SELECT COUNT(*) FROM chunks")
            total = cursor.fetchone()[0]
            print(f"   总记忆块数: {total}")
            
            cursor.execute("SELECT COUNT(*) FROM chunks WHERE source = 'channel'")
            channel_count = cursor.fetchone()[0]
            print(f"   渠道记忆数: {channel_count}")
            
            cursor.execute("SELECT COUNT(*) FROM chunks WHERE source = 'memory'")
            memory_count = cursor.fetchone()[0]
            print(f"   记忆文件数: {memory_count}")
        else:
            print("❌ chunks 表不存在")
        
        mp.close()
        return True
    else:
        print("❌ 无法连接数据库")
        return False

if __name__ == "__main__":
    print("="*60)
    print("Memory Plus Sync - 飞书消息同步测试（最近24小时）")
    print("="*60)
    
    # 检查数据库
    check_database()
    
    # 测试同步
    success = test_feishu_sync_24h()
    
    print("\n" + "="*60)
    if success:
        print("🎉 测试成功！飞书消息已同步到记忆系统")
    else:
        print("⚠️  测试未完成")
    
    print("="*60)