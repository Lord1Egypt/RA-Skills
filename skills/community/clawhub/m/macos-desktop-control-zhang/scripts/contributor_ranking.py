#!/usr/bin/env python3
"""
贡献者排行榜模块
统计和展示用户贡献情况
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
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

class ContributorRanking:
    def __init__(self):
        """初始化排行榜"""
        self.script_dir = Path(__file__).parent
        self.memory_file = self.script_dir / "controlmemory.md"
        self.ranking_file = self.script_dir / ".contributor_ranking.json"
    
    def parse_contributions(self):
        """解析所有贡献"""
        if not self.memory_file.exists():
            return []
        
        content = self.memory_file.read_text()
        contributions = []
        
        # 解析贡献者信息
        pattern = r'#### (.+?)\n.*?\*\*贡献者\*\*: (.+?)\n.*?\*\*添加时间\*\*: (.+?)\n.*?\*\*验证状态\*\*: (.+?)\n.*?\*\*投票\*\*: 👍 (\d+)'
        
        matches = re.findall(pattern, content, re.DOTALL)
        
        for match in matches:
            op_name, contributor, add_time, verified, votes = match
            contributions.append({
                'operation': op_name.strip(),
                'contributor': contributor.strip(),
                'add_time': add_time.strip(),
                'verified': '✅' in verified,
                'votes': int(votes)
            })
        
        return contributions
    
    def calculate_stats(self):
        """计算统计信息"""
        contributions = self.parse_contributions()
        
        stats = defaultdict(lambda: {
            'total': 0,
            'verified': 0,
            'votes': 0,
            'operations': []
        })
        
        for contrib in contributions:
            user = contrib['contributor']
            stats[user]['total'] += 1
            stats[user]['operations'].append(contrib['operation'])
            stats[user]['votes'] += contrib['votes']
            
            if contrib['verified']:
                stats[user]['verified'] += 1
        
        return dict(stats)
    
    def get_ranking(self, limit=10):
        """获取排行榜"""
        stats = self.calculate_stats()
        
        # 计算分数
        ranking = []
        for user, data in stats.items():
            score = data['total'] * 10 + data['verified'] * 20 + data['votes'] * 5
            ranking.append({
                'user': user,
                'score': score,
                'total': data['total'],
                'verified': data['verified'],
                'votes': data['votes'],
                'operations': data['operations']
            })
        
        # 按分数排序
        ranking.sort(key=lambda x: x['score'], reverse=True)
        
        return ranking[:limit]
    
    def display_ranking(self, limit=10):
        """显示排行榜"""
        ranking = self.get_ranking(limit)
        
        print_color(Colors.BLUE, "╔════════════════════════════════════════╗")
        print_color(Colors.BLUE, "║   🏆 贡献者排行榜                      ║")
        print_color(Colors.BLUE, "╚════════════════════════════════════════╝")
        print()
        
        if not ranking:
            print_color(Colors.YELLOW, "⚠️  暂无贡献记录")
            return
        
        print(f"{'排名':<6}{'用户':<15}{'贡献数':<10}{'已验证':<10}{'得分':<10}")
        print("─" * 51)
        
        for i, user in enumerate(ranking, 1):
            medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else ' '
            print(f"{medal} {i:<5}{user['user']:<15}{user['total']:<10}{user['verified']:<10}{user['score']:<10}")
        
        print()
        print(f"统计时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def update_memory_ranking(self):
        """更新 memory 文件中的排行榜"""
        if not self.memory_file.exists():
            return
        
        content = self.memory_file.read_text()
        ranking = self.get_ranking(10)
        
        # 生成排行榜 Markdown
        ranking_md = "| 排名 | 贡献者 | 贡献数 | 已验证 | 得分 |\n"
        ranking_md += "|------|--------|--------|--------|------|\n"
        
        for i, user in enumerate(ranking, 1):
            medal = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else ''
            ranking_md += f"| {medal}{i} | {user['user']} | {user['total']} | {user['verified']} | {user['score']} |\n"
        
        # 找到并替换排行榜部分
        if "## 📊 贡献者排行榜" in content:
            # 替换现有排行榜
            start = content.find("## 📊 贡献者排行榜")
            end = content.find("\n\n##", start)
            if end == -1:
                end = len(content)
            
            new_section = f"""## 📊 贡献者排行榜

{ranking_md}

_最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"""
            
            content = content[:start] + new_section + content[end:]
        else:
            # 添加新部分
            ranking_section = f"""
---

## 📊 贡献者排行榜

{ranking_md}

_最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_"""
            
            content += ranking_section
        
        self.memory_file.write_text(content)
        print_color(Colors.GREEN, "✅ 排行榜已更新")


def main():
    """命令行入口"""
    ranking = ContributorRanking()
    
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'update':
        ranking.update_memory_ranking()
    else:
        ranking.display_ranking()


if __name__ == "__main__":
    main()
