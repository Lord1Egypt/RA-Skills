#!/usr/bin/env python3
"""
Hermes-WorkBuddy 通信队列管理器
支持：消息发送、接收、状态管理、历史查询
"""

import json
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class CommunicationQueue:
    """通信队列管理器"""
    
    def __init__(self, queue_dir: Optional[str] = None):
        # 支持环境变量配置
        self.queue_dir = Path(queue_dir or os.environ.get(
            "HERMES_COMM_QUEUE_DIR", 
            Path.home() / ".hermes" / "shared" / "communication"
        ))
        self.queue_file = self.queue_dir / "queue.json"
        self.history_file = self.queue_dir / "history.json"
        
        # 确保目录存在
        self.queue_dir.mkdir(parents=True, exist_ok=True)
        self._init_queue_file()
    
    def _init_queue_file(self):
        """初始化队列文件"""
        if not self.queue_file.exists():
            default_queue = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "messages": [],
                "stats": {
                    "total_messages": 0,
                    "pending_messages": 0,
                    "hermes_to_workbuddy": 0,
                    "workbuddy_to_hermes": 0
                }
            }
            self._write_json(self.queue_file, default_queue)
    
    def send_message(self, 
                    sender: str, 
                    receiver: str, 
                    content: str,
                    msg_type: str = "message",
                    priority: str = "normal",
                    metadata: Optional[Dict] = None) -> str:
        """
        发送消息到队列
        
        Args:
            sender: 发送者 (hermes|workbuddy)
            receiver: 接收者 (hermes|workbuddy)
            content: 消息内容
            msg_type: 消息类型 (message|task|file|status|query|response)
            priority: 优先级 (low|normal|high|urgent)
            metadata: 附加元数据
            
        Returns:
            消息ID
        """
        msg_id = f"msg_{int(time.time())}_{sender[:3]}"
        
        message = {
            "id": msg_id,
            "timestamp": datetime.now().isoformat(),
            "sender": sender,
            "receiver": receiver,
            "type": msg_type,
            "content": content,
            "priority": priority,
            "status": "pending",
            "metadata": metadata or {}
        }
        
        # 读取并更新队列
        queue = self._read_queue()
        queue["messages"].append(message)
        
        # 更新统计
        queue["stats"]["total_messages"] += 1
        queue["stats"]["pending_messages"] += 1
        key = f"{sender}_to_{receiver}"
        if key in queue["stats"]:
            queue["stats"][key] += 1
        
        self._write_queue(queue)
        
        # 记录到历史
        self._add_to_history(message)
        
        return msg_id
    
    def get_messages(self, 
                    receiver: str, 
                    status: str = "pending",
                    limit: int = 10) -> List[Dict]:
        """
        获取指定接收者的消息
        
        Args:
            receiver: 接收者
            status: 消息状态 (pending|processing|completed|failed)
            limit: 返回数量限制
            
        Returns:
            消息列表
        """
        queue = self._read_queue()
        messages = [
            msg for msg in queue["messages"]
            if msg["receiver"] == receiver and msg["status"] == status
        ]
        return messages[:limit]
    
    def mark_as_processed(self, msg_id: str, status: str = "completed"):
        """
        标记消息为已处理
        
        Args:
            msg_id: 消息ID
            status: 新状态 (completed|failed)
        """
        queue = self._read_queue()
        
        for msg in queue["messages"]:
            if msg["id"] == msg_id:
                old_status = msg["status"]
                msg["status"] = status
                msg["processed_at"] = datetime.now().isoformat()
                
                # 更新统计
                if old_status == "pending" and status in ("completed", "failed"):
                    queue["stats"]["pending_messages"] -= 1
                
                self._write_queue(queue)
                return True
        
        return False
    
    def get_stats(self) -> Dict:
        """获取队列统计信息"""
        queue = self._read_queue()
        return queue["stats"]
    
    def clear_old_messages(self, days: int = 7):
        """清理指定天数前的已完成消息"""
        queue = self._read_queue()
        cutoff_time = time.time() - (days * 24 * 3600)
        
        # 保留未完成和最近的消息
        queue["messages"] = [
            msg for msg in queue["messages"]
            if (msg["status"] != "completed" or 
                time.mktime(datetime.fromisoformat(msg["timestamp"]).timetuple()) > cutoff_time)
        ]
        
        self._write_queue(queue)
    
    # 私有方法
    def _read_queue(self) -> Dict:
        """读取队列文件"""
        return self._read_json(self.queue_file)
    
    def _write_queue(self, queue: Dict):
        """写入队列文件"""
        self._write_json(self.queue_file, queue)
    
    def _add_to_history(self, message: Dict):
        """添加到历史记录"""
        history = self._read_json(self.history_file, default={"messages": []})
        history["messages"].append(message)
        # 限制历史记录大小
        if len(history["messages"]) > 1000:
            history["messages"] = history["messages"][-1000:]
        self._write_json(self.history_file, history)
    
    @staticmethod
    def _read_json(filepath: Path, default=None):
        """读取JSON文件"""
        if not filepath.exists():
            return default if default is not None else {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default if default is not None else {}
    
    @staticmethod
    def _write_json(filepath: Path, data: Dict):
        """写入JSON文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"写入文件失败: {e}")


# CLI 接口
def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Hermes-WorkBuddy 通信队列管理器")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # send 命令
    send_parser = subparsers.add_parser("send", help="发送消息")
    send_parser.add_argument("sender", help="发送者")
    send_parser.add_argument("receiver", help="接收者")
    send_parser.add_argument("content", help="消息内容")
    send_parser.add_argument("--type", default="message", help="消息类型")
    send_parser.add_argument("--priority", default="normal", help="优先级")
    
    # receive 命令
    receive_parser = subparsers.add_parser("receive", help="接收消息")
    receive_parser.add_argument("receiver", help="接收者")
    receive_parser.add_argument("--status", default="pending", help="消息状态")
    receive_parser.add_argument("--limit", type=int, default=10, help="数量限制")
    
    # stats 命令
    stats_parser = subparsers.add_parser("stats", help="查看统计")
    
    # clear 命令
    clear_parser = subparsers.add_parser("clear", help="清理旧消息")
    clear_parser.add_argument("--days", type=int, default=7, help="保留天数")
    
    # mark 命令
    mark_parser = subparsers.add_parser("mark", help="标记消息状态")
    mark_parser.add_argument("msg_id", help="消息ID")
    mark_parser.add_argument("status", help="新状态")
    
    args = parser.parse_args()
    queue = CommunicationQueue()
    
    if args.command == "send":
        msg_id = queue.send_message(
            sender=args.sender,
            receiver=args.receiver,
            content=args.content,
            msg_type=args.type,
            priority=args.priority
        )
        print(f"✅ 消息已发送: {msg_id}")
        
    elif args.command == "receive":
        messages = queue.get_messages(
            receiver=args.receiver,
            status=args.status,
            limit=args.limit
        )
        if messages:
            print(f"📨 找到 {len(messages)} 条消息:")
            for msg in messages:
                print(f"  [{msg['timestamp']}] {msg['sender']} → {msg['receiver']}:")
                print(f"     内容: {msg['content'][:80]}...")
                print(f"     类型: {msg['type']}, 优先级: {msg['priority']}")
                print()
        else:
            print("📭 没有新消息")
            
    elif args.command == "stats":
        stats = queue.get_stats()
        print("📊 通信队列统计:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    elif args.command == "clear":
        queue.clear_old_messages(days=args.days)
        print(f"🧹 已清理 {args.days} 天前的已完成消息")
        
    elif args.command == "mark":
        success = queue.mark_as_processed(args.msg_id, args.status)
        if success:
            print(f"✅ 消息 {args.msg_id} 标记为 {args.status}")
        else:
            print(f"❌ 消息 {args.msg_id} 未找到")


if __name__ == "__main__":
    main()