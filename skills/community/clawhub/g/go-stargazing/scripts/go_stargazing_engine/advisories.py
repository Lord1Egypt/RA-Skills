from typing import List, Optional

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

def _moon_advisory(moon_interference: Optional[float]) -> str:
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
    if wind_kmh is None:
        return None
    if wind_kmh >= 40:
        return "风速较高（注意三脚架防风）"
    if wind_kmh >= 30:
        return "风速偏大，建议检查三脚架稳定性"
    return None

def _weather_code_advisory(codes: Optional[List[int]]) -> Optional[str]:
    if not codes:
        return None
    unique = sorted(set(codes))
    names = [_WEATHER_CODE_MAP.get(c, f"code({c})") for c in unique[:3]]
    if len(unique) == 1:
        return f"天气：{names[0]}"
    return f"天气：{'/'.join(names)}"

def _dew_point_advisory(dew_point_c: Optional[float], temp_c: Optional[float] = None) -> Optional[str]:
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
    if max_precip_mm is None:
        return None
    if max_precip_mm >= 5:
        return "有降水（注意防雨/雪）"
    if max_precip_mm >= 1:
        return "局部有弱降水"
    return None

def build_reference_info_note(moon_advisory: Optional[str] = None, light_pollution_note: Optional[str] = None, extra_indicators: Optional[List[str]] = None, no_candidates: bool = False) -> dict:
    used = ["云量", "风速", "湿度", "夜间通透度", "月光影响", "光污染粗估（城市距离法，非实测）"]
    if extra_indicators:
        used.extend(extra_indicators)
    omitted = ["真实视宁度", "实测光污染", "具体机位遮挡"]
    summary = "这轮主要看云量、风速、湿度、夜间通透度和月光影响。"
    suitable = "更适合做区域级筛选和判断值不值得继续细看"
    if extra_indicators:
        indicator_text = "、".join(dict.fromkeys(extra_indicators))
        summary = summary.rstrip("。") + f"；另外还参考了 {indicator_text}。"
    if no_candidates:
        summary = "这轮先按云量做粗筛，再尝试结合风速、湿度、夜间通透度和月光影响做细筛；但当前没有筛出达到推荐阈值的候选区域。"
        suitable = "更适合先判断这晚整体值不值得冲，不适合直接下具体区域结论"
    lunar_line = f"月光建议：{moon_advisory}" if moon_advisory else None
    note_parts = [f"本轮参考信息：{summary}"]
    if lunar_line:
        note_parts.append(lunar_line)
    if light_pollution_note:
        note_parts.append(f"光污染：{light_pollution_note}")
    note_parts.append(f"未直接查真实视宁度、实测光污染和具体机位遮挡，所以{ suitable }，不适合当成机位级最终结论。")
    note = " ".join(note_parts)
    short_parts = ["主要看云量、风、湿度、通透度和月光"]
    if no_candidates:
        short_parts.append("没筛出达到推荐阈值的候选区域")
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
        "no_candidates": no_candidates,
    }
