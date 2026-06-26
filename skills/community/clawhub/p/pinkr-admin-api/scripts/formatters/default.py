from typing import Any, Dict

from .base import BaseFormatter


class DefaultFormatter(BaseFormatter):
    """默认格式化器：直接返回原始数据"""

    def format(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return raw
