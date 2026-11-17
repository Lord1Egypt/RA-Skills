#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 检测器封装层

将 detectors/run_all_detectors.py 封装为可编程调用的类。
orchestrator 通过这个模块调用检测，不直接调子进程。
"""

import sys
from pathlib import Path


import logging
import threading
from .contracts import DetectorResult

_log = logging.getLogger("detector_wrapper")
_detector_lock = threading.RLock()

# 类型 -> 权重映射（可配置）
CLASSIFICATION_WEIGHTS = {
    "GREEN": 0.0,
    "YELLOW": 0.3,
    "RED": 0.5,
}

# 支持的 genre 列表
VALID_GENRES = {"general", "fantasy", "urban", "history", "xianxia", "romance", "suspense"}


class DetectorWrapper:
    """检测器封装，懒加载 run_all_detectors（importlib 方式）"""

    def __init__(self):
        self._run_all = None

    def _load(self):
        """加载检测引擎（懒加载，用 importlib 避免 sys.path 污染）"""
        import importlib.util
        det_dir = Path(__file__).parent.parent / "detectors"
        spec = importlib.util.spec_from_file_location(
            "_detector_isolated",
            str(det_dir / "run_all_detectors.py")
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self._run_all = mod

    def check(self, text: str, genre: str = "general", fast: bool = False,
              safety: bool = False, bname: str = "") -> list:
        """检测文本，返回 DetectorResult（兼容旧接口）。"""
        if self._run_all is None:
            self._load()
        if not bname:
            bname = "detector_wrapper"
        result = self._run_all.run_all(text, bname=bname, genre=genre,
                                        safety=safety, fast_mode=fast)
        issues = result.get("issues", [])
        cls_raw = result.get("classification", "[GREEN] 人类创作")
        if "[RED]" in cls_raw:
            cls = "RED"
        elif "[YELLOW]" in cls_raw:
            cls = "YELLOW"
        else:
            cls = "GREEN"
        from .contracts import DetectorResult
        return DetectorResult(issues=issues, classification=cls,
            weighted_score=0.0 if not issues else 0.3 if cls == "YELLOW" else 0.5,
            passed=(cls == "GREEN"))
