# -*- coding: utf-8 -*-
"""用训练好的 MiniViT 识别图片里的数字。

用法: python vision/predict.py 图1.png 图2.png ... [--ckpt checkpoints/vit]
自动处理:转灰度、缩放 28x28、白底黑字自动反色(训练数据是黑底白字)。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from PIL import Image

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
REPO_ROOT = _HERE.parent

from vit import ViTConfig, VisionTransformer


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MiniViT 数字识别")
    p.add_argument("images", nargs="+", help="png/jpg 图片路径")
    p.add_argument("--ckpt", default=str(REPO_ROOT / "checkpoints" / "vit"))
    p.add_argument("--device", default="auto")
    p.add_argument("--json", action="store_true")
    return p.parse_args()


def preprocess(path: str, mean: float, std: float):
    img = Image.open(path).convert("L").resize((28, 28))
    t = torch.frombuffer(bytearray(img.tobytes()), dtype=torch.uint8).reshape(28, 28).float() / 255
    inverted = False
    if t.mean() > 0.5:          # 白底黑字 → 反色成黑底白字
        t = 1.0 - t
        inverted = True
    x = ((t - mean) / std).unsqueeze(0).unsqueeze(0)
    return x, inverted


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = parse_args()
    device = ("cuda" if torch.cuda.is_available() else "cpu") if args.device == "auto" else args.device

    ckpt_path = Path(args.ckpt) / "ckpt.pt"
    if not ckpt_path.exists():
        sys.exit(f"[错误] 找不到 {ckpt_path},请先运行 python vision/train_vit.py")
    state = torch.load(str(ckpt_path), map_location=device, weights_only=True)
    cfg = ViTConfig.from_dict(state["config"])
    model = VisionTransformer(cfg).to(device)
    model.load_state_dict(state["model"])
    model.eval()
    mean, std = float(state["mean"]), float(state["std"])
    print(f"已加载: {ckpt_path}(数据集 {state.get('dataset')},"
          f"epoch {state.get('epoch')},测试准确率 {state.get('test_acc', 0):.2%})\n")

    out = []
    with torch.no_grad():
        for path in args.images:
            try:
                x, inverted = preprocess(path, mean, std)
            except Exception as e:
                print(f"{path}: 读取失败 {e}")
                continue
            probs = torch.softmax(model(x.to(device))[0], dim=-1)
            top = torch.topk(probs, 3)
            pred = int(top.indices[0])
            conf = float(top.values[0])
            out.append({"image": path, "pred": pred, "conf": round(conf, 4),
                        "top3": {int(i): round(float(v), 4) for i, v in zip(top.indices, top.values)},
                        "inverted": inverted})
            tag = "(已反色)" if inverted else ""
            tops = ", ".join(f"{int(i)}:{float(v):.1%}" for i, v in zip(top.indices, top.values))
            print(f"{Path(path).name}: 识别为 {pred}(置信度 {conf:.1%}){tag} | top3: {tops}")
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
