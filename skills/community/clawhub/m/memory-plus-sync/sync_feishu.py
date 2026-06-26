#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Plus Sync - 同步最近1小时飞书消息
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from collector import MultiChannelCollector
from memory_plus import MemoryPlus

def sync_recent_feishu_messages(hours=1):
    """同步最近指定小时的飞书消息"""
    print(f"🔄 开始同步最近 {hours} 小时的飞书消息...")
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. 采集飞书消息
    mcc = MultiChannelCollector()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)
    
    print(f"时间范围: {start_time.strftime('%Y-%m-%d %H:%M:%S')} 到 {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    messages = mcc.collect_and_merge(
        channels=['feishu'],
        start_time=start_time,
        end_time=end_time
    )
    
    print(f"📥 采集到 {len(messages)} 条飞书消息")
    
    if not messages:
        print("⚠️  没有采集到飞书消息")
        return {
            'success': False,
            'message': '没有采集到飞书消息',
            'count': 0
        }
    
    # 显示消息摘要
    print("\n📋 消息摘要:")
    for i, msg in enumerate(messages):
        content = msg.get('content', '无内容')
        timestamp = msg.get('timestamp', '未知时间')
        sender = msg.get('sender', '未知发送者')
        print(f"  {i+1}. [{timestamp}] {sender}: {content[:60]}...")
    
    # 2. 同步到记忆系统
    print("\n💾 同步到记忆系统...")
    mp = MemoryPlus()
    if not mp.connect():
        print("❌ 数据库连接失败")
        return {
            'success': False,
            'message': '数据库连接失败',
            'count': 0
        }
    
    try:
        mp.sync_from_channel('feishu', messages)
        
        # 验证同步结果
        cursor = mp.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM chunks WHERE source = 'channel' AND path LIKE '%feishu%'")
        total_feishu = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM chunks 
            WHERE source = 'channel' AND path LIKE '%feishu%'
            AND updated_at >= ?
        """, (int(start_time.timestamp() * 1000),))
        recent_feishu = cursor.fetchone()[0]
        
        print(f"✅ 同步完成！")
        print(f"   数据库中的飞书记忆总数: {total_feishu}")
        print(f"   最近 {hours} 小时新增: {recent_feishu}")
        
        # 检查记忆文件
        memory_file = Path.home() / '.openclaw' / 'memory' / 'feishu' / f"{datetime.now().strftime('%Y-%m-%d')}.md"
        if memory_file.exists():
            print(f"   记忆文件: {memory_file}")
            print(f"   文件大小: {memory_file.stat().st_size} 字节")
        
        return {
            'success': True,
            'message': f'成功同步 {len(messages)} 条飞书消息',
            'count': len(messages),
            'total_feishu': total_feishu,
            'recent_feishu': recent_feishu
        }
        
    except Exception as e:
        print(f"❌ 同步失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'message': f'同步失败: {str(e)}',
            'count': 0
        }
    finally:
        mp.close()

def main():
    """主函数"""
    print("="*60)
    print("Memory Plus Sync - 飞书消息同步工具")
    print("="*60)
    
    # 默认同步最近1小时
    hours = 1
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
        except ValueError:
            print(f"⚠️  参数错误，使用默认值: {hours} 小时")
    
    print(f"同步最近 {hours} 小时的飞书消息...")
    
    result = sync_recent_feishu_messages(hours)
    
    print("\n" + "="*60)
    if result['success']:
        print(f"🎉 同步成功！")
        print(f"   处理消息: {result['count']} 条")
        print(f"   飞书记忆总数: {result.get('total_feishu', 0)}")
        print(f"   最近新增: {result.get('recent_feishu', 0)}")
    else:
        print(f"⚠️  同步未完成")
        print(f"   原因: {result['message']}")
    
    print("="*60)
    
    # 返回结果用于cron job
    return result

if __name__ == "__main__":
    main()