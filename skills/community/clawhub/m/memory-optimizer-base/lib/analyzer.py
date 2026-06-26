#!/usr/bin/env python3
"""
记忆分析器（增强版）- 扫描公共+私有双层记忆系统
"""

import os
import re
from datetime import datetime, date, timedelta
from pathlib import Path
import config

class MemoryAnalyzer:
    def __init__(self, config_obj):
        self.config = config_obj
        base_path = self.config.get('memory.base_path', '~/.openclaw/workspace')
        self.workspace_root = Path(base_path).expanduser()

    def analyze(self, agent_id=None, include_public=True):
        """
        执行全面分析

        Args:
            agent_id: 指定Agent（None表示分析所有）
            include_public: 是否包含公共空间

        Returns:
            dict: 分析报告
        """
        report = {
            'total_files': 0,
            'total_entries': 0,
            'total_size_bytes': 0,
            'by_agent': {},
            'by_tier': {'short': 0, 'medium': 0, 'long': 0},
            'health_score': 100,
            'issues': [],
            'suggestions': [],
            'spaces': {}
        }

        # 分析私有空间
        if agent_id:
            private_report = self._analyze_private(agent_id)
            report['by_agent'][agent_id] = private_report
            report['total_files'] += private_report['files']
            report['total_entries'] += private_report['entries']
            report['total_size_bytes'] += private_report['size']
            report['by_tier']['medium'] += private_report.get('medium_count', 0)
            report['by_tier']['long'] += private_report.get('long_count', 0)
        else:
            # 分析所有Agent的私有空间
            private_root = self.workspace_root / self.config.get('memory.private_root')
            if private_root.exists():
                for agent_dir in private_root.iterdir():
                    if agent_dir.is_dir():
                        agent_report = self._analyze_private(agent_dir.name)
                        report['by_agent'][agent_dir.name] = agent_report
                        report['total_files'] += agent_report['files']
                        report['total_entries'] += agent_report['entries']
                        report['total_size_bytes'] += agent_report['size']
                        report['by_tier']['medium'] += agent_report.get('medium_count', 0)
                        report['by_tier']['long'] += agent_report.get('long_count', 0)

        # 分析公共空间
        if include_public:
            public_report = self._analyze_public()
            report['spaces']['public'] = public_report
            report['total_files'] += public_report['files']
            report['total_entries'] += public_report['entries']
            report['total_size_bytes'] += public_report['size']

        # 健康度评估
        report['health_score'] = self._calculate_health_score(report)

        # 生成建议
        report['suggestions'] = self._generate_suggestions(report)

        return report

    def _analyze_private(self, agent_id):
        """分析单个Agent的私有记忆"""
        private_root = self.workspace_root / self.config.get('memory.private_root') / agent_id
        report = {
            'files': 0,
            'entries': 0,
            'size': 0,
            'medium_count': 0,
            'long_count': 0,
            'last_updated': None
        }

        if not private_root.exists():
            return report

        # 扫描 medium-term 和 long-term
        for tier in ['medium-term', 'long-term']:
            tier_dir = private_root / tier
            if tier_dir.exists():
                for file_path in tier_dir.rglob('*.md'):
                    try:
                        stat = file_path.stat()
                        report['files'] += 1
                        report['size'] += stat.st_size

                        # 估算条目数（基于 markdown 标题）
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            entries = len(re.findall(r'^#{1,6} ', content, re.MULTILINE))
                            report['entries'] += max(1, entries)

                        if tier == 'medium-term':
                            report['medium_count'] += 1
                        else:
                            report['long_count'] += 1

                        # 更新最近修改时间
                        if report['last_updated'] is None or stat.st_mtime > report['last_updated']:
                            report['last_updated'] = stat.st_mtime

                    except Exception as e:
                        pass

        return report

    def _analyze_public(self):
        """分析公共记忆空间"""
        public_root = self.workspace_root / self.config.get('memory.public_root')
        report = {
            'files': 0,
            'entries': 0,
            'size': 0,
            'agents': set(),
            'date_range': {'earliest': None, 'latest': None},
            'by_agent': {}
        }

        if not public_root.exists():
            return report

        for agent_dir in public_root.iterdir():
            if not agent_dir.is_dir():
                continue

            agent_id = agent_dir.name
            report['agents'].add(agent_id)
            agent_files = 0
            agent_size = 0

            for date_dir in agent_dir.iterdir():
                if not date_dir.is_dir():
                    continue

                try:
                    dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d').date()
                    if report['date_range']['earliest'] is None or dir_date < report['date_range']['earliest']:
                        report['date_range']['earliest'] = dir_date
                    if report['date_range']['latest'] is None or dir_date > report['date_range']['latest']:
                        report['date_range']['latest'] = dir_date
                except:
                    continue

                for file_path in date_dir.glob('*.md'):
                    try:
                        stat = file_path.stat()
                        report['files'] += 1
                        report['size'] += stat.st_size
                        agent_files += 1
                        agent_size += stat.st_size

                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            entries = len(re.findall(r'^#{1,6} ', content, re.MULTILINE))
                            report['entries'] += max(1, entries)
                    except:
                        pass

            report['by_agent'][agent_id] = {'files': agent_files, 'size': agent_size}

        report['agents'] = list(report['agents'])
        return report

    def _calculate_health_score(self, report):
        """计算健康度评分"""
        score = 100

        # 文件总数
        if report['total_files'] == 0:
            score -= 50
            report['issues'].append({'type': 'no_files', 'description': '未找到任何记忆文件'})
        elif report['total_files'] < 5:
            score -= 20
            report['issues'].append({'type': 'few_files', 'description': '记忆文件较少'})

        # 配置文件
        has_private = any(a.get('files', 0) > 0 for a in report['by_agent'].values())
        has_public = report['spaces'].get('public', {}).get('files', 0) > 0

        if not has_private:
            score -= 30
            report['issues'].append({'type': 'no_private', 'description': '缺乏私有记忆空间'})

        if not has_public:
            score -= 20
            report['issues'].append({'type': 'no_public', 'description': '缺乏公共记忆空间'})

        # 最近更新检查
        today = date.today()
        has_today_update = False
        for agent_data in report['by_agent'].values():
            # 简化：检查末次修改时间
            pass  # 需要额外跟踪，暂略

        if not has_today_update:
            score -= 10
            report['issues'].append({'type': 'stale', 'description': '今日无记忆更新'})

        return max(0, score)

    def _generate_suggestions(self, report):
        """生成优化建议"""
        suggestions = []

        if report['health_score'] < 80:
            suggestions.append("增加记忆记录频率，及时总结每日工作")

        if 'public' not in report['spaces'] or report['spaces']['public']['files'] == 0:
            suggestions.append("公共记忆空间为空，建议上传重要总结")

        if len(report['by_agent']) == 0:
            suggestions.append("尚未配置任何Agent，请运行 init 命令初始化")

        if report['total_entries'] < 50:
            suggestions.append("记忆条目较少，建议持续积累")

        # 检查空间分布
        if 'public' in report['spaces']:
            public_ratio = report['spaces']['public']['files'] / max(1, report['total_files'])
            if public_ratio < 0.2:
                suggestions.append("公共记忆占比过低，鼓励多分享经验到公共空间")

        return suggestions
