"""
代码所有权追踪器 - 分析代码维护者和贡献者

这个脚本追踪每个文件/模块的主要维护者，识别专家和活跃贡献者。
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Set
from collections import defaultdict
import json
from datetime import datetime


class OwnershipTracker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def analyze_project_ownership(self, max_files: int = 100) -> Dict:
        """
        分析整个项目的代码所有权

        Args:
            max_files: 最多分析的文件数

        Returns:
            所有权分析结果
        """
        print(f"分析项目代码所有权: {self.project_root}")

        # 获取所有代码文件
        code_files = self._get_code_files()

        # 限制分析文件数
        code_files = code_files[:max_files]

        # 分析每个文件的所有权
        file_ownership = {}
        for file_path in code_files:
            ownership = self._analyze_file_ownership(file_path)
            file_ownership[str(file_path)] = ownership

        # 聚合分析
        author_stats = self._aggregate_author_stats(file_ownership)
        expert_areas = self._identify_expert_areas(file_ownership)
        collaboration_network = self._build_collaboration_network(file_ownership)

        return {
            'project_root': str(self.project_root),
            'analyzed_files': len(file_ownership),
            'file_ownership': file_ownership,
            'author_stats': author_stats,
            'expert_areas': expert_areas,
            'collaboration_network': collaboration_network
        }

    def analyze_file_ownership(self, file_path: str) -> Dict:
        """
        分析单个文件的所有权

        Args:
            file_path: 文件路径（相对于项目根目录）

        Returns:
            文件所有权信息
        """
        print(f"分析文件所有权: {file_path}")
        return self._analyze_file_ownership(file_path)

    def find_experts(self, topic: str, context: str = None) -> List[Dict]:
        """
        根据主题找到专家

        Args:
            topic: 主题关键词
            context: 上下文（可选，用于缩小搜索范围）

        Returns:
            专家列表
        """
        print(f"查找专家: {topic}")

        # 搜索相关文件
        relevant_files = self._search_files_by_topic(topic, context)

        # 分析这些文件的所有权
        file_owners = []
        for file_path in relevant_files[:20]:  # 限制文件数
            ownership = self._analyze_file_ownership(file_path)
            file_owners.append({
                'file': file_path,
                'ownership': ownership
            })

        # 聚合专家信息
        experts = self._aggregate_experts(file_owners)

        return experts

    def get_maintainer_suggestions(self, file_path: str,
                                  recent_days: int = 90) -> Dict:
        """
        获取维护者建议

        Args:
            file_path: 文件路径
            recent_days: 考察最近多少天

        Returns:
            维护者建议
        """
        print(f"获取维护者建议: {file_path}")

        ownership = self._analyze_file_ownership(file_path)

        # 获取最近的提交记录
        recent_commits = self._get_recent_commits(file_path, recent_days)

        # 获取活跃时间
        active_hours = self._get_active_hours(file_path)

        # 综合建议
        primary_maintainer = ownership['primary_author']

        recent_contributors = list(set([
            commit['author'] for commit in recent_commits
        ]))

        return {
            'file': file_path,
            'primary_maintainer': primary_maintainer,
            'secondary_maintainers': ownership['top_contributors'][:3],
            'recent_contributors': recent_contributors,
            'recent_commit_count': len(recent_commits),
            'active_hours': active_hours,
            'suggestion': self._generate_maintainer_suggestion(
                ownership, recent_commits, active_hours
            )
        }

    def _get_code_files(self) -> List[Path]:
        """获取所有代码文件"""
        extensions = ['.py', '.js', '.ts', '.tsx', '.java', '.go', '.rb', '.php']
        code_files = []

        for ext in extensions:
            code_files.extend(self.project_root.rglob(f'*{ext}'))

        return code_files

    def _analyze_file_ownership(self, file_path: str) -> Dict:
        """分析文件的所有权"""
        try:
            # 使用 git blame 分析每行的归属
            blame_result = subprocess.run(
                ['git', 'blame', '--line-porcelain', file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            # 解析 blame 输出
            line_authors = self._parse_blame_for_ownership(blame_result.stdout)

            if not line_authors:
                return {
                    'total_lines': 0,
                    'authors': {},
                    'primary_author': None,
                    'top_contributors': []
                }

            # 统计每个作者的代码行数
            author_line_counts = defaultdict(int)
            for author in line_authors:
                author_line_counts[author] += 1

            total_lines = len(line_authors)

            # 找出主要作者（贡献超过 50%）
            primary_author = None
            for author, count in author_line_counts.items():
                if count / total_lines >= 0.5:
                    primary_author = author
                    break

            # 找出前 5 位贡献者
            top_contributors = sorted(
                author_line_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            # 获取作者的最近提交时间
            author_last_active = self._get_author_last_active(file_path)

            return {
                'total_lines': total_lines,
                'authors': dict(author_line_counts),
                'primary_author': primary_author,
                'top_contributors': [
                    {'author': author, 'lines': count,
                     'percentage': count / total_lines}
                    for author, count in top_contributors
                ],
                'author_last_active': author_last_active
            }

        except subprocess.CalledProcessError:
            return {
                'total_lines': 0,
                'authors': {},
                'primary_author': None,
                'top_contributors': []
            }

    def _parse_blame_for_ownership(self, blame_output: str) -> List[str]:
        """从 blame 输出中提取作者列表"""
        lines = blame_output.split('\n')
        authors = []

        for line in lines:
            if line.startswith('author '):
                authors.append(line[7:])

        return authors

    def _get_author_last_active(self, file_path: str) -> Dict[str, str]:
        """获取作者最后活跃时间"""
        try:
            result = subprocess.run(
                ['git', 'log', '--format=%an|%ai', '--', file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            author_last_active = {}
            for line in result.stdout.strip().split('\n'):
                if line:
                    author, date = line.split('|')
                    if author not in author_last_active:
                        author_last_active[author] = date

            return author_last_active

        except subprocess.CalledProcessError:
            return {}

    def _get_recent_commits(self, file_path: str, days: int) -> List[Dict]:
        """获取最近的提交"""
        try:
            since_date = datetime.now().strftime(f'%Y-%m-%d')

            result = subprocess.run(
                ['git', 'log', f'--since={since_date}', '--format=%an|%ai|%s',
                 '--', file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    author, date, message = line.split('|', 2)
                    commits.append({
                        'author': author,
                        'date': date,
                        'message': message
                    })

            return commits

        except subprocess.CalledProcessError:
            return []

    def _get_active_hours(self, file_path: str) -> List[int]:
        """获取活跃时间段（小时）"""
        try:
            result = subprocess.run(
                ['git', 'log', '--format=%ai', '--', file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            hours = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    # 提取小时
                    hour = int(line.split(' ')[1].split(':')[0])
                    hours.append(hour)

            # 统计最常见的小时
            from collections import Counter
            hour_counts = Counter(hours)

            return [hour for hour, count in hour_counts.most_common(3)]

        except subprocess.CalledProcessError:
            return []

    def _aggregate_author_stats(self, file_ownership: Dict) -> Dict:
        """聚合作者统计"""
        author_stats = defaultdict(lambda: {
            'files_owned': 0,
            'total_lines': 0,
            'primary_files': []
        })

        for file_path, ownership in file_ownership.items():
            primary_author = ownership['primary_author']
            if primary_author:
                author_stats[primary_author]['files_owned'] += 1
                author_stats[primary_author]['total_lines'] += ownership['total_lines']
                author_stats[primary_author]['primary_files'].append(file_path)

        return dict(author_stats)

    def _identify_expert_areas(self, file_ownership: Dict) -> List[Dict]:
        """识别专家领域"""
        # 简单实现：基于文件路径分类
        expert_areas = []

        for file_path, ownership in file_ownership.items():
            primary_author = ownership['primary_author']
            if primary_author:
                # 从文件路径提取模块/主题
                path_parts = Path(file_path).parts

                if len(path_parts) >= 2:
                    module = path_parts[-2]  # 倒数第二个部分
                    expert_areas.append({
                        'author': primary_author,
                        'module': module,
                        'file': file_path,
                        'ownership': ownership['top_contributors'][0]['percentage']
                    })

        # 聚合相同作者的相同模块
        from collections import defaultdict
        module_experts = defaultdict(lambda: defaultdict(list))

        for area in expert_areas:
            module_experts[area['module']][area['author']].append(area['ownership'])

        result = []
        for module, authors in module_experts.items():
            for author, ownerships in authors.items():
                avg_ownership = sum(ownerships) / len(ownerships)
                result.append({
                    'module': module,
                    'author': author,
                    'file_count': len(ownerships),
                    'average_ownership': avg_ownership
                })

        return sorted(result, key=lambda x: x['average_ownership'], reverse=True)[:20]

    def _build_collaboration_network(self, file_ownership: Dict) -> Dict:
        """构建协作网络"""
        from itertools import combinations

        collaborations = defaultdict(lambda: {'count': 0, 'files': []})

        for file_path, ownership in file_ownership.items():
            contributors = [
                contributor['author']
                for contributor in ownership['top_contributors'][:5]
            ]

            # 计算所有两两组合
            for author1, author2 in combinations(contributors, 2):
                key = tuple(sorted([author1, author2]))
                collaborations[key]['count'] += 1
                collaborations[key]['files'].append(file_path)

        # 转换为可序列化的格式
        result = {}
        for (author1, author2), info in collaborations.items():
            key = f"{author1} <-> {author2}"
            result[key] = {
                'count': info['count'],
                'files': info['files'][:10]  # 限制文件数
            }

        # 排序
        result = dict(sorted(
            result.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        )[:20])

        return result

    def _search_files_by_topic(self, topic: str, context: str = None) -> List[str]:
        """根据主题搜索文件"""
        # 使用 git log 搜索关键词
        search_cmd = ['git', 'log', '--all', '--pretty=format:', '--name-only',
                     '--grep', topic]

        if context:
            search_cmd.append(context)

        try:
            result = subprocess.run(
                search_cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )

            files = set()
            for line in result.stdout.strip().split('\n'):
                if line and not line.startswith('.'):
                    files.add(line)

            return list(files)

        except subprocess.CalledProcessError:
            return []

    def _aggregate_experts(self, file_owners: List[Dict]) -> List[Dict]:
        """聚合专家信息"""
        from collections import defaultdict

        expert_scores = defaultdict(lambda: {
            'files': 0,
            'total_ownership': 0,
            'files_list': []
        })

        for file_info in file_owners:
            ownership = file_info['ownership']
            for contributor in ownership['top_contributors'][:3]:
                author = contributor['author']
                score = contributor['percentage']

                expert_scores[author]['files'] += 1
                expert_scores[author]['total_ownership'] += score
                expert_scores[author]['files_list'].append({
                    'file': file_info['file'],
                    'ownership': score
                })

        # 计算综合得分
        experts = []
        for author, info in expert_scores.items():
            avg_ownership = info['total_ownership'] / info['files']
            score = info['files'] * avg_ownership  # 文件数 × 平均所有权

            experts.append({
                'author': author,
                'file_count': info['files'],
                'average_ownership': avg_ownership,
                'total_ownership': info['total_ownership'],
                'score': score,
                'sample_files': info['files_list'][:5]
            })

        return sorted(experts, key=lambda x: x['score'], reverse=True)[:10]

    def _generate_maintainer_suggestion(self, ownership: Dict,
                                      recent_commits: List[Dict],
                                      active_hours: List[int]) -> str:
        """生成维护者建议"""
        if not ownership['primary_author']:
            return "此文件没有明确的主要维护者，建议联系最近的贡献者"

        primary = ownership['primary_author']

        if recent_commits:
            last_commit_author = recent_commits[0]['author']
            if last_commit_author != primary:
                return f"主要维护者是 {primary}，但最近由 {last_commit_author} 活跃"

        if active_hours:
            peak_hours = ', '.join(str(h) for h in active_hours)
            return f"主要维护者是 {primary}，通常在 {peak_hours} 点活跃"

        return f"主要维护者是 {primary}"


def track_ownership(project_root: str, file_path: str = None,
                    topic: str = None, output_file: str = None) -> Dict:
    """
    追踪代码所有权

    Args:
        project_root: 项目根目录
        file_path: 要分析的文件路径（可选）
        topic: 要搜索的主题（可选）
        output_file: 输出 JSON 文件路径（可选）

    Returns:
        所有权分析结果
    """
    tracker = OwnershipTracker(project_root)

    if file_path:
        result = tracker.get_maintainer_suggestions(file_path)
    elif topic:
        result = {
            'topic': topic,
            'experts': tracker.find_experts(topic)
        }
    else:
        result = tracker.analyze_project_ownership()

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"报告已保存到: {output_file}")

    return result


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python ownership_tracker.py <项目根目录> [文件路径] [主题] [输出文件]")
        sys.exit(1)

    project_root = sys.argv[1]
    file_path = sys.argv[2] if len(sys.argv) > 2 else None
    topic = sys.argv[3] if len(sys.argv) > 3 else None
    output_file = sys.argv[4] if len(sys.argv) > 4 else None

    result = track_ownership(project_root, file_path, topic, output_file)

    print("\n=== 代码所有权分析摘要 ===")
    if file_path:
        print(f"文件: {file_path}")
        if 'suggestion' in result:
            print(f"建议: {result['suggestion']}")
    elif topic:
        print(f"主题: {topic}")
        if 'experts' in result:
            print(f"专家数量: {len(result['experts'])}")
    else:
        print(f"分析文件数: {result['analyzed_files']}")
