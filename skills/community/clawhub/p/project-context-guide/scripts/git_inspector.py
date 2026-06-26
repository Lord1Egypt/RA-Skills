"""
Git 历史检查器 - 追溯代码决策和变更历史

这个脚本分析 Git 历史记录，提取关键决策点、设计讨论和变更时间线。
"""

import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import json


class GitInspector:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self._validate_git_repo()

    def _validate_git_repo(self):
        """验证是否为 Git 仓库"""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Git 仓库确认: {self.project_root}")
        except subprocess.CalledProcessError:
            raise ValueError(f"{self.project_root} 不是有效的 Git 仓库")

    def analyze_file_history(self, file_path: str, max_commits: int = 50) -> Dict:
        """
        分析单个文件的完整历史

        Args:
            file_path: 文件路径（相对于项目根目录）
            max_commits: 最多分析的提交数

        Returns:
            文件历史分析结果
        """
        print(f"分析文件历史: {file_path}")

        # 获取文件的完整历史
        commits = self._get_file_commits(file_path, max_commits)

        # 获取每个提交的详细信息
        detailed_commits = []
        for commit in commits:
            details = self._get_commit_details(commit['hash'])
            details['file_change'] = self._get_file_change(commit['hash'], file_path)
            detailed_commits.append(details)

        # 分析关键决策点
        key_decisions = self._identify_key_decisions(detailed_commits)

        # 统计贡献者
        contributors = self._analyze_contributors(detailed_commits)

        # 构建时间线
        timeline = self._build_timeline(detailed_commits)

        return {
            'file': file_path,
            'total_commits': len(detailed_commits),
            'first_commit': detailed_commits[-1] if detailed_commits else None,
            'latest_commit': detailed_commits[0] if detailed_commits else None,
            'commits': detailed_commits,
            'key_decisions': key_decisions,
            'contributors': contributors,
            'timeline': timeline
        }

    def analyze_line_history(self, file_path: str, line_number: int,
                            context_lines: int = 3) -> Dict:
        """
        追溯特定代码行或代码块的历史

        Args:
            file_path: 文件路径
            line_number: 行号
            context_lines: 上下文行数

        Returns:
            代码块历史分析
        """
        print(f"追溯代码块历史: {file_path}:{line_number}")

        # 使用 git blame 获取行的历史
        blame_output = self._git_blame(file_path, line_number, context_lines)

        # 解析 blame 输出
        blamed_lines = self._parse_blame_output(blame_output)

        # 获取这些提交的详细信息
        commits = {}
        for line_info in blamed_lines:
            commit_hash = line_info['commit']
            if commit_hash not in commits:
                commits[commit_hash] = self._get_commit_details(commit_hash)

        return {
            'file': file_path,
            'line_number': line_number,
            'context_lines': context_lines,
            'blamed_lines': blamed_lines,
            'related_commits': list(commits.values())
        }

    def search_commits_by_keyword(self, keyword: str, file_path: str = None,
                                 max_results: int = 20) -> List[Dict]:
        """
        根据关键词搜索提交

        Args:
            keyword: 搜索关键词
            file_path: 限制搜索范围（可选）
            max_results: 最大结果数

        Returns:
            匹配的提交列表
        """
        print(f"搜索提交关键词: {keyword}")

        # 构建搜索命令
        search_cmd = ['git', 'log', '--all', '--grep', keyword,
                     '--format=%H', '-n', str(max_results)]

        if file_path:
            search_cmd.extend(['--', file_path])

        result = subprocess.run(
            search_cmd,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=True
        )

        commit_hashes = result.stdout.strip().split('\n') if result.stdout.strip() else []

        # 获取每个提交的详细信息
        commits = []
        for commit_hash in commit_hashes:
            if commit_hash:
                details = self._get_commit_details(commit_hash)
                if file_path:
                    details['file_change'] = self._get_file_change(commit_hash, file_path)
                commits.append(details)

        return commits

    def _get_file_commits(self, file_path: str, max_commits: int) -> List[Dict]:
        """获取文件的提交历史"""
        result = subprocess.run(
            ['git', 'log', '--format=%H|%ai|%an', '--follow',
             '--', file_path, '-n', str(max_commits)],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                hash_str, date_str, author = line.split('|')
                commits.append({
                    'hash': hash_str,
                    'date': date_str,
                    'author': author
                })

        return commits

    def _get_commit_details(self, commit_hash: str) -> Dict:
        """获取提交的详细信息"""
        # 获取提交信息
        message_result = subprocess.run(
            ['git', 'log', '-1', '--format=%B', commit_hash],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=True
        )

        # 获取提交的其他信息
        log_result = subprocess.run(
            ['git', 'log', '-1', '--format=%H|%ai|%an|%ae|%P',
             commit_hash],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=True
        )

        hash_str, date_str, author, email, parents = log_result.stdout.strip().split('|')

        # 提取 issue/PR 编号
        issue_numbers = self._extract_issue_numbers(message_result.stdout)

        # 提取关键词
        keywords = self._extract_keywords(message_result.stdout)

        return {
            'hash': hash_str,
            'date': date_str,
            'author': author,
            'email': email,
            'parents': parents.split(' ') if parents else [],
            'message': message_result.stdout.strip(),
            'issue_numbers': issue_numbers,
            'keywords': keywords
        }

    def _get_file_change(self, commit_hash: str, file_path: str) -> Dict:
        """获取文件在特定提交中的变更"""
        try:
            # 获取变更统计
            stat_result = subprocess.run(
                ['git', 'show', '--stat', '--format=', commit_hash, '--',
                 file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            # 获取实际的 diff
            diff_result = subprocess.run(
                ['git', 'show', commit_hash, '--', file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            return {
                'stats': stat_result.stdout.strip(),
                'diff': diff_result.stdout,
                'lines_added': stat_result.stdout.count('+') if stat_result.stdout else 0,
                'lines_removed': stat_result.stdout.count('-') if stat_result.stdout else 0
            }

        except subprocess.CalledProcessError:
            return {}

    def _git_blame(self, file_path: str, line_number: int, context: int) -> str:
        """执行 git blame 命令"""
        start_line = max(1, line_number - context)
        end_line = line_number + context

        result = subprocess.run(
            ['git', 'blame', '-L', f'{start_line},{end_line}',
             '--line-porcelain', file_path],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            check=True
        )

        return result.stdout

    def _parse_blame_output(self, blame_output: str) -> List[Dict]:
        """解析 git blame 输出"""
        lines = blame_output.split('\n')
        blamed_lines = []
        current_line_info = {}

        for line in lines:
            if line.startswith('\t'):
                # 这是代码内容行
                current_line_info['content'] = line[1:]
                blamed_lines.append(current_line_info)
                current_line_info = {}
            else:
                # 这是 blame 信息行
                if line.startswith('author '):
                    current_line_info['author'] = line[7:]
                elif line.startswith('author-mail '):
                    current_line_info['email'] = line[12:]
                elif line.startswith('author-time '):
                    current_line_info['timestamp'] = int(line[12:])
                elif line.startswith('summary '):
                    current_line_info['summary'] = line[8:]
                elif not line.startswith('\t') and not line.startswith(' '):
                    # 这是 commit hash
                    current_line_info['commit'] = line.split()[0]

        return blamed_lines

    def _identify_key_decisions(self, commits: List[Dict]) -> List[Dict]:
        """识别关键决策点"""
        key_decisions = []

        for commit in commits:
            # 基于关键词识别重要决策
            decision_keywords = ['重构', '重构', '架构', '设计', '决策', '优化',
                                'refactor', 'architecture', 'design', 'decision',
                                'migration', 'upgrade']

            if any(keyword in commit['message'].lower() for keyword in decision_keywords):
                key_decisions.append({
                    'commit': commit['hash'],
                    'date': commit['date'],
                    'author': commit['author'],
                    'message': commit['message'],
                    'type': self._classify_decision(commit['message'])
                })

        return key_decisions[:10]  # 限制返回数量

    def _classify_decision(self, message: str) -> str:
        """分类决策类型"""
        if '重构' in message or 'refactor' in message.lower():
            return 'refactor'
        elif '架构' in message or 'architecture' in message.lower():
            return 'architecture'
        elif '优化' in message or 'optimization' in message.lower() or 'optimize' in message.lower():
            return 'optimization'
        elif '迁移' in message or 'migration' in message.lower():
            return 'migration'
        elif '修复' in message or 'fix' in message.lower():
            return 'bugfix'
        else:
            return 'other'

    def _analyze_contributors(self, commits: List[Dict]) -> List[Dict]:
        """分析贡献者"""
        contributor_stats = {}

        for commit in commits:
            author = commit['author']
            if author not in contributor_stats:
                contributor_stats[author] = {
                    'commits': 0,
                    'first_commit': commit['date'],
                    'latest_commit': commit['date']
                }

            contributor_stats[author]['commits'] += 1
            contributor_stats[author]['latest_commit'] = commit['date']

        # 排序
        sorted_contributors = sorted(
            contributor_stats.items(),
            key=lambda x: x[1]['commits'],
            reverse=True
        )

        return [
            {'author': author, **stats}
            for author, stats in sorted_contributors
        ]

    def _build_timeline(self, commits: List[Dict]) -> List[Dict]:
        """构建时间线"""
        timeline = []

        for commit in commits:
            timeline.append({
                'date': commit['date'],
                'commit': commit['hash'],
                'author': commit['author'],
                'summary': commit['message'].split('\n')[0],
                'type': self._classify_decision(commit['message'])
            })

        return timeline

    def _extract_issue_numbers(self, message: str) -> List[str]:
        """从提交消息中提取 issue/PR 编号"""
        # 匹配 #123, #1234 等格式
        pattern = r'#(\d{3,})'
        matches = re.findall(pattern, message)
        return matches

    def _extract_keywords(self, message: str) -> List[str]:
        """从提交消息中提取关键词"""
        # 常见的关键词列表
        tech_keywords = [
            '性能', '并发', '缓存', '数据库', 'API', '前端', '后端',
            '测试', '部署', '配置', '依赖', '版本', '兼容',
            'performance', 'concurrency', 'cache', 'database', 'api',
            'frontend', 'backend', 'testing', 'deployment', 'config',
            'dependency', 'version', 'compatibility'
        ]

        found = []
        for keyword in tech_keywords:
            if keyword.lower() in message.lower():
                found.append(keyword)

        return found


def inspect_git_history(project_root: str, file_path: str = None,
                        function_name: str = None, output_file: str = None) -> Dict:
    """
    检查 Git 历史

    Args:
        project_root: 项目根目录
        file_path: 要分析的文件路径（可选）
        function_name: 要搜索的关键词（可选）
        output_file: 输出 JSON 文件路径（可选）

    Returns:
        Git 历史分析结果
    """
    inspector = GitInspector(project_root)

    if file_path:
        # 分析文件历史
        if function_name:
            # 假设 function_name 是行号
            try:
                line_number = int(function_name)
                return inspector.analyze_line_history(file_path, line_number)
            except ValueError:
                # 搜索关键词
                commits = inspector.search_commits_by_keyword(function_name, file_path)
                result = {'file': file_path, 'keyword': function_name, 'commits': commits}
        else:
            result = inspector.analyze_file_history(file_path)
    elif function_name:
        # 全局搜索关键词
        commits = inspector.search_commits_by_keyword(function_name)
        result = {'keyword': function_name, 'commits': commits}
    else:
        result = {'error': '需要指定 file_path 或 function_name'}

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到: {output_file}")

    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python git_inspector.py <项目根目录> [文件路径] [关键词/行号] [输出文件]")
        sys.exit(1)

    project_root = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else None
    function_name = sys.argv[3] if len(sys.argv) > 3 else None
    output_file = sys.argv[4] if len(sys.argv) > 4 else None

    result = inspect_git_history(project_root, file_path, function_name, output_file)

    print("\n=== Git 历史分析摘要 ===")
    if file_path:
        print(f"文件: {file_path}")
        if 'total_commits' in result:
            print(f"总提交数: {result['total_commits']}")
        if 'blamed_lines' in result:
            print(f"追溯代码块: {len(result['blamed_lines'])} 行")
    elif function_name:
        print(f"关键词: {function_name}")
        if 'commits' in result:
            print(f"匹配提交数: {len(result['commits'])}")
