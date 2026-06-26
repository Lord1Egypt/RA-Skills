#!/usr/bin/env python3
"""
检索引擎 - 搜索公共记忆空间（跨Agent知识检索）
"""

import re
from pathlib import Path
from datetime import datetime, date, timedelta
import config

class MemoryRetriever:
    def __init__(self, config_obj):
        self.config = config_obj
        base_path = self.config.get('memory.base_path', '~/.openclaw/workspace')
        self.workspace_root = Path(base_path).expanduser()

    def search_public(self, query, agent_filter=None, date_range=None, limit=None):
        """
        搜索公共记忆空间

        Args:
            query: 搜索关键词
            agent_filter: 限制特定Agent (str or list)
            date_range: 日期范围 (start_date, end_date) 元组
            limit: 最大返回结果数

        Returns:
            dict: 搜索结果
        """
        if limit is None:
            limit = self.config.get('search.max_public_results', 5)

        min_relevance = self.config.get('search.min_relevance', 0.5)

        # 1. 扫描公共空间
        public_root = self.workspace_root / self.config.get('memory.public_root')
        if not public_root.exists():
            return {
                'success': True,
                'query': query,
                'total': 0,
                'results': [],
                'message': '公共记忆空间为空'
            }

        # 2. 收集所有公共文件
        candidates = self._collect_public_files(public_root, agent_filter, date_range)

        # 3. 计算相关性得分
        scored_results = []
        for file_path, metadata in candidates:
            score = self._calculate_relevance(query, file_path, metadata)
            if score >= min_relevance:
                scored_results.append({
                    'path': str(file_path),
                    'agent': metadata.get('agent'),
                    'date': metadata.get('date'),
                    'title': metadata.get('title'),
                    'score': round(score, 3),
                    'snippet': self._extract_snippet(file_path, query),
                    'keywords': metadata.get('keywords', '')
                })

        # 4. 排序并限制数量
        scored_results.sort(key=lambda x: -x['score'])
        total = len(scored_results)
        results = scored_results[:limit]

        return {
            'success': True,
            'query': query,
            'total': total,
            'returned': len(results),
            'results': results,
            'search_scope': 'public',
            'timestamp': datetime.now().isoformat()
        }

    def search_private(self, query, agent_id, limit=None):
        """搜索当前Agent的私有记忆"""
        if limit is None:
            limit = self.config.get('search.max_private_results', 3)

        private_dir = self.workspace_root / self.config.get('memory.private_root') / agent_id
        if not private_dir.exists():
            return {
                'success': True,
                'query': query,
                'total': 0,
                'results': [],
                'message': f'Agent {agent_id} 的私有记忆为空'
            }

        # 收集私有文件
        candidates = []
        for pattern in ['medium-term/*.md', 'long-term/**/*.md']:
            for file_path in private_dir.glob(pattern):
                if file_path.is_file():
                    metadata = self._extract_metadata(file_path)
                    candidates.append((file_path, metadata))

        # 计算得分
        scored = []
        for file_path, metadata in candidates:
            score = self._calculate_relevance(query, file_path, metadata)
            scored.append({
                'path': str(file_path),
                'agent': agent_id,
                'date': metadata.get('date'),
                'title': metadata.get('title', file_path.stem),
                'score': round(score, 3),
                'snippet': self._extract_snippet(file_path, query),
                'scope': 'private'
            })

        scored.sort(key=lambda x: -x['score'])
        return {
            'success': True,
            'query': query,
            'total': len(scored),
            'returned': len(scored[:limit]),
            'results': scored[:limit],
            'search_scope': 'private'
        }

    def search_all(self, query, agent_id=None, limit=None):
        """
        智能搜索：优先公共空间，然后私有（如果指定agent）
        遵循配置：search.public_first
        """
        public_first = self.config.get('search.public_first', True)

        if agent_id and public_first:
            # 先搜公共，再搜私有
            public_results = self.search_public(query, limit=limit)
            private_results = self.search_private(query, agent_id, limit=limit)

            # 合并结果，公共加权更高
            all_results = []
            weight_public = self.config.get('search.weight_public', 1.2)
            weight_private = self.config.get('search.weight_private', 1.0)

            for r in public_results['results']:
                r['score'] *= weight_public
                r['scope'] = 'public'
                all_results.append(r)

            for r in private_results['results']:
                r['score'] *= weight_private
                r['scope'] = 'private'
                all_results.append(r)

            all_results.sort(key=lambda x: -x['score'])
            final_limit = limit or (public_results['limit'] + private_results['limit'])

            return {
                'success': True,
                'query': query,
                'total': len(all_results),
                'returned': len(all_results[:final_limit]),
                'results': all_results[:final_limit],
                'search_scope': 'public+private',
                'strategy': 'public_first'
            }

        elif agent_id:
            # 只搜私有
            return self.search_private(query, agent_id, limit)

        else:
            # 只搜公共
            return self.search_public(query, limit=limit)

    def _collect_public_files(self, public_root, agent_filter=None, date_range=None):
        """收集公共记忆文件"""
        candidates = []

        for agent_dir in public_root.iterdir():
            if not agent_dir.is_dir():
                continue

            agent_id = agent_dir.name

            # Agent过滤
            if agent_filter:
                if isinstance(agent_filter, str):
                    if agent_id != agent_filter:
                        continue
                elif isinstance(agent_filter, list) and agent_id not in agent_filter:
                    continue

            # 遍历日期目录
            for date_dir in agent_dir.iterdir():
                if not date_dir.is_dir():
                    continue

                try:
                    dir_date = datetime.strptime(date_dir.name, '%Y-%m-%d').date()
                except ValueError:
                    continue

                # 日期范围过滤
                if date_range:
                    start, end = date_range
                    if dir_date < start or dir_date > end:
                        continue

                # 收集文件
                for file_path in date_dir.glob('*.md'):
                    metadata = self._extract_metadata(file_path)
                    candidates.append((file_path, metadata))

        return candidates

    def _extract_metadata(self, file_path):
        """从文件提取元数据"""
        metadata = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(2000)  # 只读前2K

            # YAML front matter
            if content.startswith('---'):
                end = content.find('---', 3)
                if end != -1:
                    front = content[3:end].strip()
                    for line in front.split('\n'):
                        if ':' in line:
                            key, val = line.split(':', 1)
                            metadata[key.strip()] = val.strip()

            # 如果元数据缺少关键字段，从路径推断
            if 'agent' not in metadata:
                # public/{agent}/{date}/file.md
                parts = file_path.parts
                if len(parts) >= 4:
                    metadata['agent'] = parts[-3]
            if 'date' not in metadata:
                try:
                    metadata['date'] = file_path.parent.name
                except:
                    pass
            if 'title' not in metadata:
                metadata['title'] = file_path.stem

        except Exception as e:
            pass

        return metadata

    def _calculate_relevance(self, query, file_path, metadata):
        """计算查询相关性得分"""
        score = 0.0

        # 1. 标题匹配（最高权重）
        title = metadata.get('title', '').lower()
        if query.lower() in title:
            score += 0.4

        # 2. 关键词匹配
        keywords = metadata.get('keywords', '').lower()
        if query.lower() in keywords:
            score += 0.3

        # 3. Agent 名称匹配（如果查询是 agent 名）
        agent = metadata.get('agent', '').lower()
        if query.lower() in agent:
            score += 0.2

        # 4. 内容全文搜索（简易：抽样）
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sample = f.read(5000).lower()
            if query.lower() in sample:
                score += 0.1
        except:
            pass

        # 5. 新鲜度衰减（越新的文档得分略高）
        try:
            file_date = datetime.strptime(metadata.get('date', '2000-01-01'), '%Y-%m-%d').date()
            days_old = (date.today() - file_date).days
            recency_bonus = max(0, 0.1 - days_old * 0.001)  # 每天衰减0.1%
            score += recency_bonus
        except:
            pass

        return min(1.0, score)  # 封顶1.0

    def _extract_snippet(self, file_path, query, max_length=200):
        """提取包含查询词的内容片段"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(10000)  # 读前10K

            # 查找查询词位置
            idx = content.lower().find(query.lower())
            if idx == -1:
                return ''

            # 提取上下文
            start = max(0, idx - 50)
            end = min(len(content), idx + len(query) + 150)
            snippet = content[start:end].replace('\n', ' ')

            if start > 0:
                snippet = '...' + snippet
            if end < len(content):
                snippet = snippet + '...'

            return snippet

        except Exception as e:
            return ''
