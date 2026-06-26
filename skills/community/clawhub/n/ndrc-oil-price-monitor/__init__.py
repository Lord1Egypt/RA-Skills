"""
Oil Price Monitor - 发改委成品油价格调整监控

监控国家发改委官网成品油价格调整公告，
每10个工作日自动推送通知。
"""

import sys
from pathlib import Path

# 添加 chinese-workdays 到路径
workspace_skills = Path(__file__).parent.parent
if workspace_skills not in sys.path:
    sys.path.insert(0, str(workspace_skills))

try:
    from chinese_workdays import ChineseWorkdays
except ImportError:
    # 如果在技能目录内运行，尝试相对导入
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent / 'chinese-workdays'))
        from chinese_workdays import ChineseWorkdays
    except ImportError:
        ChineseWorkdays = None

from .oil_price_monitor import OilPriceMonitor, main

__version__ = "1.0.0"
__all__ = ["OilPriceMonitor", "main"]