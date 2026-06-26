"""Export YOLOv8s-World v2 to ONNX with custom class vocabulary.

This script converts `yolov8s-worldv2.pt` into `yolov8s-worldv2.onnx`,
injecting the package-detection class list via `set_classes()` so the
exported ONNX matches `CLASS_NAMES` used by `yolo_world_onnx.py` at runtime.

Usage:
    # called automatically by setup.sh when the ONNX file is missing
    python export_model.py

    # force re-export even if the ONNX already exists
    python export_model.py --force

If `yolov8s-worldv2.pt` is not present locally, the Ultralytics library
will download it on first load.
"""

import argparse
import os
import shutil
import sys

# IMPORTANT: must stay in sync with DEFAULT_CLASS_NAMES in yolo_world_onnx.py
# Order matters — the ONNX class index returned at runtime maps directly into this list.
CLASS_NAMES = [
    "parcel", "package", "delivery box", "person",
    "Cardboard box", "Packaging Box", "backpack", "handbag", "suitcase",
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PT_PATH = os.path.join(SCRIPT_DIR, "yolov8s-worldv2.pt")
ONNX_PATH = os.path.join(SCRIPT_DIR, "yolov8s-worldv2.onnx")
IMG_SIZE = 320


def main() -> int:
    parser = argparse.ArgumentParser(description="Export YOLO-World ONNX with custom classes")
    parser.add_argument("--force", action="store_true",
                        help="Re-export even if the ONNX file already exists")
    parser.add_argument("--imgsz", type=int, default=IMG_SIZE,
                        help=f"Export image size (default: {IMG_SIZE})")
    args = parser.parse_args()

    if os.path.isfile(ONNX_PATH) and not args.force:
        print(f"[i] ONNX already exists, skip export: {ONNX_PATH}")
        print(f"    (run with --force to re-export)")
        return 0

    try:
        from ultralytics import YOLO
    except ImportError:
        print("[x] ultralytics is not installed. Install it first:", file=sys.stderr)
        print("    pip install ultralytics", file=sys.stderr)
        return 2

    pt_source = PT_PATH if os.path.isfile(PT_PATH) else "yolov8s-worldv2.pt"
    print(f"[i] Loading model: {pt_source}")
    model = YOLO(pt_source)

    print(f"[i] Injecting custom vocabulary ({len(CLASS_NAMES)} classes):")
    for i, name in enumerate(CLASS_NAMES):
        print(f"      [{i}] {name}")
    model.set_classes(CLASS_NAMES)

    print(f"[i] Exporting to ONNX (imgsz={args.imgsz})...")
    exported = model.export(format="onnx", imgsz=args.imgsz)
    # `exported` is the path returned by ultralytics; move/copy to skill dir if needed
    exported_path = str(exported) if exported else ""
    if exported_path and os.path.isfile(exported_path) and \
            os.path.abspath(exported_path) != os.path.abspath(ONNX_PATH):
        shutil.copy2(exported_path, ONNX_PATH)
        print(f"[i] Copied {exported_path} -> {ONNX_PATH}")

    if os.path.isfile(ONNX_PATH):
        size_mb = os.path.getsize(ONNX_PATH) / (1024 * 1024)
        print(f"[\u2713] Export complete: {ONNX_PATH} ({size_mb:.1f} MB)")
        return 0

    print(f"[x] Export finished but ONNX file not found at {ONNX_PATH}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
