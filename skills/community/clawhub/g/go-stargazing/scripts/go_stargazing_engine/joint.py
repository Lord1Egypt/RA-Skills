from typing import Dict, Optional


def build_joint_brief_advice(region: dict, confidence: Optional[str] = None) -> str:
    label = region.get("display_label") or region.get("label", "该区域")
    return f"{label} 当前没有额外联合复核信息。"


def build_joint_judgement(model_results: Dict[str, dict], confidence: Optional[str] = None) -> dict:
    return {
        "summary": {
            "consensus_count": 0,
            "candidate_count": 0,
            "disputed_count": 0,
            "reject_count": 0,
            "stability_level": None,
            "stability_note": None,
        },
        "top_joint_advice": None,
        "consensus_regions": [],
    }
