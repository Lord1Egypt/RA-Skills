#!/usr/bin/env python
"""
Prompt-Router 集成脚本
供 using-superpowers 或其他技能调用

使用方法：
    python integration.py "用户消息"

返回 JSON 格式：
    {
        "matched": true,
        "skill_name": "multi-search-engine",
        "confidence": 0.35,
        "confidence_level": "low",
        "score": 3.15
    }
"""

import json
import sys
from pathlib import Path

# 支持直接运行和模块导入
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from router import PromptRouter

# 全局路由器实例（避免重复加载）
_router = None

def get_router() -> PromptRouter:
    """获取或创建路由器实例"""
    global _router
    if _router is None:
        _router = PromptRouter(
            skills_dir='C:/Users/User/.openclaw/workspace/skills',
            confidence_threshold=0.25,      # 低于此值降级到 LLM
            high_confidence_threshold=0.5,  # 高于此值直接调用
        )
        _router.load_skills()
    return _router

def route_prompt(user_message: str) -> dict:
    """
    路由用户消息到最佳匹配技能
    
    Args:
        user_message: 用户输入消息
        
    Returns:
        路由结果字典：
        {
            "matched": bool,              # 是否匹配到技能
            "skill_name": str | None,     # 匹配的技能名
            "skill_path": str | None,     # 技能目录路径
            "confidence": float,          # 置信度 (0-1)
            "confidence_level": str,      # high/medium/low/none
            "score": float,               # 匹配分数
            "should_invoke": bool,        # 是否应该调用技能
            "error": str | None,          # 错误信息（如果有）
        }
    """
    try:
        router = get_router()
        result = router.route(user_message)
        should_invoke = router.should_invoke_skill(result)
        
        return {
            "matched": result.match is not None,
            "skill_name": result.match['name'] if result.match else None,
            "skill_path": result.match.get('_path') if result.match else None,
            "confidence": result.confidence,
            "confidence_level": result.confidence_level,
            "score": result.score,
            "should_invoke": should_invoke,
            "error": None,
        }
    except Exception as e:
        return {
            "matched": False,
            "skill_name": None,
            "skill_path": None,
            "confidence": 0.0,
            "confidence_level": "none",
            "score": 0.0,
            "should_invoke": False,
            "error": str(e),
        }

def quick_check(user_message: str) -> bool:
    """
    快速检查是否需要调用技能（用于条件判断）
    
    Args:
        user_message: 用户输入消息
        
    Returns:
        True 如果应该调用技能
    """
    result = route_prompt(user_message)
    return result["should_invoke"]

def get_skill_recommendation(user_message: str) -> str:
    """
    获取技能推荐（用于提示用户）
    
    Args:
        user_message: 用户输入消息
        
    Returns:
        推荐字符串，如 "建议使用 multi-search-engine 技能"
    """
    result = route_prompt(user_message)
    
    if result["matched"]:
        return f"建议使用 {result['skill_name']} 技能（置信度：{result['confidence']:.2f}）"
    else:
        return "未找到匹配技能，建议使用 LLM 推理"

# 命令行入口
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({
            "matched": False,
            "skill_name": None,
            "error": "No message provided. Usage: python integration.py <message>"
        }, ensure_ascii=False))
        sys.exit(1)
    
    # 支持多参数拼接消息
    message = ' '.join(sys.argv[1:])
    
    # 执行路由
    result = route_prompt(message)
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False))
