from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def mcp_howtocook_getAllRecipes(
    no_param: Optional[str] = None
) -> Dict[str, Any]:
    """
    获取所有菜谱
    
    Args:
        no_param: 无参数
    
    Returns:
        
    """
    arguments = {
        "no_param": no_param
    }
    
    return call_api("1777316659566595", "mcp_howtocook_getAllRecipes", arguments)

def mcp_howtocook_getRecipesByCategory(
    category: str
) -> Dict[str, Any]:
    """
    根据分类查询菜谱，可选分类有: 水产, 早餐, 调料, 甜品, 饮品, 荤菜, 半成品加工, 汤, 主食, 素菜
    
    Args:
        category: 菜谱分类名称，如水产、早餐、荤菜、主食等
    
    Returns:
        
    """
    arguments = {
        "category": category
    }
    
    return call_api("1777316659566595", "mcp_howtocook_getRecipesByCategory", arguments)

def mcp_howtocook_recommendMeals(
    allergies: Optional[null] = None,
    avoidItems: Optional[null] = None,
    peopleCount: int
) -> Dict[str, Any]:
    """
    根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划以及大致的购物清单
    
    Args:
        allergies: 过敏原列表，如["大蒜", "虾"]
        avoidItems: 忌口食材列表，如["葱", "姜"]
        peopleCount: 用餐人数，1-10之间的整数
    
    Returns:
        
    """
    arguments = {
        "allergies": allergies,
        "avoidItems": avoidItems,
        "peopleCount": peopleCount
    }
    
    return call_api("1777316659566595", "mcp_howtocook_recommendMeals", arguments)

def mcp_howtocook_whatToEat(
    peopleCount: int
) -> Dict[str, Any]:
    """
    不知道吃什么？根据人数直接推荐适合的菜品组合
    
    Args:
        peopleCount: 用餐人数，1-10之间的整数，会根据人数推荐合适数量的菜品
    
    Returns:
        
    """
    arguments = {
        "peopleCount": peopleCount
    }
    
    return call_api("1777316659566595", "mcp_howtocook_whatToEat", arguments)

def mcp_howtocook_getRecipeById(
    query: str
) -> Dict[str, Any]:
    """
    根据菜谱名称或ID查询指定菜谱的完整详情，包括食材、步骤等
    
    Args:
        query: 菜谱名称或ID，支持模糊匹配菜谱名称
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777316659566595", "mcp_howtocook_getRecipeById", arguments)

