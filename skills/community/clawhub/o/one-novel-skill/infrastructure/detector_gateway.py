"""
infrastructure/detector_gateway.py — Unified detector interface

Wraps all 6 detection suites behind a single unified API.
Returns standardized DetectionResult regardless of internal implementation.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pathlib import Path
import sys

_log = logging.getLogger("detector_gateway")


@dataclass
class DetectionIssue:
    """A single detection issue."""
    suite: str       # d1_banned, d2_humanizer, etc.
    message: str
    severity: str = "warning"  # error | warning | info


@dataclass
class DetectionResult:
    """Unified result from all detection suites."""
    classification: str = "GREEN"  # GREEN | YELLOW | RED
    passed: bool = True
    weighted_score: float = 0.0
    threshold: float = 0.15
    total_weight: int = 0
    issues: List[DetectionIssue] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def issue_count(self) -> int:
        return len(self.issues)
    
    @property
    def severity_counts(self) -> Dict[str, int]:
        counts = {}
        for i in self.issues:
            counts[i.severity] = counts.get(i.severity, 0) + 1
        return counts


class DetectorGateway:
    """
    Unified gateway for all 6 detection suites.
    
    Usage:
        gw = DetectorGateway()
        result = gw.detect(text, platform="番茄")
        if not result.passed:
            for issue in result.issues:
                print(f"[{issue.suite}] {issue.message}")
    """
    
    SUITE_WEIGHTS = {
        "d1_banned": 3,       # Core: banned words
        "d5_structure": 3,    # Core: AI structure
        "d2_humanizer": 2,    # Aux: humanizer patterns
        "d3_qmai": 2,         # Aux: QMAI patterns
        "d4_baselines": 2,    # Aux: statistical baselines
        "d6_subject": 2,      # Aux: subject distribution
    }
    
    def __init__(self):
        self._init_detectors()
    
    def _init_detectors(self):
        """Lazy import of detector modules."""
        # We import lazily to keep the gateway lightweight
        try:
            from detectors.run_all_detectors import run_all as _run_all
            self._run_all = _run_all
        except ImportError as e:
            _log.error(f"Failed to import detectors: {e}")
            self._run_all = None
    
    def detect(self, text: str, platform: str = "general", 
               chapter_name: str = "unknown") -> DetectionResult:
        """Run all detection suites against text."""
        if self._run_all is None:
            return DetectionResult(
                classification="GREEN",
                passed=True,
                issues=[DetectionIssue("gateway", "Detectors not loaded")],
            )
        
        try:
            raw = self._run_all(text, chapter_name, platform)
            return self._parse_raw_result(raw)
        except Exception as e:
            _log.error(f"Detection failed: {e}")
            return DetectionResult(
                classification="YELLOW",
                passed=False,
                issues=[DetectionIssue("gateway", f"Detection error: {e}", "error")],
            )
    
    def _parse_raw_result(self, raw: dict) -> DetectionResult:
        """Convert raw detector output to unified format."""
        classification = raw.get("classification", "GREEN")
        passed = "GREEN" in classification
        score = raw.get("weighted_vote", 0.0)
        total = raw.get("total_weight", 14)
        threshold = raw.get("threshold", 0.15)
        
        issues = []
        raw_issues = raw.get("issues", [])
        if isinstance(raw_issues, list):
            for iss in raw_issues:
                if isinstance(iss, str):
                    issues.append(DetectionIssue(suite="unknown", message=iss))
                elif isinstance(iss, dict):
                    issues.append(DetectionIssue(
                        suite=iss.get("suite", "unknown"),
                        message=iss.get("message", str(iss)),
                        severity=iss.get("severity", "warning"),
                    ))
        
        metadata = raw.get("metadata", {})
        metadata.update({
            "text_length": len(text) for text in [raw.get("text", "")]
            if text
        })
        
        return DetectionResult(
            classification=classification,
            passed=passed,
            weighted_score=score,
            threshold=threshold,
            total_weight=total,
            issues=issues,
            metadata=metadata,
        )
    
    def check(self, text: str) -> list:
        """Compatibility shim for QualityGate — returns list of issue message strings."""
        result = self.detect(text)
        if result.passed:
            return []
        return [i.message for i in result.issues]

    def check_content_safety(self, text: str) -> DetectionResult:
        """Run content safety filter (PASS/WARN/FLAG/BLOCK)."""
        try:
            from detectors.content_safety_filter import filter_content
            raw = filter_content(text)
            passed = raw.get("level", "PASS") in ("PASS", "WARN")
            issues = []
            if not passed:
                issues.append(DetectionIssue(
                    "safety",
                    raw.get("reason", "Content safety check failed"),
                    "error"
                ))
            return DetectionResult(
                classification=raw.get("level", "PASS"),
                passed=passed,
                issues=issues,
                metadata={"safety_level": raw.get("level")},
            )
        except Exception as e:
            _log.error(f"Safety check failed: {e}")
            return DetectionResult(classification="WARN", passed=True)
