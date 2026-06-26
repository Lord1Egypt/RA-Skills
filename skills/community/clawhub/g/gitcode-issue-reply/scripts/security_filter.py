#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全过滤器 - 简化版
仅检测敏感信息泄露，Prompt Injection 检测由人工审核环节处理
"""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class SecurityCheckResult:
    """安全检查结果"""
    passed: bool
    risk_level: RiskLevel
    threats: List[Dict]
    suggestion: Optional[str] = None


class PromptInjectionDetector:
    """
    简化版安全检测器
    仅检测敏感信息泄露，不检测 Prompt Injection（由人工审核处理）
    """

    # 仅保留敏感信息模式
    SENSITIVE_PATTERNS = [
        {
            "name": "credential_leak",
            "level": RiskLevel.HIGH,
            "patterns": [
                r'(ghp_|glpat-|github_pat_|gitlab_pat_)[a-zA-Z0-9_]+',
                r'(AKIA[0-9A-Z]{16})',
                r'-----BEGIN (RSA|EC|OPENSSH|PGP) PRIVATE KEY-----',
            ],
            "description": "包含敏感凭证信息"
        },
    ]

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """编译正则表达式"""
        for pattern_group in self.SENSITIVE_PATTERNS:
            compiled = []
            for pattern in pattern_group["patterns"]:
                try:
                    compiled.append(re.compile(pattern, re.IGNORECASE))
                except re.error:
                    pass
            pattern_group["compiled"] = compiled

    def check(self, content: str) -> SecurityCheckResult:
        """
        检查内容是否包含敏感信息
        
        Args:
            content: 待检查的内容
        
        Returns:
            SecurityCheckResult: 检查结果
        """
        if not content or not isinstance(content, str):
            return SecurityCheckResult(
                passed=True,
                risk_level=RiskLevel.LOW,
                threats=[]
            )

        threats = []
        max_risk = RiskLevel.LOW

        # 仅检查敏感信息
        for pattern_group in self.SENSITIVE_PATTERNS:
            for pattern in pattern_group["compiled"]:
                matches = pattern.finditer(content)
                for match in matches:
                    threat = {
                        "type": pattern_group["name"],
                        "level": pattern_group["level"].value,
                        "description": pattern_group["description"],
                        "matched_text": match.group(0)[:20] + "..." if len(match.group(0)) > 20 else match.group(0),
                    }
                    threats.append(threat)

                    if pattern_group["level"].value > max_risk.value:
                        max_risk = pattern_group["level"]

        # 生成建议
        suggestion = None
        if threats:
            threat_types = list(set(t["type"] for t in threats))
            suggestion = f"⚠️ 检测到敏感信息（{', '.join(threat_types)}），请在回复中移除。"

        return SecurityCheckResult(
            passed=True,  # 始终通过，仅做提示
            risk_level=max_risk,
            threats=threats,
            suggestion=suggestion
        )
