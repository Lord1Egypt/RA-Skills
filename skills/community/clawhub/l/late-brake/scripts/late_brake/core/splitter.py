# -*- coding: utf-8 -*-
"""
Late Brake - Automatic Lap Splitter

根据赛道起终点线自动分割单圈

US-005 验收条件：
1. ✓ 根据赛道定义的起终点线gate坐标，自动判断车辆何时通过起跑线
2. ✓ 能够识别完整圈和不完整圈，标记 is_complete 字段
3. ✓ 每圈正确计算 start_time/end_time, start_distance/end_distance, total_time, lap_distance
4. ✓ 能够处理多圈连续数据，正确切分出每个独立单圈
5. ✓ 无法匹配赛道时给出明确错误提示
6. ✓ 支持 --track 参数强制指定赛道分割
"""

from typing import List, Tuple
from geographiclib.geodesic import Geodesic

from late_brake.models import Track, Lap, DataPoint


geod = Geodesic.WGS84


def point_to_line_distance(
    lat: float,
    lon: float,
    gate_start_lat: float,
    gate_start_lon: float,
    gate_end_lat: float,
    gate_end_lon: float
) -> float:
    """
    计算点到起终点线（线段）的最短距离（米）
    使用 geographiclib  geodesic 计算
    """
    # 起点到点
    res1 = geod.Inverse(gate_start_lat, gate_start_lon, lat, lon)
    d1 = res1["s12"]
    azi1 = res1["azi1"]

    # 终点到点
    res2 = geod.Inverse(gate_end_lat, gate_end_lon, lat, lon)
    d2 = res2["s12"]

    # 线段长度
    res_gate = geod.Inverse(gate_start_lat, gate_start_lon, gate_end_lat, gate_end_lon)
    L = res_gate["s12"]
    azi_gate = res_gate["azi1"]

    if L == 0:
        return (d1 + d2) / 2

    # 计算点到线段距离，球面三角近似
    # 参考: https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#On_a_sphere

    res = geod.Inverse(gate_start_lat, gate_start_lon, lat, lon)
    alpha1 = azi_gate - res["azi1"]
    sigma1 = res["a12"] * res["s12"] / res["a12"] if res["a12"] != 0 else 0

    # 点在线段投影后的距离
    x = (res["s12"] * res["s12"] + L * L - d2 * d2) / (2 * L)
    if x < 0:
        return d1
    if x > L:
        return d2

    # 垂距 - 用 math 近似，足够精确
    import math
    h = res["s12"] * abs(math.asin(math.sin(math.radians(alpha1)) * math.cos(math.radians(sigma1))))
    return abs(h)


def side_of_line(
    lat: float,
    lon: float,
    gate_start_lat: float,
    gate_start_lon: float,
    gate_end_lat: float,
    gate_end_lon: float
) -> int:
    """
    判断点在gate线的哪一侧
    返回: +1 或 -1，表示方向
    使用方位角判断
    """
    # 计算起点->终点方位，起点->点方位
    res = geod.Inverse(gate_start_lat, gate_start_lon, gate_end_lat, gate_end_lon)
    azi_gate = res["azi1"]

    res2 = geod.Inverse(gate_start_lat, gate_start_lon, lat, lon)
    azi_point = res2["azi1"]

    delta = azi_point - azi_gate
    # normalize to [-180, 180]
    while delta > 180:
        delta -= 360
    while delta < -180:
        delta += 360

    return 1 if delta > 0 else -1


def split_laps(
    points: List[DataPoint],
    track: Track,
    source_file: str,
    min_lap_time_sec: float = 30.0
) -> List[Lap]:
    """
    根据gate线自动分割单圈
    :param points: 所有数据点
    :param track: 赛道信息
    :param source_file: 源文件路径，用于Lap ID生成
    :param min_lap_time_sec: 最小圈时，避免噪声误检测
    :return: 分割后的Lap列表
    """
    if len(points) < 2:
        return []

    # gate线两个端点
    (gate_start_lat, gate_start_lon) = track.gate[0]
    (gate_end_lat, gate_end_lon) = track.gate[1]

    laps: List[Lap] = []
    crossings: List[Tuple[int, DataPoint]] = []  # 存储穿越点索引和点信息

    last_side = None
    lap_number = 0

    # 遍历所有点，检测穿越
    for i, point in enumerate(points):
        current_side = side_of_line(
            point.latitude, point.longitude,
            gate_start_lat, gate_start_lon,
            gate_end_lat, gate_end_lon
        )

        if last_side is not None and current_side != last_side:
            # 方向改变，可能发生了穿越
            # 检查距离gate线足够近（避免远侧穿越误判）
            dist = point_to_line_distance(
                point.latitude, point.longitude,
                gate_start_lat, gate_start_lon,
                gate_end_lat, gate_end_lon
            )
            if dist < 5.0:  # 5米阈值
                # 确认穿越
                crossings.append((i, point))

        last_side = current_side

    # 现在根据穿越点切分圈
    # 我们只保留行驶方向正确的穿越（这里简化，只要穿越就算，后续根据圈时过滤）
    if not crossings:
        return []

    # 先处理开头不完整圈（第一个穿越前）
    if crossings:
        first_cross_idx, first_cross_point = crossings[0]
        # 特殊情况：只有一次穿越，且第一个穿越就在末尾 → 整个圈是完整的，起点在开头，不需要插入不完整圈
        if len(crossings) == 1 and (len(points) - first_cross_idx) <= 10:
            # 不插入开头不完整圈，留给后面特殊情况处理
            pass
        elif first_cross_idx > 0:
            # 有数据在第一个穿越前，且这不是末尾穿越 → 这是不完整圈
            points_before = points[:first_cross_idx]
            if len(points_before) >= 10:  # 至少有10个点才算一个不完整圈
                lap_number += 1
                first_point = points_before[0]
                last_point = points_before[-1]
                lap = Lap(
                    id=f"{source_file}.Lap{lap_number}",
                    source_file=source_file,
                    lap_number=lap_number,
                    total_time=last_point.timestamp - first_point.timestamp,
                    start_time=first_point.timestamp,
                    end_time=last_point.timestamp,
                    start_distance=first_point.distance,
                    end_distance=last_point.distance,
                    is_complete=False,
                    lap_distance=last_point.distance - first_point.distance,
                    points=points_before
                )
                # 插到最前面
                laps.insert(0, lap)

    # 切分各圈
    # 情况1：多个穿越点，正常切分完整圈
    for cross_idx in range(len(crossings) - 1):
        start_idx, start_point = crossings[cross_idx]
        end_idx, end_point = crossings[cross_idx + 1]

        lap_number += 1
        lap_points = points[start_idx:end_idx]

        if not lap_points:
            continue

        total_time = end_point.timestamp - start_point.timestamp
        if total_time < min_lap_time_sec:
            # 圈时太短，可能是连续误穿越，跳过
            continue

        lap = Lap(
            id=f"{source_file}.Lap{lap_number}",
            source_file=source_file,
            lap_number=lap_number,
            total_time=total_time,
            start_time=start_point.timestamp,
            end_time=end_point.timestamp,
            start_distance=start_point.distance,
            end_distance=end_point.distance,
            is_complete=True,
            lap_distance=end_point.distance - start_point.distance,
            points=lap_points
        )
        laps.append(lap)

    # 情况2：只有一次穿越，且穿越点在末尾附近 → 数据从起点开始，冲线后结束，是单圈飞行圈
    if len(crossings) == 1:
        cross_idx, cross_point = crossings[0]
        # 如果第一个穿越点就是终点，说明起点在数据开头，冲线结束
        if cross_idx > 10 and (len(points) - cross_idx) <= 10 and len(laps) == 0:
            lap_number += 1
            lap_points = points[0:cross_idx + 1]
            total_time = cross_point.timestamp - lap_points[0].timestamp
            if total_time >= min_lap_time_sec:
                # 这就是完整单圈：从起跑线静止起步，冲线结束
                lap = Lap(
                    id=f"{source_file}.Lap{lap_number}",
                    source_file=source_file,
                    lap_number=lap_number,
                    total_time=total_time,
                    start_time=lap_points[0].timestamp,
                    end_time=cross_point.timestamp,
                    start_distance=lap_points[0].distance,
                    end_distance=cross_point.distance,
                    is_complete=True,
                    lap_distance=cross_point.distance - lap_points[0].distance,
                    points=lap_points
                )
                laps.append(lap)

    # 处理结尾不完整圈（最后一个穿越后）
    if crossings:
        last_cross_idx, last_cross_point = crossings[-1]
        if last_cross_idx < len(points) - 10:
            # 有数据在最后一个穿越后，这是不完整圈
            points_after = points[last_cross_idx:]
            lap_number += 1
            first_point = points_after[0]
            last_point = points_after[-1]
            lap = Lap(
                id=f"{source_file}.Lap{lap_number}",
                source_file=source_file,
                lap_number=lap_number,
                total_time=last_point.timestamp - first_point.timestamp,
                start_time=first_point.timestamp,
                end_time=last_point.timestamp,
                start_distance=first_point.distance,
                end_distance=last_point.distance,
                is_complete=False,
                lap_distance=last_point.distance - first_point.distance,
                points=points_after
            )
            laps.append(lap)

    # 重新编号，保持连续
    for idx, lap in enumerate(laps, 1):
        lap.lap_number = idx
        lap.id = f"{source_file}.Lap{idx}"

    return laps
