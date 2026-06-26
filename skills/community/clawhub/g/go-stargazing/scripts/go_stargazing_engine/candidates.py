from datetime import datetime
from typing import Dict, List, Optional, Tuple
from shapely.geometry import MultiPolygon

from .geo import add_province_context, cluster_centroid, cluster_label, cluster_points, _light_pollution_estimate
from .models import BoundingBox, SamplePoint
from .regions import build_region_brief_advice, build_region_human_view, region_decision_rank_score, region_qualification
from .scoring import classify_cloud_stability, derive_night_window, low_cloud_terrain_assessment


def summarize_cluster(cluster: List[SamplePoint], boxes: List[BoundingBox], target_date, prefecture_polygons: Optional[Dict[str, MultiPolygon]] = None, county_polygons: Optional[Dict[str, MultiPolygon]] = None) -> dict:
    provinces = sorted({p.province for p in cluster})
    label = cluster_label(cluster, boxes, prefecture_polygons=prefecture_polygons, county_polygons=county_polygons)
    label = add_province_context(label, provinces)
    lat, lng = cluster_centroid(cluster)
    lp_label, lp_note = _light_pollution_estimate(lat, lng)
    best = sorted(cluster, key=lambda p: (-(p.final_score or -1), p.night_avg_cloud if p.night_avg_cloud is not None else 999.0))[0]
    elevs = [p.elevation_m for p in cluster if p.elevation_m is not None]
    nc = [p.night_avg_cloud for p in cluster if p.night_avg_cloud is not None]
    nw = [p.night_worst_cloud for p in cluster if p.night_worst_cloud is not None]
    nh = [p.night_avg_humidity for p in cluster if p.night_avg_humidity is not None]
    nv = [p.night_avg_visibility for p in cluster if p.night_avg_visibility is not None]
    nwi = [p.night_avg_wind for p in cluster if p.night_avg_wind is not None]
    nt = [p.night_avg_temperature for p in cluster if p.night_avg_temperature is not None]
    ng = [p.night_max_gust for p in cluster if p.night_max_gust is not None]
    mi = [p.moon_interference for p in cluster if p.moon_interference is not None]
    uh = [p.usable_hours for p in cluster if p.usable_hours is not None]
    ls = [p.longest_usable_streak_hours for p in cluster if p.longest_usable_streak_hours is not None]
    cs = [p.cloud_stddev for p in cluster if p.cloud_stddev is not None]
    nd = [p.night_avg_dew_point for p in cluster if p.night_avg_dew_point is not None]
    np = [p.night_max_precip for p in cluster if p.night_max_precip is not None]
    ncl = [p.night_avg_cloud_low for p in cluster if p.night_avg_cloud_low is not None]
    ncm = [p.night_avg_cloud_mid for p in cluster if p.night_avg_cloud_mid is not None]
    nch = [p.night_avg_cloud_high for p in cluster if p.night_avg_cloud_high is not None]
    moon_scores = [p.moon_factor or 0.0 for p in cluster]

    astro_window = derive_night_window(lat, lng, target_date)
    astro_start_h, astro_end_h = astro_window
    astro_start_str = f"{astro_start_h % 24:02d}:00"
    astro_end_str = f"{astro_end_h % 24:02d}:00"

    avg_elevation_m = round(sum(elevs) / len(elevs), 0) if elevs else None
    night_avg_visibility_m = round(sum(nv) / len(nv), 0) if nv else None
    night_max_precip = max(np) if np else None
    low_cloud_assessment = low_cloud_terrain_assessment(
        round(sum(ncl) / len(ncl), 1) if ncl else None,
        round(sum(ncm) / len(ncm), 1) if ncm else None,
        round(sum(nch) / len(nch), 1) if nch else None,
        avg_elevation_m,
        night_avg_visibility_m,
        night_max_precip,
    )

    summary = {
        "label": label,
        "provinces": provinces,
        "cluster_size": len(cluster),
        "lat": round(lat, 5),
        "lng": round(lng, 5),
        "best_point_id": best.id,
        "final_score": round(sum((p.final_score or 0.0) for p in cluster) / len(cluster), 2),
        "best_score": best.final_score,
        "astronomical_night_start": astro_start_str,
        "astronomical_night_end": astro_end_str,
        "best_window_start": best.best_window_start,
        "best_window_end": best.best_window_end,
        "night_avg_cloud": round(sum(nc) / len(nc), 1) if nc else None,
        "night_worst_cloud": round(max(nw), 1) if nw else None,
        "night_avg_humidity": round(sum(nh) / len(nh), 1) if nh else None,
        "night_avg_humidity_pct": round(sum(nh) / len(nh), 1) if nh else None,
        "night_avg_visibility_m": night_avg_visibility_m,
        "night_avg_wind_kmh": round(sum(nwi) / len(nwi), 1) if nwi else None,
        "night_avg_temperature": round(sum(nt) / len(nt), 1) if nt else None,
        "night_avg_temperature_c": round(sum(nt) / len(nt), 1) if nt else None,
        "night_max_gust_kmh": round(max(ng), 1) if ng else None,
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
        "avg_elevation_m": avg_elevation_m,
        "members": [p.id for p in sorted(cluster, key=lambda x: x.id)],
        "night_avg_dew_point": round(sum(nd) / len(nd), 1) if nd else None,
        "night_avg_dew_point_c": round(sum(nd) / len(nd), 1) if nd else None,
        "night_max_precip": night_max_precip,
        "night_max_precip_mm": night_max_precip,
        "night_avg_cloud_low": round(sum(ncl) / len(ncl), 1) if ncl else None,
        "night_avg_cloud_mid": round(sum(ncm) / len(ncm), 1) if ncm else None,
        "night_avg_cloud_high": round(sum(nch) / len(nch), 1) if nch else None,
        "low_cloud_terrain_penalty": low_cloud_assessment.get("penalty"),
        "low_cloud_terrain_state": low_cloud_assessment.get("state"),
        "low_cloud_terrain_note": low_cloud_assessment.get("note"),
        "night_weather_codes": best.night_weather_codes,
        "light_pollution_bortle": lp_label,
        "light_pollution_note": lp_note,
    }
    summary["qualification"] = region_qualification(summary)
    summary["decision_rank_score"] = region_decision_rank_score(summary)
    summary["ranking_score"] = summary["decision_rank_score"]
    summary["score_semantics"] = "single-night-ranking"
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


def _best_photo_window_note(region: dict) -> Optional[str]:
    start = _humanize_iso_time(region.get("best_window_start"))
    end = _humanize_iso_time(region.get("best_window_end"))
    astro_start = _humanize_iso_time(region.get("astronomical_night_start"))
    astro_end = _humanize_iso_time(region.get("astronomical_night_end"))
    start, end = _clamp_window_to_astronomical_night(start, end, astro_start, astro_end)
    segment = region.get("best_window_segment")
    streak = region.get("longest_usable_streak_hours")
    if start and end:
        note = f"更值得守的是 {start}-{end} 这一段。"
        if streak is not None and streak < 2:
            note += " 但整晚窗口偏碎，不太像能轻松整晚守的类型。"
        elif segment:
            note += f" 整体更偏{segment}出窗口。"
        return note
    if segment:
        return f"这晚更偏{segment}出窗口，但没有特别完整的长时间可拍段。"
    return "整晚窗口比较碎，没有特别稳的长时间可拍段。"


def _wind_photo_note(region: dict) -> Optional[str]:
    gust = region.get("night_max_gust_kmh")
    avg_wind = region.get("night_avg_wind_kmh") or region.get("night_avg_wind")
    if gust is None and avg_wind is None:
        return None
    ref = gust if gust is not None else avg_wind
    if ref is None:
        return None
    if ref >= 35:
        return "阵风偏明显，三脚架和长曝光稳定性一般。"
    if ref >= 22:
        return "阵风有一点存在感，长曝光稳定性会受轻微影响。"
    return "夜里风相对稳，器材稳定性压力不大。"


def _dew_photo_note(region: dict) -> Optional[str]:
    temp = region.get("night_avg_temperature")
    dew = region.get("night_avg_dew_point")
    humidity = region.get("night_avg_humidity")
    if temp is None or dew is None:
        return None
    spread = temp - dew
    if spread <= 2 or (spread <= 3 and humidity is not None and humidity >= 90):
        return "夜里温度和露点接近，返潮风险高，建议提前做好防露。"
    if spread <= 4 or (spread <= 5 and humidity is not None and humidity >= 85):
        return "后半夜有一定返潮风险，建议留意镜头防露。"
    return "整晚结露风险较低，器材受潮压力不大。"


def build_photo_notes(region: Optional[dict]) -> dict:
    if not region:
        return {}
    notes = {
        "best_window": _best_photo_window_note(region),
        "wind": _wind_photo_note(region),
        "dew": _dew_photo_note(region),
    }
    return {k: v for k, v in notes.items() if v}


def build_weather_indicator_lines(region: Optional[dict]) -> List[str]:
    if not region:
        return []
    lines: List[str] = []

    astro_start = _humanize_iso_time(region.get("astronomical_night_start"))
    astro_end = _humanize_iso_time(region.get("astronomical_night_end"))
    best_start = _humanize_iso_time(region.get("best_window_start"))
    best_end = _humanize_iso_time(region.get("best_window_end"))
    clamped_best_start, clamped_best_end = _clamp_window_to_astronomical_night(best_start, best_end, astro_start, astro_end)
    if astro_start and astro_end:
        lines.append(f"- 天文夜窗：{astro_start}-{astro_end}")
    if clamped_best_start and clamped_best_end:
        lines.append(f"- 最佳可拍窗口：{clamped_best_start}-{clamped_best_end}")
    elif best_start and best_end:
        lines.append(f"- 最佳可拍窗口：{best_start}-{best_end}")

    usable_hours = region.get("usable_hours")
    longest_streak = region.get("longest_usable_streak_hours")
    if usable_hours is not None or longest_streak is not None:
        seg = []
        if usable_hours is not None:
            seg.append(f"可拍小时数 {usable_hours:.1f}h")
        if longest_streak is not None:
            seg.append(f"最长连续窗口 {longest_streak:.1f}h")
        lines.append(f"- 可拍时段：{'，'.join(seg)}")

    cloud_bits = []
    if region.get("night_avg_cloud") is not None:
        cloud_bits.append(f"夜间平均云量 {region['night_avg_cloud']:.1f}%")
    if region.get("night_worst_cloud") is not None:
        cloud_bits.append(f"最差时段云量 {region['night_worst_cloud']:.1f}%")
    if cloud_bits:
        lines.append(f"- 云量：{'，'.join(cloud_bits)}")

    layer_bits = []
    if region.get("night_avg_cloud_low") is not None:
        layer_bits.append(f"低云 {region['night_avg_cloud_low']:.1f}%")
    if region.get("night_avg_cloud_mid") is not None:
        layer_bits.append(f"中云 {region['night_avg_cloud_mid']:.1f}%")
    if region.get("night_avg_cloud_high") is not None:
        layer_bits.append(f"高云 {region['night_avg_cloud_high']:.1f}%")
    if layer_bits:
        lines.append(f"- 分层云覆盖：{'，'.join(layer_bits)}")

    wind_bits = []
    if region.get("night_avg_wind_kmh") is not None:
        wind_bits.append(f"夜间平均风速 {region['night_avg_wind_kmh']:.1f} km/h")
    if region.get("night_max_gust_kmh") is not None:
        wind_bits.append(f"夜间最大阵风 {region['night_max_gust_kmh']:.1f} km/h")
    if wind_bits:
        lines.append(f"- 风：{'，'.join(wind_bits)}")

    temp = region.get("night_avg_temperature_c") if region.get("night_avg_temperature_c") is not None else region.get("night_avg_temperature")
    dew = region.get("night_avg_dew_point_c") if region.get("night_avg_dew_point_c") is not None else region.get("night_avg_dew_point")
    humidity = region.get("night_avg_humidity_pct") if region.get("night_avg_humidity_pct") is not None else region.get("night_avg_humidity")
    thermo_bits = []
    if temp is not None:
        thermo_bits.append(f"夜间平均温度 {temp:.1f}℃")
    if dew is not None:
        thermo_bits.append(f"夜间平均露点 {dew:.1f}℃")
    if humidity is not None:
        thermo_bits.append(f"夜间平均湿度 {humidity:.1f}%")
    if thermo_bits:
        lines.append(f"- 温湿：{'，'.join(thermo_bits)}")

    if region.get("night_avg_visibility_m") is not None:
        lines.append(f"- 通透度：夜间平均能见度 {region['night_avg_visibility_m']:.0f} m")

    precip = region.get("night_max_precip_mm") if region.get("night_max_precip_mm") is not None else region.get("night_max_precip")
    weather_codes = region.get("night_weather_codes")
    precip_bits = []
    if precip is not None:
        precip_bits.append(f"夜间最大降水 {precip:.2f} mm/h")
    if weather_codes:
        precip_bits.append(f"天气现象码 {weather_codes}")
    if precip_bits:
        lines.append(f"- 天气现象：{'，'.join(precip_bits)}")

    moon_interference = region.get("moon_interference")
    if moon_interference is not None:
        lines.append(f"- 月光影响：{moon_interference:.1f}/100（数值越高干扰越低）")

    data_quality = region.get("weather_source")
    if data_quality:
        lines.append(f"- 数据来源：{data_quality}")
    return lines


def _select_ranked_candidate_regions(labels: List[dict], limit: int = 10, min_score: float = 70.0, relative_drop: float = 10.0) -> List[dict]:
    if not labels:
        return []
    ordered = sorted(labels, key=lambda x: (-(x.get("ranking_score") or x.get("decision_rank_score") or x.get("final_score") or 0.0), -(x.get("final_score") or 0.0), x.get("display_label") or x.get("label") or ""))
    top_score = ordered[0].get("ranking_score") or ordered[0].get("decision_rank_score") or ordered[0].get("final_score") or 0.0
    threshold = max(min_score, top_score - relative_drop)
    qualified = [row for row in ordered if row.get("qualification") in {"recommended", "backup"}]
    selected = [
        row for row in qualified
        if ((row.get("ranking_score") or row.get("decision_rank_score") or row.get("final_score") or 0.0) >= threshold)
    ]
    min_keep = min(3, len(qualified))
    if len(selected) < min_keep:
        seen = {id(row) for row in selected}
        for row in qualified:
            if id(row) in seen:
                continue
            selected.append(row)
            seen.add(id(row))
            if len(selected) >= min_keep:
                break

    if not selected:
        judgement_rank = {"共识推荐": 0, "备选": 1, "单模型亮点": 2, "争议区": 3, "不建议": 4}
        non_reject = sorted(
            [row for row in ordered if row.get("judgement") in {"共识推荐", "备选", "单模型亮点"}],
            key=lambda x: (
                judgement_rank.get(x.get("judgement"), 9),
                -(x.get("ranking_score") or x.get("decision_rank_score") or x.get("final_score") or 0.0),
                x.get("display_label") or x.get("label") or "",
            ),
        )
        selected = non_reject[: min(3, len(non_reject))]

    if not selected:
        selected = ordered[: min(3, len(ordered))]
    return selected[:limit]


def build_ranked_candidates(labels: List[dict], limit: int = 10, min_score: float = 70.0, relative_drop: float = 10.0) -> List[dict]:
    selected = _select_ranked_candidate_regions(labels, limit=limit, min_score=min_score, relative_drop=relative_drop)
    if not selected:
        return []
    ranked: List[dict] = []
    for idx, region in enumerate(selected, 1):
        label = region.get("display_label") or region.get("label") or "?"
        refined_label = region.get("refined_label") or region.get("label") or label
        astro_start = _humanize_iso_time(region.get("astronomical_night_start"))
        astro_end = _humanize_iso_time(region.get("astronomical_night_end"))
        bw_start = _humanize_iso_time(region.get("best_window_start"))
        bw_end = _humanize_iso_time(region.get("best_window_end"))
        bw_start, bw_end = _clamp_window_to_astronomical_night(bw_start, bw_end, astro_start, astro_end)
        ranked.append({
            "rank": idx,
            "display_label": label,
            "refined_label": refined_label,
            "ranking_score": round(region.get("ranking_score") or region.get("decision_rank_score") or region.get("final_score") or 0.0, 2),
            "weather_score": round(region.get("final_score") or 0.0, 2),
            "best_window_start": bw_start,
            "best_window_end": bw_end,
            "astronomical_night_start": astro_start,
            "astronomical_night_end": astro_end,
            "usable_hours": region.get("usable_hours"),
            "longest_usable_streak_hours": region.get("longest_usable_streak_hours"),
            "cloud_stability": region.get("cloud_stability"),
            "night_avg_cloud": region.get("night_avg_cloud"),
            "night_worst_cloud": region.get("night_worst_cloud"),
            "night_avg_cloud_low": region.get("night_avg_cloud_low"),
            "night_avg_cloud_mid": region.get("night_avg_cloud_mid"),
            "night_avg_cloud_high": region.get("night_avg_cloud_high"),
            "night_avg_wind_kmh": region.get("night_avg_wind_kmh"),
            "night_max_gust_kmh": region.get("night_max_gust_kmh"),
            "night_avg_temperature_c": region.get("night_avg_temperature"),
            "night_avg_dew_point_c": region.get("night_avg_dew_point"),
            "night_avg_humidity_pct": region.get("night_avg_humidity"),
            "night_avg_visibility_m": region.get("night_avg_visibility_m"),
            "night_max_precip_mm": region.get("night_max_precip"),
            "night_weather_codes": region.get("night_weather_codes"),
            "low_cloud_terrain_note": region.get("low_cloud_terrain_note"),
            "moon_interference": region.get("moon_interference"),
            "light_pollution_bortle": region.get("light_pollution_bortle"),
            "avg_elevation_m": region.get("avg_elevation_m"),
            "brief_advice": region.get("brief_advice"),
        })
    return ranked


def build_ranked_candidate_lines(ranked_candidates: List[dict]) -> List[str]:
    if not ranked_candidates:
        return []
    lines: List[str] = []
    for row in ranked_candidates:
        lines.append(f"- {row['rank']}. {row['display_label']}（{row['ranking_score']:.2f}分）")
        if row.get("best_window_start") and row.get("best_window_end"):
            lines.append(f"  - 最佳窗口：{row['best_window_start']}-{row['best_window_end']}")
        if row.get("usable_hours") is not None:
            lines.append(f"  - 可拍时段：{row['usable_hours']:.1f}h")
        if row.get("longest_usable_streak_hours") is not None:
            lines.append(f"  - 最长连续窗口：{row['longest_usable_streak_hours']:.1f}h")
        cloud_parts = []
        if row.get("night_avg_cloud") is not None:
            cloud_parts.append(f"平均云量 {row['night_avg_cloud']:.1f}%")
        if row.get("night_worst_cloud") is not None:
            cloud_parts.append(f"最差云量 {row['night_worst_cloud']:.1f}%")
        if cloud_parts:
            lines.append(f"  - 云况：{'，'.join(cloud_parts)}")
        layer_parts = []
        if row.get("night_avg_cloud_low") is not None:
            layer_parts.append(f"低云 {row['night_avg_cloud_low']:.1f}%")
        if row.get("night_avg_cloud_mid") is not None:
            layer_parts.append(f"中云 {row['night_avg_cloud_mid']:.1f}%")
        if row.get("night_avg_cloud_high") is not None:
            layer_parts.append(f"高云 {row['night_avg_cloud_high']:.1f}%")
        if layer_parts:
            lines.append(f"  - 云层分布：{'，'.join(layer_parts)}")
        wind_parts = []
        if row.get("night_avg_wind_kmh") is not None:
            wind_parts.append(f"平均风 {row['night_avg_wind_kmh']:.1f} km/h")
        if row.get("night_max_gust_kmh") is not None:
            wind_parts.append(f"最大阵风 {row['night_max_gust_kmh']:.1f} km/h")
        if wind_parts:
            lines.append(f"  - 风况：{'，'.join(wind_parts)}")
        thermo_parts = []
        if row.get("night_avg_temperature_c") is not None:
            thermo_parts.append(f"温度 {row['night_avg_temperature_c']:.1f}℃")
        if row.get("night_avg_dew_point_c") is not None:
            thermo_parts.append(f"露点 {row['night_avg_dew_point_c']:.1f}℃")
        if row.get("night_avg_humidity_pct") is not None:
            thermo_parts.append(f"湿度 {row['night_avg_humidity_pct']:.1f}%")
        if thermo_parts:
            lines.append(f"  - 温湿：{'，'.join(thermo_parts)}")
        if row.get("night_avg_visibility_m") is not None:
            lines.append(f"  - 能见度：{row['night_avg_visibility_m']:.0f} m")
        if row.get("moon_interference") is not None:
            lines.append(f"  - 月光影响：{row['moon_interference']:.1f} / 100")
        if row.get("light_pollution_bortle"):
            lines.append(f"  - 光污染：{row['light_pollution_bortle']}")
        if row.get("night_max_precip_mm") is not None:
            lines.append(f"  - 夜间最大降水：{row['night_max_precip_mm']:.2f} mm/h")
        if row.get("night_weather_codes"):
            lines.append(f"  - 天气现象码：{row['night_weather_codes']}")
        if row.get("low_cloud_terrain_note"):
            lines.append(f"  - 低云地形说明：{row['low_cloud_terrain_note']}")
    return lines


def build_backup_photo_diff(primary: Optional[dict], backup: Optional[dict]) -> Optional[str]:
    if not backup:
        return None
    backup_label = backup.get("display_label") or backup.get("label") or "备选区域"
    primary_streak = primary.get("longest_usable_streak_hours") if primary else None
    backup_streak = backup.get("longest_usable_streak_hours")
    primary_gust = primary.get("night_max_gust_kmh") if primary else None
    backup_gust = backup.get("night_max_gust_kmh")
    primary_temp = primary.get("night_avg_temperature") if primary else None
    primary_dew = primary.get("night_avg_dew_point") if primary else None
    backup_temp = backup.get("night_avg_temperature")
    backup_dew = backup.get("night_avg_dew_point")
    primary_segment = primary.get("best_window_segment") if primary else None
    backup_segment = backup.get("best_window_segment")

    if backup_streak is not None and primary_streak is not None and backup_streak >= primary_streak + 1.0:
        return f"{backup_label} 的连续窗口更完整，更适合长一点的守候。"
    if backup_segment and backup_segment != primary_segment:
        return f"{backup_label} 更偏{backup_segment}出窗口。"
    if backup_gust is not None and primary_gust is not None and backup_gust <= primary_gust - 3:
        return f"{backup_label} 的风况相对更稳。"
    if None not in (primary_temp, primary_dew, backup_temp, backup_dew):
        primary_spread = primary_temp - primary_dew
        backup_spread = backup_temp - backup_dew
        if backup_spread >= primary_spread + 1.5:
            return f"{backup_label} 的返潮压力相对更小。"
    if backup_segment:
        return f"{backup_label} 更适合当作{backup_segment}窗口的备选。"
    return None


def aggregate_labels(points: List[SamplePoint], boxes: List[BoundingBox], top_n: int, cluster_km: float, target_date, prefecture_polygons: Optional[Dict[str, MultiPolygon]] = None, county_polygons: Optional[Dict[str, MultiPolygon]] = None, confidence: Optional[str] = None) -> List[dict]:
    if not points:
        return []
    clusters = cluster_points(points, cluster_km=cluster_km)
    summaries = [summarize_cluster(c, boxes, target_date, prefecture_polygons=prefecture_polygons, county_polygons=county_polygons) for c in clusters]
    summaries.sort(key=lambda x: (-(x.get("ranking_score") or x["decision_rank_score"]), -x["final_score"], x["avg_cloud_cover"], x["label"]))
    summaries = summaries[:top_n]
    for region in summaries:
        region["brief_advice"] = build_region_brief_advice(region, confidence=confidence)
    return summaries
