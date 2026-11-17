#!/usr/bin/env python3
"""异常体系。参考 algorithmic-novel-writer 的 exceptions.py"""


class NovelEngineError(Exception):
    """所有引擎异常的基类"""
    def __init__(self, message: str, engine: str = "", detail: str = ""):
        self.engine = engine
        self.detail = detail
        super().__init__(f"[{engine}] {message}" + (f" ({detail})" if detail else ""))


class EngineConfigError(NovelEngineError):
    """配置异常"""
    pass


class EngineRuntimeError(NovelEngineError):
    """运行时异常"""
    pass


class EngineAnalysisError(EngineRuntimeError):
    """分析过程异常"""
    pass


class EngineInputError(NovelEngineError):
    """输入校验异常"""
    pass


class EngineDependencyError(NovelEngineError):
    """依赖缺失异常"""
    pass


class EngineIntegrityError(NovelEngineError):
    """数据完整性异常"""
    pass


class PipelineError(Exception):
    """管线异常"""
    def __init__(self, message: str, phase: str = "", recoverable: bool = False):
        self.phase = phase
        self.recoverable = recoverable
        super().__init__(f"[{phase}] {message}")
