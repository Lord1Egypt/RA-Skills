"""Lightweight structural validator (full schema validation is optional)."""
from __future__ import annotations
from typing import Dict, Any, List


REQUIRED_TOP = {"resourceType", "type", "entry"}
REQUIRED_RESOURCE = {"resourceType"}


def validate_fhir(bundle: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[str] = []
    if not REQUIRED_TOP.issubset(bundle):
        issues.append(f"Bundle missing keys: {REQUIRED_TOP - set(bundle)}")
    if bundle.get("resourceType") != "Bundle":
        issues.append("Top-level resourceType must be 'Bundle'.")
    for i, e in enumerate(bundle.get("entry", [])):
        res = e.get("resource", {})
        if not REQUIRED_RESOURCE.issubset(res):
            issues.append(f"entry[{i}].resource missing resourceType")
    return {"ok": not issues, "issues": issues, "entry_count": len(bundle.get("entry", []))}
