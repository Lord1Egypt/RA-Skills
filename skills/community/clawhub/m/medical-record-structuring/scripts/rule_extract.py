"""Rule-based extractor — vitals, demographics, simple diagnoses, drugs."""
from __future__ import annotations
import re
from typing import Dict, List, Any

VITALS_PATTERN = re.compile(
    r"(?:T|体温)[:：\s]*([\d.]+)\s*[°℃C]|"
    r"(?:P|脉搏)[:：\s]*(\d+)\s*次?\/?分?|"
    r"(?:R|呼吸)[:：\s]*(\d+)\s*次?\/?分?|"
    r"(?:BP|血压)[:：\s]*(\d+)\s*\/\s*(\d+)\s*mmHg"
)
AGE_PATTERN = re.compile(r"(\d+)\s*岁")
GENDER_PATTERN = re.compile(r"性别[:：\s]*(男|女)|患者\s*\S+\s*[,，]?\s*(男|女)")


def rule_extract(text: str, sections: Dict[str, str], record_type: str) -> Dict[str, List[Any]]:
    out: Dict[str, List[Any]] = {
        "patient": [],
        "vitals": [],
        "diagnosis": [],
        "medication": [],
        "lab": [],
        "procedure": [],
    }

    # ---- Patient demographics ----
    p: Dict[str, Any] = {}
    if (m := AGE_PATTERN.search(text)):
        p["age"] = int(m.group(1))
    if (m := GENDER_PATTERN.search(text)):
        p["gender"] = m.group(1) or m.group(2)
    if p:
        out["patient"].append(p)

    # ---- Vitals ----
    for m in VITALS_PATTERN.finditer(text):
        groups = m.groups()
        if groups[0]:
            out["vitals"].append({"name": "temperature", "value": float(groups[0]), "unit": "C"})
        elif groups[1]:
            out["vitals"].append({"name": "pulse", "value": int(groups[1]), "unit": "/min"})
        elif groups[2]:
            out["vitals"].append({"name": "respiration", "value": int(groups[2]), "unit": "/min"})
        elif groups[3] and groups[4]:
            out["vitals"].append({"name": "systolic_bp", "value": int(groups[3]), "unit": "mmHg"})
            out["vitals"].append({"name": "diastolic_bp", "value": int(groups[4]), "unit": "mmHg"})

    # ---- Diagnoses from the diagnosis section ----
    if "diagnosis" in sections:
        for line in sections["diagnosis"].splitlines():
            cleaned = re.sub(r"^\s*\d+[\.\)、]\s*", "", line).strip()
            if cleaned and len(cleaned) <= 80:
                out["diagnosis"].append({"text": cleaned, "icd10": None, "confidence": 0.85})

    # ---- Medications — very rough placeholder pattern ----
    drug_pat = re.compile(r"([\u4e00-\u9fa5A-Za-z]{2,15})\s*(\d+(?:\.\d+)?)\s*(mg|g|ml|IU)\s*(qd|bid|tid|qid|q\dh|prn)?")
    for m in drug_pat.finditer(text):
        out["medication"].append({
            "name": m.group(1),
            "dose": float(m.group(2)),
            "unit": m.group(3),
            "frequency": m.group(4) or "unspecified",
        })

    return out
