#!/usr/bin/env python3
"""
HyperMemory-4D Retention Policy Engine
MVP: salience_level, retention_tier, tier mapping rules
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json


@dataclass
class RetentionPolicy:
    """HM4D salience + retention tier rules"""

    def classify(self, record_type: str, importance: float, path_prefix: str,
                 text: Optional[str] = None) -> Dict[str, str]:
        lowered = (text or "").lower()
        
        # pinned: decision/preference or very high importance
        if record_type in ("decision", "preference") or importance >= 0.95:
            return {
                "salience_level": "pinned",
                "retention_tier": "structured"
            }
        
        # hot: project-state/todo/incident/entity or high importance
        if record_type in ("project-state", "todo", "incident", "entity") or importance >= 0.9:
            return {
                "salience_level": "hot",
                "retention_tier": "structured"
            }
        
        # warm: reports/structured/general compact
        if path_prefix in ("memory/reports/", "memory/structured/"):
            return {
                "salience_level": "warm",
                "retention_tier": "compact"
            }
        
        # cold: debug/log/temporary
        if any(k in lowered for k in ("debug", "log", "trace", "temporary")):
            return {
                "salience_level": "cold",
                "retention_tier": "index"
            }
        
        # default: warm/compact
        return {
            "salience_level": "warm",
            "retention_tier": "compact"
        }


def infer_delta_from(record_type: str, source_id: Optional[str]) -> Optional[str]:
    """infer delta_from parent id for structured derivations"""
    if record_type == "structured" and source_id:
        return source_id
    return None


def build_policy() -> RetentionPolicy:
    return RetentionPolicy()


def evaluate(record: Dict[str, Any]) -> Dict[str, Any]:
    """evaluate a record record and assign HM4D fields"""
    policy = build_policy()
    
    # extract fields
    record_type = record.get("type", "episodic")
    importance = float(record.get("importance", 0.65))
    path = record.get("source_path", "")
    text = record.get("summary", "")
    parent_id = record.get("delta_from")
    
    # classify
    result = policy.classify(record_type, importance, path, text)
    result["delta_from"] = infer_delta_from(record_type, parent_id)
    
    return {
        "salience_level": result["salience_level"],
        "retention_tier": result["retention_tier"],
        "delta_from": result["delta_from"],
    }


if __name__ == "__main__":
    # self-test
    policy = build_policy()
    
    test_cases = [
        ("decision", 0.93, "memory/semantic/decisions.md", ""),
        ("preference", 0.94, "memory/structured/preferences.md", ""),
        ("project-state", 0.9, "memory/structured/state.md", ""),
        ("episodic", 0.7, "memory/daily/xxx.summary.md", ""),
        ("structured", 0.91, "memory/structured/decisions.md", "mem_xxx"),
    ]
    
    for rt, imp, path, parent in test_cases:
        result = policy.classify(rt, imp, path, "test text")
        result["delta_from"] = infer_delta_from(rt, parent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
