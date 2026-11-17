# -*- coding: utf-8 -*-
"""视觉数据集:优先下载 MNIST(官方镜像);网络不通时用 PIL 本地渲染合成数字,完全离线可跑。

直接运行可查看数据集自检结果:python vision/data.py
"""

from __future__ import annotations

import gzip
import random
import struct
import sys
import urllib.request
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE.parent
MNIST_DIR = REPO_ROOT / "data" / "mnist"

MIRRORS = [
    "https://ossci-datasets.s3.amazonaws.com/mnist/",
    "https://storage.googleapis.com/cvdf-datasets/mnist/",
]
FILES = [
    "train-images-idx3-ubyte.gz", "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz", "t10k-labels-idx1-ubyte.gz",
]


def _download_mnist() -> bool:
    MNIST_DIR.mkdir(parents=True, exist_ok=True)
    for fn in FILES:
        dst = MNIST_DIR / fn
        if dst.exists() and dst.stat().st_size > 1000:
            continue
        ok = False
        for base in MIRRORS:
            try:
                req = urllib.request.Request(base + fn, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=25) as r:
                    dst.write_bytes(r.read())
                print(f"[下载OK] {fn}", file=sys.stderr)
                ok = True
                break
            except Exception as e:
                print(f"[下载失败] {base}{fn}: {type(e).__name__}", file=sys.stderr)
        if not ok:
            return False
    return True


def _read_images(path: Path) -> torch.Tensor:
    with gzip.open(path, "rb") as f:
        b = f.read()
    n = struct.unpack(">I", b[4:8])[0]
    return torch.frombuffer(bytearray(b[16:]), dtype=torch.uint8).reshape(n, 28, 28)


def _read_labels(path: Path) -> torch.Tensor:
    with gzip.open(path, "rb") as f:
        b = f.read()
    return torch.frombuffer(bytearray(b[8:]), dtype=torch.uint8)


def make_synthetic(n_train: int = 12000, n_test: int = 2000, seed: int = 7):
    """PIL 渲染合成数字:多字体 + 随机旋转/平移/模糊。黑底白字,与 MNIST 一致。"""
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    rng = random.Random(seed)
    fonts = []
    # 训练字体(故意不含 comic/segoepr/segoesc,留给 make_samples 当分布外考题)
    for name in ["arial.ttf", "arialbd.ttf", "times.ttf", "consola.ttf",
                 "calibri.ttf", "segoeui.ttf", "tahoma.ttf", "georgia.ttf",
                 "verdana.ttf", "trebuc.ttf", "couri.ttf", "impact.ttf"]:
        try:
            fonts.append(ImageFont.truetype(name, 46))
        except Exception:
            continue
    if not fonts:
        fonts = [ImageFont.load_default()]

    def render(digit: int) -> torch.Tensor:
        big = 64                      # 先在大画布上完整画出字形,再缩到 28x28,避免裁切
        img = Image.new("L", (big, big), 0)
        ImageDraw.Draw(img).text((big // 2, big // 2), str(digit), fill=255,
                                 font=rng.choice(fonts), anchor="mm")
        img = img.rotate(rng.uniform(-25, 25), resample=Image.BILINEAR, fillcolor=0)
        dx, dy = rng.randint(-3, 3), rng.randint(-3, 3)
        img = img.transform((big, big), Image.AFFINE, (1, 0, -dx, 0, 1, -dy),
                            resample=Image.BILINEAR, fillcolor=0)
        if rng.random() < 0.5:
            img = img.filter(ImageFilter.GaussianBlur(rng.uniform(0.5, 1.2)))
        img = img.resize((28, 28), Image.BILINEAR)
        return torch.frombuffer(bytearray(img.tobytes()), dtype=torch.uint8).reshape(28, 28)

    def make(n: int):
        xs = torch.zeros((n, 28, 28), dtype=torch.uint8)
        ys = torch.zeros(n, dtype=torch.uint8)
        for i in range(n):
            y = rng.randrange(10)
            xs[i] = render(y)
            ys[i] = y
        return xs, ys

    trx, tryy = make(n_train)
    tex, tey = make(n_test)
    return trx, tryy, tex, tey


def load_dataset(prefer: str = "auto"):
    """返回 (数据集名, 训练图, 训练标签, 测试图, 测试标签)。MNIST 优先,失败自动合成。"""
    if prefer in ("auto", "mnist"):
        try:
            if _download_mnist():
                trx = _read_images(MNIST_DIR / FILES[0])
                tryy = _read_labels(MNIST_DIR / FILES[1])
                tex = _read_images(MNIST_DIR / FILES[2])
                tey = _read_labels(MNIST_DIR / FILES[3])
                return "mnist", trx, tryy, tex, tey
        except Exception as e:
            print(f"[MNIST 不可用] {e} → 改用本地合成数字", file=sys.stderr)
    trx, tryy, tex, tey = make_synthetic()
    return "synthetic", trx, tryy, tex, tey


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    name, trx, tryy, tex, tey = load_dataset()
    print(f"数据集自检: {name} | 训练 {trx.shape[0]:,} 张 | 测试 {tex.shape[0]:,} 张 | "
          f"{trx.shape[1]}x{trx.shape[2]} 灰度图 | 标签范围 {int(tryy.min())}~{int(tryy.max())}")
