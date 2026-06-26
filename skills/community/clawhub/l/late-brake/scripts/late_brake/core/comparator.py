# -*- coding: utf-8 -*-
"""
Late Brake - Lap Comparator

对比两个圈速数据，计算时间差和速度差

US-007 / US-008 / US-009 / US-020 基础对比功能
"""

from typing import List, Tuple, Optional, Dict
import numpy as np

from late_brake.models import Track, Lap, DataPoint


def resample_lap(lap: Lap, step_m: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    按距离对圈速数据重采样
    返回 (distance数组, speed数组)
    distance: 0 ~ lap_distance，每 step_m 一个点
    """
    # 提取原始距离和速度
    distances = np.array([p.distance - lap.start_distance for p in lap.points])
    speeds = np.array([p.speed for p in lap.points])

    # 创建采样点
    total_dist = lap.lap_distance
    num_steps = int(np.floor(total_dist / step_m)) + 1
    sample_distances = np.linspace(0, total_dist, num_steps)

    # 线性插值
    sample_speeds = np.interp(sample_distances, distances, speeds)

    return sample_distances, sample_speeds


def get_speed_at_distance(lap: Lap, target_dist_abs: float) -> float:
    """
    在圈中找到给定绝对距离（相对于赛道起点）对应的速度
    通过线性插值得到更准确的速度
    """
    # 转换为相对于单圈起点的距离
    # target_dist_abs: 距离赛道起点的米数
    # lap.start_distance: 单圈起点距离整个文件起点的米数
    target_dist = target_dist_abs

    # 目标距离已经是赛道起点为0，单圈起点距离赛道起点是 0，所以不需要再减 lap.start_distance
    # lap.start_distance 是相对于整个文件起点，不是赛道起点

    # 如果超出范围，返回边界速度
    if target_dist <= 0:
        return lap.points[0].speed if lap.points else 0.0
    if target_dist >= lap.lap_distance:
        return lap.points[-1].speed if lap.points else 0.0

    # 找到包围目标距离的两个点
    prev_point = None
    next_point = None

    for p in lap.points:
        dist = p.distance - lap.start_distance
        if dist <= target_dist:
            prev_point = p
        if dist >= target_dist and next_point is None:
            next_point = p
            break

    if prev_point is None:
        return next_point.speed if next_point else 0.0
    if next_point is None:
        return prev_point.speed

    if prev_point is next_point:
        return prev_point.speed

    # 线性插值
    prev_dist = prev_point.distance - lap.start_distance
    next_dist = next_point.distance - lap.start_distance
    factor = (target_dist - prev_dist) / (next_dist - prev_dist)
    speed = prev_point.speed + factor * (next_point.speed - prev_point.speed)

    return speed


def sector_avg_speed(lap: Lap, start_dist: float, end_dist: float, distance: float) -> float:
    """
    计算分段平均速度 (km/h)
    distance 是分段长度（米）
    """
    time = sector_time(lap, start_dist, end_dist)
    if time <= 0:
        return 0.0
    # 距离米 / 时间秒 × 3.6 → km/h
    return (distance / time) * 3.6


def compare_laps(
    lap1: Lap,
    lap2: Lap,
    track: Optional[Track] = None,
    step_m: float = 1.0
) -> Dict:
    """
    对比两个圈，返回对比结果
    包含：总时间差、分段时间差、分段速度差、弯道时间/速度对比
    所有浮点数字段遵循US-040精度约定
    """
    result = {
        "lap1": {
            "number": lap1.lap_number,
            "total_time": round(lap1.total_time, 4),
            "distance": round(lap1.lap_distance, 2),
        },
        "lap2": {
            "number": lap2.lap_number,
            "total_time": round(lap2.total_time, 4),
            "distance": round(lap2.lap_distance, 2),
        },
        "total_time_diff": round(lap2.total_time - lap1.total_time, 4),
        "sector_diff": [],
        "turn_diff": [],
    }

    # 重采样对齐
    dist1, speed1 = resample_lap(lap1, step_m)
    dist2, speed2 = resample_lap(lap2, step_m)

    # 计算整体平均速度差异统计
    min_len = min(len(dist1), len(dist2))
    speed_diff = speed2[:min_len] - speed1[:min_len]
    result["avg_speed_diff"] = round(float(np.mean(speed_diff)), 2)

    # 如果有赛道分段，计算分段时间差和平均速度差
    if track is not None and track.sectors is not None:
        for sector in track.sectors:
            # 在原始圈中计算分段时间
            t1 = sector_time(lap1, sector.start_distance_m, sector.end_distance_m)
            t2 = sector_time(lap2, sector.start_distance_m, sector.end_distance_m)
            # 计算分段平均速度
            sector_dist = sector.end_distance_m - sector.start_distance_m
            av1 = sector_avg_speed(lap1, sector.start_distance_m, sector.end_distance_m, sector_dist)
            av2 = sector_avg_speed(lap2, sector.start_distance_m, sector.end_distance_m, sector_dist)
            result["sector_diff"].append({
                "sector_id": sector.id,
                "sector_name": sector.name,
                "start_distance": round(sector.start_distance_m, 2),
                "end_distance": round(sector.end_distance_m, 2),
                "time1": round(t1, 4),
                "time2": round(t2, 4),
                "time_diff": round(t2 - t1, 4),
                "avg_speed1": round(av1, 2),
                "avg_speed2": round(av2, 2),
                "avg_speed_diff": round(av2 - av1, 2),
            })

    # 如果有赛道弯道信息，计算每个弯道的对比
    if track is not None and track.turns is not None:
        for turn in track.turns:
            # 计算弯道时间
            t1 = sector_time(lap1, turn.start_distance_m, turn.end_distance_m)
            t2 = sector_time(lap2, turn.start_distance_m, turn.end_distance_m)
            # 获取各特征点速度
            se1 = get_speed_at_distance(lap1, turn.start_distance_m)
            se2 = get_speed_at_distance(lap2, turn.start_distance_m)
            ap1 = get_speed_at_distance(lap1, turn.apex_distance_m)
            ap2 = get_speed_at_distance(lap2, turn.apex_distance_m)
            ex1 = get_speed_at_distance(lap1, turn.end_distance_m)
            ex2 = get_speed_at_distance(lap2, turn.end_distance_m)
            # 计算弯道平均速度
            turn_dist = turn.end_distance_m - turn.start_distance_m
            av1 = sector_avg_speed(lap1, turn.start_distance_m, turn.end_distance_m, turn_dist)
            av2 = sector_avg_speed(lap2, turn.start_distance_m, turn.end_distance_m, turn_dist)
            # 存入结果
            result["turn_diff"].append({
                "turn_name": turn.name,
                "turn_type": turn.type,
                "start_distance": round(turn.start_distance_m, 2),
                "apex_distance": round(turn.apex_distance_m, 2),
                "end_distance": round(turn.end_distance_m, 2),
                "time1": round(t1, 4),
                "time2": round(t2, 4),
                "time_diff": round(t2 - t1, 4),
                "speed_entry1": round(se1, 2),
                "speed_entry2": round(se2, 2),
                "speed_entry_diff": round(se2 - se1, 2),
                "speed_apex1": round(ap1, 2),
                "speed_apex2": round(ap2, 2),
                "speed_apex_diff": round(ap2 - ap1, 2),
                "speed_exit1": round(ex1, 2),
                "speed_exit2": round(ex2, 2),
                "speed_exit_diff": round(ex2 - ex1, 2),
                "avg_speed1": round(av1, 2),
                "avg_speed2": round(av2, 2),
                "avg_speed_diff": round(av2 - av1, 2),
            })

    return result


def sector_time(lap: Lap, start_dist: float, end_dist: float) -> float:
    """
    计算圈在某分段（从start_dist到end_dist）所花时间
    """
    # 找到起点和终点
    start_point = None
    end_point = None

    for p in lap.points:
        dist_abs = p.distance - lap.start_distance
        if start_point is None and dist_abs >= start_dist:
            start_point = p
        if end_point is None and dist_abs >= end_dist:
            end_point = p
            break

    if start_point is None:
        return 0.0
    if end_point is None:
        if lap.points:
            end_point = lap.points[-1]
        else:
            return 0.0

    return end_point.timestamp - start_point.timestamp
