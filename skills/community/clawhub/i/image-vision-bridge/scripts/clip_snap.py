#!/usr/bin/env python3
"""
剪贴板图片快照 — 一键保存剪贴板图片到固定目录，输出路径到控制台。

用法:
    python clip_snap.py              # 保存到默认目录，输出路径
    python clip_snap.py -q           # 安静模式，仅输出路径（适合管道）
    python clip_snap.py --dir ./imgs # 指定输出目录

输出:
    图片保存路径（同时尝试复制到剪贴板，方便直接粘贴到聊天框）

依赖: pip install pillow pyperclip (pyperclip 可选，用于复制路径到剪贴板)
      没有 pyperclip 也能用，路径会打印到控制台。
"""

import sys
import os
import argparse
from datetime import datetime
from pathlib import Path

DEFAULT_DIR = os.path.expanduser("~/.workbuddy/clip-snaps")


def save_clipboard_image(output_dir: str, quiet: bool = False) -> str | None:
    """从剪贴板读取图片并保存，返回文件路径。"""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:18]
    filename = f"snap_{timestamp}.png"
    filepath = os.path.join(output_dir, filename)

    # 优先用 Pillow 读剪贴板
    try:
        from PIL import ImageGrab

        img = ImageGrab.grabclipboard()
        if img is None:
            if not quiet:
                print("[ERROR] 剪贴板中没有图片", file=sys.stderr)
            return None
        if isinstance(img, list):
            # 多文件时取第一个
            img = Image.open(img[0]) if img else None
        if img is None:
            if not quiet:
                print("[ERROR] 无法读取剪贴板图片", file=sys.stderr)
            return None
        img.save(filepath, "PNG")
    except ImportError:
        # Pillow 不可用时，通过 stdin 将路径安全传入 PowerShell
        import subprocess

        ps_script = r"""
$path = $input | Out-String | ForEach-Object { $_.Trim() }
Add-Type -AssemblyName System.Windows.Forms
$img = [System.Windows.Forms.Clipboard]::GetImage()
if ($img) {
    $img.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output "OK"
} else {
    Write-Output "NO_IMAGE"
}
"""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            input=filepath,
            capture_output=True, text=True, timeout=10
        )
        if "NO_IMAGE" in result.stdout:
            if not quiet:
                print("[ERROR] 剪贴板中没有图片", file=sys.stderr)
            return None
        if not os.path.exists(filepath):
            if not quiet:
                print("[ERROR] PowerShell 保存图片失败", file=sys.stderr)
            return None

    if not quiet:
        print(f"[OK] 已保存: {filepath}", file=sys.stderr)

    return filepath


def copy_to_clipboard(text: str) -> bool:
    """复制路径到剪贴板，方便粘贴到聊天框。"""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        try:
            import subprocess
            # 安全：通过 stdin 传递文本，避免注入
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "$txt = $input | Out-String; Set-Clipboard -Value $txt"],
                input=text,
                capture_output=True, text=True, timeout=5
            )
            return True
        except Exception:
            return False


def main():
    parser = argparse.ArgumentParser(description="一键保存剪贴板图片")
    parser.add_argument(
        "--dir", "-d",
        default=DEFAULT_DIR,
        help=f"输出目录 (默认: {DEFAULT_DIR})",
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="安静模式，仅输出路径",
    )
    parser.add_argument(
        "--no-clip",
        action="store_true",
        help="不自动复制路径到剪贴板",
    )
    args = parser.parse_args()

    filepath = save_clipboard_image(args.dir, quiet=args.quiet)
    if filepath is None:
        sys.exit(1)

    # 输出路径到 stdout
    print(filepath)

    # 尝试复制路径到剪贴板
    if not args.no_clip:
        if copy_to_clipboard(filepath):
            if not args.quiet:
                print("[OK] 路径已复制到剪贴板，直接 Ctrl+V 粘贴到聊天框", file=sys.stderr)


if __name__ == "__main__":
    main()
