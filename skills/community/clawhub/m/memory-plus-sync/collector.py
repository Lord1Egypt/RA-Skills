#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Plus 多渠道采集器

功能：
- 从飞书采集消息
- 从微信采集消息（需配置）
- 从 Telegram 采集消息（需配置）
- 统一格式输出

作者：伊娃 (Eva)
版本：1.0
创建：2026-04-07
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger('MemoryPlus-Collector')


class ChannelCollector:
    """渠道采集器基类"""
    
    def __init__(self, channel: str):
        self.channel = channel
        self.last_sync_time = None
    
    def collect(self, 
                start_time: Optional[datetime] = None,
                end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        采集消息
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
        
        Returns:
            消息列表
        """
        raise NotImplementedError


class FeishuCollector(ChannelCollector):
    """飞书消息采集器"""
    
    def __init__(self):
        super().__init__('feishu')
        self.chat_history_dir = Path.home() / '.openclaw' / 'workspace' / 'chat_history'
    
    def collect(self, 
                start_time: Optional[datetime] = None,
                end_time: Optional[datetime] = None,
                chat_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        从飞书采集消息
        
        说明：
        - 从 chat_history 目录读取已保存的聊天记录
        - 实际部署时应集成飞书 API
        """
        logger.info(f"📥 开始采集飞书消息")
        
        messages = []
        
        # 检查 chat_history 目录
        if not self.chat_history_dir.exists():
            logger.warning(f"⚠️  聊天记录目录不存在：{self.chat_history_dir}")
            return messages
        
        # 读取最近的聊天记录
        recent_files = sorted(
            self.chat_history_dir.glob('*.json'),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )[:10]  # 最近 10 个文件
        
        for file_path in recent_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
                
                # 提取消息
                if isinstance(chat_data, list):
                    for msg in chat_data:
                        if self._filter_by_time(msg, start_time, end_time):
                            messages.append(self._normalize_message(msg, 'feishu'))
                elif isinstance(chat_data, dict) and 'messages' in chat_data:
                    for msg in chat_data['messages']:
                        if self._filter_by_time(msg, start_time, end_time):
                            messages.append(self._normalize_message(msg, 'feishu'))
                
            except Exception as e:
                logger.error(f"❌ 读取文件失败 {file_path}: {e}")
        
        logger.info(f"✅ 飞书消息采集完成：{len(messages)} 条")
        self.last_sync_time = datetime.now()
        
        return messages
    
    def _filter_by_time(self, 
                       msg: Dict[str, Any],
                       start_time: Optional[datetime],
                       end_time: Optional[datetime]) -> bool:
        """按时间过滤消息"""
        if not start_time and not end_time:
            return True
        
        msg_time = msg.get('timestamp')
        if not msg_time:
            return True
        
        try:
            if isinstance(msg_time, str):
                msg_dt = datetime.fromisoformat(msg_time.replace('Z', '+00:00'))
            elif isinstance(msg_time, (int, float)):
                msg_dt = datetime.fromtimestamp(msg_time)
            else:
                return True
            
            if start_time and msg_dt < start_time:
                return False
            if end_time and msg_dt > end_time:
                return False
            
            return True
            
        except:
            return True
    
    def _normalize_message(self, msg: Dict[str, Any], channel: str) -> Dict[str, Any]:
        """标准化消息格式"""
        return {
            'content': msg.get('content', msg.get('text', '')),
            'sender': msg.get('sender', msg.get('user_name', 'unknown')),
            'timestamp': msg.get('timestamp', datetime.now().isoformat()),
            'message_id': msg.get('message_id', msg.get('id', '')),
            'channel': channel,
            'raw': msg  # 保留原始数据
        }


class WechatCollector(ChannelCollector):
    """微信消息采集器"""
    
    def __init__(self):
        super().__init__('wechat')
        # 微信消息存储位置（需要根据实际配置调整）
        self.wechat_dir = Path.home() / '.openclaw' / 'workspace' / 'wechat_messages'
    
    def collect(self, 
                start_time: Optional[datetime] = None,
                end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        从微信采集消息
        
        说明：
        - 需要配置微信消息导出工具
        - 目前返回空列表，等待实际集成
        """
        logger.info(f"📥 开始采集微信消息")
        
        messages = []
        
        # TODO: 集成微信消息采集
        # 可能的方案：
        # 1. WeChatFerry (https://github.com/lich0821/WeChatFerry)
        # 2. 手动导出聊天记录
        
        if self.wechat_dir.exists():
            logger.warning("⚠️  微信目录存在但未实现采集逻辑")
        else:
            logger.info("ℹ️  微信消息目录未配置，跳过采集")
        
        self.last_sync_time = datetime.now()
        return messages


class TelegramCollector(ChannelCollector):
    """Telegram 消息采集器"""
    
    def __init__(self):
        super().__init__('telegram')
        self.tg_dir = Path.home() / '.openclaw' / 'workspace' / 'telegram_messages'
    
    def collect(self, 
                start_time: Optional[datetime] = None,
                end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        从 Telegram 采集消息
        
        说明：
        - 需要配置 Telegram API
        - 目前返回空列表，等待实际集成
        """
        logger.info(f"📥 开始采集 Telegram 消息")
        
        messages = []
        
        # TODO: 集成 Telegram API
        # 使用 python-telegram-bot 或 Telethon
        
        if self.tg_dir.exists():
            logger.warning("⚠️  Telegram 目录存在但未实现采集逻辑")
        else:
            logger.info("ℹ️  Telegram 消息目录未配置，跳过采集")
        
        self.last_sync_time = datetime.now()
        return messages


class VoiceCollector(ChannelCollector):
    """语音对话采集器"""
    
    def __init__(self):
        super().__init__('voice')
        self.voice_log_dir = Path.home() / '.openclaw' / 'workspace' / 'voice_logs'
    
    def collect(self, 
                start_time: Optional[datetime] = None,
                end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        采集语音对话记录
        
        从 voice_loop.py 的日志中采集
        """
        logger.info(f"📥 开始采集语音对话记录")
        
        messages = []
        
        # 读取语音日志
        log_file = self.voice_log_dir / 'voice_conversations.jsonl'
        
        if not log_file.exists():
            logger.info("ℹ️  语音日志文件不存在，跳过采集")
            self.last_sync_time = datetime.now()
            return messages
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        
                        # 检查时间范围
                        if self._filter_by_time(record, start_time, end_time):
                            # 用户输入
                            if 'user_input' in record:
                                messages.append({
                                    'content': record['user_input'],
                                    'sender': 'user',
                                    'timestamp': record.get('timestamp', ''),
                                    'message_id': f"voice_{len(messages)}",
                                    'channel': 'voice'
                                })
                            
                            # AI 回复
                            if 'ai_response' in record:
                                messages.append({
                                    'content': record['ai_response'],
                                    'sender': '伊娃',
                                    'timestamp': record.get('timestamp', ''),
                                    'message_id': f"voice_{len(messages)+1}",
                                    'channel': 'voice'
                                })
                    except:
                        continue
                        
        except Exception as e:
            logger.error(f"❌ 读取语音日志失败：{e}")
        
        logger.info(f"✅ 语音对话采集完成：{len(messages)} 条")
        self.last_sync_time = datetime.now()
        
        return messages
    
    def _filter_by_time(self, 
                       record: Dict[str, Any],
                       start_time: Optional[datetime],
                       end_time: Optional[datetime]) -> bool:
        """按时间过滤"""
        if not start_time and not end_time:
            return True
        
        timestamp = record.get('timestamp')
        if not timestamp:
            return True
        
        try:
            if isinstance(timestamp, str):
                msg_dt = datetime.fromisoformat(timestamp)
            elif isinstance(timestamp, (int, float)):
                msg_dt = datetime.fromtimestamp(timestamp)
            else:
                return True
            
            if start_time and msg_dt < start_time:
                return False
            if end_time and msg_dt > end_time:
                return False
            
            return True
            
        except:
            return True


class MultiChannelCollector:
    """多渠道采集器管理器"""
    
    def __init__(self):
        self.collectors = {
            'feishu': FeishuCollector(),
            'wechat': WechatCollector(),
            'telegram': TelegramCollector(),
            'voice': VoiceCollector()
        }
    
    def collect_all(self,
                   channels: List[str] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        从所有渠道采集消息
        
        Args:
            channels: 指定渠道列表，None 表示所有
            start_time: 开始时间
            end_time: 结束时间
        
        Returns:
            按渠道分组的消息字典
        """
        if channels is None:
            channels = list(self.collectors.keys())
        
        results = {}
        
        logger.info(f"🚀 开始多渠道采集：{channels}")
        
        for channel in channels:
            if channel not in self.collectors:
                logger.warning(f"⚠️  未知渠道：{channel}，跳过")
                continue
            
            collector = self.collectors[channel]
            messages = collector.collect(start_time, end_time)
            results[channel] = messages
        
        total = sum(len(msgs) for msgs in results.values())
        logger.info(f"✅ 多渠道采集完成：总计 {total} 条消息")
        
        return results
    
    def collect_and_merge(self,
                         channels: List[str] = None,
                         start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        采集并合并所有渠道的消息（按时间排序）
        
        Returns:
            按时间排序的消息列表
        """
        results = self.collect_all(channels, start_time, end_time)
        
        # 合并所有消息
        all_messages = []
        for channel_messages in results.values():
            all_messages.extend(channel_messages)
        
        # 按时间排序
        def get_timestamp(msg):
            ts = msg.get('timestamp', '')
            try:
                if isinstance(ts, str):
                    return datetime.fromisoformat(ts.replace('Z', '+00:00'))
                elif isinstance(ts, (int, float)):
                    return datetime.fromtimestamp(ts)
            except:
                pass
            return datetime.min
        
        all_messages.sort(key=get_timestamp)
        
        return all_messages


def demo():
    """演示功能"""
    print("=" * 60)
    print("Memory Plus 多渠道采集器演示")
    print("=" * 60)
    
    # 创建采集器
    mcc = MultiChannelCollector()
    
    # 采集最近 1 小时的消息
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    print(f"\n采集时间范围：{start_time} ~ {end_time}")
    
    # 采集所有渠道
    results = mcc.collect_all(
        channels=['feishu', 'voice'],
        start_time=start_time,
        end_time=end_time
    )
    
    # 输出结果
    print("\n采集结果:")
    for channel, messages in results.items():
        print(f"\n{channel.upper()}: {len(messages)} 条")
        for msg in messages[:5]:  # 只显示前 5 条
            print(f"  [{msg['timestamp']}] {msg['sender']}: {msg['content'][:50]}...")
    
    # 合并所有消息
    print("\n" + "=" * 60)
    print("合并所有渠道（按时间排序）:")
    
    merged = mcc.collect_and_merge(
        channels=['feishu', 'voice'],
        start_time=start_time,
        end_time=end_time
    )
    
    for msg in merged[:10]:  # 只显示前 10 条
        print(f"  [{msg['channel']}] {msg['timestamp']}: {msg['sender']} - {msg['content'][:40]}...")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demo()
    else:
        # 默认运行演示
        demo()
