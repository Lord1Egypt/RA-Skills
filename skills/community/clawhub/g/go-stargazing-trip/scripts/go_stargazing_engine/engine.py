from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .astronomy import nightly_observation_window
from .geo import *
from .geo import _light_pollution_estimate
from .models import *
from .scoring import *
from .weather import *

def parse_target_datetime(value: Optional[str]) -> datetime:
    if value:
        return datetime.fromisoformat(value)
    return datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)


def select_stage2_budget(points: List[SamplePoint], max_stage2_points: int, direct_stage2_threshold: int = 10) -> List[SamplePoint]:
    ordered = sorted(points, key=lambda p: (0 if p.stage1_status == "pass" else 1, p.night_avg_cloud if p.night_avg_cloud is not None else (p.cloud_cover if p.cloud_cover is not None else 999.0), p.id))
    if len(ordered) <= direct_stage2_threshold:
        return ordered
    return ordered[:max_stage2_points]


def generate_adaptive_refinement_points(points: List[SamplePoint], boxes: List[BoundingBox], max_parent_points: int = 4) -> List[SamplePoint]:
    """Generate a small local neighborhood around the best coarse-filtered points.
    Purpose: reduce the chance of missing local weather peaks between coarse sample nodes.
    """
    if not points:
        return []
    box_map = {b.province: b for b in boxes}
    selected = sorted(
        points,
        key=lambda p: (p.night_avg_cloud if p.night_avg_cloud is not None else (p.cloud_cover if p.cloud_cover is not None else 999.0), p.id)
    )[:max_parent_points]
    out: List[SamplePoint] = []
    for parent in selected:
        box = box_map.get(parent.province)
        if not box:
            continue
        lat_step = max((box.max_lat - box.min_lat) * 0.08, 0.12)
        lng_step = max((box.max_lng - box.min_lng) * 0.08, 0.12)
        candidates = [
            (parent.lat + lat_step, parent.lng),
            (parent.lat - lat_step, parent.lng),
            (parent.lat, parent.lng + lng_step),
            (parent.lat, parent.lng - lng_step),
        ]
        for lat, lng in candidates:
            lat = min(max(lat, box.min_lat), box.max_lat)
            lng = min(max(lng, box.min_lng), box.max_lng)
            if abs(lat - parent.lat) < 1e-6 and abs(lng - parent.lng) < 1e-6:
                continue
            out.append(SamplePoint(id=f"{parent.province}:{lat:.4f}:{lng:.4f}", province=parent.province, scope_name=parent.scope_name, lat=lat, lng=lng))
    return out


def summarize_cluster(cluster: List[SamplePoint], boxes: List[BoundingBox], target_date, prefecture_polygons: Optional[Dict[str, MultiPolygon]] = None, county_polygons: Optional[Dict[str, MultiPolygon]] = None) -> dict:
    provinces = sorted({p.province for p in cluster})
    label = cluster_label(cluster, boxes, prefecture_polygons=prefecture_polygons, county_polygons=county_polygons)
    label = add_province_context(label, provinces)
    lat, lng = cluster_centroid(cluster)
    lp_label, lp_note = _light_pollution_estimate(lat, lng)
    best = sorted(cluster,
 key=lambda p: (-(p.final_score or -1), p.night_avg_cloud if p.night_avg_cloud is not None else 999.0))[0]
    elevs = [p.elevation_m for p in cluster if p.elevation_m is not None]
    # Aggregate nightly weather across cluster members
    nc = [p.night_avg_cloud for p in cluster if p.night_avg_cloud is not None]
    nw = [p.night_worst_cloud for p in cluster if p.night_worst_cloud is not None]
    nh = [p.night_avg_humidity for p in cluster if p.night_avg_humidity is not None]
    nv = [p.night_avg_visibility for p in cluster if p.night_avg_visibility is not None]
    nwi = [p.night_avg_wind for p in cluster if p.night_avg_wind is not None]
    mi = [p.moon_interference for p in cluster if p.moon_interference is not None]
    uh = [p.usable_hours for p in cluster if p.usable_hours is not None]
    ls = [p.longest_usable_streak_hours for p in cluster if p.longest_usable_streak_hours is not None]
    cs = [p.cloud_stddev for p in cluster if p.cloud_stddev is not None]
    nd = [p.night_avg_dew_point for p in cluster if p.night_avg_dew_point is not None]
    np = [p.night_max_precip for p in cluster if p.night_max_precip is not None]
    ncb = [p.night_min_cloud_base for p in cluster if p.night_min_cloud_base is not None]
    moon_scores = [p.moon_factor or 0.0 for p in cluster]

    # Astronomical night window for this region's centroid (independent of weather)
    astro_window = derive_night_window(lat, lng, target_date)
    astro_start_h, astro_end_h = astro_window
    astro_start_str = f"{astro_start_h % 24:02d}:00"
    astro_end_str = f"{astro_end_h % 24:02d}:00"

    summary = {
        "label": label,
        "provinces": provinces,
        "cluster_size": len(cluster),
        "lat": round(lat, 5),
        "lng": round(lng, 5),
        "best_point_id": best.id,
        "final_score": round(sum((p.final_score or 0.0) for p in cluster) / len(cluster), 2),
        "best_score": best.final_score,
        # Astronomical night window (twilight-based, location-specific)
        "astronomical_night_start": astro_start_str,
        "astronomical_night_end": astro_end_str,
        # Best scoring window within the night (from best point)
        "best_window_start": best.best_window_start,
        "best_window_end": best.best_window_end,
        # Nightly aggregated weather
        "night_avg_cloud": round(sum(nc) / len(nc), 1) if nc else None,
        "night_worst_cloud": round(max(nw), 1) if nw else None,
        "night_avg_humidity": round(sum(nh) / len(nh), 1) if nh else None,
        "night_avg_visibility_m": round(sum(nv) / len(nv), 0) if nv else None,
        "night_avg_wind_kmh": round(sum(nwi) / len(nwi), 1) if nwi else None,
        "moon_interference": round(sum(mi) / len(mi), 1) if mi else None,
        "moonrise": best.moonrise,
        "moonset": best.moonset,
        "moon_dark_window": best.moon_dark_window,
        "usable_hours": round(sum(uh) / len(uh), 1) if uh else None,
        "longest_usable_streak_hours": round(sum(ls) / len(ls), 1) if ls else None,
        "best_window_start": best.best_window_start,
        "best_window_end": best.best_window_end,
        "best_window_segment": best.best_window_segment,
        "cloud_stddev": round(sum(cs) / len(cs), 1) if cs else None,
        "cloud_stability": classify_cloud_stability(round(sum(cs) / len(cs), 1)) if cs else None,
        "worst_cloud_segment": best.worst_cloud_segment,
        "avg_moonlight_score": round(sum(moon_scores) / len(moon_scores), 1),
        "avg_cloud_cover": round(sum((p.cloud_cover or 0.0) for p in cluster) / len(cluster), 2),
        "avg_elevation_m": round(sum(elevs) / len(elevs), 0) if elevs else None,
        "members": [p.id for p in sorted(cluster, key=lambda x: x.id)],
        # New detailed weather
        "night_avg_dew_point": round(sum(nd) / len(nd), 1) if nd else None,
        "night_max_precip": max(np) if np else None,
        "night_min_cloud_base": min(ncb) if ncb else None,
        "night_weather_codes": best.night_weather_codes,
        # Light pollution estimate (city-distance based, NOT measured)
        "light_pollution_bortle": lp_label,
        "light_pollution_note": lp_note,
    }
    summary["qualification"] = region_qualification(summary)
    summary["decision_rank_score"] = region_decision_rank_score(summary)
    summary["human_view"] = build_region_human_view(summary)
    return summary


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


def _window_phrase(region: dict) -> Optional[str]:
    # Prefer astronomical night window (location-specific) over best-point scoring window
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
        return f"天文夜窗 {start}-{end}（月光干扰最低的时段偏{segment}）"
    if segment:
        return f"相对更好的守候时段偏{segment}，天文夜窗大致{start}-{end}"
    return None


def _confidence_phrase(confidence: Optional[str], model: Optional[str] = None) -> Optional[str]:
    # model_quality: higher = better (ecmwf > gfs > icon for China region generally)
    model_rank = {"ecmwf_ifs": 3, "gfs_global": 2, "icon_global": 2, "best_match": 1, None: 0}.get(model, 0)
    horizon_score = {"high": 3, "medium": 2, "low": 1, None: 0}.get(confidence, 0)
    # terrain complexity: rough heuristic
    combined = model_rank + horizon_score
    if confidence == "high" and model_rank >= 2:
        return "短期预报可信度较高，且使用了较高分辨率模型，结果相对可靠"
    if confidence == "high":
        return "短期预报可信度较高"
    if confidence == "medium" and model_rank >= 2:
        return "属于中期预报，但使用了较高分辨率模型，参考价值仍较强，建议出发前再复查一次"
    if confidence == "medium":
        return "属于中期预报，预报精度有所下降，建议出发前再复查一次"
    if confidence == "low" and model_rank >= 2:
        return "属于中远期预报，更适合作趋势参考；较高分辨率模型有助于减少误判"
    if confidence == "low":
        return "属于中远期预报，当前更适合作趋势参考"
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


def _evidence_phrase(evidence_type: Optional[str], model_coverage: Optional[int]) -> Optional[str]:
    if evidence_type in {"dual_model", "multi_model"}:
        return f"有 {model_coverage or 2} 个模型提供支持"
    if evidence_type == "single_model":
        return "目前只有 1 个模型给出较明显支持"
    return None


def _judgement_phrase(judgement: Optional[str], dispute_type: Optional[str] = None) -> Optional[str]:
    if judgement == "共识推荐":
        return "多模型结论一致，适合优先关注"
    if judgement == "备选":
        return "可以留在候选名单里"
    if judgement == "单模型亮点":
        return "只有单个模型明显看好，适合保守看待"
    if judgement == "争议区":
        if dispute_type == "强分歧区":
            return "模型分歧较大，风险偏高"
        if dispute_type == "单模型乐观区":
            return "只有部分模型乐观，不能直接当首选"
        if dispute_type == "窗口不稳区":
            return "虽然有可拍时段，但窗口不够稳"
        return "模型之间还有争议"
    if judgement == "不建议":
        return "当前不建议优先考虑"
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
    cloud_base = region.get("night_min_cloud_base")
    weather_codes = region.get("night_weather_codes")
    stability = region.get("cloud_stability")
    qualification = region.get("qualification")
    evidence_type = region.get("evidence_type")
    model_coverage = region.get("model_coverage")
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
    if cloud_base is not None:
        cb_note = _cloud_base_advisory(cloud_base)
        if cb_note:
            risks.append(cb_note)
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
        "联合判断": _judgement_phrase(judgement, dispute_type),
        "模型支持": _evidence_phrase(evidence_type, model_coverage),
        "可拍窗口": _hours_phrase(usable_hours),
        "最长连续窗口": _hours_phrase(streak),
        "平均云量": f"约 {avg_cloud:.1f}%" if avg_cloud is not None else None,
        "最差时段云量": f"约 {worst_cloud:.0f}%" if worst_cloud is not None else None,
        "云量走势": stability_text,
        "夜间平均风速": f"约 {wind:.1f} km/h" if wind is not None else None,
        "月光影响": f"约 {moon:.1f}/100" if moon is not None else None,
        "月光详情": moon_lines if moon_lines else None,
        "露点": f"约 {dew:.1f}°C" if dew is not None else None,
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



def aggregate_labels(points: List[SamplePoint], boxes: List[BoundingBox], top_n: int, cluster_km: float, target_date, prefecture_polygons: Optional[Dict[str, MultiPolygon]] = None, county_polygons: Optional[Dict[str, MultiPolygon]] = None, confidence: Optional[str] = None) -> List[dict]:
    if not points:
        return []
    clusters = cluster_points(points, cluster_km=cluster_km)
    summaries = [summarize_cluster(c, boxes, target_date, prefecture_polygons=prefecture_polygons, county_polygons=county_polygons) for c in clusters]
    summaries.sort(key=lambda x: (-x["decision_rank_score"], -x["final_score"], x["avg_cloud_cover"], x["label"]))
    summaries = summaries[:top_n]
    for region in summaries:
        region["brief_advice"] = build_region_brief_advice(region, confidence=confidence)
    return summaries


DIRECTION_SUFFIXES = ["东北部", "西北部", "东南部", "西南部", "东部", "西部", "南部", "北部", "中部"]


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
    return labels


def dedupe_display_labels(labels: List[dict]) -> List[dict]:
    deduped: Dict[str, dict] = {}
    for region in labels:
        key = region.get("display_label") or region.get("label")
        prev = deduped.get(key)
        if not prev:
            deduped[key] = region
            continue
        prev_score = prev.get("decision_rank_score", prev.get("final_score", 0.0)) or 0.0
        curr_score = region.get("decision_rank_score", region.get("final_score", 0.0)) or 0.0
        if curr_score > prev_score:
            deduped[key] = region
    return list(deduped.values())


def summarize_fetch_health(points: List[SamplePoint]) -> dict:
    total = len(points)
    failed = sum(1 for p in points if p.weather_source == "fetch_error")
    success = total - failed
    ratio = (failed / total) if total else 0.0
    retried = sum(1 for p in points if (p.fetch_attempts or 0) > 1)
    recovered = sum(1 for p in points if p.fetch_recovered)
    error_breakdown: Dict[str, int] = {}
    for p in points:
        if p.weather_source != "fetch_error":
            continue
        key = p.fetch_error_type or "unknown"
        error_breakdown[key] = error_breakdown.get(key, 0) + 1
    status = "ok"
    user_note = None
    if ratio >= 0.35:
        status = "degraded"
        user_note = "本轮天气数据抓取缺失偏多，结果更适合先看趋势，建议稍后再复查一次。"
    elif ratio > 0:
        status = "partial"
        user_note = "本轮有少量点位数据抓取失败，但整体结论仍可参考。"
    elif recovered > 0:
        user_note = "本轮有少量点位初次抓取失败，但已在重试后恢复。"
    return {
        "status": status,
        "total_points": total,
        "successful_points": success,
        "failed_points": failed,
        "failed_ratio": round(ratio, 3),
        "retried_points": retried,
        "recovered_points": recovered,
        "error_breakdown": error_breakdown,
        "user_note": user_note,
    }


def build_scope_meta(boxes: List[BoundingBox]) -> dict:
    provinces = sorted({b.province for b in boxes})
    coverage_boxes = [
        {
            "name": b.name,
            "province": b.province,
            "min_lat": b.min_lat,
            "max_lat": b.max_lat,
            "min_lng": b.min_lng,
            "max_lng": b.max_lng,
        }
        for b in boxes
    ]
    min_lat = min(b.min_lat for b in boxes)
    max_lat = max(b.max_lat for b in boxes)
    min_lng = min(b.min_lng for b in boxes)
    max_lng = max(b.max_lng for b in boxes)

    if len(boxes) == 1:
        area = abs((boxes[0].max_lat - boxes[0].min_lat) * (boxes[0].max_lng - boxes[0].min_lng))
        scope_mode = "point_check" if area <= 2.0 else "regional"
    elif len(provinces) >= 3:
        scope_mode = "national"
    else:
        scope_mode = "regional"

    guardrail = {"ok": True, "warnings": []}
    if scope_mode == "national":
        # Simple anti-omission guardrail: national scans should cover broad west-to-east and north-to-south extents,
        # otherwise they are likely partial national subsets masquerading as nationwide results.
        if min_lng > 90:
            guardrail["warnings"].append("national_scope_missing_far_west")
        if max_lng < 115:
            guardrail["warnings"].append("national_scope_missing_far_east_or_northeast")
        if max_lat < 43:
            guardrail["warnings"].append("national_scope_missing_northern_band")
        if min_lat > 28:
            guardrail["warnings"].append("national_scope_missing_southwestern_band")
        if len(provinces) < 5:
            guardrail["warnings"].append("national_scope_province_count_too_small")
        guardrail["ok"] = len(guardrail["warnings"]) == 0

    if scope_mode == "national" and not guardrail["ok"]:
        scope_reduction_reason = "partial_national_subset"
    else:
        scope_reduction_reason = "none"

    return {
        "scope_mode": scope_mode,
        "scope_coverage": {
            "province_count": len(provinces),
            "provinces": provinces,
            "box_count": len(boxes),
            "boxes": coverage_boxes,
            "envelope": {
                "min_lat": min_lat,
                "max_lat": max_lat,
                "min_lng": min_lng,
                "max_lng": max_lng,
            },
        },
        "scope_reduction_reason": scope_reduction_reason,
        "scope_guardrail": guardrail,
    }


def _moon_advisory(moon_interference: Optional[float]) -> str:
    """Return a human-readable stargazing advisory based on moon interference score (0-100)."""
    if moon_interference is None:
        return "月光情况未知"
    if moon_interference >= 90:
        return "月光极低，极适合拍银心"
    if moon_interference >= 70:
        return "月光较弱，可尝试拍银心"
    if moon_interference >= 50:
        return "月光中等，银心略受影响，可试星野"
    if moon_interference >= 30:
        return "月光较亮，银心难见，宜拍星野或月景"
    return "月光很强，建议以月景/星野为主"


def _wind_advisory(wind_kmh: Optional[float]) -> Optional[str]:
    """Return a tripod stability warning if wind is dangerously high."""
    if wind_kmh is None:
        return None
    if wind_kmh >= 40:
        return "风速较高（注意三脚架防风）"
    if wind_kmh >= 30:
        return "风速偏大，建议检查三脚架稳定性"
    return None


_WEATHER_CODE_MAP = {
    0: "晴",
    1: "晴",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾凇",
    51: "毛毛雨",
    53: "毛毛雨",
    55: "毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "阵雨",
    81: "中阵雨",
    82: "强阵雨",
    85: "阵雪",
    86: "强阵雪",
    95: "雷暴",
    96: "雷暴+冰雹",
    99: "雷暴+大雨+冰雹",
}


def _weather_code_advisory(codes: Optional[List[int]]) -> Optional[str]:
    """Return a human-readable weather summary from a list of weather codes."""
    if not codes:
        return None
    unique = sorted(set(codes))
    names = [_WEATHER_CODE_MAP.get(c, f"code({c})") for c in unique[:3]]
    if len(unique) == 1:
        return f"天气：{names[0]}"
    return f"天气：{'/'.join(names)}"


def _dew_point_advisory(dew_point_c: Optional[float], temp_c: Optional[float] = None) -> Optional[str]:
    """Return a condensation/dew risk note.

    Dew point close to temperature means high relative humidity and condensation risk.
    For stargazing: if dew_point close to 0°C (high altitude) -> frost risk.
    """
    if dew_point_c is None:
        return None
    if temp_c is not None:
        spread = temp_c - dew_point_c
        if spread <= 2:
            return "结露风险很高，建议带防潮布"
        if spread <= 5:
            return "露点接近气温，略防潮"
    if dew_point_c <= 0:
        return "露点低于0°C，高原夜间注意设备结霜"
    if dew_point_c <= 5:
        return "露点较低，注意镜头结雾"
    return None


def _precip_advisory(max_precip_mm: Optional[float]) -> Optional[str]:
    """Return a precipitation warning if rain/snow is expected."""
    if max_precip_mm is None:
        return None
    if max_precip_mm >= 5:
        return "有降水（注意防雨/雪）"
    if max_precip_mm >= 1:
        return "局部有弱降水"
    return None


def _cloud_base_advisory(min_cloud_base_m: Optional[float]) -> Optional[str]:
    """Return a low-cloud warning if cloud base is dangerously low for stargazing."""
    if min_cloud_base_m is None:
        return None
    if min_cloud_base_m < 200:
        return "云底极低（<200m），完全被云遮盖"
    if min_cloud_base_m < 500:
        return "云底偏低（<500m），山顶易被云遮"
    return None


def build_reference_info_note(trip_mode: bool = False, moon_advisory: Optional[str] = None, light_pollution_note: Optional[str] = None, extra_indicators: Optional[List[str]] = None) -> dict:
    used = ["云量", "风速", "湿度", "夜间通透度", "月光影响", "光污染粗估（城市距离法，非实测）"]
    if extra_indicators:
        used.extend(extra_indicators)
    omitted = ["真实视宁度", "实测光污染", "具体机位遮挡"]
    if trip_mode:
        summary = "这轮主要看云量、风速、湿度、夜间通透度和月光影响；多天模式还额外考虑了跨晚转场与路线连续性。"
        suitable = "更适合做多天区域筛选和路线判断"
    else:
        summary = "这轮主要看云量、风速、湿度、夜间通透度和月光影响。"
        suitable = "更适合做区域级筛选和判断值不值得继续细看"
    lunar_line = f"月光建议：{moon_advisory}" if moon_advisory else None
    note_parts = [f"本轮参考信息：{summary}"]
    if lunar_line:
        note_parts.append(lunar_line)
    if light_pollution_note:
        note_parts.append(f"光污染：{light_pollution_note}")
    note_parts.append(f"这次没直接查真实视宁度、实测光污染和具体机位遮挡，所以{ suitable }，不适合直接当成机位级最终结论。")
    note = " ".join(note_parts)
    short_parts = [f"主要看云量、风、湿度、通透度和月光"]
    if lunar_line:
        short_parts.append(f"{lunar_line[4:]}")
    if light_pollution_note:
        short_parts.append(f"光污染{light_pollution_note}")
    short_note = "，".join(short_parts) + "。"
    return {
        "used_weather_indicators": used,
        "not_directly_checked": omitted,
        "suitable_for": suitable,
        "summary": summary,
        "note": note,
        "short_note": short_note,
    }


def build_decision_summary(labels: List[dict], confidence: Optional[str] = None, joint: Optional[dict] = None, third_model_recheck: Optional[dict] = None, moon_advisory: Optional[str] = None, light_pollution_note: Optional[str] = None) -> dict:
    primary = labels[0] if labels else None
    backups = labels[1:3] if len(labels) > 1 else []

    # Prefer joint judgement as the final decision anchor when available.
    joint_regions = (joint or {}).get("consensus_regions", []) if joint else []
    if joint_regions:
        joint_primary = joint_regions[0]
        primary_region = joint_primary.get("display_label") or joint_primary.get("label")
        primary_advice = joint_primary.get("joint_brief_advice")
        backup_regions = [(x.get("display_label") or x.get("label")) for x in joint_regions[1:3]]
        refinement_note = joint_primary.get("refinement_note")
    else:
        primary_region = (primary.get("display_label") or primary.get("label")) if primary else None
        primary_advice = primary.get("brief_advice") if primary else None
        backup_regions = [(x.get("display_label") or x.get("label")) for x in backups]
        refinement_note = primary.get("refinement_note") if primary else None

    reference_info = build_reference_info_note(trip_mode=False, moon_advisory=moon_advisory, light_pollution_note=light_pollution_note)
    summary = {
        "primary_region": primary_region,
        "primary_advice": primary_advice,
        "backup_regions": backup_regions,
        "confidence_note": _confidence_phrase(confidence),
        "risk_note": None,
        "third_model_note": None,
        "joint_note": None,
        "refinement_note": refinement_note,
        "reference_info": reference_info,
        "reference_note": reference_info.get("note"),
        "light_pollution_note": light_pollution_note,
        "next_step_note": None,
        "one_line": None,
        "final_reply_draft": None,
        "reply_drafts": {},
    }
    if primary:
        if primary.get("cloud_stability") == "volatile":
            summary["risk_note"] = "云量波动偏大，稳定性一般"
        elif primary.get("longest_usable_streak_hours") is not None and primary.get("longest_usable_streak_hours") < 3:
            summary["risk_note"] = "连续可拍窗口偏短"

    if primary_region:
        if not refinement_note:
            refinement_note = f"大方向先看 {primary_region}；如果继续收窄，我可以再往里细看更具体的守候区域和时段。"
            summary["refinement_note"] = refinement_note
        if refinement_note:
            summary["next_step_note"] = f"如果你要继续细筛，我可以在 {primary_region} 这一带进一步收窄到更偏哪一侧、哪几个落点更值得优先守候。"
        else:
            summary["next_step_note"] = f"如果你要继续细筛，我可以接着把 {primary_region} 这一带再收窄到更具体的区域和守候时段。"
    if joint and joint.get("top_joint_advice"):
        summary["joint_note"] = joint.get("top_joint_advice")
    joint_summary = (joint or {}).get("summary") or {}
    if joint_summary.get("stability_note"):
        summary["model_stability_level"] = joint_summary.get("stability_level")
        summary["model_stability_note"] = joint_summary.get("stability_note")
    if third_model_recheck and third_model_recheck.get("enabled"):
        if third_model_recheck.get("triggered"):
            summary["third_model_note"] = f"已触发 {third_model_recheck.get('requested_model')} 复核"
        else:
            summary["third_model_note"] = f"未触发 {third_model_recheck.get('requested_model')} 复核"

    primary_region = summary.get("primary_region")
    primary_advice = summary.get("primary_advice")
    confidence_note = summary.get("confidence_note")
    risk_note = summary.get("risk_note")
    joint_note = summary.get("joint_note")
    third_note = summary.get("third_model_note")
    refinement_note = summary.get("refinement_note")
    backup_regions = summary.get("backup_regions") or []
    model_stability_note = summary.get("model_stability_note")
    reference_note = summary.get("reference_note")
    next_step_note = summary.get("next_step_note")

    if primary_region and primary_advice:
        summary["one_line"] = f"当前优先关注 {primary_region}。"

    reply_lines = []
    if primary_advice:
        reply_lines.append(f"结论：{primary_advice}")
    elif primary_region:
        reply_lines.append(f"结论：当前优先关注 {primary_region}。")

    if backup_regions:
        reply_lines.append(f"备选：{ '、'.join(backup_regions) }")
    if joint_note and joint_note != primary_advice:
        reply_lines.append(f"联合判断：{joint_note}")
    if model_stability_note:
        reply_lines.append(f"模型情况：{model_stability_note}")
    if risk_note:
        reply_lines.append(f"风险：{risk_note}")
    if refinement_note:
        reply_lines.append(f"细化说明：{refinement_note}")
    if confidence_note and (not primary_advice or confidence_note not in primary_advice):
        reply_lines.append(f"置信度：{confidence_note}")
    if third_note:
        reply_lines.append(f"复核：{third_note}")
    if reference_note:
        reply_lines.append(reference_note)
    if next_step_note:
        reply_lines.append(f"下一步：{next_step_note}")

    if reply_lines:
        summary["final_reply_draft"] = "\n".join(reply_lines)

    concise_parts = []
    if primary_region and not refinement_note:
        concise_parts.append(f"优先关注 {primary_region}")
    if risk_note:
        concise_parts.append(f"风险：{risk_note}")
    if refinement_note:
        concise_parts.append(refinement_note)
    if confidence_note:
        concise_parts.append(confidence_note)
    if concise_parts:
        concise = "；".join(part.rstrip('。') for part in concise_parts if part)
        short_reference_note = (summary.get("reference_info") or {}).get("short_note")
        if short_reference_note:
            concise += f"；{short_reference_note.rstrip('。')}"
        summary["reply_drafts"]["concise"] = concise + "。"

    standard_parts = []
    if primary_advice:
        standard_parts.append(f"结论：{primary_advice}")
    if joint_note and joint_note != primary_advice:
        standard_parts.append(f"联合判断：{joint_note}")
    if refinement_note:
        standard_parts.append(f"细化说明：{refinement_note}")
    if confidence_note and (not primary_advice or confidence_note not in primary_advice):
        standard_parts.append(f"置信度：{confidence_note}")
    if model_stability_note:
        standard_parts.append(f"模型情况：{model_stability_note}")
    if reference_note:
        standard_parts.append(reference_note)
    if next_step_note:
        standard_parts.append(f"下一步：{next_step_note}")
    if standard_parts:
        summary["reply_drafts"]["standard"] = "\n".join(standard_parts)

    if summary.get("final_reply_draft"):
        summary["reply_drafts"]["detailed"] = summary["final_reply_draft"]
    return summary


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Dynamic sampling prototype for go-stargazing")
    p.add_argument("--mode", choices=["stargazing", "moon"], default="stargazing")
    p.add_argument("--target-count", type=int, default=8, help="Target samples per box")
    p.add_argument("--dedupe-km", type=float, default=60.0, help="Cross-province dedupe distance")
    p.add_argument("--cluster-km", type=float, default=120.0, help="Cluster radius for natural regional labels")
    p.add_argument("--cloud-gap", type=float, default=8.0, help="Max cloud-cover gap for dedupe merge")
    p.add_argument("--real-weather", action="store_true", help="Fetch real weather from Open-Meteo instead of mock values")
    p.add_argument("--target-datetime", help="ISO datetime like 2026-03-27T20:00:00")
    p.add_argument("--trip-start-date", help="Start date for multi-day trip planning, e.g. 2026-04-04")
    p.add_argument("--trip-days", type=int, default=0, help="Number of nights for trip planning mode")
    p.add_argument("--trip-top-n", type=int, default=3, help="Top route plans to return in trip planning mode")
    p.add_argument("--trip-mode", choices=["quick", "standard", "deep"], default="standard", help="Execution intensity for trip planning")
    p.add_argument("--timezone", default="Asia/Shanghai", help="Timezone for Open-Meteo hourly response")
    p.add_argument("--boxes-json", help="JSON array of bounding boxes")
    p.add_argument("--scope-preset", choices=["national"], help="Use a built-in canonical scope preset when no explicit boxes are supplied")
    p.add_argument("--polygons-json", help="GeoJSON/JSON string for polygon filtering")
    p.add_argument("--polygons-file", help="Path to GeoJSON/JSON file for polygon filtering")
    p.add_argument("--max-workers", type=int, default=4, help="Max concurrent weather fetches")
    p.add_argument("--max-stage2-points", type=int, default=12, help="Budget cap for stage2 scoring points")
    p.add_argument("--direct-stage2-threshold", type=int, default=10, help="If coarse survivors <= this threshold, refine all of them directly")
    p.add_argument("--top-n", type=int, default=3, help="Max number of output regions")
    p.add_argument("--model", choices=["best_match", "gfs_global", "gfs_seamless", "icon_global", "ecmwf_ifs"], default="best_match", help="Weather model route to use. best_match = Open-Meteo default")
    p.add_argument("--compare-models", nargs="+", choices=["gfs_global", "gfs_seamless", "icon_global", "ecmwf_ifs"], help="Run the full query once per listed model and return a comparison payload")
    p.add_argument("--auto-third-model", choices=["icon_global"], help="If initial dual-model result is disputed / single-model-heavy, auto-run a third model for recheck")
    p.add_argument("--strict-national-scope", action="store_true", help="When scope_mode resolves to national, fail fast if coverage looks like a partial national subset")
    p.add_argument("--pretty", action="store_true")
    return p


def check_date_availability(target_dt: datetime) -> Tuple[bool, Optional[datetime]]:
    """Check if Open-Meteo can serve hourly data for the target night.
    We need target date + next date because the night window spans past midnight.
    Returns (is_available, latest_available_date).
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    latest = today + timedelta(days=OPEN_METEO_HOURLY_WINDOW_DAYS)
    required_end = target_dt + timedelta(days=1)
    is_available = required_end <= latest
    return is_available, latest


def _judgement_bucket(score: float) -> str:
    if score >= 75:
        return "strong"
    if score >= 60:
        return "candidate"
    return "reject"


def build_joint_brief_advice(region: dict, confidence: Optional[str] = None) -> str:
    label = region.get("display_label") or region.get("label", "该区域")
    judgement = region.get("judgement")
    spread = region.get("score_spread") or 0.0
    dispute_type = region.get("dispute_type")
    conf_phrase = _confidence_phrase(confidence)
    suffix = f"（{conf_phrase}）" if conf_phrase else ""
    model_phrase = "多模型" if (region.get("model_coverage") or 0) >= 3 else "双模型"
    if judgement == "共识推荐":
        return f"{model_phrase}都比较支持 {label}；这晚可以优先关注{suffix}。"
    if judgement == "单模型亮点":
        return f"{label} 目前主要是单个模型更看好；可以继续盯着看，但别只凭这一轮就拍板{suffix}。"
    if judgement == "备选":
        return f"{label} 可以先留在备选名单里；模型看法还没完全站到一边，出发前最好再复查一次{suffix}。"
    if judgement == "争议区":
        if dispute_type == "强分歧区":
            return f"{label} 这轮分歧比较大（模型差异约 {spread:.1f} 分）；先别急着拍板{suffix}。"
        if dispute_type == "单模型乐观区":
            return f"{label} 更像是部分模型偏乐观；还需要更多复核，先别急着定{suffix}。"
        if dispute_type == "窗口不稳区":
            return f"{label} 虽然不是完全没机会，但整晚不够稳，更适合先观察{suffix}。"
        return f"{label} 这轮模型看法分歧不小（差异约 {spread:.1f} 分）；暂时不建议直接拍板{suffix}。"
    return f"{label} 这轮不建议优先考虑{suffix}。"


def build_joint_judgement(model_results: Dict[str, dict], confidence: Optional[str] = None) -> dict:
    """Merge multiple model outputs into one consensus judgement.
    Heuristic: key by region label, compare scores/clouds across models.
    """
    by_label: Dict[str, dict] = {}
    for model_name, result in model_results.items():
        for region in result.get("region_labels", []):
            label = region.get("display_label") or region["label"]
            entry = by_label.setdefault(label, {
                "label": label,
                "display_label": region.get("display_label") or region.get("label"),
                "anchor_label": region.get("anchor_label"),
                "refined_label": region.get("refined_label") or region.get("label"),
                "refinement_note": region.get("refinement_note"),
                "provinces": region.get("provinces", []),
                "per_model": {},
            })
            entry["per_model"][model_name] = {
                "score": region.get("final_score"),
                "night_avg_cloud": region.get("night_avg_cloud"),
                "night_worst_cloud": region.get("night_worst_cloud"),
                "moon_interference": region.get("moon_interference"),
                "usable_hours": region.get("usable_hours"),
                "longest_usable_streak_hours": region.get("longest_usable_streak_hours"),
                "cloud_stability": region.get("cloud_stability"),
                "qualification": region.get("qualification"),
                "human_view": build_region_human_view({
                    "usable_hours": region.get("usable_hours"),
                    "longest_usable_streak_hours": region.get("longest_usable_streak_hours"),
                    "night_avg_cloud": region.get("night_avg_cloud"),
                    "night_worst_cloud": region.get("night_worst_cloud"),
                    "moon_interference": region.get("moon_interference"),
                    "cloud_stability": region.get("cloud_stability"),
                    "qualification": region.get("qualification"),
                }),
            }

    consensus = []
    for label, entry in by_label.items():
        model_scores = [v["score"] for v in entry["per_model"].values() if v.get("score") is not None]
        model_clouds = [v["night_avg_cloud"] for v in entry["per_model"].values() if v.get("night_avg_cloud") is not None]
        if not model_scores:
            continue
        min_score = min(model_scores)
        max_score = max(model_scores)
        avg_score = round(sum(model_scores) / len(model_scores), 2)
        score_spread = round(max_score - min_score, 2)
        avg_cloud = round(sum(model_clouds) / len(model_clouds), 1) if model_clouds else None

        buckets = [_judgement_bucket(s) for s in model_scores]
        model_coverage = len(entry["per_model"])
        dispute_type = None
        usable_vals = [v.get("usable_hours") for v in entry["per_model"].values() if v.get("usable_hours") is not None]
        stability_flags = [v.get("cloud_stability") for v in entry["per_model"].values() if v.get("cloud_stability")]
        qualifications = [v.get("qualification") for v in entry["per_model"].values() if v.get("qualification")]
        has_volatile = any(x == "volatile" for x in stability_flags)
        has_recommended = any(q == "recommended" for q in qualifications)
        all_recommended = qualifications and all(q == "recommended" for q in qualifications)
        all_backup_or_better = qualifications and all(q in {"recommended", "backup"} for q in qualifications)
        has_observe_only = any(q == "observe_only" for q in qualifications)
        if model_coverage >= 2:
            strong_count = sum(1 for b in buckets if b == "strong")
            candidate_count = sum(1 for b in buckets if b == "candidate")
            reject_count = sum(1 for b in buckets if b == "reject")
            recommended_count = sum(1 for q in qualifications if q == "recommended")
            if all(b == "strong" for b in buckets) and score_spread <= 10 and all_recommended:
                judgement = "共识推荐"
            elif model_coverage >= 3 and strong_count >= 2 and reject_count == 0 and recommended_count >= 2 and score_spread <= 15:
                judgement = "共识推荐"
            elif model_coverage >= 3 and (strong_count + candidate_count) >= 2 and reject_count <= 1 and all_backup_or_better:
                judgement = "备选"
            elif strong_count == 1 and reject_count == 0:
                judgement = "争议区"
                dispute_type = "单模型乐观区"
            elif has_observe_only or ((usable_vals and max(usable_vals) >= 3 and min(usable_vals) < 3) or has_volatile):
                judgement = "争议区"
                dispute_type = "窗口不稳区"
            elif score_spread >= 20 or any(b == "reject" for b in buckets):
                judgement = "争议区"
                dispute_type = "强分歧区"
            elif any(b == "strong" for b in buckets) and all_backup_or_better:
                judgement = "备选"
            elif all_backup_or_better:
                judgement = "备选"
            else:
                judgement = "不建议"
            evidence_type = "dual_model" if model_coverage == 2 else "multi_model"
        else:
            if all(b == "strong" for b in buckets) and has_recommended:
                judgement = "单模型亮点"
            elif any(b == "strong" for b in buckets) and not has_observe_only:
                judgement = "单模型亮点"
            elif any(b == "candidate" for b in buckets) and not has_observe_only:
                judgement = "备选"
            else:
                judgement = "不建议"
            evidence_type = "single_model"

        row = {
            "label": label,
            "display_label": entry.get("display_label") or label,
            "anchor_label": entry.get("anchor_label"),
            "refined_label": entry.get("refined_label") or label,
            "refinement_note": entry.get("refinement_note"),
            "provinces": entry.get("provinces", []),
            "judgement": judgement,
            "dispute_type": dispute_type,
            "evidence_type": evidence_type,
            "model_coverage": model_coverage,
            "avg_score": avg_score,
            "score_spread": score_spread,
            "avg_night_cloud": avg_cloud,
            "per_model": entry["per_model"],
        }
        decision_rank_score = avg_score
        if judgement == "共识推荐":
            decision_rank_score += 10
        elif judgement == "备选":
            decision_rank_score += 2
        elif judgement == "单模型亮点":
            # Fortune explicitly wanted stronger suppression of raw-score spikes that
            # only come from one model.
            decision_rank_score -= 12
        elif judgement == "争议区":
            if dispute_type == "强分歧区":
                decision_rank_score -= 16
            elif dispute_type == "单模型乐观区":
                decision_rank_score -= 12
            elif dispute_type == "窗口不稳区":
                decision_rank_score -= 10
        elif judgement == "不建议":
            decision_rank_score -= 20
        row["decision_rank_score"] = round(decision_rank_score, 2)
        row["human_view"] = build_region_human_view(row)
        row["joint_brief_advice"] = build_joint_brief_advice(row, confidence=confidence)
        consensus.append(row)

    rank = {"共识推荐": 0, "备选": 1, "单模型亮点": 2, "争议区": 3, "不建议": 4}
    consensus.sort(key=lambda x: (rank.get(x["judgement"], 9), -x["decision_rank_score"], -x["avg_score"], x["score_spread"], x["label"]))
    top_joint_advice = consensus[0].get("joint_brief_advice") if consensus else None
    summary = {
        "consensus_count": sum(1 for x in consensus if x["judgement"] == "共识推荐"),
        "single_model_count": sum(1 for x in consensus if x["judgement"] == "单模型亮点"),
        "candidate_count": sum(1 for x in consensus if x["judgement"] == "备选"),
        "disputed_count": sum(1 for x in consensus if x["judgement"] == "争议区"),
        "reject_count": sum(1 for x in consensus if x["judgement"] == "不建议"),
    }
    stability_level, stability_note = _joint_stability_level(summary)
    summary["stability_level"] = stability_level
    summary["stability_note"] = stability_note
    return {
        "summary": summary,
        "top_joint_advice": top_joint_advice,
        "consensus_regions": consensus,
    }


def _distance_penalty_km(distance_km_value: float) -> float:
    if distance_km_value < 150:
        return 0.0
    if distance_km_value < 350:
        return 6.0
    if distance_km_value < 700:
        return 14.0
    if distance_km_value < 1200:
        return 28.0
    return 60.0


def _continuity_bonus(prev_region: dict, curr_region: dict, distance_km_value: float) -> float:
    prev_provs = set(prev_region.get("provinces") or [])
    curr_provs = set(curr_region.get("provinces") or [])
    if prev_region.get("display_label") == curr_region.get("display_label"):
        return 10.0
    if prev_provs & curr_provs:
        return 6.0
    if distance_km_value < 150:
        return 8.0
    if distance_km_value < 350:
        return 4.0
    return 0.0


def _route_anchor_bonus(region: dict) -> float:
    anchor = region.get("route_anchor_strength")
    support = region.get("adjacent_night_support")
    if anchor == "strong":
        return 10.0
    if anchor == "medium":
        return 4.0
    if support == "weak":
        return -6.0
    return 0.0


def _joint_stability_level(summary: dict) -> tuple:
    disputed = summary.get("disputed_count", 0)
    single_model = summary.get("single_model_count", 0)
    consensus = summary.get("consensus_count", 0)
    candidates = summary.get("candidate_count", 0)
    if disputed == 0 and single_model == 0 and consensus > 0:
        return ("stable", "模型整体比较一致，这轮结果相对更稳。")
    if disputed <= 1 and single_model <= 1 and (consensus > 0 or candidates > 0):
        return ("mixed", "模型大方向接近，但细节还没完全站到一边，临近出发建议再复查一次。")
    return ("unstable", "模型分歧偏大，这轮更适合先观察，不建议太早拍板。")


def tune_trip_args(args) -> argparse.Namespace:
    tuned = argparse.Namespace(**vars(args))
    mode = getattr(args, "trip_mode", "standard") or "standard"
    multi_day_direct_threshold = max(args.direct_stage2_threshold, 20)
    if mode == "quick":
        tuned.target_count = min(args.target_count, 3)
        tuned.top_n = min(args.top_n, 3)
        tuned.max_stage2_points = min(args.max_stage2_points, 8)
        tuned.direct_stage2_threshold = multi_day_direct_threshold
        tuned.max_workers = min(args.max_workers, 3)
        tuned.compare_models = None
        tuned.auto_third_model = None
        tuned.model = "best_match"
    elif mode == "standard":
        tuned.target_count = min(args.target_count, 4)
        tuned.top_n = min(args.top_n, 4)
        tuned.max_stage2_points = min(args.max_stage2_points, 12)
        tuned.direct_stage2_threshold = multi_day_direct_threshold
        tuned.max_workers = min(args.max_workers, 4)
        tuned.auto_third_model = None
        if tuned.compare_models:
            tuned.compare_models = list(tuned.compare_models)[:2]
        else:
            tuned.model = "best_match"
    else:  # deep
        tuned.direct_stage2_threshold = multi_day_direct_threshold
        tuned.max_workers = min(args.max_workers, 6)
        if tuned.compare_models:
            tuned.compare_models = list(tuned.compare_models)
    return tuned


def _region_score(region: Optional[dict]) -> float:
    if not region:
        return 0.0
    return float(region.get("decision_rank_score") or region.get("final_score") or 0.0)


def _select_daily_candidate_pool(labels: List[dict], limit: int = 10, min_score: float = 70.0, relative_drop: float = 10.0) -> List[dict]:
    if not labels:
        return []
    ordered = sorted(labels, key=lambda x: (-_region_score(x), -(x.get("final_score") or 0.0), x.get("display_label") or x.get("label") or ""))
    top_score = _region_score(ordered[0])
    threshold = max(min_score, top_score - relative_drop)
    selected = [x for x in ordered if _region_score(x) >= threshold]
    if not selected:
        selected = ordered[:1]
    return selected[:limit]


def _best_route_region(day_payload: dict) -> Optional[dict]:
    regions = day_payload.get("daily_candidate_regions") or day_payload.get("route_candidate_regions") or day_payload.get("region_labels") or []
    if not regions:
        return None
    return regions[0]


def _best_adjacent_match_score(region: dict, other_day_payload: dict) -> tuple:
    candidates = other_day_payload.get("daily_candidate_regions") or other_day_payload.get("route_candidate_regions") or other_day_payload.get("region_labels") or []
    if not candidates or region.get("lat") is None or region.get("lng") is None:
        return (0.0, None)
    best_score = 0.0
    best_match = None
    for cand in candidates[:10]:
        if cand.get("lat") is None or cand.get("lng") is None:
            continue
        dist = haversine_km(region["lat"], region["lng"], cand["lat"], cand["lng"])
        overlap = set(region.get("provinces") or []) & set(cand.get("provinces") or [])
        proximity_bonus = 18.0 if dist < 150 else 10.0 if dist < 350 else 4.0 if dist < 700 else 0.0
        overlap_bonus = 10.0 if overlap else 0.0
        cand_score = _region_score(cand) * 0.6 + proximity_bonus + overlap_bonus
        if cand_score > best_score:
            best_score = cand_score
            best_match = {
                "region": cand.get("display_label") or cand.get("label"),
                "distance_km": round(dist, 1),
                "score": round(_region_score(cand), 2),
                "shared_province": bool(overlap),
            }
    return round(best_score, 2), best_match


def annotate_daily_route_context(daily_payloads: List[dict]) -> None:
    for idx, payload in enumerate(daily_payloads):
        labels = payload.get("route_candidate_regions") or payload.get("region_labels") or []
        pool = _select_daily_candidate_pool(labels, limit=10, min_score=70.0, relative_drop=10.0)
        payload["daily_candidate_regions"] = pool
        for region in pool:
            prev_score = next_score = 0.0
            prev_match = next_match = None
            if idx > 0:
                prev_score, prev_match = _best_adjacent_match_score(region, daily_payloads[idx - 1])
            if idx < len(daily_payloads) - 1:
                next_score, next_match = _best_adjacent_match_score(region, daily_payloads[idx + 1])
            support_total = round(prev_score + next_score, 2)
            if support_total >= 125 or (prev_score >= 55 and next_score >= 55):
                support = "strong"
            elif support_total >= 65 or prev_score >= 45 or next_score >= 45:
                support = "medium"
            else:
                support = "weak"
            base_score = _region_score(region)
            if base_score >= 82 and support == "strong":
                anchor = "strong"
            elif base_score >= 70 and support in ("strong", "medium"):
                anchor = "medium"
            else:
                anchor = "weak"
            note = (
                "前后日期也有较好承接，适合当多日路线锚点。" if anchor == "strong"
                else "前后日期还有一定承接，但更适合作为备选锚点。" if anchor == "medium"
                else "更像单晚亮点，前后承接一般，不建议直接当多日主锚点。"
            )
            region["adjacent_night_support"] = support
            region["route_anchor_strength"] = anchor
            region["adjacent_support_score"] = support_total
            region["adjacent_support_detail"] = {
                "previous_night": prev_match,
                "next_night": next_match,
            }
            region["route_anchor_note"] = note
        best = pool[0] if pool else None
        if best:
            payload.setdefault("decision_summary", {})["route_anchor_strength"] = best.get("route_anchor_strength")
            payload["decision_summary"]["adjacent_night_support"] = best.get("adjacent_night_support")
            payload["decision_summary"]["route_anchor_note"] = best.get("route_anchor_note")
            payload["decision_summary"]["daily_candidate_count"] = len(pool)
            payload["decision_summary"]["daily_candidate_threshold"] = {
                "min_score": 70.0,
                "relative_drop": 10.0,
                "max_candidates": 10,
            }


def _weather_indicators_str(r: dict) -> str:
    """Build a compact weather indicators string for a region."""
    parts = []
    parts.append(f"云量均值 {r.get('night_avg_cloud', '?')}%")
    parts.append(f"云量最差 {r.get('night_worst_cloud', '?')}%")
    if r.get('cloud_stability'):
        parts.append(f"云量走势 {r.get('cloud_stability')}")
    if r.get('usable_hours') is not None:
        parts.append(f"可拍窗口 {r.get('usable_hours')}h")
    if r.get('longest_usable_streak_hours') is not None:
        parts.append(f"最长连续 {r.get('longest_usable_streak_hours')}h")
    if r.get('night_avg_wind_kmh') is not None:
        parts.append(f"风速 {r.get('night_avg_wind_kmh')} km/h")
    if r.get('night_avg_humidity') is not None:
        parts.append(f"湿度 {r.get('night_avg_humidity')}%")
    if r.get('night_avg_visibility_m') is not None:
        parts.append(f"能见度 {r.get('night_avg_visibility_m'):.0f} m")
    if r.get('night_avg_dew_point') is not None:
        parts.append(f"露点 {r.get('night_avg_dew_point')}°")
    if r.get('night_max_precip') is not None:
        parts.append(f"降水 {r.get('night_max_precip')} mm")
    if r.get('night_min_cloud_base') is not None:
        parts.append(f"云底高 {r.get('night_min_cloud_base')} m")
    if r.get('moon_interference') is not None:
        parts.append(f"月光干扰 {r.get('moon_interference')}/100")
    if r.get('light_pollution_bortle'):
        parts.append(f"光污染 {r.get('light_pollution_bortle')}")
    if r.get('avg_elevation_m') is not None:
        parts.append(f"海拔 {r.get('avg_elevation_m'):.0f} m")
    if r.get('night_weather_codes') and r.get('night_weather_codes') != []:
        parts.append(f"天气代码 {r.get('night_weather_codes')}")
    return " | ".join(parts)


def _trip_daily_brief(day_payloads: List[dict]) -> List[str]:
    lines = []
    for payload in day_payloads:
        date = (payload.get("target_datetime") or "")[:10]
        ds = payload.get("decision_summary") or {}
        region = ds.get("primary_region")
        stability = ds.get("model_stability_note")
        moon_val = None
        wind_kmh = None
        lp_note = None
        labels = payload.get("region_labels") or []
        if labels:
            moon_val = labels[0].get("moon_interference")
            wind_kmh = labels[0].get("night_avg_wind_kmh")
            lp_note = labels[0].get("light_pollution_note")
        moon_advice = _moon_advisory(moon_val) if moon_val is not None else None
        wind_advice = _wind_advisory(wind_kmh) if wind_kmh is not None else None
        parts = []
        if region:
            parts.append(f"{date}：优先看 {region}")
        if moon_advice:
            parts.append(moon_advice)
        if lp_note:
            parts.append(lp_note)
        if wind_advice:
            parts.append(wind_advice)
        if stability:
            parts.append(stability)
        if parts:
            lines.append("；".join(parts))
    return lines


def _trip_daily_brief_with_metrics(day_payloads: List[dict]) -> List[str]:
    """Enhanced per-night breakdown: primary region + weather metrics + top-N candidates."""
    lines = []
    for payload in day_payloads:
        date = (payload.get("target_datetime") or "")[:10]
        ds = payload.get("decision_summary") or {}
        candidates = payload.get("daily_candidate_regions") or []
        # Use route_candidate_regions as fallback
        if not candidates:
            candidates = payload.get("route_candidate_regions") or []
        primary = candidates[0] if candidates else {}

        region = ds.get("primary_region") or primary.get("display_label") or primary.get("label")
        score = primary.get("final_score") or primary.get("decision_rank_score")
        night_window = ""
        if primary.get("astronomical_night_start") and primary.get("astronomical_night_end"):
            night_window = f"{primary['astronomical_night_start']}-{primary['astronomical_night_end']}"

        # Header line
        header = f"📅 {date}"
        if region:
            score_str = f"（综合得分 {score:.2f}）" if score else ""
            header += f" · {region}{score_str}"
        if night_window:
            header += f" | 天文夜窗 {night_window}"
        lines.append(header)

        # Weather indicators for primary region
        if primary:
            weather_str = _weather_indicators_str(primary)
            lines.append(f"   气象指标：{weather_str}")

        # Top-N candidates (score threshold: 70, show top 10)
        threshold = ds.get("daily_candidate_threshold", {})
        min_score = threshold.get("min_score", 70.0) if threshold else 70.0
        shown = [r for r in candidates if (r.get("final_score") or r.get("decision_rank_score") or 0) >= min_score][:10]
        if len(shown) > 1:
            for i, r in enumerate(shown, 1):
                r_score = r.get("final_score") or r.get("decision_rank_score") or 0
                r_label = r.get("display_label") or r.get("label") or "?"
                cloud = r.get("night_avg_cloud")
                wind = r.get("night_avg_wind_kmh")
                wind_str = f" | 风{wind}km/h" if wind is not None else ""
                lines.append(f"   {i}. {r_label}（{r_score:.2f}分）| 云量{cloud}%{wind_str}")
        lines.append("")
    return lines



def _trip_risk_note(primary_trip: Optional[dict], daily_payloads: List[dict]) -> Optional[str]:
    if not primary_trip:
        return None
    plan_type = primary_trip.get("plan_type")
    unstable_days = []
    for payload in daily_payloads:
        ds = payload.get("decision_summary") or {}
        if ds.get("model_stability_level") == "unstable":
            unstable_days.append((payload.get("target_datetime") or "")[:10])
    if plan_type == "independent_far_line":
        return "这组日期暂时没有特别顺的连续主线，更多是在单晚高分和跨晚转场之间做取舍。"
    if unstable_days:
        if len(unstable_days) == 1:
            return f"其中 {unstable_days[0]} 这晚模型分歧偏大，建议临近出发再复查。"
        return f"其中 {len(unstable_days)} 晚模型分歧偏大，建议临近出发再复查。"
    return None


def _trip_plan_summary(primary_trip: Optional[dict]) -> tuple:
    if not primary_trip:
        return ("暂无可用路线方案。", None, None)
    regions = ' → '.join(day['region'] for day in (primary_trip.get('days') or []))
    plan_type = primary_trip.get("plan_type")
    if plan_type == "main_route":
        return (
            f"这几晚更推荐按这条主线走：{regions}。",
            "这条线更看重连续性和可执行性，不会为了某一晚单独更强，就硬拼出跨大区乱跳的路线。",
            "主方案",
        )
    if plan_type == "backup_route":
        return (
            f"这几晚更像一条可执行的备选线：{regions}。",
            "整体还能走通，但连续性还不算特别顺，更适合当备选，不建议直接当唯一方案。",
            "备选方案",
        )
    if plan_type == "independent_far_line":
        return (
            f"这几晚暂时没有特别顺的连续主线；如果你更在意单晚高分，可以单独参考这条远线方案：{regions}。",
            "这条线更像追单晚条件的远线方案，不适合包装成常规主路线。",
            "远线方案",
        )
    return ("暂无可用路线方案。", None, None)


def build_trip_plans(daily_payloads: List[dict], trip_top_n: int = 3) -> List[dict]:
    candidate_days: List[List[dict]] = []
    for day in daily_payloads:
        labels = day.get("daily_candidate_regions") or day.get("route_candidate_regions") or day.get("region_labels") or []
        usable = [x for x in labels if x.get("lat") is not None and x.get("lng") is not None]
        candidate_days.append(usable[:10])
    if not candidate_days or any(not day for day in candidate_days):
        return []

    plans = []
    for combo in itertools.product(*candidate_days):
        weather_score_total = round(sum((x.get("decision_rank_score") or x.get("final_score") or 0.0) for x in combo), 2)
        travel_penalty_total = 0.0
        continuity_bonus_total = 0.0
        anchor_bonus_total = 0.0
        weak_anchor_count = 0
        segments = []
        long_jump = False
        max_segment_distance = 0.0
        for region in combo:
            anchor_bonus = _route_anchor_bonus(region)
            anchor_bonus_total += anchor_bonus
            if region.get("route_anchor_strength") == "weak":
                weak_anchor_count += 1
        for prev_region, curr_region in zip(combo, combo[1:]):
            distance_km_value = round(haversine_km(prev_region["lat"], prev_region["lng"], curr_region["lat"], curr_region["lng"]), 1)
            penalty = _distance_penalty_km(distance_km_value)
            bonus = _continuity_bonus(prev_region, curr_region, distance_km_value)
            travel_penalty_total += penalty
            continuity_bonus_total += bonus
            max_segment_distance = max(max_segment_distance, distance_km_value)
            if distance_km_value > 1200:
                long_jump = True
            segments.append({
                "from": prev_region.get("display_label") or prev_region.get("label"),
                "to": curr_region.get("display_label") or curr_region.get("label"),
                "distance_km": distance_km_value,
                "travel_penalty": penalty,
                "continuity_bonus": bonus,
            })
        if max_segment_distance > 1200:
            travel_penalty_total += 40.0
        elif max_segment_distance > 700:
            travel_penalty_total += 18.0
        if weak_anchor_count >= max(1, len(combo) - 1):
            travel_penalty_total += 16.0
        trip_score = round(weather_score_total - travel_penalty_total + continuity_bonus_total + anchor_bonus_total, 2)
        if max_segment_distance <= 350 and weak_anchor_count == 0:
            continuity_level = "high"
        elif max_segment_distance <= 700 and weak_anchor_count <= 1:
            continuity_level = "medium"
        else:
            continuity_level = "low"
        plan_type = "independent_far_line" if long_jump or max_segment_distance > 700 else ("main_route" if continuity_level == "high" else "backup_route")
        plans.append({
            "trip_score": trip_score,
            "weather_score_total": weather_score_total,
            "travel_penalty_total": round(travel_penalty_total, 2),
            "continuity_bonus_total": round(continuity_bonus_total, 2),
            "anchor_bonus_total": round(anchor_bonus_total, 2),
            "weak_anchor_count": weak_anchor_count,
            "continuity_level": continuity_level,
            "max_segment_distance_km": round(max_segment_distance, 1),
            "plan_type": plan_type,
            "days": [
                {
                    "date": day.get("target_datetime", "")[:10],
                    "region": region.get("display_label") or region.get("label"),
                    "refinement_note": region.get("refinement_note"),
                    "score": round(region.get("decision_rank_score") or region.get("final_score") or 0.0, 2),
                    "route_anchor_strength": region.get("route_anchor_strength"),
                    "route_anchor_note": region.get("route_anchor_note"),
                    "lat": region.get("lat"),
                    "lng": region.get("lng"),
                }
                for day, region in zip(daily_payloads, combo)
            ],
            "segments": segments,
            "why": (
                "这条路线连续性最好，前后日期也更容易衔接，适合作为多日主方案"
                if not long_jump and continuity_level == "high"
                else (
                    "天气还可以，但有一两晚更像单晚亮点，连续走法不如主方案稳"
                    if not long_jump and continuity_level == "medium"
                    else ("虽然个别晚上有吸引力，但跨晚跳跃偏大，更适合作为独立远线方案" if long_jump else "有明显跳跃或断档，更适合作为备选，不建议当主路线")
                )
            ),
        })
    plans.sort(key=lambda x: (0 if x["plan_type"] == "main_route" else (1 if x["plan_type"] == "backup_route" else 2), -x["trip_score"]))
    deduped = []
    seen = set()
    for plan in plans:
        key = tuple(day["region"] for day in plan["days"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(plan)
        if len(deduped) >= trip_top_n:
            break
    return deduped


def build_daily_payload(args, boxes: List[BoundingBox], province_polygons, prefecture_polygons, county_polygons, target_dt: datetime, confidence: str) -> dict:
    if args.compare_models:
        compare_started = time.perf_counter()
        scope_meta = build_scope_meta(boxes)
        comparison = {
            "comparison_target_datetime": target_dt.isoformat(),
            "target_datetime": target_dt.isoformat(),
            "forecast_confidence": confidence,
            "scope_mode": scope_meta["scope_mode"],
            "scope_coverage": scope_meta["scope_coverage"],
            "scope_reduction_reason": scope_meta["scope_reduction_reason"],
            "scope_guardrail": scope_meta["scope_guardrail"],
            "compare_models": args.compare_models,
            "model_results": {},
            "fetch_health": None,
        }
        for model_name in args.compare_models:
            comparison["model_results"][model_name] = run_pipeline(args, boxes, province_polygons, prefecture_polygons, county_polygons, target_dt, confidence, model=model_name)
        comparison["joint_judgement"] = build_joint_judgement(comparison["model_results"], confidence=confidence)

        if args.auto_third_model and args.auto_third_model not in comparison["model_results"]:
            summary = comparison["joint_judgement"].get("summary", {})
            should_rerun = summary.get("disputed_count", 0) > 0 or summary.get("single_model_count", 0) > 0
            comparison["third_model_recheck"] = {
                "enabled": True,
                "requested_model": args.auto_third_model,
                "triggered": should_rerun,
                "reason": "initial_dual_model_disputed_or_single_model_heavy" if should_rerun else "initial_dual_model_already_stable",
            }
            if should_rerun:
                comparison["model_results"][args.auto_third_model] = run_pipeline(
                    args, boxes, province_polygons, prefecture_polygons, county_polygons, target_dt, confidence, model=args.auto_third_model
                )
                comparison["joint_judgement"] = build_joint_judgement(comparison["model_results"], confidence=confidence)
                comparison["compare_models"] = list(comparison["model_results"].keys())

        fetch_rows = [v.get("fetch_health") for v in comparison["model_results"].values() if v.get("fetch_health")]
        if fetch_rows:
            total_points = sum(x.get("total_points", 0) for x in fetch_rows)
            successful_points = sum(x.get("successful_points", 0) for x in fetch_rows)
            failed_points = sum(x.get("failed_points", 0) for x in fetch_rows)
            retried_points = sum(x.get("retried_points", 0) for x in fetch_rows)
            recovered_points = sum(x.get("recovered_points", 0) for x in fetch_rows)
            failed_ratio = (failed_points / total_points) if total_points else 0.0
            error_breakdown: Dict[str, int] = {}
            for row in fetch_rows:
                for key, value in (row.get("error_breakdown") or {}).items():
                    error_breakdown[key] = error_breakdown.get(key, 0) + value
            user_note = None
            if failed_ratio > 0:
                user_note = "本轮有部分模型查询出现抓取缺失，结论可参考，但更建议临近出发前再复查。"
            elif recovered_points > 0:
                user_note = "本轮有少量点位初次抓取失败，但已在重试后恢复。"
            comparison["fetch_health"] = {
                "status": "degraded" if failed_ratio >= 0.35 else ("partial" if failed_ratio > 0 else "ok"),
                "total_points": total_points,
                "successful_points": successful_points,
                "failed_points": failed_points,
                "failed_ratio": round(failed_ratio, 3),
                "retried_points": retried_points,
                "recovered_points": recovered_points,
                "error_breakdown": error_breakdown,
                "user_note": user_note,
            }

        first_model_key = next(iter(comparison["model_results"].keys())) if comparison["model_results"] else None
        first_labels = comparison["model_results"].get(first_model_key, {}).get("region_labels", []) if first_model_key else []
        if not first_labels:
            first_labels = []
            for row in comparison.get("joint_judgement", {}).get("consensus_regions", [])[:3]:
                first_labels.append({
                    "label": row.get("label"),
                    "display_label": row.get("display_label") or row.get("label"),
                    "brief_advice": row.get("joint_brief_advice"),
                    "cloud_stability": None,
                    "longest_usable_streak_hours": None,
                    "refinement_note": row.get("refinement_note"),
                })
        comparison["route_candidate_regions"] = first_labels
        comparison_lunar_advisory = None
        comparison_lp_note = None
        if first_labels:
            moon_val = first_labels[0].get("moon_interference")
            if moon_val is not None:
                comparison_lunar_advisory = _moon_advisory(moon_val)
            comparison_lp_note = first_labels[0].get("light_pollution_note")
        comparison["decision_summary"] = build_decision_summary(
            first_labels,
            confidence=confidence,
            joint=comparison.get("joint_judgement"),
            third_model_recheck=comparison.get("third_model_recheck"),
            moon_advisory=comparison_lunar_advisory,
            light_pollution_note=comparison_lp_note,
        )
        if comparison.get("fetch_health", {}).get("user_note"):
            note = comparison["fetch_health"]["user_note"]
            comparison["decision_summary"]["data_quality_note"] = note
            if comparison["decision_summary"].get("final_reply_draft"):
                comparison["decision_summary"]["final_reply_draft"] += f"\n数据完整性：{note}"
            if comparison["decision_summary"]["reply_drafts"].get("concise"):
                clean_note = str(note).rstrip("。")
                comparison["decision_summary"]["reply_drafts"]["concise"] = comparison["decision_summary"]["reply_drafts"]["concise"].rstrip("。") + f"；{clean_note}。"
            if comparison["decision_summary"]["reply_drafts"].get("standard"):
                comparison["decision_summary"]["reply_drafts"]["standard"] += f"\n数据完整性：{note}"
            if comparison["decision_summary"].get("final_reply_draft"):
                comparison["decision_summary"]["reply_drafts"]["detailed"] = comparison["decision_summary"]["final_reply_draft"]

        total_ms = round((time.perf_counter() - compare_started) * 1000, 1)
        comparison["timing"] = {
            "elapsed_ms": total_ms,
            "elapsed_seconds": round(total_ms / 1000.0, 2),
            "per_model_seconds": {
                k: v.get("timing", {}).get("elapsed_seconds") for k, v in comparison["model_results"].items()
            },
        }
        return comparison

    payload = run_pipeline(args, boxes, province_polygons, prefecture_polygons, county_polygons, target_dt, confidence, model=args.model)
    payload["route_candidate_regions"] = payload.get("region_labels", [])
    return payload


def run_pipeline(args, boxes: List[BoundingBox], province_polygons, prefecture_polygons, county_polygons, target_dt: datetime, confidence: str, model: Optional[str] = None) -> dict:
    """Run the full sampling → weather → score → aggregate pipeline once for a given model."""
    started_at = time.perf_counter()
    all_points: List[SamplePoint] = []
    generated_count_before_filter = 0
    for box in boxes:
        pts = generate_grid_points(box, args.target_count)
        generated_count_before_filter += len(pts)
        pts = filter_points_by_polygon(pts, province_polygons, prefecture_polygons)
        all_points.extend(pts)

    hydrate_weather(all_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model=model)
    coarse_pass = coarse_filter(all_points, args.mode)

    # Adaptive refinement: add a few local neighbor probes around the best coarse-pass points,
    # then let them compete for the stage-2 budget. This reduces the chance of missing local peaks.
    adaptive_points = generate_adaptive_refinement_points(coarse_pass, boxes)
    if adaptive_points:
        hydrate_weather(adaptive_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model=model)
        adaptive_points = coarse_filter(adaptive_points, args.mode)
        coarse_pass = coarse_pass + adaptive_points

    stage2_points = select_stage2_budget(
        coarse_pass,
        max_stage2_points=args.max_stage2_points,
        direct_stage2_threshold=args.direct_stage2_threshold,
    )
    for p in stage2_points:
        compute_final_score(p, args.mode)
    deduped = dedupe_cross_province(stage2_points, distance_km=args.dedupe_km, score_gap=args.cloud_gap)
    labels = aggregate_labels(deduped, boxes, top_n=args.top_n, cluster_km=args.cluster_km, target_date=target_dt.date(), prefecture_polygons=prefecture_polygons, county_polygons=county_polygons, confidence=confidence)

    elapsed_ms = round((time.perf_counter() - started_at) * 1000, 1)
    scope_meta = build_scope_meta(boxes)
    labels = apply_label_presentation(labels, scope_meta)
    labels = dedupe_display_labels(labels)
    labels.sort(key=lambda x: (-x["decision_rank_score"], -(x.get("final_score") or 0.0), x.get("display_label") or x["label"]))
    labels = labels[: args.top_n]
    for region in labels:
        region["brief_advice"] = build_region_brief_advice(region, confidence=confidence)
        region["human_view"] = build_region_human_view(region)
    top_region_advice = labels[0].get("brief_advice") if labels else None
    fetch_health = summarize_fetch_health(all_points + adaptive_points)
    moon_advisory = None
    lp_note = None
    if labels:
        moon_val = labels[0].get("moon_interference")
        if moon_val is not None:
            moon_advisory = _moon_advisory(moon_val)
        lp_note = labels[0].get("light_pollution_note")
    decision_summary = build_decision_summary(labels, confidence=confidence, moon_advisory=moon_advisory, light_pollution_note=lp_note)
    if fetch_health.get("user_note"):
        note = fetch_health.get("user_note")
        decision_summary["data_quality_note"] = note
        if decision_summary.get("final_reply_draft"):
            decision_summary["final_reply_draft"] += f"\n数据完整性：{note}"
        decision_summary.setdefault("reply_drafts", {})
        if decision_summary["reply_drafts"].get("concise"):
            clean_note = str(note).rstrip("。")
            decision_summary["reply_drafts"]["concise"] = decision_summary["reply_drafts"]["concise"].rstrip("。") + f"；{clean_note}。"
        if decision_summary["reply_drafts"].get("standard"):
            decision_summary["reply_drafts"]["standard"] += f"\n数据完整性：{note}"
        if decision_summary.get("final_reply_draft"):
            decision_summary["reply_drafts"]["detailed"] = decision_summary["final_reply_draft"]
    return {
        "mode": args.mode,
        "target_datetime": target_dt.isoformat(),
        "weather_model": model or "best_match",
        "forecast_confidence": confidence,
        "scope_mode": scope_meta["scope_mode"],
        "scope_coverage": scope_meta["scope_coverage"],
        "scope_reduction_reason": scope_meta["scope_reduction_reason"],
        "scope_guardrail": scope_meta["scope_guardrail"],
        "fetch_health": fetch_health,
        "decision_summary": decision_summary,
        "top_region_advice": top_region_advice,
        "timing": {
            "elapsed_ms": elapsed_ms,
            "elapsed_seconds": round(elapsed_ms / 1000.0, 2),
        },
        "confidence_note": {
            "high": "3天内：数据可靠，接近实况",
            "medium": "4-7天：预报精度有所下降，建议参考趋势",
            "low": "8-16天：预报不确定性较高，请以当天Windy等本地工具为准",
        }.get(confidence, ""),
        "budget": {"max_workers": args.max_workers, "max_stage2_points": args.max_stage2_points, "direct_stage2_threshold": args.direct_stage2_threshold, "top_n": args.top_n},
        "polygon_filtering": {
            "enabled": bool(province_polygons or prefecture_polygons),
            "province_count": len(province_polygons),
            "prefecture_count": len(prefecture_polygons),
            "generated_before_filter": generated_count_before_filter,
            "remaining_after_filter": len(all_points),
        },
        "input_boxes": [asdict(b) for b in boxes],
        "generated_points": [asdict(p) for p in all_points],
        "stage1_survivors": [asdict(p) for p in coarse_pass],
        "stage2_points": [asdict(p) for p in stage2_points],
        "deduped_survivors": [asdict(p) for p in deduped],
        "region_labels": labels,
    }


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.boxes_json:
        boxes = parse_boxes(args.boxes_json)
    elif args.scope_preset:
        boxes = load_scope_preset(args.scope_preset)
    else:
        parser.error("--boxes-json is required unless --scope-preset is provided")
    target_dt = parse_target_datetime(args.target_datetime)

    # Date availability check
    if args.real_weather:
        available, latest_dt = check_date_availability(target_dt)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_ahead = (target_dt.date() - today.date()).days
        confidence = "high" if days_ahead <= 3 else "medium" if days_ahead <= 7 else "low"
        if not available:
            print(json.dumps({
                "error": "date_out_of_range",
                "message": f"Open-Meteo 实时预报最晚只支持查询 {latest_dt.date().isoformat()}（今天起 +{OPEN_METEO_HOURLY_WINDOW_DAYS} 天）。"
                           f"你指定的日期 {target_dt.date().isoformat()} 超出范围。",
                "target_date": target_dt.date().isoformat(),
                "latest_available_date": latest_dt.date().isoformat(),
                "forecast_confidence": confidence,
                "suggestion": f"清明节（4月4日）距今超过 {OPEN_METEO_HOURLY_WINDOW_DAYS} 天，建议在 4 月 1 日之后再查询。",
            }, ensure_ascii=False), file=sys.stderr)
            return
    else:
        confidence = "mock"

    province_polygons, prefecture_polygons = load_polygons(args.polygons_json, args.polygons_file)

    scope_meta = build_scope_meta(boxes)
    if args.strict_national_scope and scope_meta["scope_mode"] == "national" and not scope_meta["scope_guardrail"]["ok"]:
        print(json.dumps({
            "error": "national_scope_guardrail_failed",
            "message": "当前 boxes 更像局部全国子集，不足以代表全国默认扫描。",
            "scope_mode": scope_meta["scope_mode"],
            "scope_coverage": scope_meta["scope_coverage"],
            "scope_reduction_reason": scope_meta["scope_reduction_reason"],
            "scope_guardrail": scope_meta["scope_guardrail"],
            "suggestion": "补全全国范围 boxes，或显式把本次查询改成 regional。",
        }, ensure_ascii=False), file=sys.stderr)
        return

    # County/banner refinement is intentionally disabled in the packaged skill.
    # We only use bundled province + prefecture GeoJSON data.
    county_polygons: Dict[str, MultiPolygon] = {}

    if args.trip_start_date and args.trip_days and args.trip_days > 1:
        start_date = datetime.fromisoformat(args.trip_start_date).date()
        base_time = target_dt.time()
        trip_args = tune_trip_args(args)
        daily_payloads = []
        for day_offset in range(args.trip_days):
            trip_dt = datetime.combine(start_date + timedelta(days=day_offset), base_time)
            if args.real_weather:
                available, latest_dt = check_date_availability(trip_dt)
                if not available:
                    print(json.dumps({
                        "error": "date_out_of_range",
                        "message": f"Open-Meteo 实时预报最晚只支持查询 {latest_dt.date().isoformat()}（今天起 +{OPEN_METEO_HOURLY_WINDOW_DAYS} 天）。",
                        "target_date": trip_dt.date().isoformat(),
                        "latest_available_date": latest_dt.date().isoformat(),
                    }, ensure_ascii=False), file=sys.stderr)
                    return
                today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                days_ahead = (trip_dt.date() - today.date()).days
                trip_confidence = "high" if days_ahead <= 3 else "medium" if days_ahead <= 7 else "low"
            else:
                trip_confidence = "mock"
            daily_payloads.append(build_daily_payload(trip_args, boxes, province_polygons, prefecture_polygons, county_polygons, trip_dt, trip_confidence))

        annotate_daily_route_context(daily_payloads)
        trip_plans = build_trip_plans(daily_payloads, trip_top_n=args.trip_top_n)
        primary_trip = trip_plans[0] if trip_plans else None
        trip_one_line, route_style_note, plan_label = _trip_plan_summary(primary_trip)
        trip_daily_lines = _trip_daily_brief_with_metrics(daily_payloads)
        trip_risk_note = _trip_risk_note(primary_trip, daily_payloads)
        trip_moon_advisory = None
        trip_lp_note = None
        if daily_payloads:
            first_ds = daily_payloads[0].get("decision_summary") or {}
            top_region = (first_ds.get("region_labels") or [{}])[0] if first_ds.get("region_labels") else {}
            moon_val = top_region.get("moon_interference")
            if moon_val is not None:
                trip_moon_advisory = _moon_advisory(moon_val)
            trip_lp_note = top_region.get("light_pollution_note")
        trip_reference_info = build_reference_info_note(trip_mode=True, moon_advisory=trip_moon_advisory, light_pollution_note=trip_lp_note)
        trip_reply_lines = [trip_one_line]
        if route_style_note:
            trip_reply_lines.append(f"说明：{route_style_note}")
        if trip_risk_note:
            trip_reply_lines.append(f"风险：{trip_risk_note}")
        trip_reply_lines.append(trip_reference_info.get("note"))
        if trip_daily_lines:
            trip_reply_lines.append("逐晚建议：")
            trip_reply_lines.extend(trip_daily_lines)
        payload = {
            "trip_mode": True,
            "trip_profile": args.trip_mode,
            "trip_start_date": args.trip_start_date,
            "trip_days": args.trip_days,
            "trip_dates": [x.get("target_datetime", "")[:10] for x in daily_payloads],
            "budget": {
                "max_workers": trip_args.max_workers,
                "max_stage2_points": trip_args.max_stage2_points,
                "direct_stage2_threshold": trip_args.direct_stage2_threshold,
                "top_n": trip_args.top_n,
                "source_direct_stage2_threshold": args.direct_stage2_threshold,
            },
            "daily_results": daily_payloads,
            "daily_best_regions": [
                {
                    "date": x.get("target_datetime", "")[:10],
                    "region": (_best_route_region(x) or {}).get("display_label") or (_best_route_region(x) or {}).get("label"),
                    "adjacent_night_support": (_best_route_region(x) or {}).get("adjacent_night_support"),
                    "route_anchor_strength": (_best_route_region(x) or {}).get("route_anchor_strength"),
                    "route_anchor_note": (_best_route_region(x) or {}).get("route_anchor_note"),
                }
                for x in daily_payloads if _best_route_region(x)
            ],
            "daily_candidate_regions": [
                {
                    "date": x.get("target_datetime", "")[:10],
                    "threshold": x.get("decision_summary", {}).get("daily_candidate_threshold"),
                    "count": len(x.get("daily_candidate_regions") or []),
                    "candidates": [
                        {
                            "region": row.get("display_label") or row.get("label"),
                            "score": round(_region_score(row), 2),
                            "night_avg_cloud": row.get("night_avg_cloud"),
                            "night_worst_cloud": row.get("night_worst_cloud"),
                            "cloud_stability": row.get("cloud_stability"),
                            "usable_hours": row.get("usable_hours"),
                            "longest_usable_streak_hours": row.get("longest_usable_streak_hours"),
                            "night_avg_wind_kmh": row.get("night_avg_wind_kmh"),
                            "night_avg_humidity": row.get("night_avg_humidity"),
                            "night_avg_visibility_m": row.get("night_avg_visibility_m"),
                            "night_avg_dew_point": row.get("night_avg_dew_point"),
                            "night_max_precip": row.get("night_max_precip"),
                            "night_min_cloud_base": row.get("night_min_cloud_base"),
                            "moon_interference": row.get("moon_interference"),
                            "light_pollution_bortle": row.get("light_pollution_bortle"),
                            "avg_elevation_m": row.get("avg_elevation_m"),
                            "night_weather_codes": row.get("night_weather_codes"),
                            "adjacent_night_support": row.get("adjacent_night_support"),
                            "route_anchor_strength": row.get("route_anchor_strength"),
                            "route_anchor_note": row.get("route_anchor_note"),
                        }
                        for row in (x.get("daily_candidate_regions") or [])
                    ],
                }
                for x in daily_payloads
            ],
            "trip_plans": trip_plans,
            "decision_summary": {
                "primary_route": primary_trip,
                "backup_routes": trip_plans[1:] if len(trip_plans) > 1 else [],
                "plan_label": plan_label,
                "trip_refine_note": "这次多天路线规划会把更多候选区域一起保留下来，避免只看单晚第一名，结果把能连起来走的方案过早裁掉。",
                "route_style_note": route_style_note,
                "risk_note": trip_risk_note,
                "reference_info": trip_reference_info,
                "reference_note": trip_reference_info.get("note"),
                "light_pollution_note": trip_lp_note,
                "daily_brief": trip_daily_lines,
                "one_line": trip_one_line,
                "final_reply_draft": "\n".join(trip_reply_lines),
                "reply_drafts": {
                    "concise": trip_one_line,
                    "standard": "\n".join(trip_reply_lines[:4]) if len(trip_reply_lines) >= 4 else "\n".join(trip_reply_lines),
                    "detailed": "\n".join(trip_reply_lines),
                },
            },
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
        return

    payload = build_daily_payload(args, boxes, province_polygons, prefecture_polygons, county_polygons, target_dt, confidence)
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
