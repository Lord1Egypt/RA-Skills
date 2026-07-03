from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def start_mbti_test(
    testType: str
) -> Dict[str, Any]:
    """
    开始MBTI人格测试。用户可以选择测试类型：simplified(简化版28题)或cognitive(认知功能版48题)。返回第一道题目和测试会话状态。
    
    Args:
        testType: 测试类型：simplified(简化版)或cognitive(认知功能版)
    
    Returns:
        
    """
    arguments = {
        "testType": testType
    }
    
    return call_api("1777316659619843", "start_mbti_test", arguments)

def answer_question(
    session: null,
    score: float
) -> Dict[str, Any]:
    """
    提交当前问题的答案(1-5分)，并获取下一题或测试进度。需要传入完整的测试会话状态。
    
    Args:
        session: 测试会话状态，包含testType、answers数组和currentQuestionIndex
        score: 对当前问题的回答(1=强烈不同意, 2=不同意, 3=中立, 4=同意, 5=强烈同意)
    
    Returns:
        
    """
    arguments = {
        "session": session,
        "score": score
    }
    
    return call_api("1777316659619843", "answer_question", arguments)

def get_progress(
    session: null
) -> Dict[str, Any]:
    """
    查询当前测试进度。需要传入测试会话状态。
    
    Args:
        session: 测试会话状态
    
    Returns:
        
    """
    arguments = {
        "session": session
    }
    
    return call_api("1777316659619843", "get_progress", arguments)

def calculate_mbti_result(
    session: null
) -> Dict[str, Any]:
    """
    根据所有答案计算最终的MBTI类型和详细结果。需要传入完整的测试会话状态。
    
    Args:
        session: 测试会话状态，必须包含所有题目的答案
    
    Returns:
        
    """
    arguments = {
        "session": session
    }
    
    return call_api("1777316659619843", "calculate_mbti_result", arguments)

