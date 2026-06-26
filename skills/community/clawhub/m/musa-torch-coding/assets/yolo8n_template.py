"""
YOLOv8n Training/Inference Template for MUSA (Moore Threads GPU)
适配摩尔线程 GPU 的 YOLOv8-nano 目标检测代码

Environment:
    - conda v1.2 or v1.3 with torch_musa installed
    - MUSA driver 2.7.0+, MUSAToolkits rc3.1.0+

Usage:
    python yolo8n_template.py --mode train --data coco128.yaml
    python yolo8n_template.py --mode val --weights runs/train/exp/weights/best.pt
    python yolo8n_template.py --mode predict --weights best.pt --source image.jpg
"""

import os
import argparse
import torch
import torch.distributed as dist
import torch_musa  # MUST import for MUSA support
from pathlib import Path


def setup_distributed():
    """Setup MUSA DDP (Distributed Data Parallel)"""
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        # MUSA uses 'mccl' backend instead of 'nccl'
        dist.init_process_group(backend="mccl", rank=rank, world_size=world_size)
        return rank, world_size
    return 0, 1


def get_device():
    """Get MUSA device if available"""
    if torch.musa.is_available():
        print(f"✅ MUSA GPU available: {torch.musa.device_count()} device(s)")
        for i in range(torch.musa.device_count()):
            print(f"   MUSA:{i} - {torch.musa.get_device_name(i)}")
        return torch.device("musa")
    else:
        print("⚠️  MUSA not available, using CPU")
        return torch.device("cpu")


def train(args):
    """Train YOLOv8n on MUSA"""
    from ultralytics import YOLO
    
    # Setup
    device = get_device()
    rank, world_size = setup_distributed()
    
    # Load model
    model = YOLO(args.weights if args.weights else "yolov8n.pt")
    
    # Training args
    train_args = {
        "data": args.data,
        "epochs": args.epochs,
        "batch": args.batch,
        "imgsz": args.imgsz,
        "device": str(device),  # YOLO expects string like "musa" or "0,1,2,3"
        "workers": args.workers,
        "project": args.project,
        "name": args.name,
        "exist_ok": False,
        "pretrained": True,
        "optimizer": "AdamW",
        "lr0": 0.01,
        "amp": True,  # Automatic Mixed Precision
    }
    
    # Multi-GPU DDP
    if world_size > 1:
        train_args["device"] = list(range(torch.musa.device_count()))
    
    # Train
    results = model.train(**train_args)
    
    # Cleanup
    if world_size > 1:
        dist.destroy_process_group()
    
    return results


def validate(args):
    """Validate YOLOv8n on MUSA"""
    from ultralytics import YOLO
    
    device = get_device()
    model = YOLO(args.weights)
    
    metrics = model.val(
        data=args.data,
        device=str(device),
        batch=args.batch,
        imgsz=args.imgsz,
    )
    
    print(f"\n📊 Validation Results:")
    print(f"   mAP50: {metrics.box.map50:.4f}")
    print(f"   mAP50-95: {metrics.box.map:.4f}")
    
    return metrics


def predict(args):
    """Inference with YOLOv8n on MUSA"""
    from ultralytics import YOLO
    
    device = get_device()
    model = YOLO(args.weights)
    
    results = model(
        args.source,
        device=str(device),
        imgsz=args.imgsz,
        conf=args.conf,
        show=args.show,
        save=args.save,
    )
    
    for result in results:
        print(f"Detected {len(result.boxes)} objects")
    
    return results


def export_model(args):
    """Export model to ONNX/TensorRT"""
    from ultralytics import YOLO
    
    device = get_device()
    model = YOLO(args.weights)
    
    export_path = model.export(
        format=args.format,
        device=str(device),
        imgsz=args.imgsz,
    )
    
    print(f"✅ Exported to: {export_path}")
    return export_path


def main():
    parser = argparse.ArgumentParser(description="YOLOv8n for MUSA GPU")
    parser.add_argument("--mode", choices=["train", "val", "predict", "export"], required=True)
    parser.add_argument("--data", default="coco128.yaml", help="Dataset config")
    parser.add_argument("--weights", default="", help="Model weights path")
    parser.add_argument("--source", default="0", help="Inference source (image/video/camera)")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--project", default="runs/train")
    parser.add_argument("--name", default="yolo8n_musa")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold")
    parser.add_argument("--format", default="onnx", choices=["onnx", "engine", "torchscript"])
    parser.add_argument("--show", action="store_true", help="Show results")
    parser.add_argument("--save", action="store_true", help="Save results")
    
    args = parser.parse_args()
    
    # Run mode
    if args.mode == "train":
        train(args)
    elif args.mode == "val":
        validate(args)
    elif args.mode == "predict":
        predict(args)
    elif args.mode == "export":
        export_model(args)


if __name__ == "__main__":
    main()
