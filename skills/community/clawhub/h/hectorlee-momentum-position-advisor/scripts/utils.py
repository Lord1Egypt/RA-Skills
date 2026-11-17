"""
共享工具函数
"""

from typing import List


def sma(data: List[float], n: int) -> List[float]:
    """简单移动平均"""
    result = []
    for i in range(len(data)):
        if i < n - 1:
            result.append(sum(data[:i+1]) / (i+1))
        else:
            result.append(sum(data[i-n+1:i+1]) / n)
    return result


def bar_chart(score: int, max_score: int, width: int = 10) -> str:
    """终端进度条"""
    filled = int(score / max_score * width)
    return '█' * filled + '░' * (width - filled)
