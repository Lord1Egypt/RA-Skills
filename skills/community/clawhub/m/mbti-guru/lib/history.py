#!/usr/bin/env python3
"""
MBTI Guru - 历史记录模块
支持测试历史存储和查询
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "history")

def ensure_data_dir(chat_id: int = None):
    """确保数据目录存在"""
    if chat_id:
        os.makedirs(os.path.join(DATA_DIR, str(chat_id)), exist_ok=True)
    else:
        os.makedirs(DATA_DIR, exist_ok=True)

def save_test_result(chat_id: int, type_code: str, scores: Dict, clarity: Dict, version: int, answers_count: int) -> str:
    """
    保存测试结果
    
    Args:
        chat_id: 用户ID
        type_code: MBTI类型如"INFP"
        scores: 维度得分
        clarity: 清晰度
        version: 测试版本
        answers_count: 答题数量
    
    Returns:
        test_id: 测试记录ID
    """
    import time
    ensure_data_dir(chat_id)
    
    test_id = f"{chat_id}_{int(time.time())}"
    
    test_data = {
        "test_id": test_id,
        "chat_id": chat_id,
        "type_code": type_code,
        "scores": scores,
        "clarity": {k: {"value": v[0], "label": v[1]} for k, v in clarity.items()},
        "version": version,
        "answers_count": answers_count,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": int(time.time())
    }
    
    filepath = os.path.join(DATA_DIR, str(chat_id), "tests.json")
    
    # 读取现有历史或创建新的
    history = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    # 添加新记录到开头
    history.insert(0, test_data)
    
    # 只保留最近20条
    history = history[:20]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return test_id

def get_test_history(chat_id: int, limit: int = 10) -> List[Dict]:
    """
    获取测试历史
    
    Args:
        chat_id: 用户ID
        limit: 返回数量限制
    
    Returns:
        测试历史列表
    """
    ensure_data_dir(chat_id)
    
    filepath = os.path.join(DATA_DIR, str(chat_id), "tests.json")
    
    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    return history[:limit]

def get_test_detail(chat_id: int, test_id: str) -> Optional[Dict]:
    """
    获取某次测试的详细信息
    
    Args:
        chat_id: 用户ID
        test_id: 测试ID
    
    Returns:
        测试详情或None
    """
    history = get_test_history(chat_id, limit=20)
    
    for test in history:
        if test['test_id'] == test_id:
            return test
    
    return None

def compare_tests(test1: Dict, test2: Dict) -> Dict:
    """
    对比两次测试结果
    
    Args:
        test1: 测试1数据
        test2: 测试2数据
    
    Returns:
        对比分析结果
    """
    changes = {}
    
    for dim in ['EI', 'SN', 'TF', 'JP']:
        score1 = test1['scores'].get(dim, 50)
        score2 = test2['scores'].get(dim, 50)
        diff = score2 - score1
        
        if abs(diff) < 5:
            label = "基本不变"
        elif diff > 0:
            label = f"偏好增加 +{diff:.0f}%"
        else:
            label = f"偏好减少 {diff:.0f}%"
        
        changes[dim] = {
            "test1_score": score1,
            "test2_score": score2,
            "change": diff,
            "label": label
        }
    
    type_change = "相同" if test1['type_code'] == test2['type_code'] else f"{test1['type_code']} → {test2['type_code']}"
    
    return {
        "type_change": type_change,
        "dimension_changes": changes,
        "date1": test1['date'],
        "date2": test2['date']
    }

def delete_history(chat_id: int, test_id: str = None) -> bool:
    """
    删除历史记录
    
    Args:
        chat_id: 用户ID
        test_id: 测试ID，如果为None则删除全部
    
    Returns:
        是否删除成功
    """
    if test_id is None:
        # 删除全部
        filepath = os.path.join(DATA_DIR, str(chat_id), "tests.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    # 删除单条
    history = get_test_history(chat_id, limit=20)
    history = [t for t in history if t['test_id'] != test_id]
    
    filepath = os.path.join(DATA_DIR, str(chat_id), "tests.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    
    return True
