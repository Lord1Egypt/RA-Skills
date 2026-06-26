#!/usr/bin/env python3
"""
voice_preprocessor.py — 音频预处理工具（Phase 1）

将微信/QQ 语音消息及其他音频转为干净的 WAV 文件，
同时服务于文字转录（audio_transcriber.py）和声音训练（GPT-SoVITS）。

处理流水线：
  1. 格式转换：silk/amr/mp3/m4a/ogg → WAV 16kHz mono
  2. 降噪增强（可选但推荐）
  3. 输出到 processed/ 目录

依赖：
  必需：pilk（silk 解码）、soundfile
  推荐：noisereduce（降噪）
  系统：ffmpeg（非 silk 格式转换）

用法：
  # 处理单个文件
  python voice_preprocessor.py --file msg.silk --output out.wav

  # 批量处理目录（微信语音导出场景）
  python voice_preprocessor.py --dir ./voice_messages/ --outdir ./processed/

  # 跳过降噪（加快速度）
  python voice_preprocessor.py --dir ./voices/ --outdir ./processed/ --no-denoise

  # 指定目标采样率（默认 16000，GPT-SoVITS 训练推荐）
  python voice_preprocessor.py --dir ./voices/ --outdir ./processed/ --sample-rate 24000
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

# ── 支持的格式 ────────────────────────────────────────────────────────────────

SILK_EXTS = {".silk", ".slk"}
AMR_EXTS = {".amr"}
FFMPEG_EXTS = {".mp3", ".m4a", ".ogg", ".flac", ".aac", ".wma", ".opus", ".wav", ".webm"}
ALL_AUDIO_EXTS = SILK_EXTS | AMR_EXTS | FFMPEG_EXTS


# ── 格式转换 ──────────────────────────────────────────────────────────────────

def convert_silk_to_wav(silk_path: str, wav_path: str, sample_rate: int = 16000) -> bool:
    """将微信/QQ silk 格式转为 WAV。"""
    try:
        import pilk
    except ImportError:
        print("[错误] 未安装 pilk，请运行：pip install pilk")
        return False

    try:
        # pilk 解码到 PCM，再用临时文件转 WAV
        # pilk.decode 输出的是 raw PCM，采样率 24000
        pcm_path = wav_path + ".pcm"

        # 微信 silk 文件可能有 #!SILK_V3 头部，pilk 会自动处理
        duration = pilk.decode(silk_path, pcm_path)

        # PCM → WAV（pilk 默认输出 24000Hz mono 16bit）
        _pcm_to_wav(pcm_path, wav_path, src_rate=24000, dst_rate=sample_rate)

        # 清理临时 PCM
        if os.path.exists(pcm_path):
            os.remove(pcm_path)

        return True
    except Exception as e:
        print(f"  [失败] silk 转换出错：{e}")
        return False


def convert_with_ffmpeg(input_path: str, wav_path: str, sample_rate: int = 16000) -> bool:
    """用 ffmpeg 将任意音频格式转为 WAV 16kHz mono。"""
    try:
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-ar", str(sample_rate),
            "-ac", "1",
            "-sample_fmt", "s16",
            wav_path,
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"  [失败] ffmpeg 错误：{result.stderr[:200]}")
            return False
        return True
    except FileNotFoundError:
        print("[错误] 未找到 ffmpeg，请安装 ffmpeg 并确保在 PATH 中")
        return False
    except subprocess.TimeoutExpired:
        print("  [失败] ffmpeg 超时")
        return False


def _pcm_to_wav(pcm_path: str, wav_path: str, src_rate: int = 24000, dst_rate: int = 16000) -> None:
    """将 raw PCM 转为 WAV 文件，可选重采样。"""
    import numpy as np
    import soundfile as sf

    # 读取 raw PCM（16-bit signed, mono）
    pcm_data = np.fromfile(pcm_path, dtype=np.int16)
    float_data = pcm_data.astype(np.float32) / 32768.0

    # 重采样（如果需要）
    if src_rate != dst_rate:
        try:
            from scipy.signal import resample
            num_samples = int(len(float_data) * dst_rate / src_rate)
            float_data = resample(float_data, num_samples)
        except ImportError:
            # 没有 scipy，直接用源采样率
            dst_rate = src_rate

    sf.write(wav_path, float_data, dst_rate, subtype="PCM_16")


def convert_file(input_path: str, wav_path: str, sample_rate: int = 16000) -> bool:
    """根据文件格式自动选择转换方法。"""
    ext = Path(input_path).suffix.lower()

    if ext in SILK_EXTS:
        return convert_silk_to_wav(input_path, wav_path, sample_rate)
    elif ext in AMR_EXTS:
        return convert_with_ffmpeg(input_path, wav_path, sample_rate)
    elif ext in FFMPEG_EXTS:
        # WAV 也走 ffmpeg 统一重采样到目标采样率
        return convert_with_ffmpeg(input_path, wav_path, sample_rate)
    else:
        print(f"  [跳过] 不支持的格式：{ext}")
        return False


# ── 降噪 ─────────────────────────────────────────────────────────────────────

def denoise_wav(wav_path: str, output_path: Optional[str] = None) -> bool:
    """对 WAV 文件进行降噪处理。"""
    if output_path is None:
        output_path = wav_path  # 原地替换

    try:
        import noisereduce as nr
        import soundfile as sf
        import numpy as np

        data, rate = sf.read(wav_path, dtype="float32")

        # noisereduce stationary noise reduction
        reduced = nr.reduce_noise(
            y=data,
            sr=rate,
            stationary=True,
            prop_decrease=0.75,   # 降噪强度，0.75 适中
        )

        sf.write(output_path, reduced, rate, subtype="PCM_16")
        return True

    except ImportError:
        print("  [警告] 未安装 noisereduce，跳过降噪（pip install noisereduce）")
        if output_path != wav_path:
            shutil.copy2(wav_path, output_path)
        return False
    except Exception as e:
        print(f"  [警告] 降噪失败：{e}，保留原始音频")
        if output_path != wav_path:
            shutil.copy2(wav_path, output_path)
        return False


# ── 音频信息 ──────────────────────────────────────────────────────────────────

def get_audio_info(wav_path: str) -> dict:
    """获取 WAV 文件的基本信息。"""
    try:
        import soundfile as sf
        info = sf.info(wav_path)
        return {
            "duration": info.duration,
            "sample_rate": info.samplerate,
            "channels": info.channels,
        }
    except Exception:
        return {"duration": 0, "sample_rate": 0, "channels": 0}


def fmt_duration(seconds: float) -> str:
    s = int(seconds)
    h, r = divmod(s, 3600)
    m, sec = divmod(r, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


# ── 批量处理 ──────────────────────────────────────────────────────────────────

def process_directory(
    input_dir: str,
    output_dir: str,
    sample_rate: int = 16000,
    do_denoise: bool = True,
) -> dict:
    """批量处理目录下所有音频文件。"""
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([
        f for f in os.listdir(input_dir)
        if Path(f).suffix.lower() in ALL_AUDIO_EXTS
    ])

    if not files:
        print(f"[警告] 目录中没有支持的音频文件：{input_dir}")
        return {"total": 0, "success": 0, "failed": 0, "skipped": 0, "duration": 0}

    print(f"[扫描] 找到 {len(files)} 个音频文件")

    stats = {"total": len(files), "success": 0, "failed": 0, "skipped": 0, "duration": 0}
    results = []

    for i, fname in enumerate(files, 1):
        input_path = os.path.join(input_dir, fname)
        stem = Path(fname).stem
        wav_name = f"{stem}.wav"
        wav_path = os.path.join(output_dir, wav_name)

        print(f"[{i}/{len(files)}] {fname}", end="")

        # Step 1: 格式转换
        if Path(fname).suffix.lower() == ".wav" and not do_denoise:
            # 已经是 WAV 且不降噪，直接复制
            shutil.copy2(input_path, wav_path)
            ok = True
        else:
            # 转换到临时文件，再降噪到最终路径
            if do_denoise:
                tmp_wav = wav_path + ".tmp.wav"
                ok = convert_file(input_path, tmp_wav, sample_rate)
            else:
                ok = convert_file(input_path, wav_path, sample_rate)

        if not ok:
            stats["failed"] += 1
            print(" ✗")
            continue

        # Step 2: 降噪
        if do_denoise and ok:
            tmp_wav = wav_path + ".tmp.wav"
            if os.path.exists(tmp_wav):
                denoise_wav(tmp_wav, wav_path)
                os.remove(tmp_wav)
            else:
                # convert_file 可能直接写到了 wav_path
                denoise_wav(wav_path)

        # Step 3: 统计
        info = get_audio_info(wav_path)
        dur = info.get("duration", 0)
        stats["duration"] += dur
        stats["success"] += 1
        results.append({"file": wav_name, "duration": dur})
        print(f" → {wav_name} ({fmt_duration(dur)})")

    return stats


# ── 报告生成 ──────────────────────────────────────────────────────────────────

def generate_report(stats: dict, input_dir: str, output_dir: str) -> str:
    lines = [
        "# 音频预处理报告",
        "",
        f"**输入目录**：{input_dir}",
        f"**输出目录**：{output_dir}",
        "",
        f"- 总文件数：{stats['total']}",
        f"- 成功转换：{stats['success']}",
        f"- 转换失败：{stats['failed']}",
        f"- 总时长：{fmt_duration(stats['duration'])}",
        "",
    ]

    if stats["duration"] > 0:
        lines += [
            "## 训练建议",
            "",
        ]
        dur = stats["duration"]
        if dur < 30:
            lines.append("⚠️ 有效音频不足 30 秒，建议使用 CosyVoice 零样本模式，或继续收集更多音频。")
        elif dur < 180:
            lines.append(f"音频 {fmt_duration(dur)}，可使用 GPT-SoVITS few-shot 模式（效果一般）或 CosyVoice 零样本。")
            lines.append("建议继续收集音频至 3-5 分钟以获得更好效果。")
        elif dur < 600:
            lines.append(f"音频 {fmt_duration(dur)}，适合 GPT-SoVITS 微调训练，预期效果良好。")
        else:
            lines.append(f"音频 {fmt_duration(dur)}，非常充足，GPT-SoVITS 微调后预期效果极佳。")
        lines.append("")

    lines += [
        "---",
        "*预处理完成后，这些 WAV 文件可用于：*",
        "*1. audio_transcriber.py — 转录为文字，填充纪念档案*",
        '*2. GPT-SoVITS — 训练声音模型，让档案"发出 ta 的声音"*',
    ]
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="音频预处理工具 — 微信/QQ 语音转为干净 WAV",
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="单个音频文件")
    src.add_argument("--dir", help="批量处理：音频文件所在目录")

    parser.add_argument("--output", help="单文件模式的输出路径")
    parser.add_argument("--outdir", default="./processed",
                        help="批量模式的输出目录（默认 ./processed）")
    parser.add_argument("--sample-rate", type=int, default=16000,
                        help="目标采样率（默认 16000，GPT-SoVITS 推荐）")
    parser.add_argument("--no-denoise", action="store_true",
                        help="跳过降噪步骤（加快处理速度）")
    parser.add_argument("--report", help="输出处理报告的路径")

    args = parser.parse_args()

    if args.file:
        # 单文件模式
        if not os.path.exists(args.file):
            print(f"[错误] 找不到文件：{args.file}")
            sys.exit(1)

        out = args.output or (Path(args.file).stem + "_processed.wav")
        print(f"[处理] {args.file} → {out}")

        ok = convert_file(args.file, out, args.sample_rate)
        if ok and not args.no_denoise:
            denoise_wav(out)

        if ok:
            info = get_audio_info(out)
            print(f"[完成] {fmt_duration(info['duration'])} / {info['sample_rate']}Hz / {info['channels']}ch")
        else:
            sys.exit(1)
    else:
        # 批量模式
        if not os.path.isdir(args.dir):
            print(f"[错误] 找不到目录：{args.dir}")
            sys.exit(1)

        stats = process_directory(
            args.dir, args.outdir, args.sample_rate,
            do_denoise=not args.no_denoise,
        )

        print(f"\n[汇总] 成功 {stats['success']}/{stats['total']}，"
              f"总时长 {fmt_duration(stats['duration'])}")

        if args.report:
            report = generate_report(stats, args.dir, args.outdir)
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"[报告] 已保存到 {args.report}")


if __name__ == "__main__":
    main()
