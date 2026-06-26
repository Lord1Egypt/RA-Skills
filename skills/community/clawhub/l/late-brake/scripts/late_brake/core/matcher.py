# -*- coding: utf-8 -*-
"""
Late Brake - Automatic Track Matcher

根据GPS轨迹自动匹配已配置赛道
基于锚点位置匹配：计算轨迹中心点与所有赛道锚点距离，选择距离小于锚点半径的赛道

US-017 验收条件：
1. ✓ 根据导入的GPS轨迹，自动与所有已配置赛道进行匹配
2. ✓ 基于锚点范围判断，确定匹配结果
3. ✓ 匹配成功自动关联赛道信息，继续后续处理
4. ✓ 匹配失败（无匹配/多个匹配）输出明确错误提示
5. ✓ 支持 --json 输出匹配结果
"""

from typing import List, Optional, Tuple
from geographiclib.geodesic import Geodesic

from late_brake.models import Track, DataPoint
from late_brake.io.track_store import list_all_tracks


geod = Geodesic.WGS84


def calculate_centroid(points: List[DataPoint]) -> Tuple[float, float]:
    """计算轨迹点的中心点（平均经纬度）"""
    if not points:
        return 0.0, 0.0

    # 球面平均比较复杂，这里用简单平均足够匹配使用
    # 对于赛道匹配来说，误差在几百米不影响，因为锚点半径通常>1km
    lat_sum = sum(p.latitude for p in points)
    lon_sum = sum(p.longitude for p in points)
    n = len(points)
    return lat_sum / n, lon_sum / n


def match_track(points: List[DataPoint]) -> Tuple[Optional[Track], str]:
    """
    自动匹配赛道
    返回 (匹配到的赛道, 信息消息)
    如果无匹配或多个匹配，返回 (None, 错误信息)
    """
    if not points:
        return None, "没有有效的GPS数据，无法匹配赛道"

    centroid_lat, centroid_lon = calculate_centroid(points)
    all_tracks = list_all_tracks()

    if not all_tracks:
        return None, "没有已配置的赛道，请先添加赛道"

    candidates: List[Track] = []

    for track in all_tracks:
        anchor = track.anchor
        result = geod.Inverse(
            centroid_lat, centroid_lon,
            anchor.lat, anchor.lon
        )
        distance_m = result["s12"]
        if distance_m <= anchor.radius_m:
            candidates.append(track)

    if len(candidates) == 0:
        return None, (
            "没有找到匹配的赛道。\n"
            "请使用 --track <track-id> 手动指定赛道。"
        )
    elif len(candidates) == 1:
        return candidates[0], f"自动匹配成功: {candidates[0].id} - {candidates[0].name}"
    else:
        # 多个匹配
        track_list = ", ".join(f"{t.id} ({t.name})" for t in candidates)
        return None, (
            f"匹配到多个赛道: {track_list}\n"
            "请使用 --track <track-id> 手动指定。"
        )
