#!/usr/bin/env python3
"""
获取今日待复习错题
"""

import json
from datetime import datetime
from pathlib import Path
import os

DATA_DIR = Path(os.environ.get('WORKSPACE', '.')) / 'mistake-data'
INDEX_FILE = DATA_DIR / 'index.json'


def load_json(filepath):
    """加载JSON文件"""
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_today_reviews() -> list:
    """
    获取今日待复习错题
    
    Returns:
        今日到期和超期的错题列表
    """
    if not INDEX_FILE.exists():
        return []
    
    index_data = load_json(INDEX_FILE)
    if not index_data:
        return []
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 筛选今日需复习的错题
    to_review = []
    for item in index_data.get('mistakes', []):
        # 跳过已掌握的
        if item.get('mastered', False):
            continue
        
        next_review = item.get('next_review', '')
        # 今日到期或已超期
        if next_review <= today:
            to_review.append(item)
    
    # 按优先级排序：超期 > 今日到期 > 错误次数 > 难度
    def sort_key(m):
        is_overdue = 0 if m.get('next_review', '') < today else 1
        error_count = m.get('error_count', 0)
        difficulty_order = {'困难': 0, '中等': 1, '简单': 2}
        difficulty = difficulty_order.get(m.get('difficulty', '中等'), 1)
        return (is_overdue, -error_count, difficulty)
    
    to_review.sort(key=sort_key)
    
    return to_review


def get_mistake_detail(mistake_id: str) -> dict:
    """获取错题详情"""
    if not INDEX_FILE.exists():
        return None
    
    # 从ID推断文件路径
    parts = mistake_id.split('-')
    if len(parts) < 2:
        return None
    
    code = parts[0]
    
    # 搜索该科目下的所有文件
    subject_dir = DATA_DIR / code
    if not subject_dir.exists():
        return None
    
    for topic_file in subject_dir.glob('*.json'):
        data = load_json(topic_file)
        if data:
            for mistake in data.get('mistakes', []):
                if mistake.get('id') == mistake_id:
                    return mistake
    
    return None


def format_review_list(mistakes: list) -> str:
    """格式化复习列表"""
    if not mistakes:
        return "📭 今日无待复习错题"
    
    output = [f"📝【今日待复习 - {len(mistakes)}题】\n"]
    
    for i, m in enumerate(mistakes, 1):
        subject = m.get('subject', '未知')
        topic = m.get('topic', '未分类')
        difficulty = m.get('difficulty', '中等')
        mistake_id = m.get('id', '')
        
        # 状态标记
        next_review = m.get('next_review', '')
        today = datetime.now().strftime('%Y-%m-%d')
        status = "⚠️ 已超期" if next_review < today else "📅 今日到期"
        
        output.append(f"{i}. {status}")
        output.append(f"   [{subject}-{topic}]")
        output.append(f"   难度: {difficulty}")
        output.append(f"   ID: {mistake_id}")
        output.append("")
    
    output.append("💡 回复「开始复习」或「查看题目 [ID]」")
    
    return '\n'.join(output)


def main():
    """测试"""
    mistakes = get_today_reviews()
    print(format_review_list(mistakes))
    
    if mistakes:
        print("\n" + "="*50)
        detail = get_mistake_detail(mistakes[0]['id'])
        if detail:
            print(f"\n【题目详情】")
            print(f"题目: {detail.get('question')}")
            print(f"错误答案: {detail.get('wrong_answer')}")
            print(f"正确答案: {detail.get('correct_answer')}")


if __name__ == '__main__':
    main()
