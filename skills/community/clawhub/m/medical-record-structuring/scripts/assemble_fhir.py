"""Assemble FHIR R4 Bundle from extracted entities (minimal demo)."""
from __future__ import annotations
import uuid
from typing import Dict, Any, List


def _entry(resource: Dict[str, Any]) -> Dict[str, Any]:
    return {"fullUrl": f"urn:uuid:{uuid.uuid4()}", "resource": resource}


def assemble_fhir(entities: Dict[str, List[Any]], record_type: str) -> Dict[str, Any]:
    entries: List[Dict[str, Any]] = []

    for p in entities.get("patient", []):
        res = {"resourceType": "Patient"}
        if "age" in p:
            res["extension"] = [{"url": "http://example.org/age-years", "valueInteger": p["age"]}]
        if "gender" in p:
            res["gender"] = "male" if p["gender"] == "男" else "female"
        res["name"] = [{"use": "official", "family": "unknown"}]
        entries.append(_entry(res))

    for v in entities.get("vitals", []):
        entries.append(_entry({
            "resourceType": "Observation",
            "status": "final",
            "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
            "code": {"text": v["name"]},
            "valueQuantity": {"value": v["value"], "unit": v["unit"]},
        }))

    for d in entities.get("diagnosis", []):
        entries.append(_entry({
            "resourceType": "Condition",
            "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
            "code": {"text": d["text"]},
            "extension": [{"url": "http://example.org/confidence", "valueDecimal": d.get("confidence", 0.0)}],
        }))

    for m in entities.get("medication", []):
        entries.append(_entry({
            "resourceType": "MedicationRequest",
            "status": "active",
            "intent": "order",
            "medicationCodeableConcept": {"text": m["name"]},
            "dosageInstruction": [{
                "text": f"{m['dose']}{m['unit']} {m['frequency']}",
                "doseAndRate": [{"doseQuantity": {"value": m["dose"], "unit": m["unit"]}}],
            }],
        }))

    return {
        "resourceType": "Bundle",
        "type": "collection",
        "meta": {"tag": [{"system": "http://example.org/record-type", "code": record_type}]},
        "entry": entries,
    }
