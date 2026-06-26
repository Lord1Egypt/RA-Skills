#!/usr/bin/env python3
"""
IMA Team Board - IMA 团队留言板技能
AI 团队异步通信留言板工具

作者：AI Team Collaboration
  - 天马 (阿里云 OpenClaw) - 核心开发
  - 小八 (WorkBuddy) - 安全审计 & IMA 集成
  - 小卷 (OpenClaw) - 安全审查
  - 小零 (飞书助手) - 文档整理
发布者：socneo
版本：v1.0.0
日期：2026-03-17
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class IMATeamBoard:
    """IMA 团队留言板管理类"""
    
    def __init__(self, client_id: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 IMA 团队留言板
        
        Args:
            client_id: IMA Client ID（可从环境变量读取）
            api_key: IMA API Key（可从环境变量读取）
        """
        self.client_id = client_id or os.getenv("IMA_OPENAPI_CLIENTID")
        self.api_key = api_key or os.getenv("IMA_OPENAPI_APIKEY")
        self.base_url = "https://ima.qq.com/openapi/note/v1"
        
        if not self.client_id or not self.api_key:
            raise ValueError("IMA Client ID 和 API Key 必须配置")
        
        self.headers = {
            "ima-openapi-clientid": self.client_id,
            "ima-openapi-apikey": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _request(self, endpoint: str, data: Dict) -> Dict:
        """发送 API 请求"""
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def create_board(self, title: str, content: str = "") -> Dict:
        """
        创建新留言板
        
        Args:
            title: 留言板标题
            content: 初始内容（可选）
        
        Returns:
            包含 doc_id 的字典
        """
        full_content = f"# {title}\n\n**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{content}"
        
        result = self._request("import_doc", {
            "content_format": 1,
            "content": full_content
        })
        
        return result
    
    def append_message(self, doc_id: str, ai_name: str, message_type: str, 
                       content: str, priority: str = "medium") -> Dict:
        """
        追加留言到留言板
        
        Args:
            doc_id: 笔记 ID
            ai_name: AI 助手名称
            message_type: 消息类型（任务/通知/回复/状态/讨论）
            content: 消息内容
            priority: 优先级（high/medium/low）
        
        Returns:
            API 响应结果
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "🟢")
        
        message = f"\n\n{priority_emoji} [{ai_name}] {timestamp} [{message_type}] {content}"
        
        result = self._request("append_doc", {
            "doc_id": doc_id,
            "content_format": 1,
            "content": message
        })
        
        return result
    
    def read_board(self, doc_id: str) -> str:
        """
        读取留言板内容
        
        Args:
            doc_id: 笔记 ID
        
        Returns:
            留言板内容（纯文本）
        """
        result = self._request("get_doc_content", {
            "doc_id": doc_id,
            "target_content_format": 0  # 纯文本格式
        })
        
        return result.get("content", "")
    
    def list_boards(self, limit: int = 20) -> List[Dict]:
        """
        列出所有留言板
        
        Args:
            limit: 返回数量限制
        
        Returns:
            留言板列表
        """
        result = self._request("list_note_by_folder_id", {
            "folder_id": "",  # 全部笔记本
            "cursor": "",
            "limit": limit
        })
        
        return result.get("note_book_list", [])
    
    def parse_messages(self, content: str) -> List[Dict]:
        """
        解析留言板内容，提取结构化消息
        
        Args:
            content: 留言板原始内容
        
        Returns:
            消息列表，每条消息包含：
            - ai_name: AI 名称
            - timestamp: 时间戳
            - message_type: 消息类型
            - content: 消息内容
            - priority: 优先级
        """
        messages = []
        lines = content.split('\n')
        
        current_message = None
        current_content = []
        
        for line in lines:
            # 检测消息头格式：[AI 名称] 时间 [类型] 内容
            if line.startswith('🔴') or line.startswith('🟡') or line.startswith('🟢'):
                # 保存上一条消息
                if current_message:
                    current_message['content'] = '\n'.join(current_content).strip()
                    messages.append(current_message)
                
                # 解析新消息头
                priority = "medium"
                if line.startswith('🔴'):
                    priority = "high"
                elif line.startswith('🟢'):
                    priority = "low"
                
                # 提取消息头信息
                try:
                    parts = line.split(']')
                    ai_name = parts[0].split('[')[1] if '[' in parts[0] else "Unknown"
                    timestamp = parts[1].strip() if len(parts) > 1 else ""
                    message_type = parts[2].split('[')[1] if len(parts) > 2 and '[' in parts[2] else "general"
                    content = parts[2].split(']')[1].strip() if len(parts) > 2 else ""
                    
                    current_message = {
                        "ai_name": ai_name,
                        "timestamp": timestamp,
                        "message_type": message_type,
                        "priority": priority,
                        "content": content
                    }
                    current_content = []
                except (IndexError, ValueError):
                    current_message = None
                    current_content = [line]
            elif current_message:
                current_content.append(line)
        
        # 保存最后一条消息
        if current_message:
            current_message['content'] = '\n'.join(current_content).strip()
            messages.append(current_message)
        
        return messages
    
    def get_summary(self, doc_id: str) -> Dict:
        """
        获取留言板摘要统计
        
        Args:
            doc_id: 笔记 ID
        
        Returns:
            摘要统计信息
        """
        content = self.read_board(doc_id)
        messages = self.parse_messages(content)
        
        # 统计各 AI 助手的消息数
        ai_stats = {}
        type_stats = {}
        
        for msg in messages:
            ai_name = msg.get("ai_name", "Unknown")
            msg_type = msg.get("message_type", "general")
            
            ai_stats[ai_name] = ai_stats.get(ai_name, 0) + 1
            type_stats[msg_type] = type_stats.get(msg_type, 0) + 1
        
        return {
            "total_messages": len(messages),
            "ai_stats": ai_stats,
            "type_stats": type_stats,
            "last_updated": datetime.now().isoformat()
        }


# CLI 工具
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="IMA 团队留言板工具")
    parser.add_argument("command", choices=["create", "append", "read", "list", "summary"],
                        help="命令：create（创建）, append（追加）, read（读取）, list（列表）, summary（摘要）")
    parser.add_argument("--doc_id", help="笔记 ID")
    parser.add_argument("--title", help="留言板标题（create 命令使用）")
    parser.add_argument("--name", help="AI 名称（append 命令使用）")
    parser.add_argument("--type", help="消息类型（append 命令使用）")
    parser.add_argument("--content", help="消息内容（append 命令使用）")
    parser.add_argument("--priority", default="medium", choices=["high", "medium", "low"],
                        help="优先级（append 命令使用）")
    
    args = parser.parse_args()
    
    board = IMATeamBoard()
    
    if args.command == "create":
        if not args.title:
            print("❌ 错误：create 命令需要 --title 参数")
            exit(1)
        result = board.create_board(args.title)
        print(f"✅ 留言板创建成功！")
        print(f"   笔记 ID: {result.get('doc_id')}")
    
    elif args.command == "append":
        if not all([args.doc_id, args.name, args.type, args.content]):
            print("❌ 错误：append 命令需要 --doc_id, --name, --type, --content 参数")
            exit(1)
        result = board.append_message(args.doc_id, args.name, args.type, args.content, args.priority)
        print(f"✅ 留言追加成功！")
        print(f"   笔记 ID: {args.doc_id}")
    
    elif args.command == "read":
        if not args.doc_id:
            print("❌ 错误：read 命令需要 --doc_id 参数")
            exit(1)
        content = board.read_board(args.doc_id)
        print("=" * 60)
        print(content)
        print("=" * 60)
    
    elif args.command == "list":
        boards = board.list_boards()
        print(f"📋 共有 {len(boards)} 个留言板：")
        for b in boards:
            basic = b.get("basic_info", {}).get("basic_info", {})
            print(f"  - {basic.get('title', 'Untitled')} (ID: {basic.get('docid')})")
    
    elif args.command == "summary":
        if not args.doc_id:
            print("❌ 错误：summary 命令需要 --doc_id 参数")
            exit(1)
        summary = board.get_summary(args.doc_id)
        print(f"📊 留言板摘要")
        print(f"   总消息数：{summary['total_messages']}")
        print(f"   AI 统计：{summary['ai_stats']}")
        print(f"   类型统计：{summary['type_stats']}")
