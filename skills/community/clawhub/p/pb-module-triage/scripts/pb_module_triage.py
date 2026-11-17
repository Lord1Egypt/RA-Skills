#!/usr/bin/env python3
"""Triage BrainNode TotalDataCore protobuf recordings by module evidence."""

from __future__ import annotations

import argparse
import bisect
import json
import math
import re
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.message import DecodeError


BUFFER_SPECS = (
    ("data_core_frames_buffer", "DataCoreFrame", "data_core", "raw sensors"),
    ("perceptor_frames_buffer", "PerceptorFrame", "perception", "lidar perception"),
    ("camera_perceptor_frames_buffer", "CameraPerceptorFrame", "camera_perception", "camera perception"),
    ("contextor_frames_buffer", "ContextInfo", "localization_contextor", "localization/contextor"),
    ("tasker_frames_buffer", "TaskerFrame", "planning_tasker", "task planning"),
    ("controller_frames_buffer", "Controller", "control", "control command"),
    ("data_chassis_frames_buffer", "DataCahssisFrame", "chassis", "chassis feedback"),
    ("data_chassis_status_frames_buffer", "DataCahssisFrame", "chassis", "chassis status"),
    ("stormer_frames_buffer", "DataStormFrame", "task_dispatch", "task dispatch"),
    ("state_management_buffer", "StateManagement", "state_management", "state management"),
    ("diagnostics_frames_buffer", "DiagnosticsFrame", "diagnostics", "diagnostics"),
)

ISSUE_KEYWORDS = {
    "data_core": (
        "pb", "record", "data", "sensor", "raw", "lidar", "h264", "rangeframe",
        "imu", "gps", "pointcloud", "point cloud", "timestamp", "drop", "missing",
        "数据", "录制", "传感器", "点云", "雷达", "相机", "图像", "丢帧", "时间戳",
    ),
    "perception": (
        "perception", "perceptor", "obstacle", "object", "dynamic", "static", "sem",
        "ground", "boundary", "detect", "lidar", "避障", "障碍", "感知", "漏检",
        "误检", "大车", "行人", "目标", "地面", "边界",
    ),
    "camera_perception": (
        "camera", "image", "segment", "bbox", "视觉", "相机", "图像", "车道线",
        "分割", "框", "标定",
    ),
    "localization_contextor": (
        "localization", "contextor", "relocal", "slam", "odom", "map", "pose",
        "drift", "jump", "residual", "confidence", "定位", "重定位", "漂", "飘",
        "跳", "丢定位", "地图", "位姿", "匹配", "残差",
    ),
    "planning_tasker": (
        "planning", "planner", "tasker", "path", "trajectory", "route", "mppi",
        "ccpp", "coverage", "roi", "uturn", "规划", "路径", "轨迹", "路线",
        "卡住", "绕行", "不走", "到不了", "清扫", "掉头", "画龙",
    ),
    "control": (
        "control", "controller", "steer", "steering", "brake", "eps", "speed",
        "tracking", "lateral", "控制", "方向盘", "转向", "刹车", "速度慢",
        "跟踪", "横向", "抖动", "振荡",
    ),
    "chassis": (
        "chassis", "gear", "emergency", "bumper", "touch", "wheel", "bms",
        "battery", "底盘", "档位", "急停", "防撞条", "轮速", "电池", "刹车",
    ),
    "task_dispatch": (
        "stormer", "dispatch", "task", "nav_task", "poi", "destination",
        "map version", "任务", "派发", "目的地", "下发", "地图版本", "POI",
    ),
    "state_management": (
        "state", "mode", "abnormal", "ready", "状态", "模式", "异常", "未就绪",
    ),
    "diagnostics": (
        "diagnostic", "warn", "error", "stale", "process", "cpu", "memory",
        "诊断", "告警", "错误", "进程", "掉线", "内存",
    ),
}


@dataclass
class FrameRef:
    path: str
    frame: Any


@dataclass
class ModuleSummary:
    key: str
    label: str
    frame_count: int = 0
    parse_errors: int = 0
    time: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)
    anomalies: list[str] = field(default_factory=list)


@dataclass
class TriageResult:
    issue: str
    inputs: dict[str, Any]
    modules: dict[str, ModuleSummary]
    scores: dict[str, float]
    score_reasons: dict[str, list[str]]
    cross_checks: list[str]
    skipped_files: list[str]


def natural_sort_key(path: Path) -> list[Any]:
    parts = re.split(r"(\d+)", path.name)
    return [int(part) if part.isdigit() else part for part in parts]


def human_size(size: int) -> str:
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    value = float(size)
    for unit in units:
        if abs(value) < 1024.0 or unit == units[-1]:
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.2f} {unit}"
        value /= 1024.0
    return f"{size} B"


def parse_size(text: str) -> int:
    value = text.strip().lower()
    multipliers = {
        "tib": 1024**4,
        "tb": 1024**4,
        "t": 1024**4,
        "gib": 1024**3,
        "gb": 1024**3,
        "g": 1024**3,
        "mib": 1024**2,
        "mb": 1024**2,
        "m": 1024**2,
        "kib": 1024,
        "kb": 1024,
        "k": 1024,
        "b": 1,
    }
    for suffix, multiplier in multipliers.items():
        if value.endswith(suffix):
            return int(float(value[: -len(suffix)]) * multiplier)
    return int(float(value))


def percentile(values: list[float], ratio: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    index = (len(ordered) - 1) * ratio
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[int(index)]
    return ordered[lower] * (upper - index) + ordered[upper] * (index - lower)


def numeric_stats(values: Iterable[float]) -> dict[str, Any]:
    clean = [float(v) for v in values if math.isfinite(float(v))]
    if not clean:
        return {"count": 0}
    return {
        "count": len(clean),
        "min": min(clean),
        "max": max(clean),
        "mean": statistics.fmean(clean),
        "p50": percentile(clean, 0.50),
        "p95": percentile(clean, 0.95),
    }


def stamp_ns_from_header(header: Any) -> int:
    try:
        return int(header.stamp.sec) * 1_000_000_000 + int(header.stamp.nanosec)
    except AttributeError:
        return 0


def frame_stamp_ns(message: Any) -> int:
    stamp = stamp_ns_from_header(getattr(message, "header", None))
    if stamp > 0:
        return stamp
    for name in ("point_cloud", "image", "wifi_data"):
        child = getattr(message, name, None)
        if child is not None:
            stamp = stamp_ns_from_header(getattr(child, "header", None))
            if stamp > 0:
                return stamp
    for name in ("gps", "imu", "h264", "rangeframe"):
        items = getattr(message, name, [])
        if items:
            stamp = stamp_ns_from_header(getattr(items[0], "header", None))
            if stamp > 0:
                return stamp
    return 0


def has_field(message: Any, field_name: str) -> bool:
    try:
        return bool(message.HasField(field_name))
    except (AttributeError, ValueError):
        return False


def enum_name(message: Any, field_name: str, value: int) -> str:
    try:
        field = message.DESCRIPTOR.fields_by_name[field_name]
        enum_value = field.enum_type.values_by_number.get(int(value))
        if enum_value is not None:
            return enum_value.name
    except Exception:
        pass
    return str(value)


def counter_to_dict(counter: Counter) -> dict[str, int]:
    return {str(key): int(value) for key, value in counter.most_common()}


def add_score(
    scores: dict[str, float],
    reasons: dict[str, list[str]],
    module: str,
    amount: float,
    reason: str,
) -> None:
    scores[module] += float(amount)
    reasons[module].append(reason)


def discover_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for path in (current, *current.parents):
        if (path / "brainnode_interface" / "proto" / "brainnode_pb2.py").exists():
            return path
    return start.resolve()


def import_brainnode_pb2(repo_root: Path, proto_dir: str | None):
    candidates: list[Path] = []
    if proto_dir:
        candidates.append(Path(proto_dir).expanduser())
    candidates.extend(
        [
            repo_root / "brainnode_interface" / "proto",
            repo_root / "brainnode_toolkit" / "fast_tasker_sim" / "proto",
            repo_root / "brainnode_toolkit" / "playback_datacore" / "proto",
        ]
    )
    for candidate in candidates:
        if (candidate / "brainnode_pb2.py").exists() and str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
    import brainnode_pb2  # type: ignore

    return brainnode_pb2


def collect_pb_files(paths: list[str], max_files: int, include_maps: bool) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_file():
            candidates = [path]
        elif path.is_dir():
            candidates = sorted(path.rglob("*.pb"), key=natural_sort_key)
        else:
            continue
        for candidate in candidates:
            name = candidate.name
            if candidate.is_dir():
                continue
            if not include_maps and path.is_dir():
                if (
                    name.startswith("reference_route")
                    or name.startswith("semantic_map")
                    or name.startswith("submap_")
                    or name.endswith("_semantic_map.pb")
                ):
                    continue
            try:
                real = candidate.resolve()
            except OSError:
                real = candidate
            if real in seen:
                continue
            seen.add(real)
            files.append(candidate)
            if len(files) >= max_files:
                return files
    return files


def total_buffer_count(total: Any) -> int:
    count = 0
    for field_name, _, _, _ in BUFFER_SPECS:
        if hasattr(total, field_name):
            count += len(getattr(total, field_name))
    return count


def load_total_messages(raw: bytes, pb2: Any) -> list[Any]:
    single = pb2.TotalDataCore()
    try:
        consumed = single.MergeFromString(raw)
        if consumed == len(raw) and total_buffer_count(single) > 0:
            return [single]
    except DecodeError:
        pass

    messages: list[Any] = []
    offset = 0
    try:
        while offset < len(raw):
            size, payload_offset = _DecodeVarint32(raw, offset)
            end = payload_offset + size
            if end > len(raw) or size <= 0:
                return []
            message = pb2.TotalDataCore()
            consumed = message.MergeFromString(raw[payload_offset:end])
            if consumed != size:
                return []
            if total_buffer_count(message) > 0:
                messages.append(message)
            offset = end
    except Exception:
        return []
    return messages


def direct_message_candidates(pb2: Any) -> tuple[tuple[str, str, str], ...]:
    return (
        ("DataCoreFrame", "data_core", "raw sensors"),
        ("PerceptorFrame", "perception", "lidar perception"),
        ("CameraPerceptorFrame", "camera_perception", "camera perception"),
        ("ContextInfo", "localization_contextor", "localization/contextor"),
        ("TaskerFrame", "planning_tasker", "task planning"),
        ("Controller", "control", "control command"),
        ("DataCahssisFrame", "chassis", "chassis feedback"),
        ("DataStormFrame", "task_dispatch", "task dispatch"),
        ("StateManagement", "state_management", "state management"),
        ("DiagnosticsFrame", "diagnostics", "diagnostics"),
    )


def parse_direct_message(raw: bytes, pb2: Any) -> tuple[str, str, str, Any] | None:
    for type_name, module, label in direct_message_candidates(pb2):
        if not hasattr(pb2, type_name):
            continue
        message = getattr(pb2, type_name)()
        try:
            message.ParseFromString(raw)
        except DecodeError:
            continue
        if len(message.ListFields()) > 0:
            return type_name, module, label, message
    return None


def is_map_artifact(path: Path) -> bool:
    name = path.name.lower()
    return (
        name.startswith("semantic_map")
        or name.startswith("reference_route")
        or name.startswith("submap_")
        or name.endswith("_semantic_map.pb")
    )


def decode_total_buffers(total_messages: list[Any], pb2: Any, path: Path) -> tuple[dict[str, list[FrameRef]], dict[str, int]]:
    frames: dict[str, list[FrameRef]] = defaultdict(list)
    errors: dict[str, int] = defaultdict(int)
    for total in total_messages:
        for field_name, type_name, module, _ in BUFFER_SPECS:
            if not hasattr(total, field_name) or not hasattr(pb2, type_name):
                continue
            message_cls = getattr(pb2, type_name)
            for payload in getattr(total, field_name):
                message = message_cls()
                try:
                    message.ParseFromString(payload)
                    frames[module].append(FrameRef(str(path), message))
                except DecodeError:
                    errors[module] += 1
    return frames, errors


def summarize_time(frames: list[FrameRef]) -> dict[str, Any]:
    stamps = sorted(stamp for stamp in (frame_stamp_ns(item.frame) for item in frames) if stamp > 0)
    result: dict[str, Any] = {"timestamped": len(stamps)}
    if not stamps:
        return result
    first = stamps[0]
    last = stamps[-1]
    span_s = (last - first) / 1e9
    result.update(
        {
            "first_s": first / 1e9,
            "last_s": last / 1e9,
            "span_s": span_s,
            "rate_hz": (len(stamps) - 1) / span_s if span_s > 0 and len(stamps) > 1 else None,
        }
    )
    gaps_ms = [(b - a) / 1e6 for a, b in zip(stamps, stamps[1:]) if b > a]
    if gaps_ms:
        result["gap_ms"] = {
            "max": max(gaps_ms),
            "p95": percentile(gaps_ms, 0.95),
            "mean": statistics.fmean(gaps_ms),
        }
    seqs = [int(getattr(getattr(item.frame, "header", None), "seq", 0)) for item in frames]
    seqs = [value for value in seqs if value > 0]
    if len(seqs) > 1:
        drops = sum(max(0, b - a - 1) for a, b in zip(seqs, seqs[1:]) if b > a)
        result["seq_drops"] = drops
    return result


def nearest_delta_ms(source: list[int], target: list[int]) -> dict[str, Any]:
    source = sorted(value for value in source if value > 0)
    target = sorted(value for value in target if value > 0)
    if not source or not target:
        return {"count": 0}
    deltas: list[float] = []
    for stamp in source:
        pos = bisect.bisect_left(target, stamp)
        best: int | None = None
        for index in (pos - 1, pos):
            if 0 <= index < len(target):
                delta = abs(target[index] - stamp)
                best = delta if best is None else min(best, delta)
        if best is not None:
            deltas.append(best / 1e6)
    stats = numeric_stats(deltas)
    return stats


def layer_summary(semantic_map: Any) -> tuple[int, Counter]:
    total_entities = 0
    layers: Counter = Counter()
    for layer in getattr(semantic_map, "layers", []):
        count = len(getattr(layer, "entities", []))
        total_entities += count
        name = getattr(layer, "name", "") or "<unnamed>"
        layers[name] += count
    return total_entities, layers


def analyze_data_core(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    counts = Counter()
    gps_status = Counter()
    pc_bytes: list[float] = []
    speeds: list[float] = []
    imu_per_frame: list[float] = []
    gps_per_frame: list[float] = []
    for item in frames:
        frame = item.frame
        if has_field(frame, "point_cloud"):
            counts["point_cloud"] += 1
            pc_bytes.append(float(len(frame.point_cloud.data)))
        if has_field(frame, "image"):
            counts["image"] += 1
        if has_field(frame, "env"):
            counts["env"] += 1
        if has_field(frame, "wifi_data"):
            counts["wifi_data"] += 1
        counts["h264"] += len(getattr(frame, "h264", []))
        counts["rangeframe"] += len(getattr(frame, "rangeframe", []))
        imu_count = len(getattr(frame, "imu", []))
        gps_count = len(getattr(frame, "gps", []))
        imu_per_frame.append(float(imu_count))
        gps_per_frame.append(float(gps_count))
        counts["imu"] += imu_count
        counts["gps"] += gps_count
        speeds.append(float(getattr(frame, "speed", 0.0)))
        for gps in getattr(frame, "gps", []):
            gps_status[int(gps.status.status)] += 1
    summary.metrics["payload_counts"] = counter_to_dict(counts)
    summary.metrics["gps_status"] = counter_to_dict(gps_status)
    summary.metrics["point_cloud_bytes"] = numeric_stats(pc_bytes)
    summary.metrics["speed_mps"] = numeric_stats(speeds)
    summary.metrics["imu_per_frame"] = numeric_stats(imu_per_frame)
    summary.metrics["gps_per_frame"] = numeric_stats(gps_per_frame)
    if frames and counts["point_cloud"] == 0 and counts["rangeframe"] == 0:
        summary.anomalies.append("no point_cloud or rangeframe payloads in DataCoreFrame")
    bad_gps = sum(value for key, value in gps_status.items() if int(key) < 0)
    if bad_gps:
        summary.anomalies.append(f"gps status < 0 count={bad_gps}")


def analyze_perception(summary: ModuleSummary, frames: list[FrameRef], module: str) -> None:
    counts = Counter()
    layers = Counter()
    entity_counts: list[float] = []
    lidar_diag_levels = Counter()
    gps_diag_levels = Counter()
    for item in frames:
        frame = item.frame
        if module == "camera_perception":
            counts["segment_object"] += len(getattr(frame, "segment_object", []))
            counts["static_objects"] += len(getattr(frame, "static_objects", []))
            counts["moving_objects"] += len(getattr(frame, "moving_objects", []))
            counts["driving_spaces"] += len(getattr(frame, "driving_spaces", []))
            if has_field(frame, "semantic_map"):
                entities, names = layer_summary(frame.semantic_map)
                entity_counts.append(float(entities))
                layers.update(names)
            continue
        if has_field(frame, "odom"):
            counts["odom"] += 1
        if has_field(frame, "debug_point_cloud"):
            counts["debug_point_cloud"] += 1
        if has_field(frame, "image"):
            counts["image"] += 1
        if has_field(frame, "sem_perception"):
            entities, names = layer_summary(frame.sem_perception)
            entity_counts.append(float(entities))
            layers.update(names)
        if has_field(frame, "lidar_diag"):
            lidar_diag_levels[int(getattr(frame.lidar_diag, "level", 0))] += 1
        if has_field(frame, "gps"):
            gps_diag_levels[int(getattr(frame.gps, "level", 0))] += 1
    summary.metrics["counts"] = counter_to_dict(counts)
    summary.metrics["semantic_entities_per_frame"] = numeric_stats(entity_counts)
    summary.metrics["semantic_layer_entity_counts"] = counter_to_dict(layers)
    if lidar_diag_levels:
        summary.metrics["lidar_diag_levels"] = counter_to_dict(lidar_diag_levels)
    if gps_diag_levels:
        summary.metrics["gps_diag_levels"] = counter_to_dict(gps_diag_levels)
    if entity_counts and percentile(entity_counts, 0.50) == 0:
        summary.anomalies.append("semantic perception entities are empty in at least half of frames")
    if any(level > 0 and count > 0 for level, count in lidar_diag_levels.items()):
        summary.anomalies.append(f"lidar diagnostic nonzero levels: {counter_to_dict(lidar_diag_levels)}")


def analyze_contextor(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    invalid = 0
    rejected = 0
    confidence: list[float] = []
    iris: list[float] = []
    residual: list[float] = []
    ba_matches: list[float] = []
    metadata_keys = Counter()
    for item in frames:
        frame = item.frame
        if not bool(getattr(frame, "alignment_valid", False)):
            invalid += 1
        if not bool(getattr(frame, "map_accepted", False)):
            rejected += 1
        confidence.append(float(getattr(frame, "match_confidence", 0.0)))
        iris.append(float(getattr(frame, "lidar_iris_similarity", 0.0)))
        residual.append(float(getattr(frame, "map_mean_residual_m", 0.0)))
        ba_matches.append(float(getattr(frame, "semantic_ba_matches", 0.0)))
        metadata_keys.update(getattr(frame, "metadata", {}).keys())
    summary.metrics["alignment_invalid"] = invalid
    summary.metrics["map_rejected"] = rejected
    summary.metrics["match_confidence"] = numeric_stats(confidence)
    summary.metrics["lidar_iris_similarity"] = numeric_stats(iris)
    summary.metrics["map_mean_residual_m"] = numeric_stats(residual)
    summary.metrics["semantic_ba_matches"] = numeric_stats(ba_matches)
    summary.metrics["metadata_keys"] = counter_to_dict(metadata_keys)
    if invalid:
        summary.anomalies.append(f"alignment_valid=false count={invalid}/{len(frames)}")
    if rejected:
        summary.anomalies.append(f"map_accepted=false count={rejected}/{len(frames)}")
    if confidence and percentile(confidence, 0.50) is not None and percentile(confidence, 0.50) < 0.30:
        summary.anomalies.append("median match_confidence < 0.30")
    if residual and percentile(residual, 0.95) is not None and percentile(residual, 0.95) > 1.0:
        summary.anomalies.append("p95 map_mean_residual_m > 1.0")


def analyze_tasker(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    commands = Counter()
    task_types = Counter()
    abnormal = Counter()
    completion = Counter()
    traj_lengths: list[float] = []
    global_path_lengths: list[float] = []
    ccpp_reasons = Counter()
    ccpp_active = 0
    for item in frames:
        frame = item.frame
        command = getattr(frame, "command", "")
        if command:
            commands[command] += 1
        traj_lengths.append(float(len(getattr(frame, "trajectory_points", []))))
        global_path_lengths.append(float(len(getattr(frame, "global_path", []))))
        sm = getattr(frame, "state_management", None)
        if sm is not None:
            abnormal_name = enum_name(sm, "state_2", int(getattr(sm, "state_2", 0)))
            completion_name = enum_name(sm, "state_1", int(getattr(sm, "state_1", 0)))
            task_type_name = enum_name(sm, "state_4", int(getattr(sm, "state_4", 0)))
            abnormal[abnormal_name] += 1
            completion[completion_name] += 1
            task_types[task_type_name] += 1
        if has_field(frame, "ccpp_cost_map"):
            ccpp = frame.ccpp_cost_map
            if bool(getattr(ccpp, "active", False)):
                ccpp_active += 1
            reason = getattr(ccpp, "planner_reason", "") or getattr(ccpp, "task_mode", "")
            if reason:
                ccpp_reasons[reason] += 1
    summary.metrics["commands"] = counter_to_dict(commands)
    summary.metrics["trajectory_points"] = numeric_stats(traj_lengths)
    summary.metrics["global_path_points"] = numeric_stats(global_path_lengths)
    summary.metrics["state_abnormal"] = counter_to_dict(abnormal)
    summary.metrics["task_completion"] = counter_to_dict(completion)
    summary.metrics["task_types"] = counter_to_dict(task_types)
    summary.metrics["ccpp_active_frames"] = ccpp_active
    summary.metrics["ccpp_reasons"] = counter_to_dict(ccpp_reasons)
    if traj_lengths and percentile(traj_lengths, 0.50) == 0:
        summary.anomalies.append("median tasker trajectory length is 0")
    non_normal = sum(count for name, count in abnormal.items() if name != "NORMAL")
    if non_normal:
        summary.anomalies.append(f"StateManagement abnormal count={non_normal}/{len(frames)}")


def analyze_control(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    x_spd = [float(getattr(item.frame, "x_spd", 0.0)) for item in frames]
    y_spd = [float(getattr(item.frame, "y_spd", 0.0)) for item in frames]
    eps = [float(getattr(item.frame, "eps", 0.0)) for item in frames]
    brake = [float(getattr(item.frame, "brake", 0.0)) for item in frames]
    summary.metrics["x_spd_mps"] = numeric_stats(x_spd)
    summary.metrics["y_spd_mps"] = numeric_stats(y_spd)
    summary.metrics["eps_rad"] = numeric_stats(eps)
    summary.metrics["brake"] = numeric_stats(brake)
    if brake and percentile(brake, 0.95) is not None and percentile(brake, 0.95) > 0.5:
        summary.anomalies.append("controller brake p95 > 0.5")
    if x_spd and percentile([abs(v) for v in x_spd], 0.95) == 0:
        summary.anomalies.append("controller x_spd is zero for nearly all frames")


def analyze_chassis(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    x_speed: list[float] = []
    y_speed: list[float] = []
    steering: list[float] = []
    brake = Counter()
    gear = Counter()
    control_mode = Counter()
    emergency = 0
    touch_stop = 0
    for item in frames:
        frame = item.frame
        info = getattr(frame, "chassis_info", None)
        if info is not None:
            x_speed.append(float(getattr(info, "x_speed", 0.0)))
            y_speed.append(float(getattr(info, "y_speed", 0.0)))
            steering.append(float(getattr(info, "wheel_steering_angle", 0.0)))
            brake[int(getattr(info, "brake", 0))] += 1
            gear[int(getattr(info, "gear_status", 0))] += 1
            control_mode[int(getattr(info, "control_mode", 0))] += 1
        state = getattr(frame, "chassis_state", None)
        other = getattr(state, "chassis_other_info", None) if state is not None else None
        if other is not None:
            if int(getattr(other, "emergency_stop_status", 0)) != 0:
                emergency += 1
            touch_stop += sum(1 for value in getattr(other, "touch_sensor_stop_status", []) if int(value) != 0)
    summary.metrics["x_speed_mps"] = numeric_stats(x_speed)
    summary.metrics["y_speed_mps"] = numeric_stats(y_speed)
    summary.metrics["wheel_steering_angle_rad"] = numeric_stats(steering)
    summary.metrics["brake_status"] = counter_to_dict(brake)
    summary.metrics["gear_status"] = counter_to_dict(gear)
    summary.metrics["control_mode"] = counter_to_dict(control_mode)
    summary.metrics["emergency_stop_frames"] = emergency
    summary.metrics["touch_sensor_stop_count"] = touch_stop
    if emergency:
        summary.anomalies.append(f"emergency_stop_status active frames={emergency}")
    if touch_stop:
        summary.anomalies.append(f"touch_sensor_stop_status nonzero count={touch_stop}")


def analyze_state_management(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    modes = {name: Counter() for name in ("tracking_mode", "sensorfusion", "localization", "motionplanning")}
    states = {name: Counter() for name in ("state_1", "state_2", "state_3", "state_4", "state_5", "state_6")}
    task_ids = Counter()
    for item in frames:
        frame = item.frame
        if getattr(frame, "task_id", ""):
            task_ids[getattr(frame, "task_id")] += 1
        for name, counter in modes.items():
            counter[enum_name(frame, name, int(getattr(frame, name, 0)))] += 1
        for name, counter in states.items():
            counter[enum_name(frame, name, int(getattr(frame, name, 0)))] += 1
    summary.metrics["modes"] = {name: counter_to_dict(counter) for name, counter in modes.items()}
    summary.metrics["states"] = {name: counter_to_dict(counter) for name, counter in states.items()}
    summary.metrics["task_ids"] = counter_to_dict(task_ids)
    abnormal = states["state_2"]
    non_normal = sum(count for name, count in abnormal.items() if name != "NORMAL")
    if non_normal:
        summary.anomalies.append(f"abnormal state_2 count={non_normal}/{len(frames)}")
    for mode_name, counter in modes.items():
        off = counter.get("MODULE_OFF", 0)
        if off:
            summary.anomalies.append(f"{mode_name}=MODULE_OFF count={off}/{len(frames)}")


def analyze_diagnostics(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    levels = Counter()
    messages = Counter()
    names = Counter()
    status_fields = (
        "lidar_diagnostics",
        "camera_diagnostics",
        "chassis_diagnostics",
        "process_diagnostics",
        "sys_diagnostics",
    )
    for item in frames:
        frame = item.frame
        for field_name in status_fields:
            if not has_field(frame, field_name):
                continue
            status = getattr(frame, field_name)
            level = int(getattr(status, "level", 0))
            name = getattr(status, "name", "") or field_name
            names[name] += 1
            levels[f"{field_name}:{level}"] += 1
            if level > 0:
                msg = " ".join(f"{kv.key}={kv.value}" for kv in getattr(status, "values", []))
                messages[(name + " " + msg).strip()[:180]] += 1
    summary.metrics["levels"] = counter_to_dict(levels)
    summary.metrics["names"] = counter_to_dict(names)
    summary.metrics["non_ok_messages"] = counter_to_dict(messages)
    if messages:
        summary.anomalies.append("diagnostics contain WARN/ERROR/STALE statuses")


def analyze_task_dispatch(summary: ModuleSummary, frames: list[FrameRef]) -> None:
    task_ids = Counter()
    control_actions = Counter()
    map_versions = Counter()
    path_codes = Counter()
    for item in frames:
        frame = item.frame
        nav = getattr(frame, "raw_nav_task", None)
        if nav is not None and len(nav.ListFields()) > 0:
            if getattr(nav, "task_id", ""):
                task_ids[getattr(nav, "task_id")] += 1
            control_actions[enum_name(nav, "control_action", int(getattr(nav, "control_action", 0)))] += 1
            path_info = getattr(nav, "path_info", None)
            if path_info is not None:
                path_codes[int(getattr(path_info, "path_code", 0))] += 1
        map_info = getattr(frame, "map_info", None)
        if map_info is not None and getattr(map_info, "map_version", ""):
            map_versions[getattr(map_info, "map_version")] += 1
    summary.metrics["task_ids"] = counter_to_dict(task_ids)
    summary.metrics["control_actions"] = counter_to_dict(control_actions)
    summary.metrics["path_codes"] = counter_to_dict(path_codes)
    summary.metrics["map_versions"] = counter_to_dict(map_versions)
    failed_path = sum(count for code, count in path_codes.items() if int(code) < 0)
    if failed_path:
        summary.anomalies.append(f"raw_nav_task path_code < 0 count={failed_path}")


def build_module_summaries(
    frames_by_module: dict[str, list[FrameRef]],
    parse_errors: dict[str, int],
) -> dict[str, ModuleSummary]:
    labels = {module: label for _, _, module, label in BUFFER_SPECS}
    modules: dict[str, ModuleSummary] = {}
    for module in sorted(set(labels) | set(frames_by_module) | set(parse_errors)):
        frames = frames_by_module.get(module, [])
        summary = ModuleSummary(
            key=module,
            label=labels.get(module, module),
            frame_count=len(frames),
            parse_errors=parse_errors.get(module, 0),
            time=summarize_time(frames),
        )
        if module == "data_core":
            analyze_data_core(summary, frames)
        elif module in {"perception", "camera_perception"}:
            analyze_perception(summary, frames, module)
        elif module == "localization_contextor":
            analyze_contextor(summary, frames)
        elif module == "planning_tasker":
            analyze_tasker(summary, frames)
        elif module == "control":
            analyze_control(summary, frames)
        elif module == "chassis":
            analyze_chassis(summary, frames)
        elif module == "state_management":
            analyze_state_management(summary, frames)
        elif module == "diagnostics":
            analyze_diagnostics(summary, frames)
        elif module == "task_dispatch":
            analyze_task_dispatch(summary, frames)
        gap = summary.time.get("gap_ms", {}).get("max") if isinstance(summary.time.get("gap_ms"), dict) else None
        if isinstance(gap, (int, float)) and gap > 500:
            summary.anomalies.append(f"max timestamp gap {gap:.1f} ms")
        if summary.parse_errors:
            summary.anomalies.append(f"parse errors={summary.parse_errors}")
        modules[module] = summary
    return modules


def score_issue_keywords(issue: str, scores: dict[str, float], reasons: dict[str, list[str]]) -> None:
    text = issue.lower()
    for module, keywords in ISSUE_KEYWORDS.items():
        matches = [word for word in keywords if word.lower() in text]
        if matches:
            amount = min(4.0, 0.8 + 0.35 * len(matches))
            add_score(scores, reasons, module, amount, "issue keywords: " + ", ".join(matches[:8]))


def score_anomalies(modules: dict[str, ModuleSummary], scores: dict[str, float], reasons: dict[str, list[str]]) -> None:
    for module, summary in modules.items():
        if summary.parse_errors:
            add_score(scores, reasons, module, 2.0, f"{summary.parse_errors} parse errors")
        for anomaly in summary.anomalies:
            add_score(scores, reasons, module, 1.5, anomaly)
        if summary.frame_count == 0:
            continue
        gap = summary.time.get("gap_ms", {}).get("max") if isinstance(summary.time.get("gap_ms"), dict) else None
        if isinstance(gap, (int, float)) and gap > 1000:
            add_score(scores, reasons, module, 1.0, f"large timestamp gap {gap:.1f} ms")
    contextor = modules.get("localization_contextor")
    if contextor:
        invalid = int(contextor.metrics.get("alignment_invalid", 0) or 0)
        rejected = int(contextor.metrics.get("map_rejected", 0) or 0)
        if invalid or rejected:
            add_score(scores, reasons, "planning_tasker", 0.8, "planning may be affected by invalid localization/contextor")
            add_score(scores, reasons, "control", 0.5, "control may stop because upstream localization is invalid")
    tasker = modules.get("planning_tasker")
    if tasker and any("trajectory length is 0" in item for item in tasker.anomalies):
        add_score(scores, reasons, "control", 0.5, "controller may output stop because tasker trajectory is empty")


def build_cross_checks(
    frames_by_module: dict[str, list[FrameRef]],
    modules: dict[str, ModuleSummary],
    scores: dict[str, float],
    reasons: dict[str, list[str]],
) -> list[str]:
    checks: list[str] = []
    stamps = {module: [frame_stamp_ns(item.frame) for item in frames] for module, frames in frames_by_module.items()}
    base_modules = ("data_core", "perception", "localization_contextor", "planning_tasker", "control", "chassis")
    for module in base_modules:
        if module == "data_core" or module not in stamps or "data_core" not in stamps:
            continue
        stats = nearest_delta_ms(stamps[module], stamps["data_core"])
        if stats.get("count"):
            p95 = stats.get("p95")
            checks.append(f"{module} nearest DataCore timestamp delta p95={p95:.1f} ms")
            if isinstance(p95, (int, float)) and p95 > 250:
                add_score(scores, reasons, module, 1.0, f"timestamp p95 delta to DataCore is {p95:.1f} ms")

    control = modules.get("control")
    chassis = modules.get("chassis")
    if control and chassis and control.frame_count > 0 and chassis.frame_count > 0:
        target = control.metrics.get("x_spd_mps", {}).get("p50", 0)
        actual = chassis.metrics.get("x_speed_mps", {}).get("p50", 0)
        if isinstance(target, (int, float)) and isinstance(actual, (int, float)):
            checks.append(f"controller median x_spd={target:.3f} m/s, chassis median x_speed={actual:.3f} m/s")
            if abs(target) > 0.20 and abs(actual) < 0.05:
                add_score(scores, reasons, "chassis", 2.0, "controller commands movement but chassis speed is near zero")
                add_score(scores, reasons, "control", 0.8, "controller/chassis execution mismatch")

    tasker = modules.get("planning_tasker")
    if tasker and control and tasker.frame_count > 0 and control.frame_count > 0:
        traj_p50 = tasker.metrics.get("trajectory_points", {}).get("p50", 0)
        x_p95 = control.metrics.get("x_spd_mps", {}).get("p95", 0)
        if isinstance(traj_p50, (int, float)) and isinstance(x_p95, (int, float)):
            checks.append(f"tasker median trajectory_points={traj_p50:.1f}, controller x_spd p95={x_p95:.3f} m/s")
            if traj_p50 > 0 and abs(x_p95) < 0.05:
                add_score(scores, reasons, "control", 1.5, "tasker has trajectory but controller command speed is near zero")
            if traj_p50 == 0 and abs(x_p95) < 0.05:
                add_score(scores, reasons, "planning_tasker", 1.2, "empty tasker trajectory with stop command")

    perception = modules.get("perception")
    if perception and tasker and perception.frame_count > 0 and tasker.frame_count > 0:
        entities_p50 = perception.metrics.get("semantic_entities_per_frame", {}).get("p50", None)
        traj_p50 = tasker.metrics.get("trajectory_points", {}).get("p50", None)
        if isinstance(entities_p50, (int, float)) and isinstance(traj_p50, (int, float)):
            checks.append(f"perception semantic entities p50={entities_p50:.1f}, tasker trajectory p50={traj_p50:.1f}")
            if entities_p50 == 0 and traj_p50 == 0:
                add_score(scores, reasons, "perception", 1.0, "empty perception semantics can cause empty planning output")
    return checks


def module_to_dict(summary: ModuleSummary) -> dict[str, Any]:
    return {
        "key": summary.key,
        "label": summary.label,
        "frame_count": summary.frame_count,
        "parse_errors": summary.parse_errors,
        "time": summary.time,
        "metrics": summary.metrics,
        "anomalies": summary.anomalies,
    }


def result_to_dict(result: TriageResult) -> dict[str, Any]:
    ranked = sorted(result.scores.items(), key=lambda item: item[1], reverse=True)
    return {
        "issue": result.issue,
        "inputs": result.inputs,
        "ranked_modules": [
            {
                "module": module,
                "score": score,
                "reasons": result.score_reasons.get(module, []),
            }
            for module, score in ranked
            if score > 0
        ],
        "modules": {module: module_to_dict(summary) for module, summary in result.modules.items()},
        "cross_checks": result.cross_checks,
        "skipped_files": result.skipped_files,
    }


def render_markdown(result: TriageResult) -> str:
    data = result_to_dict(result)
    lines: list[str] = []
    lines.append("# PB Module Triage")
    if result.issue:
        lines.append(f"Issue: {result.issue}")
    inputs = result.inputs
    lines.append(
        f"Inputs: files={inputs.get('file_count', 0)}, bytes={human_size(int(inputs.get('total_bytes', 0)))}, "
        f"repo_root={inputs.get('repo_root')}"
    )
    if result.skipped_files:
        lines.append(f"Skipped files: {len(result.skipped_files)}")
    lines.append("")
    lines.append("## Ranked Modules")
    ranked = data["ranked_modules"]
    if not ranked:
        lines.append("- No module score above zero. Use module summaries and issue context manually.")
    for item in ranked[:8]:
        lines.append(f"- {item['module']}: score={item['score']:.2f}")
        for reason in item["reasons"][:5]:
            lines.append(f"  - {reason}")
    lines.append("")
    lines.append("## Module Evidence")
    for module, summary in result.modules.items():
        if summary.frame_count == 0 and not summary.parse_errors:
            continue
        rate = summary.time.get("rate_hz")
        rate_text = "n/a" if rate is None else f"{rate:.2f} Hz"
        lines.append(f"### {module} ({summary.label})")
        lines.append(f"- frames={summary.frame_count}, parse_errors={summary.parse_errors}, rate={rate_text}")
        if summary.time.get("gap_ms"):
            gap = summary.time["gap_ms"]
            lines.append(f"- gap_ms: max={gap.get('max'):.1f}, p95={gap.get('p95'):.1f}")
        if summary.anomalies:
            lines.append("- anomalies: " + "; ".join(summary.anomalies[:6]))
        key_metrics = []
        for key, value in summary.metrics.items():
            if len(key_metrics) >= 6:
                break
            if isinstance(value, dict) and value:
                key_metrics.append(f"{key}={json.dumps(value, ensure_ascii=False)[:240]}")
            elif value not in ({}, [], None):
                key_metrics.append(f"{key}={value}")
        for item in key_metrics:
            lines.append(f"- {item}")
    if result.cross_checks:
        lines.append("")
        lines.append("## Cross Checks")
        for check in result.cross_checks:
            lines.append(f"- {check}")
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> TriageResult:
    repo_root = Path(args.repo_root).expanduser().resolve() if args.repo_root else discover_repo_root(Path.cwd())
    pb2 = import_brainnode_pb2(repo_root, args.proto_dir)
    files = collect_pb_files(args.inputs, args.max_files, args.include_maps)
    frames_by_module: dict[str, list[FrameRef]] = defaultdict(list)
    parse_errors: dict[str, int] = defaultdict(int)
    skipped: list[str] = []
    total_bytes = 0

    for file_path in files:
        try:
            size = file_path.stat().st_size
        except OSError as exc:
            skipped.append(f"{file_path}: stat failed: {exc}")
            continue
        if size > args.max_file_bytes:
            skipped.append(f"{file_path}: skipped size {human_size(size)} > {human_size(args.max_file_bytes)}")
            continue
        total_bytes += size
        try:
            raw = file_path.read_bytes()
        except OSError as exc:
            skipped.append(f"{file_path}: read failed: {exc}")
            continue
        if is_map_artifact(file_path):
            skipped.append(f"{file_path}: map artifact is not a runtime TotalDataCore log")
            continue
        total_messages = load_total_messages(raw, pb2)
        if total_messages:
            decoded, errors = decode_total_buffers(total_messages, pb2, file_path)
            for module, items in decoded.items():
                frames_by_module[module].extend(items)
            for module, count in errors.items():
                parse_errors[module] += count
            continue
        direct = parse_direct_message(raw, pb2)
        if direct is not None:
            _, module, _, message = direct
            frames_by_module[module].append(FrameRef(str(file_path), message))
        else:
            skipped.append(f"{file_path}: not parsed as TotalDataCore or known direct message")

    for module in frames_by_module:
        frames_by_module[module].sort(key=lambda item: frame_stamp_ns(item.frame))
    modules = build_module_summaries(frames_by_module, parse_errors)
    scores: dict[str, float] = defaultdict(float)
    reasons: dict[str, list[str]] = defaultdict(list)
    score_issue_keywords(args.issue, scores, reasons)
    score_anomalies(modules, scores, reasons)
    cross_checks = build_cross_checks(frames_by_module, modules, scores, reasons)

    inputs = {
        "repo_root": str(repo_root),
        "file_count": len(files),
        "parsed_file_count": len(files) - len(skipped),
        "total_bytes": total_bytes,
        "max_files": args.max_files,
    }
    return TriageResult(
        issue=args.issue,
        inputs=inputs,
        modules=modules,
        scores=dict(scores),
        score_reasons=dict(reasons),
        cross_checks=cross_checks,
        skipped_files=skipped,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="PB file(s) or directory/directories")
    parser.add_argument("--issue", default="", help="Natural-language issue description")
    parser.add_argument("--repo-root", default="", help="Repository root containing brainnode_interface/proto")
    parser.add_argument("--proto-dir", default="", help="Directory containing brainnode_pb2.py")
    parser.add_argument("--max-files", type=int, default=20, help="Max .pb files to scan from directories")
    parser.add_argument("--max-file-bytes", type=parse_size, default=parse_size("2g"), help="Skip files larger than this")
    parser.add_argument("--include-maps", action="store_true", help="Do not skip semantic_map/reference_route/submap files in directories")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    parser.add_argument("--output", default="", help="Optional output path")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    result = run(args)
    if args.json:
        text = json.dumps(result_to_dict(result), ensure_ascii=False, indent=2) + "\n"
    else:
        text = render_markdown(result)
    if args.output:
        Path(args.output).expanduser().write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
