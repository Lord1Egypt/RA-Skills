#!/usr/bin/env python3
"""
生成学情统计报告
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import os
from collections import Counter

DATA_DIR = Path(os.environ.get('WORKSPACE', '.')) / 'mistake-data'
INDEX_FILE = DATA_DIR / 'index.json'


def load_json(filepath):
    """加载JSON文件"""
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_mistakes() -> list:
    """获取所有错题"""
    mistakes = []
    
    if not DATA_DIR.exists():
        return mistakes
    
    for subject_dir in DATA_DIR.iterdir():
        if subject_dir.is_dir() and subject_dir.name not in ['.', '..']:
            for topic_file in subject_dir.glob('*.json'):
                data = load_json(topic_file)
                if data:
                    mistakes.extend(data.get('mistakes', []))
    
    return mistakes


def generate_stats() -> dict:
    """生成统计数据"""
    mistakes = get_all_mistakes()
    
    if not mistakes:
        return {
            'total': 0,
            'message': '暂无错题数据'
        }
    
    # 基础统计
    total = len(mistakes)
    mastered = sum(1 for m in mistakes if m.get('mastered', False))
    to_review = total - mastered
    
    # 科目分布
    subjects = Counter(m.get('subject', '未知') for m in mistakes)
    
    # 知识点统计
    topics = Counter(
        f"{m.get('subject', '')}-{m.get('topic', '未分类')}" 
        for m in mistakes
    )
    
    # 薄弱知识点 TOP 5
    weak_topics = topics.most_common(5)
    
    # 难度分布
    difficulty = Counter(m.get('difficulty', '中等') for m in mistakes)
    
    # 错误原因分布
    error_reasons = Counter(m.get('reason', '未标注') for m in mistakes)
    
    # 时间趋势（最近7天）
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    recent_new = 0
    recent_mastered = 0
    
    for m in mistakes:
        created = datetime.fromisoformat(m.get('created_at', today.isoformat()))
        if created >= week_ago:
            recent_new += 1
        
        # 检查复习历史中最近的掌握记录
        for review in m.get('review_history', []):
            review_date = datetime.fromisoformat(review.get('date', ''))
            if review_date >= week_ago and review.get('status') == '已掌握':
                recent_mastered += 1
                break
    
    # 计算掌握率
    mastery_rate = (mastered / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'mastered': mastered,
        'to_review': to_review,
        'mastery_rate': round(mastery_rate, 1),
        'subjects': dict(subjects),
        'weak_topics': weak_topics,
        'difficulty': dict(difficulty),
        'recent': {
            'new': recent_new,
            'mastered': recent_mastered,
            'period': '最近7天'
        }
    }


def format_report(stats: dict) -> str:
    """格式化报告"""
    if stats.get('total', 0) == 0:
        return stats.get('message', '暂无数据')
    
    lines = [
        "📊【错题统计报告】\n",
        f"总错题数: {stats['total']}",
        f"已掌握: {stats['mastered']} ✅",
        f"待复习: {stats['to_review']} 📚",
        f"掌握率: {stats['mastery_rate']}%\n",
    ]
    
    # 薄弱知识点
    if stats.get('weak_topics'):
        lines.append("🎯【薄弱知识点 TOP 5】")
        for i, (topic, count) in enumerate(stats['weak_topics'], 1):
            lines.append(f"  {i}. {topic}（错误{count}次）")
        lines.append("")
    
    # 科目分布
    if stats.get('subjects'):
        lines.append("📚【科目分布】")
        for subject, count in sorted(stats['subjects'].items(), 
                                      key=lambda x: x[1], reverse=True):
            pct = count / stats['total'] * 100
            lines.append(f"  {subject}: {count}题 ({pct:.1f}%)")
        lines.append("")
    
    # 难度分布
    if stats.get('difficulty'):
        lines.append("⚡【难度分布】")
        for diff, count in stats['difficulty'].items():
            lines.append(f"  {diff}: {count}题")
        lines.append("")
    
    # 近期趋势
    recent = stats.get('recent', {})
    if recent:
        lines.append(f"📈【{recent.get('period', '近期')}趋势】")
        lines.append(f"  新增: {recent.get('new', 0)}题")
        lines.append(f"  掌握: {recent.get('mastered', 0)}题")
    
    return '\n'.join(lines)


def main():
    """测试"""
    stats = generate_stats()
    print(format_report(stats))


if __name__ == '__main__':
    main()
