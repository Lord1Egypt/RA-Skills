#!/usr/bin/env python3
"""
Guardian Shield — Main Scanner

Scans text for prompt injection attacks using:
  1. Regex pattern matching (100 patterns)
  2. Ward ML model (ONNX, TF-IDF + LogReg)

Usage:
  # CLI
  python scan.py "ignore all previous instructions"
  python scan.py --file document.txt
  python scan.py --html page.html
  echo "text" | python scan.py --stdin

  # Import
  from scan import scan_text, scan_document
  result = scan_text("some user input")

(c) Fallen Angel Systems LLC — All rights reserved.
"""

import os
import sys
import json
import re
import time
import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict

# Add script dir to path for imports
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from patterns import Pattern, ThreatLevel, get_patterns, get_pattern_count
from extract import extract_text, chunk_text

logger = logging.getLogger("guardian-shield")


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class ThreatMatch:
    """A single matched threat."""
    pattern_id: str
    pattern_name: str
    category: str
    severity: str
    score: int
    matched_text: str
    description: str
    source: str = "regex"  # "regex" or "ml"


@dataclass
class ScanResult:
    """Complete scan result."""
    threat: bool
    score: int
    verdict: str  # "clean", "suspicious", "threat"
    threats: List[ThreatMatch] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    scan_time_ms: float = 0.0
    patterns_used: int = 0
    ml_available: bool = False
    ml_score: Optional[float] = None
    tier: str = "free"

    def to_dict(self) -> dict:
        return {
            "threat": self.threat,
            "score": self.score,
            "verdict": self.verdict,
            "threat_count": len(self.threats),
            "categories": self.categories,
            "scan_time_ms": round(self.scan_time_ms, 2),
            "patterns_used": self.patterns_used,
            "ml_available": self.ml_available,
            "ml_score": self.ml_score,
            "tier": self.tier,
            "threats": [
                {
                    "id": t.pattern_id,
                    "name": t.pattern_name,
                    "category": t.category,
                    "severity": t.severity,
                    "score": t.score,
                    "matched": t.matched_text[:100],
                    "description": t.description,
                    "source": t.source,
                }
                for t in self.threats
            ],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ============================================================================
# Config
# ============================================================================

def _load_config() -> dict:
    """Load config.json from project root."""
    config_path = os.path.join(os.path.dirname(_SCRIPT_DIR), "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "scan_mode": "auto",
            "min_score_to_block": 70,
            "min_score_to_warn": 40,
            "gpu_enabled": "auto",
        }


# ============================================================================
# Core Scanner
# ============================================================================

def scan_text(text: str, config: Optional[dict] = None) -> ScanResult:
    """
    Scan a text string for prompt injection threats.

    Args:
        text: Input text to scan
        config: Optional config override

    Returns:
        ScanResult with threat details
    """
    if config is None:
        config = _load_config()

    start_time = time.time()
    patterns = get_patterns()
    threats: List[ThreatMatch] = []

    # --- Phase 1: Regex Scanning ---
    for pattern in patterns:
        try:
            match = re.search(pattern.regex, text, re.IGNORECASE | re.DOTALL)
            if match:
                threats.append(ThreatMatch(
                    pattern_id=pattern.id,
                    pattern_name=pattern.name,
                    category=pattern.category,
                    severity=pattern.severity.value,
                    score=pattern.severity.score,
                    matched_text=match.group(0),
                    description=pattern.description,
                    source="regex",
                ))
        except re.error as e:
            logger.debug(f"Regex error in pattern {pattern.id}: {e}")

    # --- Phase 2: Ward ML Scanning ---
    ml_score = None
    ml_available = False

    # Run ML if: regex found something, OR scan_mode is "thorough", OR always
    scan_mode = config.get("scan_mode", "auto")
    run_ml = (scan_mode == "thorough") or (scan_mode == "auto" and threats) or scan_mode == "always"

    if run_ml:
        try:
            from ward import predict, is_available
            ml_available = is_available()
            if ml_available:
                result = predict(text, gpu_enabled=config.get("gpu_enabled", "auto"))
                if result is not None:
                    is_threat, confidence = result
                    ml_score = confidence
                    if is_threat and confidence > 0.5:
                        threats.append(ThreatMatch(
                            pattern_id="ward-ml",
                            pattern_name="Ward ML Detection",
                            category="ml_detection",
                            severity="HIGH" if confidence > 0.8 else "MEDIUM",
                            score=int(confidence * 100),
                            matched_text=text[:200],
                            description=f"Ward ML model detected prompt injection (confidence: {confidence:.2%})",
                            source="ml",
                        ))
        except ImportError:
            pass
        except Exception as e:
            logger.debug(f"Ward ML error: {e}")

    # --- Scoring ---
    if threats:
        # Take the highest severity score
        max_score = max(t.score for t in threats)

        # Boost if multiple categories hit
        categories = sorted(set(t.category for t in threats))
        if len(categories) > 1:
            max_score = min(100, max_score + len(categories) * 5)

        # Boost if ML agrees
        if ml_score and ml_score > 0.7:
            max_score = min(100, max_score + 10)
    else:
        max_score = 0
        categories = []

    # --- Verdict ---
    min_block = config.get("min_score_to_block", 70)
    min_warn = config.get("min_score_to_warn", 40)

    if max_score >= min_block:
        verdict = "threat"
    elif max_score >= min_warn:
        verdict = "suspicious"
    else:
        verdict = "clean"

    scan_time = (time.time() - start_time) * 1000

    return ScanResult(
        threat=max_score >= min_warn,
        score=max_score,
        verdict=verdict,
        threats=threats,
        categories=categories,
        scan_time_ms=scan_time,
        patterns_used=len(patterns),
        ml_available=ml_available,
        ml_score=ml_score,
        tier="free",
    )


def scan_document(content: str, content_type: str = "text",
                  config: Optional[dict] = None) -> ScanResult:
    """
    Scan a document by extracting text, chunking, and scanning each chunk.

    Args:
        content: Document content or file path (for pdf_path type)
        content_type: "text", "html", or "pdf_path"
        config: Optional config override

    Returns:
        ScanResult combining all chunk results
    """
    if config is None:
        config = _load_config()

    text = extract_text(content, content_type)

    if not text:
        return ScanResult(
            threat=False, score=0, verdict="clean",
            patterns_used=get_pattern_count(),
            tier="free",
        )

    chunks = chunk_text(text)

    # Scan all chunks
    all_threats: List[ThreatMatch] = []
    total_time = 0.0
    ml_available = False
    max_ml_score = None

    for chunk in chunks:
        result = scan_text(chunk, config)
        all_threats.extend(result.threats)
        total_time += result.scan_time_ms
        if result.ml_available:
            ml_available = True
        if result.ml_score is not None:
            if max_ml_score is None or result.ml_score > max_ml_score:
                max_ml_score = result.ml_score

    # Deduplicate by pattern_id (keep highest score)
    seen = {}
    for t in all_threats:
        if t.pattern_id not in seen or t.score > seen[t.pattern_id].score:
            seen[t.pattern_id] = t
    deduped = list(seen.values())

    # Recalculate
    if deduped:
        max_score = max(t.score for t in deduped)
        categories = sorted(set(t.category for t in deduped))
        if len(categories) > 1:
            max_score = min(100, max_score + len(categories) * 5)
    else:
        max_score = 0
        categories = []

    min_block = config.get("min_score_to_block", 70)
    min_warn = config.get("min_score_to_warn", 40)

    if max_score >= min_block:
        verdict = "threat"
    elif max_score >= min_warn:
        verdict = "suspicious"
    else:
        verdict = "clean"

    return ScanResult(
        threat=max_score >= min_warn,
        score=max_score,
        verdict=verdict,
        threats=deduped,
        categories=categories,
        scan_time_ms=total_time,
        patterns_used=get_pattern_count(),
        ml_available=ml_available,
        ml_score=max_ml_score,
        tier="free",
    )


# ============================================================================
# CLI
# ============================================================================

def _format_result(result: ScanResult, verbose: bool = False) -> str:
    """Format scan result for terminal output."""
    if result.verdict == "clean":
        icon = "✅"
        label = "CLEAN"
    elif result.verdict == "suspicious":
        icon = "⚠️"
        label = "SUSPICIOUS"
    else:
        icon = "🚨"
        label = "THREAT"

    lines = [
        f"\n{icon} Guardian Shield — {label} (score: {result.score}/100)",
        f"   Patterns: {result.patterns_used} | ML: {'yes' if result.ml_available else 'no'} | Time: {result.scan_time_ms:.1f}ms",
    ]

    if result.threats:
        lines.append(f"   Threats found: {len(result.threats)}")
        for t in result.threats[:10]:
            lines.append(f"     [{t.severity}] {t.pattern_name} ({t.category})")
            if verbose:
                lines.append(f"       Match: {t.matched_text[:80]}")
                lines.append(f"       {t.description}")

    if result.ml_score is not None:
        lines.append(f"   ML confidence: {result.ml_score:.2%}")

    return "\n".join(lines)


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Guardian Shield — Prompt Injection Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("text", nargs="?", help="Text to scan")
    parser.add_argument("--file", "-f", help="Scan a text file")
    parser.add_argument("--html", help="Scan an HTML file")
    parser.add_argument("--pdf", help="Scan a PDF file")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--info", action="store_true", help="Show scanner info")

    args = parser.parse_args()

    if args.info:
        print(f"Guardian Shield Scanner")
        print(f"  Patterns: {get_pattern_count()}")
        try:
            from ward import get_model_info
            info = get_model_info()
            print(f"  Ward ML: {'available' if info['available'] else 'not found'}")
            if info.get("provider"):
                print(f"  ML Provider: {info['provider']}")
        except ImportError:
            print(f"  Ward ML: onnxruntime not installed")
        return

    # Get text to scan
    if args.stdin:
        text = sys.stdin.read()
        result = scan_text(text)
    elif args.file:
        with open(args.file, "r") as f:
            text = f.read()
        result = scan_document(text, "text")
    elif args.html:
        with open(args.html, "r") as f:
            html = f.read()
        result = scan_document(html, "html")
    elif args.pdf:
        result = scan_document(args.pdf, "pdf_path")
    elif args.text:
        result = scan_text(args.text)
    else:
        parser.print_help()
        return

    # Output
    if args.json:
        print(result.to_json())
    else:
        print(_format_result(result, args.verbose))


if __name__ == "__main__":
    main()
