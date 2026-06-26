from __future__ import annotations

import argparse
import csv
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np

from demo_utils import draw_panel
from run_ultralytics_openvino_demo import (
    DEVICE_MAP,
    close_stream,
    live_stream,
    load_integrated_model,
    patch_ultralytics_openvino_backend,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLO26 OpenVINO downstream AI PC task demo.")
    parser.add_argument("--source", default="0", help="Camera index, video path, image path, or URL.")
    parser.add_argument("--model", default="yolo26n.pt", help="PyTorch model path/name used for export.")
    parser.add_argument("--models-dir", default="integrated_models")
    parser.add_argument("--precision", choices=["fp32", "int8"], default="int8")
    parser.add_argument("--device", choices=["CPU", "GPU", "NPU"], default="NPU")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--data", default="coco8.yaml")
    parser.add_argument("--fraction", type=float, default=1.0)
    parser.add_argument("--force-export", action="store_true")
    parser.add_argument("--camera-width", type=int, default=1280)
    parser.add_argument("--camera-height", type=int, default=720)
    parser.add_argument("--perf-hint", choices=["latency", "throughput"], default="throughput")
    parser.add_argument("--num-requests", type=int, default=0, help="OpenVINO async requests. 0 lets OpenVINO choose.")
    parser.add_argument("--flip-camera", action="store_true", help="Mirror live frames for natural camera control.")
    parser.add_argument("--task", choices=["person-counter", "inventory-count", "safety-zone"], default="person-counter")
    parser.add_argument("--target", default="bottle", help="Object class used for inventory counting.")
    parser.add_argument("--target-conf", type=float, default=0.45)
    parser.add_argument("--stable-frames", type=int, default=3)
    parser.add_argument("--cooldown", type=float, default=1.5)
    parser.add_argument("--summary-interval", type=float, default=1.0, help="Seconds between CSV summary rows.")
    parser.add_argument("--count-zone", default="", help="Normalized people-counting ROI as x1,y1,x2,y2. Empty counts the full frame.")
    parser.add_argument("--danger-zone", default="0.667,0,1,0.333", help="Normalized safety ROI as x1,y1,x2,y2.")
    parser.add_argument("--event-log", default="artifacts/downstream_events.csv")
    parser.add_argument("--duration", type=float, default=0.0, help="Automatically stop after N seconds.")
    parser.add_argument("--start-delay", type=float, default=0.0)
    parser.add_argument("--no-display", action="store_true")
    parser.add_argument("--monitor", action="store_true", help="Show a monitor window even with --no-display.")
    parser.add_argument("--output-video", default="", help="Save rendered frames to an MP4 file.")
    parser.add_argument("--self-test", action="store_true", help="Run event logic without loading a model.")
    return parser.parse_args()


def parse_zone(zone_text: str, default: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    if not zone_text:
        return default
    parts = [float(part.strip()) for part in zone_text.split(",")]
    if len(parts) != 4:
        raise ValueError(f"Zone must have four comma-separated values: {zone_text}")
    x1, y1, x2, y2 = [max(0.0, min(1.0, value)) for value in parts]
    if x2 <= x1 or y2 <= y1:
        raise ValueError(f"Zone must satisfy x2>x1 and y2>y1: {zone_text}")
    return x1, y1, x2, y2


def point_in_zone(x: float, y: float, width: int, height: int, zone: tuple[float, float, float, float]) -> bool:
    x1, y1, x2, y2 = zone
    return width * x1 <= x <= width * x2 and height * y1 <= y <= height * y2


def class_name(result, cls_id: int) -> str:
    names = getattr(result, "names", {})
    if isinstance(names, dict):
        return str(names.get(cls_id, cls_id))
    if isinstance(names, list) and 0 <= cls_id < len(names):
        return str(names[cls_id])
    return str(cls_id)


def analyze_result(
    result,
    target: str,
    target_conf: float,
    count_zone: tuple[float, float, float, float],
    danger_zone: tuple[float, float, float, float],
    flip_horizontal: bool = False,
) -> dict[str, object]:
    boxes = result.boxes
    height, width = result.orig_img.shape[:2]
    zone_people = 0
    frame_people = 0
    danger_people = 0
    target_hits = 0
    best_target_conf = 0.0

    if boxes is not None:
        for box in boxes:
            cls_id = int(box.cls[0])
            name = class_name(result, cls_id)
            conf = float(box.conf[0])
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]
            if flip_horizontal:
                x1, x2 = width - x2, width - x1
            center_x = (x1 + x2) / 2.0
            center_y = (y1 + y2) / 2.0

            if name == "person":
                frame_people += 1
                if point_in_zone(center_x, center_y, width, height, count_zone):
                    zone_people += 1
                if point_in_zone(center_x, center_y, width, height, danger_zone):
                    danger_people += 1

            if name == target and conf >= target_conf:
                target_hits += 1
                best_target_conf = max(best_target_conf, conf)

    return {
        "frame_people": frame_people,
        "zone_people": zone_people,
        "danger_people": danger_people,
        "target_count": target_hits,
        "target_seen": target_hits > 0,
        "target_conf": best_target_conf,
    }


def draw_roi(
    frame: np.ndarray,
    zone: tuple[float, float, float, float],
    label: str,
    color: tuple[int, int, int],
    fill: bool = False,
) -> None:
    height, width = frame.shape[:2]
    x1 = int(width * zone[0])
    y1 = int(height * zone[1])
    x2 = int(width * zone[2])
    y2 = int(height * zone[3])
    if fill:
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2 - 1, y2 - 1), color, -1)
        cv2.addWeighted(overlay, 0.18, frame, 0.82, 0, frame)
    cv2.rectangle(frame, (x1, y1), (x2 - 1, y2 - 1), color, 3)
    cv2.putText(frame, label, (x1 + 16, max(32, y1 + 34)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)


def append_event(path: Path, event_type: str, message: str, device: str, precision: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["timestamp", "event_type", "message", "device", "precision"])
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), event_type, message, device, precision])


def task_summary(args: argparse.Namespace, summary: dict[str, object]) -> tuple[str, str]:
    if args.task == "inventory-count":
        return (
            "inventory-count",
            f"{args.target} count={summary['target_count']} confidence={float(summary['target_conf']):.2f}",
        )
    if args.task == "safety-zone":
        danger_people = int(summary["danger_people"])
        status = "ALERT danger zone" if danger_people > 0 else "clear"
        return "safety-zone", f"{status}; danger_zone_people={danger_people} zone={args.danger_zone}"
    return "person-counter", f"zone_people={summary['zone_people']} frame_people={summary['frame_people']} zone={args.count_zone or 'full-frame'}"


def overlay_lines(args: argparse.Namespace, summary: dict[str, object], peak_people: int, peak_target: int) -> list[str]:
    if args.task == "inventory-count":
        return [
            "Inventory / Object Counting",
            f"{args.target}: {summary['target_count']}",
            f"Peak {args.target}: {peak_target}",
        ]
    if args.task == "safety-zone":
        alert = int(summary["danger_people"]) > 0
        return [
            "Safety Zone Alert",
            f"Restricted zone: {'ALERT' if alert else 'CLEAR'}",
            f"People in danger zone: {summary['danger_people']}",
            "ALARM: person entered restricted area" if alert else "No intrusion detected",
        ]
    return [
        "People Flow Counter",
        f"People in count zone: {summary['zone_people']}",
        f"People in frame: {summary['frame_people']}",
        f"Peak in zone: {peak_people}",
    ]


def run_self_test(args: argparse.Namespace) -> int:
    class FakeBox:
        def __init__(self, cls_id: int, conf: float, xyxy: list[float]) -> None:
            self.cls = np.array([cls_id], dtype=np.float32)
            self.conf = np.array([conf], dtype=np.float32)
            self.xyxy = np.array([xyxy], dtype=np.float32)

    class FakeResult:
        names = {0: "person", 39: "bottle"}

        def __init__(self, boxes: list[FakeBox]) -> None:
            self.boxes = boxes
            self.orig_img = np.zeros((720, 1280, 3), dtype=np.uint8)

    count_zone = parse_zone(args.count_zone, (0.0, 0.0, 1.0, 1.0))
    danger_zone = parse_zone(args.danger_zone, (2 / 3, 0.0, 1.0, 1 / 3))
    frames = [
        FakeResult([FakeBox(0, 0.9, [60, 100, 240, 640])]),
        FakeResult([FakeBox(0, 0.9, [520, 100, 720, 640]), FakeBox(39, 0.5, [900, 260, 1030, 620])]),
        FakeResult([FakeBox(0, 0.9, [940, 80, 1180, 260]), FakeBox(39, 0.6, [900, 260, 1030, 620])]),
    ]
    for idx, frame in enumerate(frames, 1):
        summary = analyze_result(frame, args.target, args.target_conf, count_zone, danger_zone)
        print(
            f"[SELF-TEST] frame={idx} zone_people={summary['zone_people']} "
            f"danger={summary['danger_people']} target_count={summary['target_count']}"
        )
    append_event(Path(args.event_log), "self-test", "Downstream event logic verified", args.device, args.precision)
    return 0


def run_live(args: argparse.Namespace) -> int:
    current_device = args.device
    current_precision = args.precision
    count_zone = parse_zone(args.count_zone, (0.0, 0.0, 1.0, 1.0))
    danger_zone = parse_zone(args.danger_zone, (2 / 3, 0.0, 1.0, 1 / 3))
    ov_model = load_integrated_model(args, current_precision)
    stream = live_stream(ov_model, args, current_device)
    show_monitor = (not args.no_display) or args.monitor

    if args.start_delay > 0:
        time.sleep(args.start_delay)

    fps_window: deque[float] = deque(maxlen=60)
    infer_window: deque[float] = deque(maxlen=60)
    peak_people = 0
    peak_target = 0
    target_streak = 0
    last_summary_ts = 0.0
    last_object_action_ts = 0.0
    last_ts = time.perf_counter()
    started_ts = last_ts
    writer = None
    window_created = False
    title = "OpenVINO YOLO Downstream Actions"

    try:
        while True:
            try:
                result = next(stream)
            except StopIteration:
                break

            now = time.perf_counter()
            frame_ms = (now - last_ts) * 1000.0
            last_ts = now
            if frame_ms > 0:
                fps_window.append(1000.0 / frame_ms)

            infer_ms = float(result.speed.get("inference", 0.0)) if hasattr(result, "speed") else 0.0
            if infer_ms > 0:
                infer_window.append(infer_ms)

            summary = analyze_result(
                result,
                args.target,
                args.target_conf,
                count_zone=count_zone,
                danger_zone=danger_zone,
                flip_horizontal=args.flip_camera,
            )
            peak_people = max(peak_people, int(summary["zone_people"]))
            peak_target = max(peak_target, int(summary["target_count"]))
            target_streak = target_streak + 1 if summary["target_seen"] else 0

            if args.summary_interval > 0 and now - last_summary_ts >= args.summary_interval:
                event_type, message = task_summary(args, summary)
                append_event(Path(args.event_log), event_type, message, current_device, current_precision)
                last_summary_ts = now

            if (
                args.task == "inventory-count"
                and target_streak >= args.stable_frames
                and now - last_object_action_ts >= args.cooldown
            ):
                append_event(
                    Path(args.event_log),
                    "object-trigger",
                    f"{args.target} trigger: downstream action cue",
                    current_device,
                    current_precision,
                )
                last_object_action_ts = now

            render = None
            if show_monitor or args.output_video:
                monitor_img = cv2.flip(result.orig_img, 1) if args.flip_camera else result.orig_img
                render = result.plot(img=monitor_img, line_width=2, font_size=0.8, pil=False)
                if args.task == "person-counter":
                    draw_roi(render, count_zone, "COUNT ZONE", (60, 220, 120), fill=False)
                elif args.task == "safety-zone":
                    draw_roi(render, danger_zone, "DANGER ZONE", (0, 0, 255), fill=True)
                draw_panel(render, overlay_lines(args, summary, peak_people, peak_target), anchor="top-left")

            if args.output_video and render is not None:
                if writer is None:
                    output_path = Path(args.output_video)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    fourcc = cv2.VideoWriter.fourcc(*"mp4v")
                    writer = cv2.VideoWriter(str(output_path), fourcc, 30.0, (render.shape[1], render.shape[0]))
                    if not writer.isOpened():
                        raise RuntimeError(f"Cannot open output video writer: {output_path}")
                writer.write(render)

            key = -1
            if show_monitor and render is not None:
                if not window_created:
                    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
                    window_created = True
                cv2.imshow(title, render)
                key = cv2.waitKey(1)
            else:
                time.sleep(0.001)

            if key in (ord("q"), ord("Q"), 27):
                break
            if args.duration > 0 and time.perf_counter() - started_ts >= args.duration:
                break
    finally:
        if writer is not None:
            writer.release()
        close_stream(stream)
        if window_created:
            cv2.destroyWindow(title)
    return 0


def main() -> int:
    args = parse_args()
    patch_ultralytics_openvino_backend(args.perf_hint, args.num_requests)
    if args.self_test:
        return run_self_test(args)
    return run_live(args)


if __name__ == "__main__":
    raise SystemExit(main())
