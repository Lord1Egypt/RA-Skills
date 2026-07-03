from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def add(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    两个数相加
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419068744707", "add", arguments)

def subtract(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    两个数相减
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419068744707", "subtract", arguments)

def multiply(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    两个数相乘
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419068744707", "multiply", arguments)

def divide(
    a: float,
    b: float
) -> Dict[str, Any]:
    """
    两个数相除
    
    Args:
        a: null
        b: null
    
    Returns:
        null
    """
    arguments = {
        "a": a,
        "b": b
    }
    
    return call_api("1777419068744707", "divide", arguments)

def sine(
    degree: float
) -> Dict[str, Any]:
    """
    计算正弦函数
    
    Args:
        degree: null
    
    Returns:
        null
    """
    arguments = {
        "degree": degree
    }
    
    return call_api("1777419068744707", "sine", arguments)

def cos(
    degree: float
) -> Dict[str, Any]:
    """
    计算余弦函数
    
    Args:
        degree: null
    
    Returns:
        null
    """
    arguments = {
        "degree": degree
    }
    
    return call_api("1777419068744707", "cos", arguments)

def tangent(
    degree: float
) -> Dict[str, Any]:
    """
    计算正切函数
    
    Args:
        degree: null
    
    Returns:
        null
    """
    arguments = {
        "degree": degree
    }
    
    return call_api("1777419068744707", "tangent", arguments)

def cotangent(
    degree: float
) -> Dict[str, Any]:
    """
    计算余切函数
    
    Args:
        degree: null
    
    Returns:
        null
    """
    arguments = {
        "degree": degree
    }
    
    return call_api("1777419068744707", "cotangent", arguments)

def secant(
    degree: float
) -> Dict[str, Any]:
    """
    计算正割函数
    
    Args:
        degree: null
    
    Returns:
        null
    """
    arguments = {
        "degree": degree
    }
    
    return call_api("1777419068744707", "secant", arguments)

def cosecant(
    degree: float
) -> Dict[str, Any]:
    """
    计算余割函数
    
    Args:
        degree: null
    
    Returns:
        null
    """
    arguments = {
        "degree": degree
    }
    
    return call_api("1777419068744707", "cosecant", arguments)

def natural_log(
    x: float
) -> Dict[str, Any]:
    """
    计算自然对数(底数为e)
    
    Args:
        x: null
    
    Returns:
        
    """
    arguments = {
        "x": x
    }
    
    return call_api("1777419068744707", "natural_log", arguments)

def common_log(
    x: float
) -> Dict[str, Any]:
    """
    计算常用对数(底数为10)
    
    Args:
        x: null
    
    Returns:
        
    """
    arguments = {
        "x": x
    }
    
    return call_api("1777419068744707", "common_log", arguments)

def custom_log(
    x: float,
    base: float
) -> Dict[str, Any]:
    """
    根据给定的底数计算对数
    
    Args:
        x: null
        base: null
    
    Returns:
        
    """
    arguments = {
        "x": x,
        "base": base
    }
    
    return call_api("1777419068744707", "custom_log", arguments)

def math_sqrt(
    x: str
) -> Dict[str, Any]:
    """
    使用Python内置的数学模块进行平方根计算
    
    Args:
        x: null
    
    Returns:
        
    """
    arguments = {
        "x": x
    }
    
    return call_api("1777419068744707", "math_sqrt", arguments)

def operator_sqrt(
    x: float
) -> Dict[str, Any]:
    """
    使用指数运算符来计算平方根
    
    Args:
        x: null
    
    Returns:
        
    """
    arguments = {
        "x": x
    }
    
    return call_api("1777419068744707", "operator_sqrt", arguments)

def complex_sqrt(
    x: str
) -> Dict[str, Any]:
    """
    计算复数平方根
    
    Args:
        x: null
    
    Returns:
        
    """
    arguments = {
        "x": x
    }
    
    return call_api("1777419068744707", "complex_sqrt", arguments)

def exponentiation(
    base: float,
    exponent: float
) -> Dict[str, Any]:
    """
    计算幂运算，支持负整数和小数
    
    Args:
        base: null
        exponent: null
    
    Returns:
        
    """
    arguments = {
        "base": base,
        "exponent": exponent
    }
    
    return call_api("1777419068744707", "exponentiation", arguments)

def arcsin(
    value: float
) -> Dict[str, Any]:
    """
    计算反正弦函数
    
    Args:
        value: null
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777419068744707", "arcsin", arguments)

def arccos(
    value: float
) -> Dict[str, Any]:
    """
    计算反余弦函数
    
    Args:
        value: null
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777419068744707", "arccos", arguments)

def arctan(
    value: float
) -> Dict[str, Any]:
    """
    计算反正切函数
    
    Args:
        value: null
    
    Returns:
        
    """
    arguments = {
        "value": value
    }
    
    return call_api("1777419068744707", "arctan", arguments)

def factorial_math(
    n: int
) -> Dict[str, Any]:
    """
    求阶乘
    
    Args:
        n: null
    
    Returns:
        
    """
    arguments = {
        "n": n
    }
    
    return call_api("1777419068744707", "factorial_math", arguments)

