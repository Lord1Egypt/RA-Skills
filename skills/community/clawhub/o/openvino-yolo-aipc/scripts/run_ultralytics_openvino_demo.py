from __future__ import annotations

import argparse
import json
import os
import shutil
import time
from collections import deque
from pathlib import Path

import cv2
import numpy as np
import yaml

PROJECT_DIR = Path(__file__).resolve().parent
ULTRA_DIR = PROJECT_DIR / "Ultralytics"
MPL_DIR = ULTRA_DIR / "mpl"
ULTRA_DIR.mkdir(parents=True, exist_ok=True)
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("YOLO_CONFIG_DIR", str(ULTRA_DIR))
os.environ.setdefault("MPLCONFIGDIR", str(MPL_DIR))

from ultralytics import YOLO

from demo_utils import draw_panel


DEVICE_MAP = {
    "CPU": "intel:cpu",
    "GPU": "intel:gpu",
    "NPU": "intel:npu",
}

COCO_NAMES = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    4: "airplane",
    5: "bus",
    6: "train",
    7: "truck",
    8: "boat",
    9: "traffic light",
    10: "fire hydrant",
    11: "stop sign",
    12: "parking meter",
    13: "bench",
    14: "bird",
    15: "cat",
    16: "dog",
    17: "horse",
    18: "sheep",
    19: "cow",
    20: "elephant",
    21: "bear",
    22: "zebra",
    23: "giraffe",
    24: "backpack",
    25: "umbrella",
    26: "handbag",
    27: "tie",
    28: "suitcase",
    29: "frisbee",
    30: "skis",
    31: "snowboard",
    32: "sports ball",
    33: "kite",
    34: "baseball bat",
    35: "baseball glove",
    36: "skateboard",
    37: "surfboard",
    38: "tennis racket",
    39: "bottle",
    40: "wine glass",
    41: "cup",
    42: "fork",
    43: "knife",
    44: "spoon",
    45: "bowl",
    46: "banana",
    47: "apple",
    48: "sandwich",
    49: "orange",
    50: "broccoli",
    51: "carrot",
    52: "hot dog",
    53: "pizza",
    54: "donut",
    55: "cake",
    56: "chair",
    57: "couch",
    58: "potted plant",
    59: "bed",
    60: "dining table",
    61: "toilet",
    62: "tv",
    63: "laptop",
    64: "mouse",
    65: "remote",
    66: "keyboard",
    67: "cell phone",
    68: "microwave",
    69: "oven",
    70: "toaster",
    71: "sink",
    72: "refrigerator",
    73: "book",
    74: "clock",
    75: "vase",
    76: "scissors",
    77: "teddy bear",
    78: "hair drier",
    79: "toothbrush",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ultralytics-integrated YOLO26 OpenVINO demo.")
    parser.add_argument("--mode", choices=["live", "benchmark", "export"], default="live")
    parser.add_argument("--source", default="0", help="Camera index, video path, image path, or URL.")
    parser.add_argument("--model", default="yolo26n.pt", help="PyTorch model path/name used for export.")
    parser.add_argument("--models-dir", default="integrated_models", help="Where exported OpenVINO models are stored.")
    parser.add_argument("--openvino-model-dir", default="", help="Use this exact exported OpenVINO model directory instead of resolving from --models-dir/--precision.")
    parser.add_argument("--precision", choices=["fp32", "int8"], default="fp32")
    parser.add_argument("--device", choices=["CPU", "GPU", "NPU"], default="GPU")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--camera-width", type=int, default=1280, help="Requested live camera capture width.")
    parser.add_argument("--camera-height", type=int, default=720, help="Requested live camera capture height.")
    parser.add_argument("--perf-hint", choices=["latency", "throughput"], default="throughput", help="OpenVINO performance hint.")
    parser.add_argument("--num-requests", type=int, default=0, help="OpenVINO async requests. 0 lets OpenVINO choose the optimal value.")
    parser.add_argument("--benchmark-seconds", type=float, default=8.0)
    parser.add_argument("--benchmark-warmup", type=float, default=2.0)
    parser.add_argument("--data", default="coco8.yaml", help="Calibration data yaml for INT8 export.")
    parser.add_argument("--fraction", type=float, default=1.0, help="Calibration data fraction for INT8 export.")
    parser.add_argument("--force-export", action="store_true", help="Re-export even if the target model exists.")
    parser.add_argument("--show", action="store_true", help="Show live prediction window.")
    return parser.parse_args()


def patch_ultralytics_openvino_backend(perf_hint: str, num_requests: int) -> None:
    """Force Ultralytics OpenVINO backend to use the requested hint and async path."""
    from ultralytics.nn.backends.openvino import OpenVINOBackend

    OpenVINOBackend._demo_perf_hint = "THROUGHPUT" if perf_hint == "throughput" else "LATENCY"
    OpenVINOBackend._demo_num_requests = max(0, int(num_requests))
    if getattr(OpenVINOBackend, "_demo_patched", False):
        return

    def load_model(self, weight: str | Path) -> None:
        from ultralytics.utils import ARM64, LINUX, LOGGER
        from ultralytics.utils.checks import check_requirements
        import openvino as ov
        import torch

        LOGGER.info(f"Loading {weight} for OpenVINO inference...")
        check_requirements("openvino>=2024.0.0")

        core = ov.Core()
        fallback_device = "CPU" if core.available_devices == ["CPU"] else "AUTO"
        device_name = fallback_device

        if isinstance(self.device, str) and self.device.startswith("intel"):
            requested_device = self.device.split(":", 1)[1].upper()
            self.device = torch.device("cpu")
            device_name = requested_device
            if device_name not in core.available_devices:
                LOGGER.warning(f"OpenVINO device '{device_name}' not available. Using '{fallback_device}' instead.")
                device_name = fallback_device

        w = Path(weight)
        if not w.is_file():
            w = next(w.glob("*.xml"))

        ov_model = core.read_model(model=str(w), weights=w.with_suffix(".bin"))
        if ov_model.get_parameters()[0].get_layout().empty:
            ov_model.get_parameters()[0].set_layout(ov.Layout("NCHW"))

        metadata_file = w.parent / "metadata.yaml"
        if metadata_file.exists():
            from ultralytics.utils import YAML

            self.apply_metadata(YAML.load(metadata_file))

        self.inference_mode = self.__class__._demo_perf_hint
        config = {"PERFORMANCE_HINT": self.inference_mode}
        if self.__class__._demo_num_requests > 0:
            config["PERFORMANCE_HINT_NUM_REQUESTS"] = str(self.__class__._demo_num_requests)
        if LINUX and ARM64 and device_name == "CPU":
            config["EXECUTION_MODE_HINT"] = ov.properties.hint.ExecutionMode.ACCURACY
            config["INFERENCE_PRECISION_HINT"] = ov.Type.f32

        self.ov_compiled_model = core.compile_model(ov_model, device_name=device_name, config=config)
        optimal_requests = self.ov_compiled_model.get_property("OPTIMAL_NUMBER_OF_INFER_REQUESTS")
        LOGGER.info(
            f"Using OpenVINO {self.inference_mode} mode with "
            f"num_requests={self.__class__._demo_num_requests or 'AUTO'} "
            f"(optimal={optimal_requests}) for batch={self.batch} inference on "
            f"{', '.join(self.ov_compiled_model.get_property('EXECUTION_DEVICES'))}..."
        )
        self.input_name = self.ov_compiled_model.input().get_any_name()
        self.ov = ov

    OpenVINOBackend.load_model = load_model
    OpenVINOBackend._demo_patched = True


def model_dir(args: argparse.Namespace) -> Path:
    if getattr(args, "openvino_model_dir", ""):
        return Path(args.openvino_model_dir).resolve()
    model_stem = Path(args.model).stem or "yolo26"
    return Path(args.models_dir).resolve() / f"{model_stem}_{args.precision}_openvino_model"


def write_ultralytics_metadata_if_needed(target_dir: Path) -> None:
    yaml_path = target_dir / "metadata.yaml"
    if yaml_path.exists():
        return

    names = COCO_NAMES
    json_path = target_dir / "metadata.json"
    if json_path.exists():
        with json_path.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
        labels = metadata.get("labels")
        if labels:
            names = {idx: name for idx, name in enumerate(labels)}

    xml_files = sorted(target_dir.glob("*.xml"))
    bin_files = sorted(target_dir.glob("*.bin"))
    if not xml_files or not bin_files:
        return

    model_stem = xml_files[0].stem
    if xml_files[0].name != "yolo26n.xml":
        shutil.copy2(xml_files[0], target_dir / "yolo26n.xml")
    if bin_files[0].name != "yolo26n.bin":
        shutil.copy2(bin_files[0], target_dir / "yolo26n.bin")

    metadata_yaml = {
        "description": "YOLO26n OpenVINO model",
        "author": "Ultralytics",
        "version": "8.4.48",
        "license": "AGPL-3.0",
        "docs": "https://docs.ultralytics.com",
        "stride": 32,
        "task": "detect",
        "batch": 1,
        "imgsz": [640, 640],
        "names": names,
        "args": {
            "batch": 1,
            "half": False,
            "int8": "int8" in str(target_dir).lower(),
            "dynamic": False,
            "nms": False,
        },
        "channels": 3,
        "end2end": True,
    }
    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(metadata_yaml, f, sort_keys=False, allow_unicode=True)


def ensure_openvino_model(args: argparse.Namespace) -> Path:
    target_dir = model_dir(args)
    if target_dir.exists() and not args.force_export:
        write_ultralytics_metadata_if_needed(target_dir)
        return target_dir

    model_stem = Path(args.model).stem or "yolo26"
    existing_export = PROJECT_DIR / "models" / model_stem / ("_raw_export" if args.precision == "fp32" else "int8")
    if existing_export.exists() and not args.force_export:
        print(f"[ULTRA] Reusing existing OpenVINO model: {existing_export}")
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(existing_export, target_dir)
        write_ultralytics_metadata_if_needed(target_dir)
        return target_dir

    if target_dir.exists():
        shutil.rmtree(target_dir)

    print(f"[ULTRA] Exporting {args.model} to OpenVINO {args.precision.upper()}...")
    model = YOLO(args.model)
    export_kwargs = {
        "format": "openvino",
        "imgsz": args.imgsz,
        "dynamic": False,
        "half": False,
        "int8": args.precision == "int8",
    }
    if args.precision == "int8":
        export_kwargs["data"] = args.data
        export_kwargs["fraction"] = args.fraction

    exported_path = Path(model.export(**export_kwargs)).resolve()
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if exported_path != target_dir:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.move(str(exported_path), str(target_dir))

    write_ultralytics_metadata_if_needed(target_dir)
    print(f"[ULTRA] OpenVINO model ready: {target_dir}")
    return target_dir


def load_integrated_model(args: argparse.Namespace, precision: str) -> YOLO:
    local_args = argparse.Namespace(**vars(args))
    local_args.precision = precision
    ov_dir = ensure_openvino_model(local_args)
    return YOLO(str(ov_dir), task="detect")


def live_stream(model: YOLO, args: argparse.Namespace, device_alias: str):
    configure_camera_source(args.source, args.camera_width, args.camera_height)
    return model.predict(
        source=source_for_ultralytics(args.source),
        show=False,
        device=DEVICE_MAP[device_alias],
        imgsz=args.imgsz,
        conf=args.conf,
        vid_stride=1,
        stream=True,
        verbose=False,
    )


def request_label(num_requests: int) -> str:
    return "AUTO" if num_requests <= 0 else str(num_requests)


def close_stream(stream) -> None:
    close = getattr(stream, "close", None)
    if callable(close):
        close()


def source_for_ultralytics(source: str) -> str | int:
    return int(source) if source.isdigit() else source


def configure_camera_source(source: str, width: int, height: int) -> None:
    if not source.isdigit():
        return
    cap = cv2.VideoCapture(int(source), cv2.CAP_DSHOW)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.release()


def read_benchmark_frame(source: str) -> np.ndarray:
    if source.isdigit():
        cap = cv2.VideoCapture(int(source), cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap.release()
            cap = cv2.VideoCapture(int(source))
    else:
        cap = cv2.VideoCapture(source)

    if cap.isOpened():
        for _ in range(30):
            ok, frame = cap.read()
            if ok and frame is not None:
                cap.release()
                return frame
            time.sleep(0.05)
        cap.release()

    image = cv2.imread(source)
    if image is not None:
        return image

    raise RuntimeError(f"Unable to read a benchmark frame from: {source}")


def run_live(args: argparse.Namespace) -> int:
    current_device = args.device
    current_precision = args.precision
    ov_model = load_integrated_model(args, current_precision)
    stream = live_stream(ov_model, args, current_device)
    print(f"[ULTRA] Live predict: device={DEVICE_MAP[current_device]} precision={current_precision} source={args.source}")

    title = "Ultralytics YOLO26 + OpenVINO"
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    fps_window: deque[float] = deque(maxlen=60)
    infer_window: deque[float] = deque(maxlen=60)
    last_ts = time.perf_counter()
    skip_stats_frames = 8

    try:
        while True:
            try:
                result = next(stream)
            except StopIteration:
                break
            now = time.perf_counter()
            frame_ms = (now - last_ts) * 1000.0
            last_ts = now
            if skip_stats_frames > 0:
                skip_stats_frames -= 1
            elif frame_ms > 0:
                fps_window.append(1000.0 / frame_ms)

            infer_ms = float(result.speed.get("inference", 0.0)) if hasattr(result, "speed") else 0.0
            if skip_stats_frames <= 0 and infer_ms > 0:
                infer_window.append(infer_ms)

            render = result.plot(img=result.orig_img, line_width=2, font_size=0.8, pil=False)
            avg_fps = float(np.mean(fps_window)) if fps_window else 0.0
            avg_infer_ms = float(np.mean(infer_window)) if infer_window else infer_ms
            infer_fps = 1000.0 / avg_infer_ms if avg_infer_ms > 0 else 0.0

            draw_panel(
                render,
                [
                    f"Path: Ultralytics OpenVINO",
                    f"Device: {current_device} ({DEVICE_MAP[current_device]})",
                    f"Precision: {current_precision.upper()}",
                    f"OV Hint: {args.perf_hint.upper()} req={request_label(args.num_requests)}",
                    f"Live FPS: {avg_fps:.1f}",
                    f"Infer: {infer_fps:.1f} FPS / {avg_infer_ms:.1f} ms",
                    f"Detections: {len(result.boxes) if result.boxes is not None else 0}",
                ],
                anchor="top-right",
            )
            draw_panel(
                render,
                [
                    "1 CPU   2 GPU   3 NPU",
                    "F FP32  I INT8",
                    "Q / Esc exit",
                    "Ultralytics integrated path",
                ],
                anchor="top-left",
            )

            cv2.imshow(title, render)
            key = cv2.waitKey(1)
            if key in (ord("q"), ord("Q"), 27):
                break
            if key in (ord("1"), ord("2"), ord("3"), ord("f"), ord("F"), ord("i"), ord("I")):
                next_device = current_device
                next_precision = current_precision
                if key == ord("1"):
                    next_device = "CPU"
                elif key == ord("2"):
                    next_device = "GPU"
                elif key == ord("3"):
                    next_device = "NPU"
                elif key in (ord("f"), ord("F")) and not args.openvino_model_dir:
                    next_precision = "fp32"
                elif key in (ord("i"), ord("I")) and not args.openvino_model_dir:
                    next_precision = "int8"

                if next_device != current_device or next_precision != current_precision:
                    close_stream(stream)
                    current_device = next_device
                    current_precision = next_precision
                    ov_model = load_integrated_model(args, current_precision)
                    stream = live_stream(ov_model, args, current_device)
                    fps_window.clear()
                    infer_window.clear()
                    skip_stats_frames = 8
                    last_ts = time.perf_counter()
                    print(f"[ULTRA] Switched to device={DEVICE_MAP[current_device]} precision={current_precision}")
    finally:
        close_stream(stream)
        cv2.destroyWindow(title)
    return 0


def run_benchmark(args: argparse.Namespace) -> int:
    ov_dir = ensure_openvino_model(args)
    ov_model = YOLO(str(ov_dir), task="detect")
    device = DEVICE_MAP[args.device]
    frame = read_benchmark_frame(args.source)

    print("[ULTRA-BENCH] Starting Ultralytics OpenVINO benchmark")
    print(f"[ULTRA-BENCH] Model={ov_dir}")
    print(f"[ULTRA-BENCH] Device={device} Precision={args.precision.upper()} ImageSize={args.imgsz}")
    print(f"[ULTRA-BENCH] OpenVINO hint={args.perf_hint.upper()} NumRequests={request_label(args.num_requests)}")
    print(f"[ULTRA-BENCH] Warmup={args.benchmark_warmup:.1f}s Measure={args.benchmark_seconds:.1f}s")

    def predict_once():
        return ov_model.predict(
            source=frame,
            device=device,
            imgsz=args.imgsz,
            conf=args.conf,
            verbose=False,
            stream=False,
        )

    warmup_end = time.perf_counter() + max(0.0, args.benchmark_warmup)
    while time.perf_counter() < warmup_end:
        predict_once()

    wall_times: list[float] = []
    infer_times: list[float] = []
    completed = 0
    measure_start = time.perf_counter()
    measure_end = measure_start + max(0.1, args.benchmark_seconds)
    while time.perf_counter() < measure_end:
        start = time.perf_counter()
        results = predict_once()
        wall_ms = (time.perf_counter() - start) * 1000.0
        wall_times.append(wall_ms)
        completed += 1
        if results and hasattr(results[0], "speed"):
            infer_times.append(float(results[0].speed.get("inference", 0.0)))

    elapsed = time.perf_counter() - measure_start
    wall_arr = np.array(wall_times, dtype=np.float64)
    infer_arr = np.array(infer_times, dtype=np.float64) if infer_times else wall_arr
    throughput = completed / elapsed if elapsed > 0 else 0.0
    infer_throughput = 1000.0 / float(np.mean(infer_arr)) if len(infer_arr) else 0.0

    print("[ULTRA-BENCH] Results")
    print(f"[ULTRA-BENCH] Completed predictions: {completed}")
    print(f"[ULTRA-BENCH] Wall throughput: {throughput:.2f} FPS")
    print(f"[ULTRA-BENCH] Ultralytics inference throughput: {infer_throughput:.2f} FPS")
    print(f"[ULTRA-BENCH] Avg wall latency: {float(np.mean(wall_arr)):.2f} ms")
    print(f"[ULTRA-BENCH] Avg inference latency: {float(np.mean(infer_arr)):.2f} ms")
    print(f"[ULTRA-BENCH] P50 inference latency: {float(np.percentile(infer_arr, 50)):.2f} ms")
    print(f"[ULTRA-BENCH] P90 inference latency: {float(np.percentile(infer_arr, 90)):.2f} ms")
    return 0


def main() -> int:
    args = parse_args()
    os.chdir(PROJECT_DIR)
    patch_ultralytics_openvino_backend(args.perf_hint, args.num_requests)
    if args.mode == "export":
        ensure_openvino_model(args)
        return 0
    if args.mode == "benchmark":
        return run_benchmark(args)
    return run_live(args)


if __name__ == "__main__":
    raise SystemExit(main())
