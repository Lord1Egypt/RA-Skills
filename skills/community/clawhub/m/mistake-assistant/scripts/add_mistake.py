#!/usr/bin/env python3
"""
添加错题到数据库
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import uuid

# 数据目录
DATA_DIR = Path(os.environ.get('WORKSPACE', '.')) / 'mistake-data'
INDEX_FILE = DATA_DIR / 'index.json'


def init_data_dir():
    """初始化数据目录"""
    DATA_DIR.mkdir(exist_ok=True, parents=True)
    
    if not INDEX_FILE.exists():
        index_data = {
            'mistakes': [],
            'subjects': {},
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        save_json(INDEX_FILE, index_data)


def load_json(filepath):
    """加载JSON文件"""
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(filepath, data):
    """保存JSON文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def generate_mistake_id(subject: str) -> str:
    """生成错题ID"""
    subject_codes = {
        '数学': 'math', '物理': 'physics', '化学': 'chemistry',
        '英语': 'english', '语文': 'chinese', '生物': 'biology',
        '历史': 'history', '地理': 'geography', '政治': 'politics'
    }
    code = subject_codes.get(subject, 'other')
    date_str = datetime.now().strftime('%Y%m%d')
    short_id = str(uuid.uuid4())[:4]
    return f"{code}-{date_str}-{short_id}"


def calculate_next_review(review_count: int = 0) -> str:
    """计算下次复习日期（艾宾浩斯曲线）"""
    intervals = [1, 2, 4, 7, 15, 30]
    
    if review_count >= len(intervals):
        days = 30
    else:
        days = intervals[review_count]
    
    next_date = datetime.now() + timedelta(days=days)
    return next_date.strftime('%Y-%m-%d')


def add_mistake(
    subject: str,
    question: str,
    wrong_answer: str,
    correct_answer: str,
    reason: str,
    topic: str = None,
    difficulty: str = '中等',
    source: str = None,
    question_type: str = '解答题',
    options: dict = None,
    notes: str = None
) -> dict:
    """
    添加错题
    
    Args:
        subject: 科目
        question: 题目内容
        wrong_answer: 错误答案
        correct_answer: 正确答案
        reason: 错误原因
        topic: 知识点
        difficulty: 难度（简单/中等/困难）
        source: 来源
        question_type: 题型
        options: 选择题选项
        notes: 备注
    
    Returns:
        创建的错题记录
    """
    init_data_dir()
    
    # 生成ID
    mistake_id = generate_mistake_id(subject)
    
    # 创建错题记录
    mistake = {
        'id': mistake_id,
        'subject': subject,
        'topic': topic,
        'question_type': question_type,
        'question': question,
        'wrong_answer': wrong_answer,
        'correct_answer': correct_answer,
        'reason': reason,
        'difficulty': difficulty,
        'source': source,
        'options': options,
        'notes': notes,
        'created_at': datetime.now().isoformat(),
        'review_count': 0,
        'next_review': calculate_next_review(0),
        'mastered': False,
        'error_count': 1,
        'review_history': []
    }
    
    # 保存到科目文件
    subject_codes = {
        '数学': 'math', '物理': 'physics', '化学': 'chemistry',
        '英语': 'english', '语文': 'chinese', '生物': 'biology',
        '历史': 'history', '地理': 'geography', '政治': 'politics'
    }
    code = subject_codes.get(subject, 'other')
    subject_file = DATA_DIR / code / f"{topic or 'general'}.json"
    
    # 加载或创建科目数据
    if subject_file.exists():
        subject_data = load_json(subject_file)
    else:
        subject_data = {
            'subject': subject,
            'code': code,
            'topic': topic,
            'mistakes': [],
            'created_at': datetime.now().isoformat()
        }
    
    subject_data['mistakes'].append(mistake)
    subject_data['updated_at'] = datetime.now().isoformat()
    save_json(subject_file, subject_data)
    
    # 更新索引
    index_data = load_json(INDEX_FILE)
    if index_data is None:
        index_data = {'mistakes': [], 'subjects': {}}
    
    index_data['mistakes'].append({
        'id': mistake_id,
        'subject': subject,
        'topic': topic,
        'difficulty': difficulty,
        'created_at': mistake['created_at'],
        'next_review': mistake['next_review'],
        'mastered': False
    })
    
    # 更新科目统计
    if subject not in index_data['subjects']:
        index_data['subjects'][subject] = {'count': 0, 'topics': {}}
    index_data['subjects'][subject]['count'] += 1
    
    if topic:
        if topic not in index_data['subjects'][subject]['topics']:
            index_data['subjects'][subject]['topics'][topic] = 0
        index_data['subjects'][subject]['topics'][topic] += 1
    
    index_data['updated_at'] = datetime.now().isoformat()
    save_json(INDEX_FILE, index_data)
    
    return mistake


def main():
    """测试示例"""
    mistake = add_mistake(
        subject='数学',
        question='已知 f(x) = x² + 2x + 1，求 f(x) 的最小值',
        wrong_answer='最小值是 0',
        correct_answer='最小值是 -1，f(x) = (x+1)² - 1',
        reason='忘记配方，直接代入顶点公式错误',
        topic='二次函数',
        difficulty='中等',
        source='课本第23页例题',
        notes='记住配方方法：f(x) = a(x-h)² + k'
    )
    
    print(f"✅ 错题已记录")
    print(f"ID: {mistake['id']}")
    print(f"科目: {mistake['subject']} - {mistake['topic']}")
    print(f"下次复习: {mistake['next_review']}")


if __name__ == '__main__':
    main()
