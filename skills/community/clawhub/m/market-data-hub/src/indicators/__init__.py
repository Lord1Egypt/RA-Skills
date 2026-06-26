"""技术指标模块初始化"""
try:
    from .moving_average import calculate_ma
    from .macd import calculate_macd
    from .rsi import calculate_rsi
    from .bollinger import calculate_bollinger_bands
    from .kdj import calculate_kdj
except ImportError:
    from moving_average import calculate_ma
    from macd import calculate_macd
    from rsi import calculate_rsi
    from bollinger import calculate_bollinger_bands
    from kdj import calculate_kdj

__all__ = [
    "calculate_ma",
    "calculate_macd", 
    "calculate_rsi",
    "calculate_bollinger_bands",
    "calculate_kdj"
]
