#!/usr/bin/env python3
"""
投票系统模块
用户可以对操作进行投票
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 颜色输出
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_color(color, text):
    print(f"{color}{text}{Colors.NC}")

class VotingSystem:
    def __init__(self):
        """初始化投票系统"""
        self.script_dir = Path(__file__).parent
        self.memory_file = self.script_dir / "controlmemory.md"
        self.votes_file = self.script_dir / ".votes.json"
        self.user_id = self.get_user_id()
    
    def get_user_id(self):
        """获取用户 ID（匿名）"""
        import socket
        import getpass
        user_str = f"{socket.gethostname()}_{getpass.getuser()}"
        return hashlib.md5(user_str.encode()).hexdigest()[:8]
    
    def load_votes(self):
        """加载投票数据"""
        if self.votes_file.exists():
            with open(self.votes_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_votes(self, votes):
        """保存投票数据"""
        with open(self.votes_file, 'w') as f:
            json.dump(votes, f, indent=2)
    
    def vote(self, operation_name, vote_type='up'):
        """
        投票
        
        Args:
            operation_name: 操作名称
            vote_type: 投票类型 ('up' or 'down')
        """
        votes = self.load_votes()
        
        # 检查是否已投票
        if operation_name in votes:
            if self.user_id in votes[operation_name]:
                print_color(Colors.YELLOW, "⚠️  您已对此操作投票")
                return False
        
        # 添加投票
        if operation_name not in votes:
            votes[operation_name] = {}
        
        votes[operation_name][self.user_id] = vote_type
        self.save_votes(votes)
        
        # 更新 memory 文件中的投票数
        self.update_memory_votes(operation_name, votes[operation_name])
        
        print_color(Colors.GREEN, f"✅ 投票成功！({vote_type})")
        return True
    
    def update_memory_votes(self, operation_name, user_votes):
        """更新 memory 文件中的投票数"""
        if not self.memory_file.exists():
            return
        
        content = self.memory_file.read_text()
        vote_count = len(user_votes)
        
        # 更新投票数
        pattern = rf'(\*\*投票\*\*: 👍 )(\d+)'
        replacement = f'\\g<1>{vote_count}'
        
        # 简单的全局替换（实际应该更精确）
        new_content = re.sub(pattern, replacement, content)
        
        self.memory_file.write_text(new_content)
    
    def get_operation_votes(self, operation_name):
        """获取操作的投票数"""
        votes = self.load_votes()
        if operation_name in votes:
            up_votes = sum(1 for v in votes[operation_name].values() if v == 'up')
            down_votes = sum(1 for v in votes[operation_name].values() if v == 'down')
            return up_votes, down_votes
        return 0, 0
    
    def display_votes(self):
        """显示投票情况"""
        votes = self.load_votes()
        
        print_color(Colors.BLUE, "╔════════════════════════════════════════╗")
        print_color(Colors.BLUE, "║   🗳️  投票统计                        ║")
        print_color(Colors.BLUE, "╚════════════════════════════════════════╝")
        print()
        
        if not votes:
            print_color(Colors.YELLOW, "⚠️  暂无投票")
            return
        
        for op_name, user_votes in votes.items():
            up_votes = sum(1 for v in user_votes.values() if v == 'up')
            down_votes = sum(1 for v in user_votes.values() if v == 'down')
            
            print(f"{op_name}")
            print(f"  👍 {up_votes}  👎 {down_votes}")
            print()


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='投票系统')
    parser.add_argument('operation', help='操作名称')
    parser.add_argument('--up', action='store_true', help='点赞')
    parser.add_argument('--down', action='store_true', help='踩')
    parser.add_argument('--show', action='store_true', help='显示投票情况')
    
    args = parser.parse_args()
    
    voting = VotingSystem()
    
    if args.show:
        voting.display_votes()
    elif args.up:
        voting.vote(args.operation, 'up')
    elif args.down:
        voting.vote(args.operation, 'down')
    else:
        parser.print_help()


if __name__ == "__main__":
    import hashlib
    main()
