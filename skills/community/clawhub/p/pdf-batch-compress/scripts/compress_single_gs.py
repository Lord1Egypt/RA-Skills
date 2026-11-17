#!/usr/bin/env python3
"""
单文件PDF压缩脚本 - Ghostscript版
用法: python3 compress_single_gs.py <filepath> [threshold_mb]
压缩成功后替换原文件，原文件被删除。
保留文本可搜索，画质更好，速度比PyMuPDF快4-6倍。

自动检测 gs 路径（支持 Apple Silicon 和 Intel Mac）。
"""
import os
import sys
import tempfile
import shutil
import subprocess

# 自动检测阈值
THRESHOLD_MB = int(sys.argv[2]) if len(sys.argv) > 2 else 50
THRESHOLD = THRESHOLD_MB * 1024 * 1024

# 自动检测 gs 路径
GS = None
for candidate in ["/opt/homebrew/bin/gs", "/usr/local/bin/gs", "/usr/bin/gs"]:
    if os.path.exists(candidate):
        GS = candidate
        break
if not GS:
    # 尝试从 PATH 查找
    try:
        result = subprocess.run(["which", "gs"], capture_output=True, text=True)
        if result.returncode == 0:
            GS = result.stdout.strip()
    except Exception:
        pass

if not GS:
    print(f"ERROR|{sys.argv[1] if len(sys.argv) > 1 else 'unknown'}|0|0|ghostscript_not_found")
    sys.exit(1)


def get_size(path):
    return os.path.getsize(path)


def run_gs(input_path, output_path, pdfsettings="ebook", extra_args=None):
    """运行Ghostscript压缩"""
    cmd = [
        GS, "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS=/{pdfsettings}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        "-dDetectDuplicateImages=true",
        "-dCompressFonts=true",
        "-dSubsetFonts=true",
        "-dEmbedAllFonts=true",
        "-dAutoRotatePages=/None",
    ]
    if extra_args:
        cmd.extend(extra_args)
    cmd.append(f"-sOutputFile={output_path}")
    cmd.append(input_path)

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return result.returncode == 0


def compress(filepath):
    orig_size = get_size(filepath)
    orig_mb = orig_size / (1024 * 1024)

    if orig_size <= THRESHOLD:
        print(f"SKIP|{filepath}|{orig_mb:.1f}|{orig_mb:.1f}|already_small")
        return

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.pdf', dir='/tmp')
    os.close(tmp_fd)

    try:
        # 根据文件大小选择初始压缩级别
        if orig_mb <= 100:
            # 小文件：先试ebook (150dpi) 保留较好画质
            levels = ["ebook", "screen", "screen_aggressive", "screen_extreme"]
        elif orig_mb <= 200:
            # 中等文件：直接用screen
            levels = ["screen", "screen_aggressive", "screen_extreme"]
        else:
            # 大文件：直接用aggressive
            levels = ["screen_aggressive", "screen_extreme"]

        for level in levels:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

            if level == "ebook":
                success = run_gs(filepath, tmp_path, "ebook")
            elif level == "screen":
                success = run_gs(filepath, tmp_path, "screen")
            elif level == "screen_aggressive":
                # 72dpi + 额外压缩
                extra = [
                    "-dDownsampleColorImages=true",
                    "-dColorImageResolution=72",
                    "-dColorImageDownsampleThreshold=1.0",
                    "-dColorImageDownsampleType=/Bicubic",
                    "-dDownsampleGrayImages=true",
                    "-dGrayImageResolution=72",
                    "-dGrayImageDownsampleThreshold=1.0",
                    "-dGrayImageDownsampleType=/Bicubic",
                    "-dDownsampleMonoImages=true",
                    "-dMonoImageResolution=72",
                    "-dMonoImageDownsampleThreshold=1.0",
                    "-dMonoImageDownsampleType=/Bicubic",
                    "-dAutoFilterColorImages=false",
                    "-dColorImageFilter=/DCTDecode",
                    "-c .setpdfwrite << /ColorACSImageDict << /QFactor 1.5 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> >> setdistillerparams",
                ]
                success = run_gs(filepath, tmp_path, "screen", extra)
            elif level == "screen_extreme":
                # 50dpi 极限压缩
                extra = [
                    "-dDownsampleColorImages=true",
                    "-dColorImageResolution=50",
                    "-dColorImageDownsampleThreshold=1.0",
                    "-dColorImageDownsampleType=/Bicubic",
                    "-dDownsampleGrayImages=true",
                    "-dGrayImageResolution=50",
                    "-dGrayImageDownsampleThreshold=1.0",
                    "-dGrayImageDownsampleType=/Bicubic",
                    "-dDownsampleMonoImages=true",
                    "-dMonoImageResolution=50",
                    "-dMonoImageDownsampleThreshold=1.0",
                    "-dMonoImageDownsampleType=/Bicubic",
                    "-dAutoFilterColorImages=false",
                    "-dColorImageFilter=/DCTDecode",
                    "-c .setpdfwrite << /ColorACSImageDict << /QFactor 2.0 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] >> >> setdistillerparams",
                ]
                success = run_gs(filepath, tmp_path, "screen", extra)

            if not success:
                continue

            new_size = get_size(tmp_path)
            if new_size <= THRESHOLD:
                new_mb = new_size / (1024 * 1024)
                shutil.move(tmp_path, filepath)
                print(f"OK|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|{level}")
                return

        # 最佳努力
        if os.path.exists(tmp_path) and get_size(tmp_path) < orig_size * 0.7:
            new_mb = get_size(tmp_path) / (1024 * 1024)
            shutil.move(tmp_path, filepath)
            print(f"PARTIAL|{filepath}|{orig_mb:.1f}|{new_mb:.1f}|best_effort")
        else:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            print(f"FAIL|{filepath}|{orig_mb:.1f}|{orig_mb:.1f}|no_compression")

    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        print(f"ERROR|{filepath}|{orig_mb:.1f}|0|{str(e)[:100]}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: compress_single_gs.py <filepath> [threshold_mb]")
        sys.exit(1)
    compress(sys.argv[1])
