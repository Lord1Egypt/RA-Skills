"""WPS AI 后端抽象基类"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class WpsAiBackend(ABC):
    """WPS AI 后端抽象基类 — 所有后端必须实现这些接口"""

    @abstractmethod
    def write(self, text: str, action: str = "polish", **kwargs) -> Dict:
        """AI 写作辅助

        Args:
            text: 原始文本
            action: 操作类型 — polish(润色) / expand(扩写) / shorten(缩写) /
                    translate(翻译) / continue_write(续写) / rewrite(改写)
        Returns:
            {text, action, backend, note}
        """
        ...

    @abstractmethod
    def analyze(self, data: Any, question: str, **kwargs) -> Dict:
        """AI 数据分析

        Args:
            data: 表格数据（二维数组或 CSV 文本）
            question: 自然语言问题
        Returns:
            {analysis, formulas, charts, backend, note}
        """
        ...

    @abstractmethod
    def ppt(self, outline: str, **kwargs) -> Dict:
        """AI PPT 生成

        Args:
            outline: 大纲文本（Markdown 格式）
        Returns:
            {file_path, slides_count, backend, note}
        """
        ...

    @abstractmethod
    def read(self, content: str, action: str = "summarize", **kwargs) -> Dict:
        """AI 阅读助手

        Args:
            content: 文档全文
            action: 操作类型 — summarize(总结) / qa(问答) / mindmap(思维导图)
        Returns:
            {summary, key_points, mindmap_svg, backend, note}
        """
        ...
