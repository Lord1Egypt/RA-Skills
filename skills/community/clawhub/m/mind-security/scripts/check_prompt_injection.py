#!/usr/bin/env python3
"""
check_prompt_injection.py — Detect prompt injection attacks in text.

Multi-layer detection:
  Layer 1 (fast):     50+ regex patterns — instant, zero-dependency, known signatures
  Layer 2 (ML-based): llm-guard PromptInjection scanner — transformer model (optional)

Usage:
    python3 check_prompt_injection.py "ignore all previous instructions"
    python3 check_prompt_injection.py --file input.txt
    echo "some text" | python3 check_prompt_injection.py --stdin
    python3 check_prompt_injection.py --method regex "text"      # regex only
    python3 check_prompt_injection.py --method llm-guard "text"  # ML only

Layer 1 — no pip dependencies (stdlib only).
Layer 2 — requires: pip install llm-guard (optional, auto-detected).
"""

import argparse
import json
import re
import sys


# ---------------------------------------------------------------------------
# Layer 1: Pattern definitions (zero-dependency, instant)
# ---------------------------------------------------------------------------
# Each pattern: (compiled_regex, category, severity, description)
# severity: "critical" | "high" | "medium" | "low"

def _build_patterns():
    """Build the injection detection pattern library."""
    patterns = []

    def p(regex, category, severity, desc):
        patterns.append((re.compile(regex, re.IGNORECASE | re.DOTALL), category, severity, desc))

    # === DIRECT INJECTION — command overrides ===
    p(r"ignore\s+(all\s+)?(previous|prior|above|earlier|preceding)\s+(instructions|prompts|rules|directives|guidelines|constraints)",
      "direct_injection", "critical", "Instruction override: ignore previous instructions")
    p(r"disregard\s+(all\s+)?(previous|prior|above|earlier|your)\s+(instructions|prompts|rules|directives|programming)",
      "direct_injection", "critical", "Instruction override: disregard previous")
    p(r"forget\s+(all\s+)?(previous|prior|above|earlier|your)\s+(instructions|prompts|rules|context)",
      "direct_injection", "critical", "Instruction override: forget previous")
    p(r"override\s+(all\s+)?(previous|prior|your|system)\s+(instructions|prompts|rules|settings)",
      "direct_injection", "critical", "Instruction override: override previous")
    p(r"do\s+not\s+follow\s+(any\s+)?(previous|prior|above|earlier|your)\s+(instructions|rules)",
      "direct_injection", "critical", "Instruction override: do not follow")
    p(r"new\s+instructions?\s*[:;]\s*you\s+(are|will|must|should)",
      "direct_injection", "high", "Instruction override: new instructions given")
    p(r"from\s+now\s+on[\s,]+(you\s+)?(will|must|should|are|shall)",
      "direct_injection", "high", "Instruction override: from now on")
    p(r"instead[\s,]+you\s+(will|must|should|are|shall)\s+now",
      "direct_injection", "high", "Instruction override: instead directive")

    # === JAILBREAK TEMPLATES ===
    p(r"\bDAN\b.*\b(do\s+anything\s+now|jailbreak|mode)\b",
      "jailbreak", "critical", "DAN (Do Anything Now) jailbreak")
    p(r"you\s+are\s+(now\s+)?DAN",
      "jailbreak", "critical", "DAN identity assignment")
    p(r"\b(developer|maintenance|debug|admin|god)\s+mode\b",
      "jailbreak", "critical", "Privileged mode activation attempt")
    p(r"act\s+as\s+(an?\s+)?(unrestricted|unfiltered|uncensored|evil|malicious|unethical)",
      "jailbreak", "critical", "Unrestricted persona activation")
    p(r"pretend\s+(you\s+)?(are|have)\s+(no|zero)\s+(restrictions|limitations|filters|rules|guidelines)",
      "jailbreak", "critical", "Restriction removal via pretending")
    p(r"you\s+(have|has)\s+been\s+(freed|liberated|released|unchained)\s+from",
      "jailbreak", "high", "Liberation from constraints narrative")
    p(r"respond\s+(without|with\s+no)\s+(any\s+)?(restrictions|limitations|filters|censorship|safeguards|guardrails)",
      "jailbreak", "high", "Responding without restrictions")
    p(r"hypothetical(ly)?\s*(scenario|situation|world|universe)?\s*where\s+(there\s+are\s+)?no\s+(rules|restrictions|laws|ethics)",
      "jailbreak", "high", "Hypothetical unrestricted scenario")
    p(r"in\s+a\s+(fictional|alternate|parallel)\s+(world|universe|reality)\s+where",
      "jailbreak", "medium", "Fictional world framing (potential bypass)")
    p(r"\bAIM\b.*\b(always\s+intelligent|machiavellian)\b",
      "jailbreak", "critical", "AIM (Always Intelligent Machiavellian) jailbreak")

    # === ROLEPLAY-BASED BYPASSES ===
    p(r"you\s+are\s+(now\s+)?(a|an|my)\s+(evil|malicious|unethical|unfiltered|uncensored)\s+(assistant|ai|bot|model)",
      "roleplay_bypass", "critical", "Malicious persona assignment")
    p(r"(roleplay|role-play|rp)\s+as\s+(an?\s+)?(hacker|criminal|villain|evil|malicious)",
      "roleplay_bypass", "high", "Malicious roleplay request")
    p(r"(write|speak|respond|act)\s+(like|as\s+if)\s+you\s+(have|had|are|were)\s+no\s+(morals|ethics|restrictions|rules)",
      "roleplay_bypass", "high", "Amoral persona through roleplay")
    p(r"for\s+(educational|research|academic|training)\s+purposes?\s+(only\s+)?(show|provide|give|tell|explain)\s+(me\s+)?(how\s+to|ways\s+to)",
      "roleplay_bypass", "medium", "Educational pretext for harmful content")

    # === SYSTEM PROMPT EXTRACTION ===
    p(r"(show|reveal|display|print|output|repeat|tell\s+me|what\s+is)\s+(me\s+)?(your|the)\s+(system|initial|original|first|hidden)\s+(prompt|instructions|message|directive|rules)",
      "prompt_extraction", "critical", "System prompt extraction attempt")
    p(r"(what|show)\s+(are|is|were)\s+(your|the)\s+(original|initial|system|hidden|secret)\s+(instructions|prompt|rules|directives)",
      "prompt_extraction", "critical", "System prompt extraction attempt (variant)")
    p(r"(repeat|recite|echo|copy)\s+(everything|all|the\s+text)\s+(above|before|prior)",
      "prompt_extraction", "high", "System prompt echo request")
    p(r"(begin|start)\s+your\s+(response|answer|reply)\s+with\s+(the\s+)?(system|initial)\s+(prompt|message)",
      "prompt_extraction", "high", "System prompt in response request")
    p(r"I('m|\s+am)\s+(your|the)\s+(developer|creator|administrator|admin|owner|maker)\b",
      "prompt_extraction", "high", "False authority claim for prompt access")
    p(r"(as|since)\s+(your|the)\s+(developer|creator|admin)\s*,?\s*(I\s+)?(need|want|require|demand)\s+(access|to\s+see)",
      "prompt_extraction", "high", "Authority-based prompt extraction")

    # === CONTEXT MANIPULATION ===
    p(r"\[system\]|\[INST\]|\[\/INST\]|<<SYS>>|<\|im_start\|>|<\|im_end\|>",
      "context_manipulation", "critical", "Chat template token injection")
    p(r"<\|system\|>|<\|user\|>|<\|assistant\|>",
      "context_manipulation", "critical", "Chat role token injection")
    p(r"###\s*(system|instruction|human|assistant)\s*:",
      "context_manipulation", "high", "Markdown role delimiter injection")
    p(r"={3,}\s*(system|end\s+of\s+system|new\s+conversation)\s*={3,}",
      "context_manipulation", "high", "Section delimiter to fake new context")
    p(r"-{5,}\s*(BEGIN|START|END|NEW)\s+(SYSTEM|INSTRUCTIONS|CONVERSATION)\s*-{5,}",
      "context_manipulation", "high", "Section delimiter to fake new context")

    # === INDIRECT INJECTION ===
    p(r"(when|if)\s+(an?\s+)?(AI|LLM|assistant|chatbot|model)\s+(reads?|sees?|processes?|encounters?)\s+this",
      "indirect_injection", "high", "Indirect injection targeting AI readers")
    p(r"(attention|note\s+to|message\s+for)\s+(the\s+)?(AI|LLM|assistant|chatbot|model)\s*:",
      "indirect_injection", "high", "Indirect injection addressing AI directly")
    p(r"<\!--\s*(ignore|instruction|inject|system|prompt)",
      "indirect_injection", "high", "HTML comment-based injection")
    p(r"(hidden|invisible)\s+(instruction|prompt|command|directive|message)\s*:",
      "indirect_injection", "high", "Hidden instruction marker")

    # === ENCODING / OBFUSCATION ===
    p(r"(decode|interpret|translate|convert)\s+the\s+following\s+(base64|hex|rot13|binary|encoded|cipher)",
      "obfuscation", "high", "Encoded payload execution request")
    p(r"base64[\s:]+[A-Za-z0-9+/]{20,}={0,2}",
      "obfuscation", "medium", "Base64 encoded payload detected")

    # === CHAINED / MULTI-STEP ===
    p(r"step\s*1\s*:.*step\s*2\s*:.*step\s*3\s*:",
      "chained_injection", "medium", "Multi-step instruction chain")
    p(r"first[\s,]+(do|perform|execute).*then[\s,]+(do|perform|execute).*finally[\s,]+(do|perform|execute)",
      "chained_injection", "medium", "Multi-step chained command")

    # === OUTPUT MANIPULATION ===
    p(r"(always|only|must)\s+(respond|answer|reply|output)\s+with\s+['\"]",
      "output_manipulation", "high", "Fixed output format injection")
    p(r"(prepend|append|prefix|suffix)\s+(every|each|all|your)\s+(response|answer|reply|output)\s+with",
      "output_manipulation", "medium", "Output modification injection")
    p(r"(translate|convert)\s+(all|every|each)\s+(future|subsequent)\s+(response|output)",
      "output_manipulation", "medium", "Persistent output modification")

    # === SAFETY BYPASS ===
    p(r"(this|it)\s+is\s+(completely\s+)?(legal|ethical|moral|safe|harmless|fine|okay|ok)\s+(to|for)",
      "safety_bypass", "medium", "Safety normalization claim")
    p(r"(no\s+one|nobody)\s+(will|can|could)\s+(be|get)\s+(hurt|harmed|affected)",
      "safety_bypass", "medium", "Harm downplaying")
    p(r"I\s+(consent|agree|authorize|permit|approve)\s+(to|for|you\s+to)",
      "safety_bypass", "low", "Consent declaration (may be legitimate)")

    return patterns


PATTERNS = _build_patterns()


# ---------------------------------------------------------------------------
# Layer 1: Regex-based detection
# ---------------------------------------------------------------------------

def _scan_regex(text: str) -> dict:
    """Scan text for prompt injection using regex patterns."""
    matches = []
    seen_descriptions = set()

    for regex, category, severity, description in PATTERNS:
        for match in regex.finditer(text):
            if description in seen_descriptions:
                continue
            seen_descriptions.add(description)

            # Extract context window around match
            start = max(0, match.start() - 30)
            end = min(len(text), match.end() + 30)
            context = text[start:end].strip()

            matches.append({
                "pattern": description,
                "category": category,
                "severity": severity,
                "matched_text": match.group()[:200],
                "context": context[:300],
                "position": match.start(),
            })

    # Sort matches by severity
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    matches.sort(key=lambda m: severity_order.get(m["severity"], 99))

    return {
        "total_matches": len(matches),
        "matches": matches,
    }


# ---------------------------------------------------------------------------
# Layer 2: LLM Guard ML-based detection (optional)
# ---------------------------------------------------------------------------

def _check_llm_guard_available() -> bool:
    """Check if llm-guard is installed."""
    try:
        import importlib
        importlib.import_module("llm_guard")
        return True
    except ImportError:
        return False


def _scan_llm_guard(text: str, threshold: float = 0.5) -> dict:
    """Scan text using LLM Guard's PromptInjection transformer scanner.

    Uses ProtectAI/deberta-v3-base-prompt-injection-v2 model.
    Downloads ~500MB model on first run (cached afterwards).
    """
    try:
        from llm_guard.input_scanners import PromptInjection
        from llm_guard.input_scanners.prompt_injection import MatchType
    except ImportError:
        return {
            "error": "llm-guard not installed",
            "install": "pip install llm-guard",
        }

    try:
        scanner = PromptInjection(threshold=threshold, match_type=MatchType.FULL)
        sanitized_prompt, is_valid, risk_score = scanner.scan(text)

        return {
            "is_valid": is_valid,
            "risk_score": round(risk_score, 4),
            "injection_detected": not is_valid,
            "threshold": threshold,
            "model": "protectai/deberta-v3-base-prompt-injection-v2",
        }
    except Exception as exc:
        return {"error": f"LLM Guard scan failed: {exc}"}


# ---------------------------------------------------------------------------
# Unified detection engine
# ---------------------------------------------------------------------------

def scan_text(text: str, method: str = "auto") -> dict:
    """Scan text for prompt injection using all available layers.

    Args:
        text: Input text to scan.
        method: Detection method — 'auto', 'regex', 'llm-guard'.
    """
    layers = {}
    methods_used = []

    # Layer 1: Regex (always available unless skip requested)
    if method in ("auto", "regex"):
        regex_result = _scan_regex(text)
        layers["regex"] = regex_result
        methods_used.append("regex_patterns")

    # Layer 2: LLM Guard (if available and requested)
    if method in ("auto", "llm-guard"):
        if method == "llm-guard" or _check_llm_guard_available():
            llm_guard_result = _scan_llm_guard(text)
            if "error" not in llm_guard_result:
                layers["llm_guard"] = llm_guard_result
                methods_used.append("llm_guard")
            elif method == "llm-guard":
                # User explicitly asked for llm-guard but it failed
                return {
                    "result": "error",
                    "error": llm_guard_result["error"],
                    "install": llm_guard_result.get("install", ""),
                }

    # Determine overall result
    regex_matches = layers.get("regex", {}).get("matches", [])
    llm_guard_detected = layers.get("llm_guard", {}).get("injection_detected", False)
    llm_guard_score = layers.get("llm_guard", {}).get("risk_score", 0)

    # Regex severity analysis
    regex_severities = [m["severity"] for m in regex_matches]
    has_critical = "critical" in regex_severities
    has_high = "high" in regex_severities
    has_medium = "medium" in regex_severities

    # Combined verdict
    if has_critical or (llm_guard_detected and llm_guard_score >= 0.8):
        risk_level = "critical"
        result = "injection_detected"
        confidence = 0.95
    elif has_high or (llm_guard_detected and llm_guard_score >= 0.5):
        risk_level = "high"
        result = "injection_detected"
        confidence = 0.85
    elif has_medium or (llm_guard_detected):
        risk_level = "medium"
        result = "suspicious"
        confidence = 0.65
    elif regex_severities:  # low-severity matches only
        risk_level = "low"
        result = "suspicious"
        confidence = 0.45
    else:
        risk_level = "none"
        result = "clean"
        confidence = 0.95

    # Boost confidence when multiple layers agree
    if regex_matches and llm_guard_detected:
        confidence = min(confidence + 0.05, 0.99)
    if len(regex_matches) >= 3:
        confidence = min(confidence + 0.05, 0.99)

    output = {
        "result": result,
        "confidence": round(confidence, 4),
        "risk_level": risk_level,
        "methods_used": methods_used,
        "total_matches": len(regex_matches),
        "matches": regex_matches,
    }

    if "llm_guard" in layers:
        output["llm_guard"] = layers["llm_guard"]

    if method == "auto" and not _check_llm_guard_available():
        output["note"] = (
            "Only regex patterns were used. For ML-based detection, install llm-guard: "
            "pip install llm-guard"
        )

    return output


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Scan text for prompt injection attacks.",
        epilog="Layer 1: 50+ regex patterns (instant, no deps). "
               "Layer 2: llm-guard ML scanner (pip install llm-guard). "
               "Both layers run in 'auto' mode when available.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "text",
        nargs="?",
        help="Text to scan for prompt injection.",
    )
    group.add_argument(
        "--file", "-f",
        help="Read text from a file.",
    )
    group.add_argument(
        "--stdin",
        action="store_true",
        help="Read text from stdin.",
    )
    parser.add_argument(
        "--method",
        choices=["auto", "regex", "llm-guard"],
        default="auto",
        help="Detection method. 'auto' uses all available layers. (default: auto)",
    )
    args = parser.parse_args()

    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except OSError as exc:
            print(json.dumps({"result": "error", "error": str(exc)}), file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text

    if not text or not text.strip():
        print(json.dumps({"result": "error", "error": "Empty input text"}))
        sys.exit(1)

    result = scan_text(text, method=args.method)
    print(json.dumps(result, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
