#!/usr/bin/env python3
"""
源分析器：分析素材来源质量
"""

import json
from pathlib import Path
from typing import Dict, List


class SourceAnalyzer:
    """源分析器"""

    # 来源质量评分标准
    QUALITY_STANDARDS = {
        'high_quality': {
            'score': 3,
            'description': '一手来源，权威性强',
            'examples': ['书籍', '学术论文', '官方演讲', '深度访谈']
        },
        'medium_quality': {
            'score': 2,
            'description': '二手来源，有一定权威性',
            'examples': ['分析文章', '评论', '纪录片']
        },
        'low_quality': {
            'score': 1,
            'description': '非一手来源，权威性弱',
            'examples': ['社交媒体', '论坛讨论', '网络评论']
        }
    }

    def __init__(self):
        self.analysis_results = {}

    def analyze_sources(self, sources_dir: str) -> Dict:
        """分析素材来源"""

        sources_path = Path(sources_dir)

        if not sources_path.exists():
            return {
                'status': 'error',
                'message': f'目录不存在: {sources_dir}'
            }

        # 扫描素材文件
        source_files = self._scan_source_files(sources_path)

        # 分析每个来源
        analyzed_sources = []
        for source_file in source_files:
            analysis = self._analyze_single_source(source_file)
            analyzed_sources.append(analysis)

        # 生成统计报告
        statistics = self._generate_statistics(analyzed_sources)

        analysis_result = {
            'status': 'success',
            'sources_dir': sources_dir,
            'total_sources': len(analyzed_sources),
            'analyzed_sources': analyzed_sources,
            'statistics': statistics,
            'quality_assessment': self._assess_overall_quality(statistics)
        }

        self.analysis_results = analysis_result

        return analysis_result

    def _scan_source_files(self, sources_path: Path) -> List[Dict]:
        """扫描素材文件"""

        source_files = []

        # 扫描不同类型的素材
        categories = {
            'books': ['pdf', 'epub', 'mobi'],
            'articles': ['md', 'txt', 'html'],
            'transcripts': ['txt', 'md', 'srt'],
            'videos': ['mp4', 'mkv', 'avi']
        }

        for category, extensions in categories.items():
            category_path = sources_path / category
            if category_path.exists():
                for file_path in category_path.glob('*'):
                    if file_path.is_file():
                        file_ext = file_path.suffix.lower().lstrip('.')
                        if file_ext in extensions:
                            source_files.append({
                                'path': str(file_path),
                                'category': category,
                                'filename': file_path.name,
                                'extension': file_ext,
                                'size': file_path.stat().st_size
                            })

        return source_files

    def _analyze_single_source(self, source_file: Dict) -> Dict:
        """分析单个来源"""

        filename = source_file['filename']
        category = source_file['category']

        # 评估来源质量
        quality = self._assess_source_quality(category, filename)

        # 分析内容（简化处理）
        content_analysis = self._analyze_content(source_file['path'])

        return {
            'filename': filename,
            'category': category,
            'quality': quality,
            'size': source_file['size'],
            'content_analysis': content_analysis,
            'recommendation': self._generate_recommendation(category, quality)
        }

    def _assess_source_quality(self, category: str, filename: str) -> Dict:
        """评估来源质量"""

        # 基于类别和文件名评估质量
        if category == 'books':
            return {
                **self.QUALITY_STANDARDS['high_quality'],
                'score': 3,
                'category': 'high_quality'
            }
        elif category == 'articles':
            # 检查是否来自权威来源（简化处理）
            if any(keyword in filename.lower() for keyword in ['paper', 'journal', 'official']):
                return {
                    **self.QUALITY_STANDARDS['high_quality'],
                    'score': 3,
                    'category': 'high_quality'
                }
            else:
                return {
                    **self.QUALITY_STANDARDS['medium_quality'],
                    'score': 2,
                    'category': 'medium_quality'
                }
        elif category == 'transcripts':
            # 字幕通常是高质量来源
            return {
                **self.QUALITY_STANDARDS['high_quality'],
                'score': 3,
                'category': 'high_quality'
            }
        elif category == 'videos':
            # 视频质量取决于来源
            return {
                **self.QUALITY_STANDARDS['medium_quality'],
                'score': 2,
                'category': 'medium_quality'
            }
        else:
            return {
                **self.QUALITY_STANDARDS['low_quality'],
                'score': 1,
                'category': 'low_quality'
            }

    def _analyze_content(self, file_path: str) -> Dict:
        """分析内容"""

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 简化分析
            word_count = len(content.split())
            char_count = len(content)
            line_count = len(content.split('\n'))

            return {
                'word_count': word_count,
                'char_count': char_count,
                'line_count': line_count,
                'status': 'analyzed'
            }

        except Exception as e:
            return {
                'error': str(e),
                'status': 'error'
            }

    def _generate_recommendation(self, category: str,
                                   quality: Dict) -> str:
        """生成建议"""

        quality_score = quality.get('score', 1)

        if quality_score >= 3:
            return '高质量来源，优先使用'
        elif quality_score >= 2:
            return '中等质量来源，可使用'
        else:
            return '低质量来源，谨慎使用或寻找替代'

    def _generate_statistics(self, analyzed_sources: List[Dict]) -> Dict:
        """生成统计报告"""

        total_sources = len(analyzed_sources)

        if total_sources == 0:
            return {
                'total': 0,
                'by_category': {},
                'by_quality': {}
            }

        # 按类别统计
        by_category = {}
        for source in analyzed_sources:
            category = source['category']
            by_category[category] = by_category.get(category, 0) + 1

        # 按质量统计
        by_quality = {}
        for source in analyzed_sources:
            quality = source['quality']['category']
            by_quality[quality] = by_quality.get(quality, 0) + 1

        # 计算平均质量分
        average_quality = sum(
            source['quality']['score']
            for source in analyzed_sources
        ) / total_sources

        # 计算总字数
        total_words = sum(
            source.get('content_analysis', {}).get('word_count', 0)
            for source in analyzed_sources
        )

        return {
            'total': total_sources,
            'by_category': by_category,
            'by_quality': by_quality,
            'average_quality': round(average_quality, 2),
            'total_words': total_words
        }

    def _assess_overall_quality(self, statistics: Dict) -> Dict:
        """评估整体质量"""

        total = statistics.get('total', 0)
        average_quality = statistics.get('average_quality', 0)
        by_quality = statistics.get('by_quality', {})

        if total == 0:
            return {
                'overall': 'insufficient',
                'message': '素材不足'
            }

        # 评估质量分布
        high_quality_ratio = by_quality.get('high_quality', 0) / total
        low_quality_ratio = by_quality.get('low_quality', 0) / total

        if high_quality_ratio >= 0.7:
            return {
                'overall': 'excellent',
                'message': '高质量素材占多数'
            }
        elif high_quality_ratio >= 0.5:
            return {
                'overall': 'good',
                'message': '高质量素材过半'
            }
        elif average_quality >= 2.0:
            return {
                'overall': 'acceptable',
                'message': '素材质量可接受'
            }
        elif low_quality_ratio > 0.5:
            return {
                'overall': 'poor',
                'message': '低质量素材占多数，建议补充高质量素材'
            }
        else:
            return {
                'overall': 'moderate',
                'message': '素材质量中等'
            }


def main():
    import argparse

    parser = argparse.ArgumentParser(description='源分析')
    parser.add_argument('--sources-dir', type=str, required=True,
                       help='素材目录路径')

    args = parser.parse_args()

    analyzer = SourceAnalyzer()

    # 分析来源
    analysis_result = analyzer.analyze_sources(args.sources_dir)

    # 输出结果
    print(json.dumps(analysis_result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
