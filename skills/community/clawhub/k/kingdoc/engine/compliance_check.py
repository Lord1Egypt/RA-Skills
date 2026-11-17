"""KingDoc 文档内容合规检查（v4.3.0 起委托 compliance_suite）

历史实现（v3.4 ComplianceChecker / scan_sensitive / detect_leak / check_format / classify）
现统一委托 engine.compliance_suite.ComplianceCore，敏感词加载逻辑仅保留唯一来源，
消除重复维护面。对外接口与返回值保持兼容，旧 MCP 工具（kdoc_compliance_*）无需改动。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from engine.compliance_suite import (
    ComplianceCore,
    ComplianceSuite,
    SensitiveWordLoader,
    LEAK_PATTERNS,
    CLASSIFICATION_KEYWORDS,
    DEFAULT_FORMAT_SPEC,
    CLASSIFICATION_LEVELS,
    LOCAL_OCR_ENGINES,
    RISK_TIER,
)

_DEFAULT_CORE: Optional[ComplianceCore] = None


def _core(external_packs_dir: Optional[str] = None) -> ComplianceCore:
    global _DEFAULT_CORE
    if _DEFAULT_CORE is None:
        _DEFAULT_CORE = ComplianceCore(external_packs_dir=external_packs_dir)
    return _DEFAULT_CORE


class ComplianceChecker:
    """兼容别名：委托 ComplianceCore（v4.3.0 合并后唯一实现）。"""

    def __init__(self, external_packs_dir: Optional[str] = None):
        self._c = ComplianceCore(external_packs_dir=external_packs_dir)

    def scan_sensitive(
        self,
        text: str,
        custom_words: Optional[List[str]] = None,
        ignore_whitelist: bool = True,
        external_packs_dir: Optional[str] = None,
    ) -> Dict:
        ext = external_packs_dir or self._c._external_packs_dir
        return self._c.scan_sensitive(text, custom_words=custom_words, packs=None,
                                      external_packs_dir=ext)

    def detect_leak(self, text: str) -> Dict:
        return self._c.detect_leak(text)

    def check_format(self, file_path: str) -> Dict:
        return self._c.check_format(file_path)

    def classify(self, text: str) -> Dict:
        return self._c.classify(text)


def scan_sensitive(
    text: str,
    custom_words: Optional[List[str]] = None,
    external_packs_dir: Optional[str] = None,
) -> Dict:
    return _core(external_packs_dir=external_packs_dir).scan_sensitive(
        text, custom_words=custom_words, external_packs_dir=external_packs_dir)


def detect_leak(text: str) -> Dict:
    return _core().detect_leak(text)


def check_format(file_path: str) -> Dict:
    return _core().check_format(file_path)


def classify(text: str) -> Dict:
    return _core().classify(text)
