#!/usr/bin/env python3
"""
调研编排系统：6维并行调研
"""

import json
import requests
from pathlib import Path
from typing import Dict, List
import subprocess


class ResearchOrchestrator:
    """调研编排器"""

    # 6个调研维度
    DIMENSIONS = [
        '01-writings',      # 著作与系统思考
        '02-conversations', # 长对话与即兴思考
        '03-expression-dna',# 碎片表达与风格DNA
        '04-external-views',# 他者视角与批评
        '05-decisions',     # 决策记录与行动
        '06-timeline'       # 人物时间线
    ]

    # 信息源黑名单
    BLACKLISTED_SOURCES = [
        'zhihu.com',
        'mp.weixin.qq.com',
        'weixin.qq.com'
    ]

    # 优先信息源（中文人物）
    CHINESE_PRIORITY_SOURCES = [
        'bilibili.com',     # B站视频
        'ximalaya.com',     # 喜马拉雅播客
        'dedao.cn',         # 得到
        'thepaper.cn',      # 澎湃新闻
        'caixin.com',       # 财新网
        'people.com.cn',    # 人民网
        'xinhuanet.com'     # 新华网
    ]

    def __init__(self):
        self.research_plan = {}
        self.agent_tasks = {}

    def generate_research_plan(self, os_type: str, target: str,
                               mode: str = 'network') -> Dict:
        """生成调研计划"""

        # 根据HumanOS类型调整维度优先级
        dimension_priorities = self._get_dimension_priorities(os_type)

        # 根据模式调整策略
        strategy = self._get_strategy(mode)

        # 生成调研计划
        research_plan = {
            'os_type': os_type,
            'target': target,
            'mode': mode,
            'strategy': strategy,
            'dimensions': {},
            'total_dimensions': len(self.DIMENSIONS)
        }

        # 为每个维度生成任务
        for dimension in self.DIMENSIONS:
            priority = dimension_priorities.get(dimension, 2)

            research_plan['dimensions'][dimension] = {
                'priority': priority,
                'strategy': self._get_dimension_strategy(dimension, strategy),
                'sources': self._get_dimension_sources(dimension, target, strategy),
                'output_file': f"references/research/{dimension}.md",
                'status': 'pending'
            }

        self.research_plan = research_plan

        return research_plan

    def _get_dimension_priorities(self, os_type: str) -> Dict:
        """获取维度优先级"""

        # 不同HumanOS类型的维度优先级
        priorities = {
            'human': {
                '01-writings': 3,
                '02-conversations': 3,
                '03-expression-dna': 2,
                '04-external-views': 2,
                '05-decisions': 3,
                '06-timeline': 3
            },
            'theme': {
                '01-writings': 3,
                '02-conversations': 2,
                '03-expression-dna': 2,
                '04-external-views': 3,
                '05-decisions': 2,
                '06-timeline': 2
            },
            'scenario': {
                '01-writings': 2,
                '02-conversations': 2,
                '03-expression-dna': 2,
                '04-external-views': 1,
                '05-decisions': 3,
                '06-timeline': 2
            },
            'methodology': {
                '01-writings': 3,
                '02-conversations': 1,
                '03-expression-dna': 1,
                '04-external-views': 2,
                '05-decisions': 2,
                '06-timeline': 1
            }
        }

        return priorities.get(os_type, {})

    def _get_strategy(self, mode: str) -> Dict:
        """获取调研策略"""

        strategies = {
            'network': {
                'primary_mode': 'network_search',
                'local_first': False,
                'direction': 'collect_all'
            },
            'local_priority': {
                'primary_mode': 'local_analysis',
                'local_first': True,
                'direction': 'identify_gaps'
            },
            'local_only': {
                'primary_mode': 'local_analysis',
                'local_first': True,
                'direction': 'local_only'
            }
        }

        return strategies.get(mode, strategies['network'])

    def _get_dimension_strategy(self, dimension: str,
                                 strategy: Dict) -> Dict:
        """获取维度策略"""

        dimension_strategies = {
            '01-writings': {
                'focus': 'books, articles, systematic thinking',
                'search_queries': [
                    f'{dimension} books',
                    f'{dimension} essays',
                    f'{dimension} lectures'
                ]
            },
            '02-conversations': {
                'focus': 'interviews, podcasts, dialogues',
                'search_queries': [
                    f'{dimension} interview',
                    f'{dimension} podcast',
                    f'{dimension} conversation'
                ]
            },
            '03-expression-dna': {
                'focus': 'social media, quotes, style',
                'search_queries': [
                    f'{dimension} quotes',
                    f'{dimension} twitter',
                    f'{dimension} style'
                ]
            },
            '04-external-views': {
                'focus': 'criticism, analysis, reviews',
                'search_queries': [
                    f'{dimension} analysis',
                    f'{dimension} criticism',
                    f'{dimension} review'
                ]
            },
            '05-decisions': {
                'focus': 'decision records, case studies',
                'search_queries': [
                    f'{dimension} decisions',
                    f'{dimension} case studies',
                    f'{dimension} actions'
                ]
            },
            '06-timeline': {
                'focus': 'biography, evolution, timeline',
                'search_queries': [
                    f'{dimension} biography',
                    f'{dimension} timeline',
                    f'{dimension} history'
                ]
            }
        }

        return dimension_strategies.get(dimension, {})

    def _get_dimension_sources(self, dimension: str, target: str,
                                strategy: Dict) -> List[str]:
        """获取维度信息源"""

        # 简化处理，实际应该搜索并返回具体信息源
        sources = []

        # 基于策略生成搜索查询
        dimension_strategy = self._get_dimension_strategy(dimension, strategy)

        for query in dimension_strategy.get('search_queries', []):
            search_query = f"{target} {query}"
            sources.append({
                'query': search_query,
                'type': 'search',
                'status': 'pending'
            })

        return sources

    def execute_research(self, research_plan: Dict, output_dir: str) -> Dict:
        """执行调研计划"""

        execution_result = {
            'plan_id': f"research_{hash(str(research_plan))}",
            'started_at': str(subprocess.check_output(['date'])),
            'dimensions': {},
            'summary': {}
        }

        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 执行每个维度的调研
        for dimension_name, dimension_info in research_plan['dimensions'].items():
            dimension_result = self._execute_dimension_research(
                dimension_name,
                dimension_info,
                output_dir
            )

            execution_result['dimensions'][dimension_name] = dimension_result

        # 生成总结
        execution_result['summary'] = self._generate_research_summary(
            execution_result['dimensions']
        )

        return execution_result

    def _execute_dimension_research(self, dimension_name: str,
                                     dimension_info: Dict,
                                     output_dir: str) -> Dict:
        """执行单个维度调研"""

        # 模拟调研执行
        output_file = Path(output_dir) / dimension_info['output_file']
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 生成调研内容（模拟）
        content = self._generate_research_content(
            dimension_name,
            dimension_info
        )

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            'dimension': dimension_name,
            'status': 'completed',
            'output_file': str(output_file),
            'content_length': len(content),
            'sources_analyzed': len(dimension_info.get('sources', []))
        }

    def _generate_research_content(self, dimension_name: str,
                                    dimension_info: Dict) -> str:
        """生成调研内容（模拟）"""

        content = f"""# {dimension_name.replace('-', ' ').title()}

## 研究目标
分析 {dimension_name} 维度的核心内容和特征。

## 调研来源
- 搜索查询: {', '.join([s.get('query', '') for s in dimension_info.get('sources', [])])}

## 核心发现
[调研内容将在此处填充]

## 关键洞察
[关键洞察将在此处填充]

## 信息来源
[信息来源列表]
"""

        return content

    def _generate_research_summary(self, dimensions: Dict) -> Dict:
        """生成调研总结"""

        total_dimensions = len(dimensions)
        completed_dimensions = sum(
            1 for d in dimensions.values() if d.get('status') == 'completed'
        )

        return {
            'total_dimensions': total_dimensions,
            'completed_dimensions': completed_dimensions,
            'completion_rate': completed_dimensions / total_dimensions if total_dimensions > 0 else 0,
            'total_content_length': sum(
                d.get('content_length', 0) for d in dimensions.values()
            ),
            'total_sources_analyzed': sum(
                d.get('sources_analyzed', 0) for d in dimensions.values()
            )
        }

    def check_local_sources(self, target: str, sources_dir: str) -> Dict:
        """检查本地素材"""

        sources_path = Path(sources_dir)
        local_sources = {
            'books': [],
            'transcripts': [],
            'articles': [],
            'total_files': 0
        }

        if not sources_path.exists():
            return local_sources

        # 扫描本地素材
        for category in ['books', 'transcripts', 'articles']:
            category_path = sources_path / category
            if category_path.exists():
                for file_path in category_path.glob('*'):
                    local_sources[category].append({
                        'path': str(file_path),
                        'name': file_path.name,
                        'size': file_path.stat().st_size
                    })

        local_sources['total_files'] = sum(
            len(local_sources[cat]) for cat in ['books', 'transcripts', 'articles']
        )

        return local_sources


def main():
    import argparse

    parser = argparse.ArgumentParser(description='调研编排')
    parser.add_argument('--os-type', type=str, required=True,
                       choices=['human', 'theme', 'scenario', 'methodology'],
                       help='HumanOS类型')
    parser.add_argument('--target', type=str, required=True,
                       help='调研目标（人名/主题）')
    parser.add_argument('--output-dir', type=str, default='./output',
                       help='输出目录')
    parser.add_argument('--mode', type=str, default='network',
                       choices=['network', 'local_priority', 'local_only'],
                       help='调研模式')

    args = parser.parse_args()

    orchestrator = ResearchOrchestrator()

    # 生成调研计划
    research_plan = orchestrator.generate_research_plan(
        args.os_type,
        args.target,
        args.mode
    )

    print(f"生成调研计划: {args.target}")
    print(json.dumps(research_plan, ensure_ascii=False, indent=2))

    # 执行调研
    execution_result = orchestrator.execute_research(
        research_plan,
        args.output_dir
    )

    print(f"\n执行调研: {args.target}")
    print(json.dumps(execution_result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
