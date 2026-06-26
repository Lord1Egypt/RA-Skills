#!/usr/bin/env python3
"""
Multi-Agent Communication - Agent 间通信机制
实现 Agent 间的消息传递和协作

功能：
- 消息队列
- 广播消息
- 点对点通信
- 任务协作链

Usage:
  python3 communication.py --send <agent> --message "消息内容"
  python3 communication.py --broadcast --message "广播消息"
  python3 communication.py --inbox <agent>
  python3 communication.py --collaborate <task>
"""

import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

MESSAGE_FILE = Path(__file__).parent.parent / "config" / "messages.json"
COLLABORATION_FILE = Path(__file__).parent.parent / "config" / "collaborations.json"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[⚠]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

class Message:
    """消息类"""
    def __init__(self, from_agent: str, to_agent: str, content: str, msg_type: str = "direct"):
        self.id = f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.type = msg_type  # direct, broadcast, response
        self.timestamp = datetime.now()
        self.read = False
        self.replies = []
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'from_agent': self.from_agent,
            'to_agent': self.to_agent,
            'content': self.content,
            'type': self.type,
            'timestamp': self.timestamp.isoformat(),
            'read': self.read,
            'replies': self.replies
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        msg = cls(data['from_agent'], data['to_agent'], data['content'], data.get('type', 'direct'))
        msg.id = data['id']
        try:
            msg.timestamp = datetime.fromisoformat(data['timestamp'])
        except (AttributeError, ValueError):
            msg.timestamp = datetime.now()
        msg.read = data.get('read', False)
        msg.replies = data.get('replies', [])
        return msg

class CommunicationManager:
    """通信管理器"""
    
    def __init__(self):
        self.messages: List[Message] = []
        self.collaborations = []
        self.load_messages()
        self.load_collaborations()
    
    def load_messages(self):
        """加载消息"""
        if MESSAGE_FILE.exists():
            try:
                with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.messages = [Message.from_dict(m) for m in data.get('messages', [])]
                log_info(f"已加载 {len(self.messages)} 条消息")
            except Exception as e:
                log_error(f"加载消息失败：{e}")
                self.messages = []
        else:
            self.messages = []
            self.save_messages()
    
    def save_messages(self):
        """保存消息"""
        MESSAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'version': '1.0',
            'updated_at': datetime.now().isoformat(),
            'messages': [m.to_dict() for m in self.messages[-1000:]]  # 保留最近 1000 条
        }
        with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_collaborations(self):
        """加载协作记录"""
        if COLLABORATION_FILE.exists():
            try:
                with open(COLLABORATION_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.collaborations = data.get('collaborations', [])
                log_info(f"已加载 {len(self.collaborations)} 个协作记录")
            except Exception as e:
                log_error(f"加载协作记录失败：{e}")
                self.collaborations = []
        else:
            self.collaborations = []
            self.save_collaborations()
    
    def save_collaborations(self):
        """保存协作记录"""
        COLLABORATION_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(COLLABORATION_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'version': '1.0',
                'updated_at': datetime.now().isoformat(),
                'collaborations': self.collaborations[-100:]
            }, f, indent=2, ensure_ascii=False)
    
    def send_message(self, from_agent: str, to_agent: str, content: str) -> Message:
        """发送点对点消息"""
        msg = Message(from_agent, to_agent, content, "direct")
        self.messages.append(msg)
        self.save_messages()
        log_success(f"消息已发送：{from_agent} → {to_agent}")
        return msg
    
    def broadcast(self, from_agent: str, content: str, exclude: List[str] = None) -> List[Message]:
        """广播消息"""
        exclude = exclude or []
        messages = []
        
        # 获取所有 Agent
        from orchestrator import Orchestrator
        orchestrator = Orchestrator()
        
        for agent_name in orchestrator.agents.keys():
            if agent_name != from_agent and agent_name not in exclude:
                msg = self.send_message(from_agent, agent_name, content)
                msg.type = "broadcast"
                messages.append(msg)
        
        log_success(f"广播消息已发送：{from_agent} → {len(messages)} 个 Agent")
        return messages
    
    def get_inbox(self, agent_name: str, unread_only: bool = False) -> List[Message]:
        """获取收件箱"""
        inbox = []
        for msg in self.messages:
            if msg.to_agent == agent_name or msg.type == "broadcast":
                if unread_only and msg.read:
                    continue
                inbox.append(msg)
        return sorted(inbox, key=lambda m: m.timestamp, reverse=True)
    
    def mark_read(self, message_id: str):
        """标记消息已读"""
        for msg in self.messages:
            if msg.id == message_id:
                msg.read = True
                self.save_messages()
                log_success(f"消息已标记为已读：{message_id}")
                return True
        log_error(f"消息不存在：{message_id}")
        return False
    
    def reply_message(self, message_id: str, from_agent: str, content: str) -> Message:
        """回复消息"""
        original_msg = None
        for msg in self.messages:
            if msg.id == message_id:
                original_msg = msg
                break
        
        if not original_msg:
            log_error(f"消息不存在：{message_id}")
            return None
        
        reply_msg = self.send_message(from_agent, original_msg.from_agent, content)
        reply_msg.type = "response"
        original_msg.replies.append(reply_msg.id)
        self.save_messages()
        
        log_success(f"消息已回复：{from_agent} → {original_msg.from_agent}")
        return reply_msg
    
    def start_collaboration(self, task: str, agents: List[str]) -> dict:
        """启动协作任务"""
        collab_id = f"collab_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        collaboration = {
            'id': collab_id,
            'task': task,
            'agents': agents,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
            'messages': [],
            'results': []
        }
        
        self.collaborations.append(collaboration)
        self.save_collaborations()
        
        # 通知所有参与 Agent
        for agent in agents:
            self.broadcast("orchestrator", f"新协作任务：{task}", exclude=[a for a in agents if a != agent])
        
        log_success(f"协作任务已启动：{collab_id}")
        return collaboration
    
    def complete_collaboration(self, collab_id: str, result: str):
        """完成协作任务"""
        for collab in self.collaborations:
            if collab['id'] == collab_id:
                collab['status'] = 'completed'
                collab['completed_at'] = datetime.now().isoformat()
                collab['results'].append(result)
                self.save_collaborations()
                log_success(f"协作任务已完成：{collab_id}")
                return True
        log_error(f"协作任务不存在：{collab_id}")
        return False
    
    def get_collaboration_status(self, collab_id: str) -> dict:
        """获取协作状态"""
        for collab in self.collaborations:
            if collab['id'] == collab_id:
                return collab
        return None
    
    def list_collaborations(self, status: str = None) -> List[dict]:
        """列出协作任务"""
        if status:
            return [c for c in self.collaborations if c['status'] == status]
        return self.collaborations

def print_messages(messages: List[Message]):
    """打印消息列表"""
    if not messages:
        log_warning("没有消息")
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}📬 消息列表{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    for msg in messages[:20]:  # 最多显示 20 条
        icon = "📧" if msg.type == "direct" else "📢" if msg.type == "broadcast" else "💬"
        read_icon = "✓" if msg.read else "●"
        print(f"{icon} [{read_icon}] {msg.id}")
        print(f"   发件人：{msg.from_agent}")
        print(f"   收件人：{msg.to_agent}")
        print(f"   内容：{msg.content[:80]}")
        print(f"   时间：{msg.timestamp.strftime('%Y-%m-%d %H:%M')}")
        if msg.replies:
            print(f"   回复：{len(msg.replies)} 条")
        print()
    
    if len(messages) > 20:
        print(f"... 还有 {len(messages) - 20} 条消息")
    print()

def print_collaborations(collaborations: List[dict]):
    """打印协作列表"""
    if not collaborations:
        log_warning("没有协作任务")
        return
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}🤝 协作任务列表{Colors.NC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.NC}\n")
    
    for collab in collaborations[:10]:
        status_icon = "🟢" if collab['status'] == 'active' else "✅" if collab['status'] == 'completed' else "🔴"
        print(f"{status_icon} {collab['id']}")
        print(f"   任务：{collab['task'][:60]}")
        print(f"   Agent: {', '.join(collab['agents'])}")
        print(f"   状态：{collab['status']}")
        print(f"   创建：{collab['created_at'][:16]}")
        if collab['completed_at']:
            print(f"   完成：{collab['completed_at'][:16]}")
        print()
    
    if len(collaborations) > 10:
        print(f"... 还有 {len(collaborations) - 10} 个协作任务")
    print()

def main():
    parser = argparse.ArgumentParser(description='Agent 间通信管理')
    parser.add_argument('--send', type=str, help='发送消息到指定 Agent')
    parser.add_argument('--message', type=str, help='消息内容')
    parser.add_argument('--broadcast', action='store_true', help='广播消息')
    parser.add_argument('--inbox', type=str, help='查看指定 Agent 的收件箱')
    parser.add_argument('--unread', action='store_true', help='只显示未读消息')
    parser.add_argument('--reply', type=str, help='回复指定消息')
    parser.add_argument('--mark-read', type=str, help='标记消息为已读')
    parser.add_argument('--collaborate', type=str, help='启动协作任务')
    list_group = parser.add_mutually_exclusive_group()
    list_group.add_argument('--list-collab', action='store_true', help='列出协作任务')
    list_group.add_argument('--list-collab-active', action='store_true', help='列出活跃协作')
    list_group.add_argument('--list-collab-completed', action='store_true', help='列出已完成协作')
    
    args = parser.parse_args()
    
    comm = CommunicationManager()
    
    if args.send and args.message:
        # 需要指定 from_agent，这里简化处理
        comm.send_message("user", args.send, args.message)
    
    elif args.broadcast and args.message:
        comm.broadcast("orchestrator", args.message)
    
    elif args.inbox:
        messages = comm.get_inbox(args.inbox, args.unread)
        print_messages(messages)
    
    elif args.reply and args.message:
        comm.reply_message(args.reply, "user", args.message)
    
    elif args.mark_read:
        comm.mark_read(args.mark_read)
    
    elif args.collaborate and args.message:
        # 简化：使用所有可用 Agent
        from orchestrator import Orchestrator
        orchestrator = Orchestrator()
        agents = list(orchestrator.agents.keys())
        comm.start_collaboration(args.collaborate, agents)
    
    elif args.list_collab:
        collaborations = comm.list_collaborations()
        print_collaborations(collaborations)
    
    elif args.list_collab_active:
        collaborations = comm.list_collaborations('active')
        print_collaborations(collaborations)
    
    elif args.list_collab_completed:
        collaborations = comm.list_collaborations('completed')
        print_collaborations(collaborations)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
