from datetime import datetime
from typing import Dict, List, Optional, Tuple
from .advisories import _weather_code_advisory, _precip_advisory, _dew_point_advisory

DIRECTION_SUFFIXES = ["东北部", "西北部", "东南部", "西南部", "东部", "西部", "南部", "北部", "中部"]

def _humanize_iso_time(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    if isinstance(value, str) and len(value) == 5 and value[2] == ":":
        return value
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%H:%M")
    except Exception:
        return None

def _parse_hhmm_to_minutes(value: Optional[str]) -> Optional[int]:
    if not value or not isinstance(value, str) or ":" not in value:
        return None
    try:
        hh, mm = value.split(":", 1)
        return int(hh) * 60 + int(mm)
    except Exception:
        return None

def _minutes_to_hhmm(value: int) -> str:
    value = value % (24 * 60)
    return f"{value // 60:02d}:{value % 60:02d}"

def _clamp_window_to_astronomical_night(start: Optional[str], end: Optional[str], astro_start: Optional[str], astro_end: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    start_m = _parse_hhmm_to_minutes(start)
    end_m = _parse_hhmm_to_minutes(end)
    astro_start_m = _parse_hhmm_to_minutes(astro_start)
    astro_end_m = _parse_hhmm_to_minutes(astro_end)
    if None in (start_m, end_m, astro_start_m, astro_end_m):
        return start, end
    if end_m <= start_m:
        end_m += 24 * 60
    if astro_end_m <= astro_start_m:
        astro_end_m += 24 * 60
    if start_m < astro_start_m:
        start_m += 24 * 60
        end_m += 24 * 60
    clamped_start = max(start_m, astro_start_m)
    clamped_end = min(end_m, astro_end_m)
    if clamped_start >= clamped_end:
        return None, None
    return _minutes_to_hhmm(clamped_start), _minutes_to_hhmm(clamped_end)

def _window_phrase(region: dict) -> Optional[str]:
    start = _humanize_iso_time(region.get("astronomical_night_start"))
    end = _humanize_iso_time(region.get("astronomical_night_end"))
    segment = region.get("best_window_segment")

    def _looks_like_night(hhmm: str) -> bool:
        try:
            hh = int(hhmm.split(":", 1)[0])
        except Exception:
            return False
        return hh >= 18 or hh <= 6

    if start and end and _looks_like_night(start) and _looks_like_night(end):
        if segment:
            return f"天文夜窗 {start}-{end}（月光干扰最低的时段偏{segment}）"
        return f"天文夜窗 {start}-{end}"
    if segment:
        return f"相对更好的守候时段偏{segment}，天文夜窗大致{start}-{end}"
    return None

def _confidence_phrase(confidence: Optional[str], model: Optional[str] = None) -> Optional[str]:
    if confidence == "high":
        return "短期预报可信度较高，按 ECMWF 当前预报看结果相对可靠"
    if confidence == "medium":
        return "属于中期预报，当前按 ECMWF 预报可作参考，建议出发前再复查一次"
    if confidence == "low":
        return "属于中远期预报，当前按 ECMWF 预报更适合作趋势参考"
    return None

def _hours_phrase(hours: Optional[float]) -> Optional[str]:
    if hours is None:
        return None
    if hours <= 0.2:
        return "几乎没有成型的可拍窗口"
    if hours < 1.0:
        return "不到 1 小时"
    if abs(hours - round(hours)) < 1e-6:
        return f"约 {int(round(hours))} 小时"
    return f"约 {hours:.1f} 小时"

def _stability_phrase(value: Optional[str]) -> Optional[str]:
    if value == "stable":
        return "云量比较稳"
    if value == "mixed":
        return "云量有些波动"
    if value == "volatile":
        return "云量波动较大"
    return None

def _qualification_phrase(value: Optional[str]) -> Optional[str]:
    if value == "recommended":
        return "可作为优先候选"
    if value == "backup":
        return "可作为备选"
    if value == "observe_only":
        return "更适合先观察，不建议直接拍板"
    return None

def _source_phrase(weather_model: Optional[str]) -> Optional[str]:
    if weather_model == "ecmwf_ifs":
        return "基于 ECMWF 预报"
    return None

def _judgement_phrase(judgement: Optional[str], dispute_type: Optional[str] = None) -> Optional[str]:
    if judgement == "共识推荐":
        return "模型整体偏一致，可优先关注"
    if judgement == "备选":
        return "可以先放进备选名单"
    if judgement == "单模型亮点":
        return "主要是单模型亮点，暂时别太早拍板"
    if judgement == "争议区":
        if dispute_type == "强分歧区":
            return "模型分歧较大"
        if dispute_type == "单模型乐观区":
            return "更像部分模型偏乐观"
        if dispute_type == "窗口不稳区":
            return "整晚窗口不够稳"
        return "这轮模型看法分歧不小"
    if judgement == "不建议":
        return "这轮不建议优先考虑"
    return None

def build_region_human_view(region: dict) -> dict:
    usable_hours = region.get("usable_hours")
    streak = region.get("longest_usable_streak_hours")
    worst_cloud = region.get("night_worst_cloud")
    avg_cloud = region.get("night_avg_cloud")
    wind = region.get("night_avg_wind_kmh") or region.get("night_avg_wind")
    moon = region.get("moon_interference")
    moonrise = region.get("moonrise")
    moonset = region.get("moonset")
    moon_dark = region.get("moon_dark_window")
    dew = region.get("night_avg_dew_point")
    precip = region.get("night_max_precip")
    low_cloud = region.get("night_avg_cloud_low")
    mid_cloud = region.get("night_avg_cloud_mid")
    high_cloud = region.get("night_avg_cloud_high")
    low_cloud_terrain_note = region.get("low_cloud_terrain_note")
    weather_codes = region.get("night_weather_codes")
    stability = region.get("cloud_stability")
    qualification = region.get("qualification")
    judgement = region.get("judgement")
    dispute_type = region.get("dispute_type")

    highlights = []
    if usable_hours is not None:
        highlights.append(f"可拍窗口 { _hours_phrase(usable_hours) }")
    if streak is not None:
        highlights.append(f"最长连续可拍窗口 { _hours_phrase(streak) }")
    if avg_cloud is not None:
        highlights.append(f"整晚平均云量约 {avg_cloud:.1f}%")
    if worst_cloud is not None:
        highlights.append(f"最差时段云量约 {worst_cloud:.0f}%")
    if low_cloud is not None:
        highlights.append(f"低云覆盖约 {low_cloud:.1f}%")

    risks = []
    stability_text = _stability_phrase(stability)
    if stability_text:
        risks.append(stability_text)
    if wind is not None:
        risks.append(f"夜间平均风速约 {wind:.1f} km/h")
    if moon is not None:
        risks.append(f"月光影响约 {moon:.1f}/100")
    if weather_codes:
        wx_note = _weather_code_advisory(weather_codes)
        if wx_note:
            risks.append(wx_note)
    if precip is not None and precip >= 1:
        precip_note = _precip_advisory(precip)
        if precip_note:
            risks.append(precip_note)
    if low_cloud_terrain_note:
        risks.append(low_cloud_terrain_note)
    if dew is not None:
        dew_note = _dew_point_advisory(dew)
        if dew_note:
            risks.append(dew_note)

    moon_lines = []
    if moonrise or moonset:
        moon_lines.append(f"月升 {moonrise or '?'} / 月落 {moonset or '?'}")
    if moon_dark:
        moon_lines.append(f"无月光干扰窗口 {moon_dark}")

    readable = {
        "推荐级别": _qualification_phrase(qualification),
        "结果判断": _judgement_phrase(judgement, dispute_type),
        "数据来源": _source_phrase(region.get("weather_model")),
        "可拍窗口": _hours_phrase(usable_hours),
        "最长连续窗口": _hours_phrase(streak),
        "平均云量": f"约 {avg_cloud:.1f}%" if avg_cloud is not None else None,
        "最差时段云量": f"约 {worst_cloud:.0f}%" if worst_cloud is not None else None,
        "云量走势": stability_text,
        "夜间平均风速": f"约 {wind:.1f} km/h" if wind is not None else None,
        "月光影响": f"约 {moon:.1f}/100" if moon is not None else None,
        "月光详情": moon_lines if moon_lines else None,
        "露点": f"约 {dew:.1f}°C" if dew is not None else None,
        "低/中/高云覆盖": (
            f"低云约 {low_cloud:.1f}% / 中云约 {mid_cloud:.1f}% / 高云约 {high_cloud:.1f}%"
            if low_cloud is not None and mid_cloud is not None and high_cloud is not None else None
        ),
        "低云地形修正": low_cloud_terrain_note,
        "亮点摘要": [x for x in highlights if x],
        "风险摘要": [x for x in risks if x],
    }
    return readable

def region_qualification(region: dict) -> str:
    streak = region.get("longest_usable_streak_hours") or 0
    usable = region.get("usable_hours") or 0
    worst_cloud = region.get("night_worst_cloud")
    stability = region.get("cloud_stability")
    if streak >= 5 and usable >= 5 and (worst_cloud is None or worst_cloud <= 60) and stability != "volatile":
        return "recommended"
    if streak >= 3 and usable >= 3:
        return "backup"
    return "observe_only"

def region_decision_rank_score(region: dict) -> float:
    score = float(region.get("final_score") or 0.0)
    qual = region.get("qualification") or region_qualification(region)
    if qual == "recommended":
        score += 8.0
    elif qual == "backup":
        score += 1.5
    else:
        score -= 10.0
    stability = region.get("cloud_stability")
    if stability == "stable":
        score += 2.0
    elif stability == "volatile":
        score -= 6.0
    worst_cloud = region.get("night_worst_cloud")
    if worst_cloud is not None and worst_cloud > 80:
        score -= 8.0
    return round(score, 2)

def build_region_brief_advice(region: dict, confidence: Optional[str] = None) -> str:
    label = region.get("display_label") or region.get("label", "该区域")
    usable_hours = region.get("usable_hours")
    streak = region.get("longest_usable_streak_hours")
    worst_cloud = region.get("night_worst_cloud")
    score = region.get("final_score") or 0.0
    cloud_stability = region.get("cloud_stability")
    low_cloud_terrain_note = region.get("low_cloud_terrain_note")

    tail = []
    window_phrase = _window_phrase(region)
    conf_phrase = _confidence_phrase(confidence)
    if window_phrase:
        tail.append(window_phrase)
    if cloud_stability == "stable":
        tail.append("云量波动较小")
    elif cloud_stability == "volatile":
        tail.append("云量波动较大")
    if conf_phrase:
        tail.append(conf_phrase)
    if low_cloud_terrain_note:
        if "星空云海" in low_cloud_terrain_note:
            tail.append("低云偏多，但高海拔地形下存在星空云海窗口的可能")
        else:
            tail.append("低云影响已按地形海拔做保守修正")
    suffix = f"（{'，'.join(tail)}）" if tail else ""

    if usable_hours is not None and streak is not None:
        if streak >= 5 and usable_hours >= 5 and (worst_cloud is None or worst_cloud <= 60):
            return f"{label} 值得优先关注；这晚可用时段比较完整，可以放进第一候选{suffix}。"
        if streak >= 3 and usable_hours >= 3:
            return f"{label} 可以先留在备选名单里；有一段还不错的可拍时间，但出发前最好再复查一次{suffix}。"
        return f"{label} 现在不适合太早拍板；能拍的时间偏短，更适合先观察{suffix}。"

    if score >= 75:
        return f"{label} 值得优先关注；这晚整体条件比较能打，可以放进第一候选{suffix}。"
    if score >= 60:
        return f"{label} 可以先留在备选名单里；临近出发前最好再复查一次{suffix}。"
    return f"{label} 这轮不建议优先考虑{suffix}。"

def extract_direction_suffix(label: Optional[str]) -> Optional[str]:
    base = str(label or "").split("，", 1)[0].strip()
    for suffix in DIRECTION_SUFFIXES:
        if base.endswith(suffix):
            return suffix
    return None

def build_anchor_label(label: Optional[str]) -> Optional[str]:
    if not label:
        return label
    base = str(label).split("，", 1)[0].strip()
    for suffix in DIRECTION_SUFFIXES:
        if base.endswith(suffix):
            return f"{base[:-len(suffix)]}一带"
    return base

def should_use_anchor_label(scope_meta: dict) -> bool:
    scope_mode = scope_meta.get("scope_mode")
    coverage = scope_meta.get("scope_coverage") or {}
    envelope = coverage.get("envelope") or {}
    area = abs((envelope.get("max_lat", 0) - envelope.get("min_lat", 0)) * (envelope.get("max_lng", 0) - envelope.get("min_lng", 0)))
    if scope_mode == "national":
        return True
    if coverage.get("province_count", 0) >= 2:
        return True
    if area >= 20.0:
        return True
    return False

def apply_label_presentation(labels: List[dict], scope_meta: dict) -> List[dict]:
    use_anchor = should_use_anchor_label(scope_meta)
    for region in labels:
        refined_label = region.get("label")
        anchor_label = build_anchor_label(refined_label)
        direction = extract_direction_suffix(refined_label)
        region["refined_label"] = refined_label
        region["anchor_label"] = anchor_label
        region["display_label"] = anchor_label if (use_anchor and anchor_label) else refined_label
        region["display_label_role"] = "anchor" if (use_anchor and anchor_label) else "refined"
        if use_anchor and anchor_label and refined_label and anchor_label != refined_label:
            if direction:
                region["refinement_note"] = (
                    f"大方向先看 {anchor_label}；如果继续收窄，这片区域里更好的落点会偏{direction[:-1]}，"
                    f"大致落在 {refined_label}。"
                )
            else:
                region["refinement_note"] = f"大方向先看 {anchor_label}；如果继续收窄，更优落点大致会落在 {refined_label}。"
        elif (not use_anchor) and anchor_label and refined_label and anchor_label != refined_label and direction:
            region["refinement_note"] = (
                f"大方向仍在 {anchor_label} 这片区域里；继续细看时，更好的落点偏向{direction[:-1]}，"
                f"大致落在 {refined_label}。"
            )
            region["display_label_role"] = "refined"
        else:
            region["display_label_role"] = "refined"
    return labels

def dedupe_display_labels(labels: List[dict]) -> List[dict]:
    deduped: Dict[str, dict] = {}
    for region in labels:
        key = region.get("display_label") or region.get("label")
        prev = deduped.get(key)
        if not prev:
            deduped[key] = region
            continue
        prev_score = prev.get("ranking_score", prev.get("decision_rank_score", prev.get("final_score", 0.0))) or 0.0
        curr_score = region.get("ranking_score", region.get("decision_rank_score", region.get("final_score", 0.0))) or 0.0
        if curr_score > prev_score:
            deduped[key] = region
    return list(deduped.values())
