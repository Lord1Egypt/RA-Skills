from typing import Optional


def _confidence_phrase(confidence: Optional[str], model: Optional[str] = None) -> Optional[str]:
    if confidence == "high":
        return "短期预报可信度较高，按 ECMWF 当前预报看结果相对可靠"
    if confidence == "medium":
        return "属于中期预报，当前按 ECMWF 预报可作参考，建议出发前再复查一次"
    if confidence == "low":
        return "属于中远期预报，当前按 ECMWF 预报更适合作趋势参考"
    return None
