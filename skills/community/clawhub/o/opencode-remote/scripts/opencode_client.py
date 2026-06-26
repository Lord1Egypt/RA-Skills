#!/usr/bin/env python3
"""
OpenCode HTTP API 客户端
用于远程操作 OpenCode 服务器
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from typing import Optional


class OpenCodeClient:
    def __init__(self, base_url: str, proxy: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.proxy = proxy
        
    def _request(self, method: str, path: str, data: Optional[dict] = None) -> dict:
        url = f"{self.base_url}{path}"
        headers = {"Content-Type": "application/json"}
        
        req = urllib.request.Request(
            url,
            method=method,
            headers=headers,
            data=json.dumps(data).encode() if data else None
        )
        
        # 配置代理
        if self.proxy:
            proxy_handler = urllib.request.ProxyHandler({
                'http': self.proxy,
                'https': self.proxy
            })
            opener = urllib.request.build_opener(proxy_handler)
            urllib.request.install_opener(opener)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}", "details": e.read().decode()}
        except Exception as e:
            return {"error": str(e)}
    
    def health(self) -> dict:
        """检查服务器健康状态"""
        return self._request("GET", "/global/health")
    
    def list_sessions(self) -> dict:
        """列出所有 sessions"""
        return self._request("GET", "/session")
    
    def get_session(self, session_id: str) -> dict:
        """获取 session 详情"""
        return self._request("GET", f"/session/{session_id}")
    
    def get_messages(self, session_id: str) -> dict:
        """获取 session 消息记录"""
        return self._request("GET", f"/session/{session_id}/message")
    
    def get_todos(self, session_id: str) -> dict:
        """获取 session 待办事项"""
        return self._request("GET", f"/session/{session_id}/todo")
    
    def get_children(self, session_id: str) -> dict:
        """获取子 sessions"""
        return self._request("GET", f"/session/{session_id}/children")
    
    def summarize(self, session_id: str, summary_hint: str = "") -> dict:
        """对 session 进行 summarize"""
        data = {"summary": summary_hint} if summary_hint else {}
        return self._request("POST", f"/session/{session_id}/summarize", data)
    
    def send_message(self, session_id: str, content: str) -> dict:
        """向 session 发送消息"""
        data = {
            "parts": [{"type": "text", "content": content}]
        }
        return self._request("POST", f"/session/{session_id}/message", data)
    
    def abort(self, session_id: str) -> dict:
        """中止运行中的 session"""
        return self._request("POST", f"/session/{session_id}/abort", {})
    
    def create_session(self, title: Optional[str] = None) -> dict:
        """创建新 session"""
        data = {}
        if title:
            data["title"] = title
        return self._request("POST", "/session", data)
    
    def delete_session(self, session_id: str) -> dict:
        """删除 session"""
        return self._request("DELETE", f"/session/{session_id}")
    
    def fork_session(self, session_id: str) -> dict:
        """Fork session"""
        return self._request("POST", f"/session/{session_id}/fork", {})
    
    def shell_command(self, session_id: str, command: str) -> dict:
        """在 session 中执行 shell 命令"""
        return self._request("POST", f"/session/{session_id}/shell", {"command": command})


def format_session_list(sessions: list) -> str:
    """格式化 session 列表输出"""
    if not sessions:
        return "暂无 sessions"
    
    lines = ["\n📋 Sessions 列表:", "-" * 80]
    lines.append(f"{'ID':<36} {'状态':<12} {'标题':<30}")
    lines.append("-" * 80)
    
    for s in sessions:
        session_id = s.get('id', 'N/A')[:36]
        status = s.get('status', 'unknown')[:12]
        title = s.get('title', 'Untitled')[:30]
        lines.append(f"{session_id:<36} {status:<12} {title:<30}")
    
    return "\n".join(lines)


def format_session_detail(session: dict) -> str:
    """格式化 session 详情输出"""
    lines = ["\n📊 Session 详情:", "-" * 50]
    lines.append(f"ID: {session.get('id', 'N/A')}")
    lines.append(f"状态: {session.get('status', 'unknown')}")
    lines.append(f"标题: {session.get('title', 'Untitled')}")
    lines.append(f"创建时间: {session.get('createdAt', 'N/A')}")
    lines.append(f"更新时间: {session.get('updatedAt', 'N/A')}")
    
    if 'parentID' in session:
        lines.append(f"父 Session: {session['parentID']}")
    
    return "\n".join(lines)


def format_messages(messages: list) -> str:
    """格式化消息记录输出"""
    if not messages:
        return "暂无消息记录"
    
    lines = ["\n💬 消息记录:", "-" * 50]
    
    for i, msg in enumerate(messages[-10:], 1):  # 只显示最后10条
        role = msg.get('role', 'unknown')
        parts = msg.get('parts', [])
        content = ""
        for part in parts:
            if part.get('type') == 'text':
                content = part.get('content', '')[:100]
                break
        
        lines.append(f"\n[{i}] {role}:")
        lines.append(f"    {content}{'...' if len(content) == 100 else ''}")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='OpenCode HTTP API 客户端')
    parser.add_argument('--url', required=True, help='OpenCode 服务器 URL (如 http://host:port)')
    parser.add_argument('--proxy', help='代理地址 (如 socks5://127.0.0.1:1080)')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # health
    subparsers.add_parser('health', help='检查服务器健康状态')
    
    # list
    subparsers.add_parser('list', help='列出所有 sessions')
    
    # status
    status_parser = subparsers.add_parser('status', help='查看 session 状态')
    status_parser.add_argument('session_id', help='Session ID')
    
    # messages
    msg_parser = subparsers.add_parser('messages', help='查看 session 消息记录')
    msg_parser.add_argument('session_id', help='Session ID')
    
    # todos
    todo_parser = subparsers.add_parser('todos', help='查看 session 待办事项')
    todo_parser.add_argument('session_id', help='Session ID')
    
    # summarize
    sum_parser = subparsers.add_parser('summarize', help='Summarize session')
    sum_parser.add_argument('session_id', help='Session ID')
    sum_parser.add_argument('hint', nargs='?', default='', help='总结要点提示')
    
    # send
    send_parser = subparsers.add_parser('send', help='向 session 发送消息')
    send_parser.add_argument('session_id', help='Session ID')
    send_parser.add_argument('content', help='消息内容')
    
    # abort
    abort_parser = subparsers.add_parser('abort', help='中止运行中的 session')
    abort_parser.add_argument('session_id', help='Session ID')
    
    # create
    create_parser = subparsers.add_parser('create', help='创建新 session')
    create_parser.add_argument('--title', help='Session 标题')
    
    # delete
    delete_parser = subparsers.add_parser('delete', help='删除 session')
    delete_parser.add_argument('session_id', help='Session ID')
    
    # fork
    fork_parser = subparsers.add_parser('fork', help='Fork session')
    fork_parser.add_argument('session_id', help='Session ID')
    
    # shell
    shell_parser = subparsers.add_parser('shell', help='执行 shell 命令')
    shell_parser.add_argument('session_id', help='Session ID')
    shell_parser.add_argument('command', help='Shell 命令')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = OpenCodeClient(args.url, args.proxy)
    
    # 执行命令
    if args.command == 'health':
        result = client.health()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'list':
        result = client.list_sessions()
        if isinstance(result, list):
            print(format_session_list(result))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'status':
        result = client.get_session(args.session_id)
        if 'error' in result:
            print(f"❌ 错误: {result['error']}")
        else:
            print(format_session_detail(result))
    
    elif args.command == 'messages':
        result = client.get_messages(args.session_id)
        if isinstance(result, list):
            print(format_messages(result))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'todos':
        result = client.get_todos(args.session_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'summarize':
        result = client.summarize(args.session_id, args.hint)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'send':
        result = client.send_message(args.session_id, args.content)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'abort':
        result = client.abort(args.session_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'create':
        result = client.create_session(args.title)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'delete':
        result = client.delete_session(args.session_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'fork':
        result = client.fork_session(args.session_id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == 'shell':
        result = client.shell_command(args.session_id, args.command)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
