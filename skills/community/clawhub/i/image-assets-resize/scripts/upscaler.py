#!/usr/bin/env python3
"""
超分辨率放大模块

将图片放大到目标尺寸：
1. Real-ESRGAN (ncnn-vulkan) — AI 超分，质量最好，需要单独下载模型
2. Pillow LANCZOS — 内置降级方案，无需额外依赖

用法:
  from upscaler import upscale_image
  ok, method = upscale_image("input.png", "output.png", target_width=2000, target_height=1500)
"""

from __future__ import annotations

import os
import subprocess
import zipfile
from pathlib import Path
from typing import Optional

try:
    from PIL import Image
except ImportError:
    Image = None

# ── 路径配置 ──────────────────────────────────────────────────

BIN_DIR = Path.home() / ".local" / "bin"
ESRGAN_DIR = BIN_DIR / "realesrgan-ncnn-vulkan"
ESRGAN_VERSION = "v0.2.0"
ESRGAN_ZIP_URL = (
    "https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases/download/"
    f"{ESRGAN_VERSION}/realesrgan-ncnn-vulkan-{ESRGAN_VERSION}-windows.zip"
)

# 已知的模型文件清单（用于完整性检查）
REQUIRED_MODELS = [
    "realesr-animevideov3-x2.param", "realesr-animevideov3-x2.bin",
    "realesr-animevideov3-x3.param", "realesr-animevideov3-x3.bin",
    "realesr-animevideov3-x4.param", "realesr-animevideov3-x4.bin",
]


def _esrgan_dir() -> Path:
    """ESRGAN 可执行文件所在目录"""
    exe = _find_esrgan_exe()
    return exe.parent if exe else ESRGAN_DIR


def _find_esrgan_exe() -> Optional[Path]:
    """在安装目录中查找 realesrgan-ncnn-vulkan.exe"""
    if not ESRGAN_DIR.exists():
        return None
    for subdir in [ESRGAN_DIR] + list(ESRGAN_DIR.iterdir()):
        exe = subdir / "realesrgan-ncnn-vulkan.exe"
        if exe.exists():
            return exe
    return None


def _check_esrgan_models(exe_dir: Path) -> bool:
    """检查模型文件是否完整"""
    models_dir = exe_dir / "models"
    if not models_dir.exists():
        return False
    for model in REQUIRED_MODELS:
        if not (models_dir / model).exists():
            return False
    return True


def is_esrgan_available() -> tuple[bool, str]:
    """检查 Real-ESRGAN 是否可用（含模型）"""
    exe = _find_esrgan_exe()
    if not exe:
        return False, "未安装"
    if not _check_esrgan_models(exe.parent):
        return False, "模型文件缺失"
    return True, "就绪"


def install_esrgan() -> tuple[bool, str]:
    """下载安装 Real-ESRGAN（不含模型，模型需另行下载）"""
    exe = _find_esrgan_exe()
    if exe and _check_esrgan_models(exe.parent):
        return True, "已就绪"

    # 下载 binary（未含模型）
    if not exe:
        zip_path = BIN_DIR / "realesrgan.zip"
        try:
            BIN_DIR.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["curl", "-fsSL", "-o", str(zip_path), ESRGAN_ZIP_URL],
                capture_output=True, timeout=120, check=True,
            )
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(str(ESRGAN_DIR))
            zip_path.unlink()
            exe = _find_esrgan_exe()
            if not exe:
                return False, "安装失败：解压后未找到可执行文件"
        except Exception as e:
            if zip_path.exists():
                zip_path.unlink()
            return False, f"下载失败: {e}"

    return True, "binary 已安装，模型文件缺失：请从 GitHub Releases 手动下载 models/ 目录"


# ── 超分核心 ──────────────────────────────────────────────────


def upscale_image(
    input_path: str,
    output_path: str,
    target_width: int,
    target_height: int,
) -> tuple[bool, str]:
    """
    将图片放大到目标尺寸。

    返回 (成功, 使用方法描述)
    """
    if not os.path.exists(input_path):
        return False, "源文件不存在"

    if Image is None:
        return False, "Pillow 不可用"

    # 读取源尺寸
    src_img = Image.open(input_path)
    src_w, src_h = src_img.size
    src_img.close()

    # 如果目标 <= 源尺寸，直接保存
    if target_width <= src_w and target_height <= src_h:
        img = Image.open(input_path)
        img.save(output_path, "PNG")
        return True, "无需放大"

    # ── 方案 1: Real-ESRGAN（需 binary + 模型完整）──
    esrgan_ok, esrgan_status = is_esrgan_available()
    if esrgan_ok:
        scale_x = target_width / src_w
        scale_y = target_height / src_h
        esrgan_scale = max(2, min(4, int(max(scale_x, scale_y))))

        exe = _find_esrgan_exe()
        tmp_path = output_path + ".esrgan_tmp.png"

        try:
            result = subprocess.run(
                [str(exe), "-i", input_path, "-o", tmp_path,
                 "-s", str(esrgan_scale), "-f", "png"],
                capture_output=True, text=True, timeout=300,
                cwd=str(exe.parent),
            )

            if result.returncode == 0 and Path(tmp_path).exists():
                # ESRGAN 放大后再精确 resize
                img = Image.open(tmp_path)
                img_resized = img.resize((target_width, target_height), Image.LANCZOS)
                img_resized.save(output_path, "PNG")
                img.close()
                img_resized.close()
                Path(tmp_path).unlink(missing_ok=True)
                return True, f"Real-ESRGAN {esrgan_scale}x"
            else:
                Path(tmp_path).unlink(missing_ok=True)
        except Exception:
            Path(tmp_path).unlink(missing_ok=True)

        # ESRGAN 失败，降级到 Pillow
        print(f"        ESRGAN 执行失败，降级到基础放大... ")

    # ── 方案 2: Pillow LANCZOS ──
    img = Image.open(input_path)
    img_resized = img.resize((target_width, target_height), Image.LANCZOS)
    img_resized.save(output_path, "PNG")
    img.close()
    img_resized.close()

    method = "基础放大 (Pillow LANCZOS)"
    if not esrgan_ok and esrgan_status != "已安装":
        # 首次提示用户可安装 ESRGAN
        print(f"\n        💡 如需更高质量超分，可安装 Real-ESRGAN:")
        print(f"           手动下载 models/ 目录放入:")
        print(f"           {_esrgan_dir() / 'models'}/")

    return True, method


# ── CLI ──────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(description="超分辨率放大工具")
    parser.add_argument("input", nargs="?", help="输入图片路径")
    parser.add_argument("output", nargs="?", help="输出图片路径")
    parser.add_argument("--width", type=int, help="目标宽度")
    parser.add_argument("--height", type=int, help="目标高度")
    parser.add_argument("--install", action="store_true", help="安装 ESRGAN binary")
    parser.add_argument("--check", action="store_true", help="检查 ESRGAN 状态")

    args = parser.parse_args()

    if args.install:
        ok, msg = install_esrgan()
        print(f"{'✓' if ok else '✗'} {msg}")
        return

    if args.check:
        ok, msg = is_esrgan_available()
        print(f"Real-ESRGAN: {'✓' if ok else '✗'} ({msg})")
        return

    if not args.input or not args.output or not args.width or not args.height:
        parser.print_help()
        print("\nError: 缺少必要参数")
        return

    ok, method = upscale_image(args.input, args.output, args.width, args.height)
    if ok:
        print(f"✓ {method}")
    else:
        print(f"✗ {method}")


if __name__ == "__main__":
    main()
