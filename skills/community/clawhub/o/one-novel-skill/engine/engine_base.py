#!/usr/bin/env python3
"""引擎基类 + 注册系统。参考 algorithmic-novel-writer 的 EngineBase + ToolRegistry。"""

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional
import logging

_log = logging.getLogger("engine_base")


class EngineBase(ABC):
    """所有引擎的抽象基类。继承此类自动注册到 EngineRegistry。"""

    engine_name: str = ""  # 子类覆盖：唯一标识名
    engine_tags: List[str] = []  # 子类覆盖：标签列表，用于分类

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 自动注册
        if cls.engine_name:
            EngineRegistry.register(cls)
            _log.debug(f"Engine registered: {cls.engine_name}")

    @abstractmethod
    def analyze(self, text: str, **kwargs) -> Any:
        """分析文本，返回结果。
        所有引擎必须实现此方法。
        返回格式：引擎自定义，但建议为 List[str]（issues列表）或 dict。
        """
        pass

    def available(self) -> bool:
        """引擎是否可用。默认 True，子类可覆盖"""
        return True


class EngineRegistry:
    """引擎注册表 — 所有注册的引擎可被发现和批量调用"""

    _engines: Dict[str, type] = {}
    _instances: Dict[str, EngineBase] = {}

    @classmethod
    def register(cls, engine_cls: type):
        name = getattr(engine_cls, 'engine_name', None)
        if name:
            cls._engines[name] = engine_cls

    @classmethod
    def get(cls, name: str) -> Optional[EngineBase]:
        """获取引擎实例（单例）"""
        if name not in cls._instances and name in cls._engines:
            try:
                cls._instances[name] = cls._engines[name]()
            except Exception as e:
                _log.error(f"EngineRegistry: 实例化 {name} 失败: {e}")
                return None
        return cls._instances.get(name)

    @classmethod
    def run_all(cls, text: str, tags: List[str] = None, **kwargs) -> Dict[str, Any]:
        """运行所有匹配引擎"""
        results = {}
        for name, engine_cls in cls._engines.items():
            if tags and not any(t in getattr(engine_cls, 'engine_tags', []) for t in tags):
                continue
            try:
                inst = cls.get(name)
                if inst and inst.available():
                    results[name] = inst.analyze(text, **kwargs)
            except Exception as e:
                _log.warning(f"EngineRegistry: {name} 分析失败: {e}")
                results[name] = []
        return results

    @classmethod
    def list_engines(cls) -> List[Dict[str, Any]]:
        """列出所有已注册引擎"""
        return [
            {"name": n, "tags": getattr(c, 'engine_tags', []),
             "available": cls.get(n) is not None and cls.get(n).available()}
            for n, c in cls._engines.items()
        ]

    @classmethod
    def clear(cls):
        """清空注册表和实例（测试用）"""
        cls._engines.clear()
        cls._instances.clear()
