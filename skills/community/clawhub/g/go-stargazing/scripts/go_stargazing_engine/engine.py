import argparse
import copy
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple



NA_STR = "NA"
from .advisories import _moon_advisory, build_reference_info_note
from .candidates import (
    aggregate_labels,
    build_backup_photo_diff,
    build_photo_notes,
    build_ranked_candidate_lines,
    build_ranked_candidates,
    build_weather_indicator_lines,
)
from .joint import build_joint_judgement
from .phrases import _confidence_phrase
from .regions import (
    build_region_human_view,
    build_region_brief_advice,
    apply_label_presentation,
    dedupe_display_labels,
)
from .geo import *
from .models import *
from .scoring import *
from .weather import *

MULTI_DAY_ROUTE_NOTE = "如果你需要路线规划，请改用单独的路线规划 skill。"
MULTI_DAY_INTRO = "这次按逐晚独立推荐来给"
MULTI_DAY_NO_ROUTE = "不做跨晚路线连续性判断"

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
    if error_breakdown.get("daily_limit_exceeded"):
        status = "degraded"
        user_note = "今天天气源查询额度已超限，暂时拿不到新的真实天气数据，明天再查吧。"
    elif ratio >= 0.35:
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

def _display_na(value):
    return NA_STR if value is None else value



def _apply_fetch_failure_policy(decision_summary: dict, fetch_health: Optional[dict]) -> dict:
    if not fetch_health:
        return decision_summary
    if (fetch_health.get('error_breakdown') or {}).get('daily_limit_exceeded'):
        msg = '今天天气源查询额度已超限，暂时拿不到新的真实天气数据，明天再查吧。'
        decision_summary = dict(decision_summary or {})
        decision_summary['one_line'] = msg
        decision_summary['final_reply_draft'] = msg
        drafts = dict(decision_summary.get('reply_drafts') or {})
        drafts['concise'] = msg
        drafts['standard'] = msg
        drafts['detailed'] = msg
        decision_summary['reply_drafts'] = drafts
    return decision_summary


def _safe_number(value):
    return value if value is not None else None


def _night_weather_summary(codes: Optional[List[int]]) -> Optional[str]:
    if not codes:
        return None
    first = next((c for c in codes if c is not None), None)
    if first is None:
        return None
    if first == 0:
        return "晴"
    if first in {1, 2, 3}:
        return "少云到多云"
    if first in {45, 48}:
        return "有雾风险"
    if first in {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}:
        return "有降水信号"
    if first in {71, 73, 75, 77, 85, 86}:
        return "有降雪信号"
    if first in {95, 96, 99}:
        return "有雷暴风险"
    return f"天气码 {first}"


def _moon_phase_label(moon_interference: Optional[float]) -> Optional[str]:
    if moon_interference is None:
        return None
    if moon_interference < 20:
        return "月光较弱"
    if moon_interference < 50:
        return "月光中等"
    return "月光较强"


def _condensation_risk(region: dict) -> Optional[str]:
    temp = region.get("night_avg_temperature_c")
    if temp is None:
        temp = region.get("night_avg_temperature")
    dew = region.get("night_avg_dew_point_c")
    if dew is None:
        dew = region.get("night_avg_dew_point")
    humidity = region.get("night_avg_humidity_pct")
    if humidity is None:
        humidity = region.get("night_avg_humidity")
    if temp is None or dew is None:
        if humidity is None:
            return None
        if humidity >= 85:
            return "high"
        if humidity >= 70:
            return "medium"
        return "low"
    gap = temp - dew
    if gap <= 2:
        return "high"
    if gap <= 5:
        return "medium"
    return "low"


def _wind_stability_note(region: dict) -> Optional[str]:
    wind = region.get("night_avg_wind_kmh")
    gust = region.get("night_max_gust_kmh")
    if wind is None and gust is None:
        return None
    if gust is not None and wind is not None and gust - wind >= 20:
        return "均风不大，但阵风偏高"
    if wind is not None and wind <= 8:
        return "风况较稳"
    if wind is not None and wind <= 15:
        return "风况尚可"
    return "风速偏高，长曝光稳定性一般"


def _cloud_trend_note(region: dict) -> Optional[str]:
    stability = region.get("cloud_stability")
    worst_segment = region.get("worst_cloud_segment")
    avg_cloud = region.get("night_avg_cloud")
    if avg_cloud is None and stability is None and worst_segment is None:
        return None
    if stability == "stable":
        return "整晚云量较稳"
    if worst_segment:
        return f"{worst_segment}云量相对更差"
    return "云量存在波动"


def _terrain_note(region: dict) -> Optional[str]:
    note = region.get("low_cloud_terrain_note")
    if note:
        return note
    elev = region.get("avg_elevation_m")
    if elev is None:
        elev = region.get("elevation_m")
    if elev is None:
        return None
    if elev >= 3000:
        return "高海拔区域，夜间温差与体感更强"
    if elev >= 1200:
        return "中高海拔区域，需留意夜间降温与风感"
    return "相对低海拔区域，地形修正影响有限"


def _dark_sky_practical_note(region: dict) -> Optional[str]:
    lp = region.get("light_pollution_bortle") or region.get("light_pollution_level")
    if not lp:
        return None
    if "1-2" in lp:
        return "暗空优势明显，适合优先考虑星野和广角银河"
    if "3-4" in lp or "5-6" in lp:
        return "暗空条件尚可，需注意朝向和地平线光害"
    return "光污染偏重，更适合作为天气备选而非暗空首选"


def _practical_shooting_note(region: dict) -> Optional[str]:
    usable = region.get("usable_hours")
    lp = region.get("light_pollution_bortle") or region.get("light_pollution_level") or ""
    if usable is None:
        return None
    if usable >= 4 and "1-2" in lp:
        return "适合整夜守候或作为主冲夜"
    if usable >= 3:
        return "适合中夜重点守候"
    return "更适合短时突击，不建议整夜蹲守"


def _practical_best_pick(labels: List[dict]) -> Optional[str]:
    if not labels:
        return None
    def practical_key(region: dict):
        lp = region.get("light_pollution_bortle") or ""
        lp_bonus = 2 if "1-2" in lp else 1 if ("3-4" in lp or "5-6" in lp) else 0
        return (
            lp_bonus,
            region.get("usable_hours") or 0.0,
            -(region.get("moon_interference") or 999.0),
            region.get("decision_rank_score") or region.get("ranking_score") or region.get("final_score") or 0.0,
        )
    best = max(labels, key=practical_key)
    return best.get("display_label") or best.get("anchor_label") or best.get("label")


def _candidate_record(region: dict, date: str, rank: int, weather_source: str, weather_model: str, forecast_confidence: Optional[str], forecast_horizon_days: Optional[int]) -> dict:
    avg_temp = region.get("night_avg_temperature_c")
    if avg_temp is None:
        avg_temp = region.get("night_avg_temperature")
    avg_dew = region.get("night_avg_dew_point_c")
    if avg_dew is None:
        avg_dew = region.get("night_avg_dew_point")
    avg_humidity = region.get("night_avg_humidity_pct")
    if avg_humidity is None:
        avg_humidity = region.get("night_avg_humidity")
    center_lat = region.get("lat")
    center_lng = region.get("lng")
    light_pollution_level = region.get("light_pollution_bortle")
    codes = region.get("night_weather_codes")
    return {
        "date": date,
        "rank": rank,
        "area_name": region.get("display_label") or region.get("label"),
        "primary_area": region.get("anchor_label") or region.get("display_label") or region.get("label"),
        "focus_area": region.get("refined_label") or region.get("label"),
        "province_list": region.get("provinces") or ([region.get("province")] if region.get("province") else []),
        "recommended_level": region.get("qualification"),
        "ranking_score": round(region.get("ranking_score") or region.get("decision_rank_score") or region.get("final_score") or 0.0, 2),
        "final_score": round(region.get("final_score") or 0.0, 2),
        "decision_score": round(region.get("decision_rank_score") or region.get("ranking_score") or region.get("final_score") or 0.0, 2),
        "raw_label": region.get("label"),
        "score_semantics": region.get("score_semantics"),
        "center_lat": center_lat,
        "center_lng": center_lng,
        "cluster_size": region.get("cluster_size"),
        "elevation_m": region.get("avg_elevation_m") if region.get("avg_elevation_m") is not None else region.get("elevation_m"),
        "best_point_id": region.get("best_point_id"),
        "member_point_ids": region.get("members"),
        "astronomical_night_start": region.get("astronomical_night_start"),
        "astronomical_night_end": region.get("astronomical_night_end"),
        "best_window_start": region.get("best_window_start"),
        "best_window_end": region.get("best_window_end"),
        "best_window_segment": region.get("best_window_segment"),
        "usable_hours": region.get("usable_hours"),
        "longest_usable_streak_hours": region.get("longest_usable_streak_hours"),
        "avg_cloud_cover": region.get("night_avg_cloud"),
        "worst_cloud_cover": region.get("night_worst_cloud"),
        "avg_low_cloud_cover": region.get("night_avg_cloud_low"),
        "avg_mid_cloud_cover": region.get("night_avg_cloud_mid"),
        "avg_high_cloud_cover": region.get("night_avg_cloud_high"),
        "cloud_variability": region.get("cloud_stddev"),
        "cloud_stability": region.get("cloud_stability"),
        "worst_cloud_segment": region.get("worst_cloud_segment"),
        "cloud_trend_note": _cloud_trend_note(region),
        "avg_wind_speed_kmh": region.get("night_avg_wind_kmh"),
        "max_gust_kmh": region.get("night_max_gust_kmh"),
        "avg_humidity_pct": avg_humidity,
        "avg_visibility_m": region.get("night_avg_visibility_m"),
        "avg_temperature_c": avg_temp,
        "avg_dew_point_c": avg_dew,
        "condensation_risk": _condensation_risk(region),
        "wind_stability_note": _wind_stability_note(region),
        "max_precip_mm": region.get("night_max_precip_mm") if region.get("night_max_precip_mm") is not None else region.get("night_max_precip"),
        "weather_codes": codes,
        "dominant_weather_code": codes[0] if codes else None,
        "weather_summary": _night_weather_summary(codes),
        "moon_interference": region.get("moon_interference"),
        "moonrise": region.get("moonrise"),
        "moonset": region.get("moonset"),
        "moon_dark_window": region.get("moon_dark_window"),
        "moon_phase_label": _moon_phase_label(region.get("moon_interference")),
        "moonlight_score": region.get("avg_moonlight_score"),
        "light_pollution_level": light_pollution_level,
        "light_pollution_note": region.get("light_pollution_note"),
        "low_cloud_terrain_penalty": region.get("low_cloud_terrain_penalty"),
        "low_cloud_terrain_state": region.get("low_cloud_terrain_state"),
        "low_cloud_terrain_note": region.get("low_cloud_terrain_note"),
        "terrain_note": _terrain_note(region),
        "dark_sky_practical_note": _dark_sky_practical_note(region),
        "weather_source": weather_source,
        "weather_model": weather_model,
        "fetch_attempts": region.get("fetch_attempts"),
        "fetch_recovered": region.get("fetch_recovered"),
        "fetch_error_type": region.get("fetch_error_type"),
        "fetch_error_message": region.get("fetch_error_message"),
        "forecast_confidence": forecast_confidence,
        "forecast_horizon_days": forecast_horizon_days,
        "brief_advice": region.get("brief_advice"),
        "refinement_note": region.get("refinement_note"),
        "practical_note": region.get("brief_advice"),
        "risk_note": region.get("risk_note") or ("光污染偏重" if light_pollution_level and ("7-8" in light_pollution_level or "8-9" in light_pollution_level) else None),
        "why_it_ranks_here": region.get("brief_advice"),
        "practical_shooting_note": _practical_shooting_note(region),
    }


def build_professional_output(labels: List[dict], decision_summary: dict, fetch_health: dict, scope_meta: dict, target_dt: datetime, args, confidence: Optional[str], weather_model: Optional[str]) -> dict:
    date = target_dt.date().isoformat()
    today = datetime.now().date()
    forecast_horizon_days = (target_dt.date() - today).days
    weather_source = next((x.get("weather_source") for x in labels if x.get("weather_source")), "openmeteo-http" if getattr(args, "real_weather", False) else "mock")
    model_name = weather_model or "ecmwf_ifs"
    sorted_labels = sorted(labels, key=lambda x: (-(x.get("decision_rank_score") or x.get("ranking_score") or x.get("final_score") or 0.0), -(x.get("final_score") or 0.0), x.get("display_label") or x.get("label") or ""))
    candidate_rows = [
        _candidate_record(region, date, idx, weather_source, model_name, confidence, forecast_horizon_days)
        for idx, region in enumerate(sorted_labels, 1)
    ]
    top = candidate_rows[0] if candidate_rows else None
    second = candidate_rows[1] if len(candidate_rows) > 1 else None
    third = candidate_rows[2] if len(candidate_rows) > 2 else None
    practical_best_pick = _practical_best_pick(sorted_labels)
    top_level = top.get("light_pollution_level") if top else None
    runner_up_gap = round((top.get("decision_score") - second.get("decision_score")), 2) if top and second and top.get("decision_score") is not None and second.get("decision_score") is not None else None
    recommended_action = "值得主冲" if top and top.get("recommended_level") == "recommended" else "可作备选" if top else "建议观望"
    night_summary = {
        "date": date,
        "primary_area": top.get("primary_area") if top else None,
        "focus_area": top.get("focus_area") if top else None,
        "top_pick": top.get("area_name") if top else None,
        "second_pick": second.get("area_name") if second else None,
        "third_pick": third.get("area_name") if third else None,
        "top_pick_score": top.get("decision_score") if top else None,
        "recommended_level": top.get("recommended_level") if top else None,
        "decision_note": decision_summary.get("one_line") or (top.get("brief_advice") if top else "暂无推荐结果"),
        "practical_note": top.get("practical_note") if top else None,
        "top_pick_reason": top.get("why_it_ranks_here") if top else None,
        "night_risk_summary": top.get("risk_note") if top else None,
        "confidence_summary": confidence,
        "recommended_action": recommended_action,
        "practical_best_pick": practical_best_pick,
        "runner_up_gap": runner_up_gap,
        "is_strong_recommendation": bool(top and top.get("recommended_level") == "recommended"),
        "best_window_start": top.get("best_window_start") if top else None,
        "best_window_end": top.get("best_window_end") if top else None,
        "usable_hours": top.get("usable_hours") if top else None,
        "avg_cloud_cover": top.get("avg_cloud_cover") if top else None,
        "moon_interference": top.get("moon_interference") if top else None,
        "light_pollution_level": top_level,
    }
    decision_summary.setdefault("professional_bridge", {})
    decision_summary["professional_bridge"].update({
        "primary_area": night_summary.get("primary_area"),
        "focus_area": night_summary.get("focus_area"),
        "top_pick": night_summary.get("top_pick"),
        "practical_best_pick": practical_best_pick,
        "recommended_action": recommended_action,
        "runner_up_gap": runner_up_gap,
        "top_pick_reason": night_summary.get("top_pick_reason"),
        "night_risk_summary": night_summary.get("night_risk_summary"),
        "confidence_summary": confidence,
    })
    query_meta = {
        "query_mode": "single_night",
        "theme": args.mode,
        "scope_mode": scope_meta.get("scope_mode"),
        "scope_name": "全国" if scope_meta.get("scope_mode") == "national" else "、".join(scope_meta.get("scope_coverage", {}).get("provinces", [])[:5]) or "指定范围",
        "start_date": date,
        "end_date": date,
        "night_count": 1,
        "timezone": args.timezone,
        "weather_source": weather_source,
        "weather_model": model_name,
        "generated_at": datetime.now().isoformat(),
        "forecast_horizon_note": {"high": "3天内：数据可靠，接近实况", "medium": "4-7天：预报精度有所下降，建议参考趋势", "low": "8-16天：预报不确定性较高，建议临近再复查", "mock": "使用 mock 数据，仅供调试"}.get(confidence, ""),
        "missing_fields_note": "拿不到的字段已保留并建议展示为 NA。",
        "data_quality_status": fetch_health.get("status") or "ok",
        "notes": [],
    }
    data_quality = {
        "overall_status": fetch_health.get("status") or "ok",
        "total_points": fetch_health.get("total_points") or 0,
        "successful_points": fetch_health.get("successful_points") or 0,
        "failed_points": fetch_health.get("failed_points") or 0,
        "failed_ratio": fetch_health.get("failed_ratio") or 0.0,
        "retried_points": fetch_health.get("retried_points") or 0,
        "recovered_points": fetch_health.get("recovered_points") or 0,
        "error_breakdown": fetch_health.get("error_breakdown") or {},
        "user_note": fetch_health.get("user_note") or "本轮数据可用于区域级拍星筛选。",
        "missing_fields_note": query_meta["missing_fields_note"],
        "forecast_horizon_note": query_meta["forecast_horizon_note"],
    }
    professional_output = {
        "query_meta": query_meta,
        "night_summaries": [night_summary],
        "night_candidates": [{"date": date, "candidates": candidate_rows}],
        "data_quality": data_quality,
    }
    return professional_output


def _merge_error_breakdown(items: List[dict]) -> dict:
    merged: Dict[str, int] = {}
    for item in items:
        for k, v in (item or {}).items():
            merged[k] = merged.get(k, 0) + int(v or 0)
    return merged



def _clone_points(points: List[SamplePoint]) -> List[SamplePoint]:
    return [copy.deepcopy(p) for p in points]


def _coarse_status_value(status: str) -> int:
    return {"drop": 0, "edge": 1, "pass": 2}.get(status or "drop", 0)


def _coarse_status_from_value(value: float) -> str:
    if value >= 1.5:
        return "pass"
    if value >= 0.5:
        return "edge"
    return "drop"


def _hydrate_points_for_model(args, points: List[SamplePoint], target_dt: datetime, model: str, scope_mode: Optional[str] = None) -> List[SamplePoint]:
    hydrate_weather(points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model=model, scope_mode=scope_mode)
    for p in points:
        p.stage1_status = classify_cloud(p, args.mode)
        p.weather_model = model
    return points


def _coarse_screen_points(args, points: List[SamplePoint], target_dt: datetime, coarse_models: List[str], scope_mode: Optional[str] = None, icon_model: Optional[str] = None) -> dict:
    model_runs: Dict[str, List[SamplePoint]] = {}
    model_parallelism = max(1, min(len(coarse_models), 3 if scope_mode == 'national' else 1))
    with ThreadPoolExecutor(max_workers=model_parallelism) as executor:
        future_map = {
            executor.submit(_hydrate_points_for_model, args, _clone_points(points), target_dt, model_name, scope_mode): model_name
            for model_name in coarse_models
        }
        for future in as_completed(future_map):
            model_runs[future_map[future]] = future.result()
    model_runs = {k: model_runs[k] for k in coarse_models if k in model_runs}

    point_ids = [p.id for p in points]
    run_maps = {model_name: {p.id: p for p in pts} for model_name, pts in model_runs.items()}
    disputed_ids = []
    merged_points: List[SamplePoint] = []
    for point_id in point_ids:
        statuses = [run_maps[model_name][point_id].stage1_status for model_name in coarse_models if point_id in run_maps[model_name]]
        if len(set(statuses)) > 1:
            disputed_ids.append(point_id)

    icon_runs: Dict[str, SamplePoint] = {}
    icon_triggered = False
    if icon_model and disputed_ids:
        icon_triggered = True
        disputed_points = [copy.deepcopy(next(p for p in points if p.id == point_id)) for point_id in disputed_ids]
        disputed_points = _hydrate_points_for_model(args, disputed_points, target_dt, icon_model, scope_mode)
        icon_runs = {p.id: p for p in disputed_points}

    for point_id in point_ids:
        base_point = copy.deepcopy(next(p for p in points if p.id == point_id))
        samples = [run_maps[model_name][point_id] for model_name in coarse_models if point_id in run_maps[model_name]]
        if point_id in icon_runs:
            samples.append(icon_runs[point_id])
        numeric = [_coarse_status_value(p.stage1_status) for p in samples]
        avg_value = (sum(numeric) / len(numeric)) if numeric else 0.0
        merged_status = _coarse_status_from_value(avg_value)
        merged_point = samples[0] if samples else base_point
        merged_point = copy.deepcopy(merged_point)
        merged_point.stage1_status = merged_status
        merged_point.weather_model = "+".join([p.weather_model for p in samples if p.weather_model]) if samples else None
        merged_points.append(merged_point)

    coarse_pass = [p for p in merged_points if p.stage1_status in {"pass", "edge"}]
    fetch_rows = [summarize_fetch_health(pts) for pts in model_runs.values()]
    if icon_runs:
        fetch_rows.append(summarize_fetch_health(list(icon_runs.values())))
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
    return {
        "merged_points": merged_points,
        "coarse_pass": coarse_pass,
        "model_runs": model_runs,
        "coarse_models": coarse_models,
        "third_model_recheck": {
            "enabled": bool(icon_model),
            "requested_model": icon_model,
            "triggered": icon_triggered,
            "reason": "coarse_dual_model_disputed" if icon_triggered else "coarse_dual_model_already_stable",
            "disputed_point_count": len(disputed_ids),
        },
        "fetch_health": {
            "status": "degraded" if failed_ratio >= 0.35 else ("partial" if failed_ratio > 0 else "ok"),
            "total_points": total_points,
            "successful_points": successful_points,
            "failed_points": failed_points,
            "failed_ratio": round(failed_ratio, 3),
            "retried_points": retried_points,
            "recovered_points": recovered_points,
            "error_breakdown": error_breakdown,
            "user_note": None,
        },
    }


def _national_target_final_count(args) -> int:
    configured = getattr(args, 'national_target_final_count', None)
    if configured:
        return max(34, int(configured))
    return 200



def _prepare_stage2_candidates(args, boxes: List[BoundingBox], province_polygons, prefecture_polygons, target_dt: datetime) -> dict:
    all_points: List[SamplePoint] = []
    generated_count_before_filter = 0
    scope_mode = build_scope_meta(boxes).get('scope_mode')
    national_uniform_mode = len({b.province for b in boxes}) >= 34
    if national_uniform_mode:
        generated_count_before_filter = len(boxes) * args.target_count
        all_points = generate_national_uniform_points(boxes, generated_count_before_filter, province_polygons, prefecture_polygons, target_final_count=_national_target_final_count(args))
    else:
        for box in boxes:
            pts = generate_grid_points(box, args.target_count)
            generated_count_before_filter += len(pts)
            pts = filter_points_by_polygon(pts, province_polygons, prefecture_polygons)
            all_points.extend(pts)

    hydrate_weather(all_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model="ecmwf_ifs", scope_mode=scope_mode)
    coarse_pass = coarse_filter(all_points, args.mode)

    adaptive_points = generate_adaptive_refinement_points(coarse_pass, boxes)
    if adaptive_points:
        hydrate_weather(adaptive_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model="ecmwf_ifs", scope_mode=scope_mode)
        adaptive_points = coarse_filter(adaptive_points, args.mode)
        coarse_pass = coarse_pass + adaptive_points

    stage2_seed = select_stage2_budget(
        coarse_pass,
        max_stage2_points=args.max_stage2_points,
        direct_stage2_threshold=args.direct_stage2_threshold,
    )
    fetch_points = list(all_points) + list(adaptive_points)
    fetch_health = summarize_fetch_health(fetch_points)
    return {
        "generated_count_before_filter": generated_count_before_filter,
        "all_points": all_points,
        "coarse_pass": coarse_pass,
        "adaptive_points": adaptive_points,
        "stage2_seed": stage2_seed,
        "coarse_model": "ecmwf_ifs",
        "coarse_models": ["ecmwf_ifs"],
        "coarse_third_model_recheck": None,
        "coarse_fetch_health": fetch_health,
    }


def _run_stage2_model_pipeline(args, stage2_seed: List[SamplePoint], boxes: List[BoundingBox], prefecture_polygons, county_polygons, target_dt: datetime, confidence: str, generated_count_before_filter: int, coarse_pass: List[SamplePoint], all_points: List[SamplePoint], adaptive_points: List[SamplePoint], province_polygons, model: str) -> dict:
    started_at = time.perf_counter()
    scope_mode = build_scope_meta(boxes).get('scope_mode')
    model_stage2_points = _clone_points(stage2_seed)
    hydrate_weather(model_stage2_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model=model, scope_mode=scope_mode)
    for p in model_stage2_points:
        compute_final_score(p, args.mode)
    deduped = dedupe_cross_province(model_stage2_points, distance_km=args.dedupe_km, score_gap=args.cloud_gap)
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
    fetch_health = summarize_fetch_health(model_stage2_points)
    moon_advisory = None
    lp_note = None
    if labels:
        moon_val = labels[0].get("moon_interference")
        if moon_val is not None:
            moon_advisory = _moon_advisory(moon_val)
        lp_note = labels[0].get("light_pollution_note")
    decision_summary = build_decision_summary(labels, confidence=confidence, moon_advisory=moon_advisory, light_pollution_note=lp_note)
    decision_summary = _apply_fetch_failure_policy(decision_summary, fetch_health)
    if fetch_health.get("user_note") and not ((fetch_health.get("error_breakdown") or {}).get("daily_limit_exceeded")):
        note = fetch_health["user_note"]
        decision_summary["data_quality_note"] = note
        if decision_summary.get("final_reply_draft"):
            decision_summary["final_reply_draft"] += f"\n数据完整性：{note}"
        decision_summary.setdefault("reply_drafts", {})
        if decision_summary["reply_drafts"].get("concise"):
            clean_note = note.rstrip("。")
            decision_summary["reply_drafts"]["concise"] = decision_summary["reply_drafts"]["concise"].rstrip("。") + f"；{clean_note}。"
        if decision_summary["reply_drafts"].get("standard"):
            decision_summary["reply_drafts"]["standard"] += f"\n数据完整性：{note}"
        if decision_summary.get("final_reply_draft"):
            decision_summary["reply_drafts"]["detailed"] = decision_summary["final_reply_draft"]
    confidence_note_text = {
        "high": "3天内：数据可靠，接近实况",
        "medium": "4-7天：预报精度有所下降，建议参考趋势",
        "low": "8-16天：预报不确定性较高，请以当天Windy等本地工具为准",
    }.get(confidence, "")
    professional_output = build_professional_output(labels, decision_summary, fetch_health, scope_meta, target_dt, args, confidence, model)
    final_text_recommendation = decision_summary.get("reply_drafts", {}).get("standard") or decision_summary.get("final_reply_draft") or decision_summary.get("one_line")
    user_output = {
        "mode": args.mode,
        "target_datetime": target_dt.isoformat(),
        "weather_model": model,
        "forecast_confidence": confidence,
        "scope_mode": scope_meta["scope_mode"],
        "scope_coverage": scope_meta["scope_coverage"],
        "scope_reduction_reason": scope_meta["scope_reduction_reason"],
        "scope_guardrail": scope_meta["scope_guardrail"],
        "fetch_health": fetch_health,
        "decision_summary": decision_summary,
        "final_text_recommendation": final_text_recommendation,
        "top_region_advice": top_region_advice,
        "timing": {
            "elapsed_ms": elapsed_ms,
            "elapsed_seconds": round(elapsed_ms / 1000.0, 2),
        },
        "confidence_note": confidence_note_text,
        "budget": {"max_workers": args.max_workers, "max_stage2_points": args.max_stage2_points, "direct_stage2_threshold": args.direct_stage2_threshold, "top_n": args.top_n},
    }
    debug_output = {
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
        "stage2_points": [asdict(p) for p in model_stage2_points],
        "deduped_survivors": [asdict(p) for p in deduped],
        "region_labels": labels,
    }
    return {
        **user_output,
        **debug_output,
        "user_output": user_output,
        "debug_output": debug_output,
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
        if min_lng > 90:
            guardrail["warnings"].append("national_scope_missing_far_west")
        if max_lng < 115:
            guardrail["warnings"].append("national_scope_missing_far_east_or_northeast")
        if max_lat < 43:
            guardrail["warnings"].append("national_scope_missing_northern_band")
        if min_lat > 28:
            guardrail["warnings"].append("national_scope_missing_southwestern_band")
        if len(provinces) < 34:
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

def build_decision_summary(labels: List[dict], confidence: Optional[str] = None, joint: Optional[dict] = None, third_model_recheck: Optional[dict] = None, moon_advisory: Optional[str] = None, light_pollution_note: Optional[str] = None) -> dict:
    primary = labels[0] if labels else None

    joint_regions = (joint or {}).get("consensus_regions", []) if joint else []
    if joint_regions:
        ranked_candidates = build_ranked_candidates(joint_regions, limit=10, min_score=60.0)
        primary_region = ranked_candidates[0]["display_label"] if ranked_candidates else None
        primary_advice = joint_regions[0].get("joint_brief_advice") if joint_regions else None
        backup_regions = [x["display_label"] for x in ranked_candidates[1:3]]
        refinement_note = joint_regions[0].get("refinement_note") if joint_regions else None
    else:
        ranked_candidates = build_ranked_candidates(labels, limit=10)
        primary_region = ranked_candidates[0]["display_label"] if ranked_candidates else None
        primary_advice = primary.get("brief_advice") if primary else None
        backup_regions = [x["display_label"] for x in ranked_candidates[1:3]]
        refinement_note = primary.get("refinement_note") if primary else None

    backups = labels[1:3] if len(labels) > 1 else []

    extra_indicators = []
    if primary and any(primary.get(k) is not None for k in ("night_avg_cloud_low", "night_avg_cloud_mid", "night_avg_cloud_high")):
        extra_indicators.append("低/中/高云层覆盖")
    if primary and primary.get("low_cloud_terrain_note"):
        extra_indicators.append("地形海拔对低云影响的保守修正")

    reference_info = build_reference_info_note(
        moon_advisory=moon_advisory,
        light_pollution_note=light_pollution_note,
        extra_indicators=extra_indicators,
        no_candidates=not bool(labels),
    )
    primary_source_region = labels[0] if labels else None
    primary_photo_notes = build_photo_notes(primary_source_region)
    primary_indicator_lines = build_weather_indicator_lines(primary_source_region)
    ranked_candidate_lines = build_ranked_candidate_lines(ranked_candidates)
    backup_diff_note = build_backup_photo_diff(primary_source_region, backups[0] if backups else None)

    summary = {
        "primary_region": primary_region,
        "primary_advice": primary_advice,
        "backup_regions": backup_regions,
        "photo_notes": primary_photo_notes,
        "weather_indicators": primary_indicator_lines,
        "ranked_candidates": ranked_candidates,
        "ranked_candidate_lines": ranked_candidate_lines,
        "backup_photo_note": backup_diff_note,
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

    primary_region = summary.get("primary_region")
    primary_advice = summary.get("primary_advice")
    confidence_note = summary.get("confidence_note")
    risk_note = summary.get("risk_note")
    refinement_note = summary.get("refinement_note")
    backup_regions = summary.get("backup_regions") or []
    reference_note = summary.get("reference_note")
    next_step_note = summary.get("next_step_note")
    backup_photo_note = summary.get("backup_photo_note")
    weather_indicators = summary.get("weather_indicators") or []
    ranked_candidates = summary.get("ranked_candidates") or []
    ranked_candidate_lines = summary.get("ranked_candidate_lines") or []

    if primary_region and primary_advice:
        summary["one_line"] = f"当前优先关注 {primary_region}。"
    elif not primary_region:
        summary["one_line"] = "这轮没有筛出明确值得优先推荐的区域。"
        summary["next_step_note"] = "如果你愿意，我可以换个时间窗再查一次，或者直接缩小到你关心的省份 / 西北高原 / 某条出行方向继续细看。"

    reply_lines = []
    if primary_advice:
        reply_lines.append(f"结论：{primary_advice}")
    elif primary_region:
        reply_lines.append(f"结论：当前优先关注 {primary_region}。")
    else:
        reply_lines.append("结论：这轮没有筛出明确值得优先推荐的区域。")

    if backup_regions:
        reply_lines.append(f"备选：{ '、'.join(backup_regions) }")
    if backup_photo_note:
        reply_lines.append(backup_photo_note)
    if risk_note:
        reply_lines.append(f"风险：{risk_note}")
    if refinement_note:
        reply_lines.append(f"细化说明：{refinement_note}")
    if primary_photo_notes.get("best_window"):
        reply_lines.append(f"窗口：{primary_photo_notes['best_window']}")
    if primary_photo_notes.get("wind"):
        reply_lines.append(f"风况：{primary_photo_notes['wind']}")
    if primary_photo_notes.get("dew"):
        reply_lines.append(f"返潮：{primary_photo_notes['dew']}")
    if confidence_note and (not primary_advice or confidence_note not in primary_advice):
        reply_lines.append(f"置信度：{confidence_note}")
    if weather_indicators:
        reply_lines.append("气象指标摘要：")
        reply_lines.extend(weather_indicators)
    if ranked_candidate_lines:
        reply_lines.append("当晚前 10 候选（含分数）：")
        reply_lines.extend(ranked_candidate_lines)
    if reference_note:
        reply_lines.append(reference_note)
    if next_step_note:
        reply_lines.append(f"下一步：{next_step_note}")

    if reply_lines:
        summary["final_reply_draft"] = "\n".join(reply_lines)

    concise_photo_note = (
        primary_photo_notes.get("best_window")
        or primary_photo_notes.get("wind")
        or primary_photo_notes.get("dew")
    )

    concise_parts = []
    if primary_region and not refinement_note:
        concise_parts.append(f"优先关注 {primary_region}")
    elif not primary_region:
        concise_parts.append("这轮没有筛出明确值得优先推荐的区域")
    if risk_note:
        concise_parts.append(f"风险：{risk_note}")
    if refinement_note:
        concise_parts.append(refinement_note)
    if confidence_note:
        concise_parts.append(confidence_note)
    if concise_photo_note:
        concise_parts.append(concise_photo_note)
    if backup_photo_note:
        concise_parts.append(backup_photo_note)
    if concise_parts:
        concise = "；".join(part.rstrip('。') for part in concise_parts if part)
        short_reference_note = (summary.get("reference_info") or {}).get("short_note")
        if short_reference_note:
            concise += f"；{short_reference_note.rstrip('。')}"
        summary["reply_drafts"]["concise"] = concise + "。"

    standard_parts = []
    if primary_advice:
        standard_parts.append(f"结论：{primary_advice}")
    elif not primary_region:
        standard_parts.append("结论：这轮没有筛出明确值得优先推荐的区域。")
    if backup_photo_note:
        standard_parts.append(backup_photo_note)
    if refinement_note:
        standard_parts.append(f"细化说明：{refinement_note}")
    if primary_photo_notes.get("best_window"):
        standard_parts.append(f"窗口：{primary_photo_notes['best_window']}")
    if primary_photo_notes.get("wind"):
        standard_parts.append(f"风况：{primary_photo_notes['wind']}")
    if primary_photo_notes.get("dew"):
        standard_parts.append(f"返潮：{primary_photo_notes['dew']}")
    if confidence_note and (not primary_advice or confidence_note not in primary_advice):
        standard_parts.append(f"置信度：{confidence_note}")
    if weather_indicators:
        standard_parts.append("气象指标摘要：")
        standard_parts.extend(weather_indicators)
    if ranked_candidate_lines:
        standard_parts.append("当晚前 10 候选（含分数）：")
        standard_parts.extend(ranked_candidate_lines)
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
    p.add_argument("--target-count", type=int, default=8, help="Samples per box")
    p.add_argument("--dedupe-km", type=float, default=60.0, help="Dedupe distance")
    p.add_argument("--cluster-km", type=float, default=120.0, help="Cluster radius")
    p.add_argument("--cloud-gap", type=float, default=8.0, help="Cloud gap for dedupe")
    p.add_argument("--real-weather", action="store_true", help="Use Open-Meteo")
    p.add_argument("--target-datetime", help="ISO datetime")
    p.add_argument("--multi-day-start-date", "--trip-start-date", dest="multi_day_start_date", help="Multi-day start date")
    p.add_argument("--multi-day-days", "--trip-days", dest="multi_day_days", type=int, default=0, help="Number of nights")
    p.add_argument("--timezone", default="Asia/Shanghai", help="Timezone")
    p.add_argument("--boxes-json", help="Boxes JSON")
    p.add_argument("--scope-preset", choices=["national"], help="Built-in scope preset")
    p.add_argument("--polygons-json", help="Polygon JSON")
    p.add_argument("--polygons-file", help="Polygon file")
    p.add_argument("--max-workers", type=int, default=4, help="Max workers")
    p.add_argument("--national-target-final-count", type=int, default=0, help="Cap national sampling points after polygon filtering and compensation (0 = auto)")
    p.add_argument("--max-stage2-points", type=int, default=12, help="Stage2 budget")
    p.add_argument("--direct-stage2-threshold", type=int, default=10, help="Direct stage2 threshold")
    p.add_argument("--top-n", type=int, default=10, help="Max output regions")
    p.add_argument("--strict-national-scope", action="store_true", help="Fail if national scope looks partial")
    p.add_argument("--output-format", choices=["full"], default="full", help="Output full payload JSON")
    p.add_argument("--pretty", action="store_true")
    return p

def check_date_availability(target_dt: datetime) -> Tuple[bool, Optional[datetime]]:
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    latest = today + timedelta(days=OPEN_METEO_HOURLY_WINDOW_DAYS)
    required_end = target_dt + timedelta(days=1)
    is_available = required_end <= latest
    return is_available, latest

def _region_score(region: Optional[dict]) -> float:
    if not region:
        return 0.0
    return float(region.get("ranking_score") or region.get("decision_rank_score") or region.get("final_score") or 0.0)

def _multi_day_nightly_reply(day_payloads: List[dict]) -> List[str]:
    lines = [f"{MULTI_DAY_INTRO}，{MULTI_DAY_NO_ROUTE}；{MULTI_DAY_ROUTE_NOTE}", ""]
    for payload in day_payloads:
        date = (payload.get("target_datetime") or "")[:10]
        ds = payload.get("decision_summary") or {}
        lines.append(f"【{date}】")
        final_reply = ds.get("final_reply_draft") or ds.get("one_line") or "暂无单晚推荐结果。"
        lines.append(final_reply)
        lines.append("")
    return lines

def _multi_day_standard_reply(day_payloads: List[dict]) -> str:
    lines = [
        f"{MULTI_DAY_INTRO}，共 {len(day_payloads)} 晚；每晚都单独给主推荐和备选，不把它硬拼成一条路线。",
        f"如果你需要额外做路线规划，再改用单独的路线规划 skill。",
        "",
    ]
    for idx, payload in enumerate(day_payloads):
        date = (payload.get("target_datetime") or "")[:10]
        ds = payload.get("decision_summary") or {}
        primary = ds.get("primary_region")
        primary_advice = ds.get("primary_advice")
        backups = [x for x in (ds.get("backup_regions") or []) if x]
        risk_note = ds.get("risk_note")
        confidence_note = ds.get("confidence_note")
        refinement_note = ds.get("refinement_note")
        reference_info = ds.get("reference_info") or {}
        short_reference = reference_info.get("short_note")

        parts = []
        if primary_advice:
            parts.append(primary_advice.rstrip("。"))
        elif primary:
            parts.append(f"优先看 {primary}")
        else:
            parts.append("这晚暂时没筛出特别值得优先拍板的区域")
        if backups:
            parts.append(f"备选可看 {'、'.join(backups)}")
        if risk_note:
            parts.append(f"{risk_note.rstrip('。')}，建议结合临近预报再判断")
        if confidence_note:
            parts.append(confidence_note.rstrip("。"))
        if short_reference:
            parts.append(short_reference.rstrip("。"))
        if refinement_note and primary:
            parts.append(f"如需继续细筛，可在 {primary} 范围内进一步收窄到更具体的守候点")
        lines.append(f"【{date}】{'；'.join(part for part in parts if part)}。")
    return "\n".join(lines)

def build_daily_payload(args, boxes: List[BoundingBox], province_polygons, prefecture_polygons, county_polygons, target_dt: datetime, confidence: str) -> dict:
    return run_pipeline(
        args,
        boxes,
        province_polygons,
        prefecture_polygons,
        county_polygons,
        target_dt,
        confidence,
        model="ecmwf_ifs",
    )

def run_pipeline(args, boxes: List[BoundingBox], province_polygons, prefecture_polygons, county_polygons, target_dt: datetime, confidence: str, model: Optional[str] = None) -> dict:
    started_at = time.perf_counter()
    all_points: List[SamplePoint] = []
    generated_count_before_filter = 0
    national_uniform_mode = len({b.province for b in boxes}) >= 34
    if national_uniform_mode:
        generated_count_before_filter = len(boxes) * args.target_count
        all_points = generate_national_uniform_points(boxes, generated_count_before_filter, province_polygons, prefecture_polygons, target_final_count=_national_target_final_count(args))
    else:
        for box in boxes:
            pts = generate_grid_points(box, args.target_count)
            generated_count_before_filter += len(pts)
            pts = filter_points_by_polygon(pts, province_polygons, prefecture_polygons)
            all_points.extend(pts)

    scope_meta = build_scope_meta(boxes)
    hydrate_weather(all_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model=model, scope_mode=scope_meta['scope_mode'])
    coarse_pass = coarse_filter(all_points, args.mode)

    adaptive_points = generate_adaptive_refinement_points(coarse_pass, boxes)
    if adaptive_points:
        hydrate_weather(adaptive_points, real_weather=args.real_weather, target_dt=target_dt, timezone=args.timezone, mode=args.mode, max_workers=args.max_workers, model=model, scope_mode=scope_meta['scope_mode'])
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
    decision_summary = _apply_fetch_failure_policy(decision_summary, fetch_health)
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
    confidence_note_text = {
        "high": "3天内：数据可靠，接近实况",
        "medium": "4-7天：预报精度有所下降，建议参考趋势",
        "low": "8-16天：预报不确定性较高，请以当天Windy等本地工具为准",
    }.get(confidence, "")
    professional_output = build_professional_output(labels, decision_summary, fetch_health, scope_meta, target_dt, args, confidence, model)
    final_text_recommendation = decision_summary.get("reply_drafts", {}).get("standard") or decision_summary.get("final_reply_draft") or decision_summary.get("one_line")
    user_output = {
        "mode": args.mode,
        "target_datetime": target_dt.isoformat(),
        "weather_model": model or "ecmwf_ifs",
        "forecast_confidence": confidence,
        "scope_mode": scope_meta["scope_mode"],
        "scope_coverage": scope_meta["scope_coverage"],
        "scope_reduction_reason": scope_meta["scope_reduction_reason"],
        "scope_guardrail": scope_meta["scope_guardrail"],
        "fetch_health": fetch_health,
        "decision_summary": decision_summary,
        "final_text_recommendation": final_text_recommendation,
        "top_region_advice": top_region_advice,
        "timing": {
            "elapsed_ms": elapsed_ms,
            "elapsed_seconds": round(elapsed_ms / 1000.0, 2),
        },
        "confidence_note": confidence_note_text,
        "budget": {"max_workers": args.max_workers, "max_stage2_points": args.max_stage2_points, "direct_stage2_threshold": args.direct_stage2_threshold, "top_n": args.top_n},
    }
    debug_output = {
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
    return {
        **user_output,
        **debug_output,
        "user_output": user_output,
        "debug_output": debug_output,
    }

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    province_polygons, prefecture_polygons = load_polygons(args.polygons_json, args.polygons_file)
    if args.boxes_json:
        boxes = parse_boxes(args.boxes_json)
    elif args.scope_preset:
        boxes = load_scope_preset(args.scope_preset, province_polygons=province_polygons)
    else:
        parser.error("--boxes-json is required unless --scope-preset is provided")
    target_dt = parse_target_datetime(args.target_datetime)

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

    county_polygons: Dict[str, MultiPolygon] = {}

    if args.multi_day_start_date and args.multi_day_days and args.multi_day_days > 1:
        start_date = datetime.fromisoformat(args.multi_day_start_date).date()
        base_time = target_dt.time()
        nightly_args = argparse.Namespace(**vars(args))
        day_jobs = []
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for day_offset in range(args.multi_day_days):
            day_dt = datetime.combine(start_date + timedelta(days=day_offset), base_time)
            if args.real_weather:
                available, latest_dt = check_date_availability(day_dt)
                if not available:
                    print(json.dumps({
                        "error": "date_out_of_range",
                        "message": f"Open-Meteo 实时预报最晚只支持查询 {latest_dt.date().isoformat()}（今天起 +{OPEN_METEO_HOURLY_WINDOW_DAYS} 天）。",
                        "target_date": day_dt.date().isoformat(),
                        "latest_available_date": latest_dt.date().isoformat(),
                    }, ensure_ascii=False), file=sys.stderr)
                    return
                days_ahead = (day_dt.date() - today.date()).days
                day_confidence = "high" if days_ahead <= 3 else "medium" if days_ahead <= 7 else "low"
            else:
                day_confidence = "mock"
            day_jobs.append((day_offset, day_dt, day_confidence))

        ordered_payloads: Dict[int, dict] = {}
        with ThreadPoolExecutor(max_workers=max(1, min(len(day_jobs), 3))) as executor:
            future_map = {
                executor.submit(build_daily_payload, nightly_args, boxes, province_polygons, prefecture_polygons, county_polygons, day_dt, day_confidence): day_offset
                for day_offset, day_dt, day_confidence in day_jobs
            }
            for future in as_completed(future_map):
                ordered_payloads[future_map[future]] = future.result()
        daily_payloads = [ordered_payloads[idx] for idx, _, _ in day_jobs]

        nightly_reply_lines = _multi_day_nightly_reply(daily_payloads)

        n = len(daily_payloads)
        fetch_notes = []
        for dp in daily_payloads:
            fh = dp.get("fetch_health") or {}
            if fh.get("status") == "degraded":
                fetch_notes.append(f"{dp.get('target_datetime','')[:10]}数据抓取缺失偏多")
        if fetch_notes:
            fetch_note = f"本次{', '.join(fetch_notes)}，结果更适合先看趋势，建议稍后再复查。"
        else:
            fetch_note = f"本次{n}晚，每晚已附带参考信息（云量、风速、湿度、夜间通透度、月光影响）；未直接查真实视宁度、实测光污染和具体机位遮挡，不适合作为机位级最终结论，建议出发前复查。"
        top_level_reference_note = f"本轮参考信息：本次{n}晚，每晚均已附带参考信息；未直接查真实视宁度、实测光污染和具体机位遮挡，更适合做区域级筛选，不适合直接当成机位级最终结论。"

        daily_best_regions = []
        for x in daily_payloads:
            ds = x.get("decision_summary") or {}
            ranked = ds.get("ranked_candidates") or []
            if ranked:
                best = ranked[0]
                daily_best_regions.append({
                    "date": x.get("target_datetime", "")[:10],
                    "region": best.get("display_label"),
                    "score": best.get("ranking_score"),
                })
            else:
                labels = x.get("region_labels") or []
                best = labels[0] if labels else {}
                if best:
                    daily_best_regions.append({
                        "date": x.get("target_datetime", "")[:10],
                        "region": best.get("display_label") or best.get("label"),
                        "score": round(_region_score(best), 2),
                    })
        multi_day_standard_reply = _multi_day_standard_reply(daily_payloads)
        multi_day_detailed_reply = "\n".join(nightly_reply_lines)
        multi_day_count = len(daily_payloads)

        multi_day_decision_summary = {
            "one_line": f"{MULTI_DAY_INTRO}，共 {multi_day_count} 晚；每晚单独给主推荐和备选，{MULTI_DAY_NO_ROUTE}。",
            "multi_day_refine_note": f"{MULTI_DAY_ROUTE_NOTE} 当前 skill 只保留逐晚独立推荐。",
            "reference_note": top_level_reference_note,
            "data_quality_note": fetch_note if fetch_notes else None,
            "daily_brief": nightly_reply_lines,
            "final_reply_draft": multi_day_detailed_reply,
            "reply_drafts": {
                "concise": f"这次按逐晚独立推荐，共 {multi_day_count} 晚分别给主推荐和备选；不做跨晚路线判断。",
                "standard": multi_day_standard_reply,
                "detailed": multi_day_detailed_reply,
            },
        }
        daily_candidate_regions = [
            {
                "date": x.get("target_datetime", "")[:10],
                "threshold": x.get("decision_summary", {}).get("daily_candidate_threshold"),
                "count": len(x.get("decision_summary", {}).get("ranked_candidates") or []),
                "candidates": [
                    {
                        "region": row.get("display_label"),
                        "score": row.get("ranking_score"),
                        "night_avg_cloud": row.get("night_avg_cloud"),
                        "night_worst_cloud": row.get("night_worst_cloud"),
                        "cloud_stability": row.get("cloud_stability"),
                        "usable_hours": row.get("usable_hours"),
                        "longest_usable_streak_hours": row.get("longest_usable_streak_hours"),
                        "night_avg_wind_kmh": row.get("night_avg_wind_kmh"),
                        "night_avg_humidity": row.get("night_avg_humidity_pct"),
                        "night_avg_visibility_m": row.get("night_avg_visibility_m"),
                        "night_avg_cloud_low": row.get("night_avg_cloud_low"),
                        "night_avg_cloud_mid": row.get("night_avg_cloud_mid"),
                        "night_avg_cloud_high": row.get("night_avg_cloud_high"),
                        "night_avg_dew_point": row.get("night_avg_dew_point_c"),
                        "night_max_precip": row.get("night_max_precip_mm") if row.get("night_max_precip_mm") is not None else row.get("night_max_precip"),
                        "low_cloud_terrain_note": row.get("low_cloud_terrain_note"),
                        "moon_interference": row.get("moon_interference"),
                        "light_pollution_bortle": row.get("light_pollution_bortle"),
                        "night_weather_codes": row.get("night_weather_codes"),
                    }
                    for row in (x.get("decision_summary", {}).get("ranked_candidates") or [])
                ],
            }
            for x in daily_payloads
        ]
        multi_status = "degraded" if any((x.get("fetch_health") or {}).get("status") == "degraded" for x in daily_payloads) else "partial" if any((x.get("fetch_health") or {}).get("status") == "partial" for x in daily_payloads) else "ok"
        user_output = {
            "multi_day_mode": True,
            "multi_day_start_date": args.multi_day_start_date,
            "multi_day_days": args.multi_day_days,
            "multi_day_dates": [x.get("target_datetime", "")[:10] for x in daily_payloads],
            "final_text_recommendation": multi_day_standard_reply,
            "budget": {
                "max_workers": nightly_args.max_workers,
                "max_stage2_points": nightly_args.max_stage2_points,
                "direct_stage2_threshold": nightly_args.direct_stage2_threshold,
                "top_n": nightly_args.top_n,
                "source_direct_stage2_threshold": args.direct_stage2_threshold,
                "nightly_pipeline": "shared-with-single-night",
            },
            "daily_best_regions": daily_best_regions,
            "daily_candidate_regions": daily_candidate_regions,
            "decision_summary": multi_day_decision_summary,
        }
        debug_output = {
            "daily_results": daily_payloads,
        }
        payload = {
            **user_output,
            **debug_output,
            "user_output": user_output,
            "debug_output": debug_output,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
        return

    payload = build_daily_payload(args, boxes, province_polygons, prefecture_polygons, county_polygons, target_dt, confidence)
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))

if __name__ == "__main__":
    main()
