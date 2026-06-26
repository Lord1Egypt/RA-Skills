#!/usr/bin/env python3
"""
voice_synthesizer.py — 语音合成工具

输入文字 → 输出用亲人声音说出的音频。

核心策略（实测验证）：
  - SoVITS 模型：使用微调后的（学习目标人音色）
  - GPT 模型：优先使用预训练底模（方言/转录不准时效果更好）
              如果用户指定微调的 GPT 模型也支持

用法：
  # 单句合成（自动选择模型和参考音频）
  python voice_synthesizer.py --slug grandpa --text "吃亏是福"

  # 指定输出路径
  python voice_synthesizer.py --slug grandpa --text "吃亏是福" --output grandpa.wav

  # 指定参考音频（影响语气）
  python voice_synthesizer.py --slug grandpa --text "吃亏是福" --ref-audio ref.wav

  # 使用微调的 GPT（普通话清晰的数据适用）
  python voice_synthesizer.py --slug grandpa --text "吃亏是福" --use-finetuned-gpt

  # 批量合成
  python voice_synthesizer.py --slug grandpa --text-file sentences.txt --outdir ./output/

  # 检查环境
  python voice_synthesizer.py --slug grandpa --action check
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MEMORIALS_DIR = os.path.join(PROJECT_ROOT, "memorials")
DEFAULT_SOVITS_DIR = os.path.join(PROJECT_ROOT, "GPT-SoVITS")


def voice_dir(slug: str) -> str:
    return os.path.join(MEMORIALS_DIR, slug, "voice")


def get_sovits_dir() -> str:
    d = os.environ.get("GPT_SOVITS_DIR", DEFAULT_SOVITS_DIR)
    return d if os.path.isdir(d) else ""


# ── 模型查找 ──────────────────────────────────────────────────────────────────

def find_sovits_model(slug: str) -> Optional[str]:
    """查找微调的 SoVITS 模型（.pth）。"""
    model_dir = os.path.join(voice_dir(slug), "gpt_sovits")
    if not os.path.isdir(model_dir):
        return None
    pth = [f for f in os.listdir(model_dir) if f.endswith(".pth")]
    if pth:
        return os.path.join(model_dir, sorted(pth)[-1])
    # 也查 GPT-SoVITS 的输出目录
    sovits_dir = get_sovits_dir()
    if sovits_dir:
        weight_dir = os.path.join(sovits_dir, "SoVITS_weights_v2")
        if os.path.isdir(weight_dir):
            matches = [f for f in os.listdir(weight_dir) if slug in f and f.endswith(".pth")]
            if matches:
                return os.path.join(weight_dir, sorted(matches)[-1])
    return None


def find_gpt_model(slug: str, use_finetuned: bool = False) -> Optional[str]:
    """
    查找 GPT 模型。
    默认返回预训练底模（方言场景更稳定）。
    use_finetuned=True 时返回微调模型（普通话场景效果更好）。
    """
    sovits_dir = get_sovits_dir()
    if not sovits_dir:
        return None

    if use_finetuned:
        # 查找微调的 GPT 模型
        model_dir = os.path.join(voice_dir(slug), "gpt_sovits")
        if os.path.isdir(model_dir):
            ckpt = [f for f in os.listdir(model_dir) if f.endswith(".ckpt")]
            if ckpt:
                return os.path.join(model_dir, sorted(ckpt)[-1])
        weight_dir = os.path.join(sovits_dir, "GPT_weights_v2")
        if os.path.isdir(weight_dir):
            matches = [f for f in os.listdir(weight_dir) if slug in f and f.endswith(".ckpt")]
            if matches:
                return os.path.join(weight_dir, sorted(matches)[-1])

    # 预训练底模（默认，方言友好）
    pretrained = os.path.join(sovits_dir, "GPT_SoVITS", "pretrained_models",
                              "gsv-v2final-pretrained",
                              "s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt")
    if os.path.exists(pretrained):
        return pretrained
    return None


def find_ref_audio(slug: str) -> Optional[str]:
    """从训练数据中自动选择 3-10 秒的参考音频。"""
    tdir = os.path.join(voice_dir(slug), "training_data", "wavs")
    if not os.path.isdir(tdir):
        return None
    try:
        import soundfile as sf
        best, best_score = None, float("inf")
        for f in os.listdir(tdir):
            if not f.endswith(".wav"):
                continue
            path = os.path.join(tdir, f)
            dur = sf.info(path).duration
            # GPT-SoVITS 要求 3-10 秒
            if 3 <= dur <= 10:
                score = abs(dur - 7)  # 7 秒最理想
                if score < best_score:
                    best, best_score = path, score
        return best
    except Exception:
        return None


def find_ref_text(ref_audio: str, slug: str) -> str:
    """从标注文件中查找参考音频对应的转录文本。"""
    ann_path = os.path.join(voice_dir(slug), "training_data", "annotations.list")
    if not os.path.exists(ann_path) or not ref_audio:
        return ""
    ref_name = os.path.basename(ref_audio)
    try:
        with open(ann_path, encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 4 and ref_name in parts[0]:
                    return parts[3]
    except Exception:
        pass
    return ""


# ── GPT-SoVITS 本地推理 ──────────────────────────────────────────────────────

_model_loaded = {"gpt": None, "sovits": None}


def _ensure_sovits_path():
    """确保 GPT-SoVITS 在 Python path 中。"""
    sovits_dir = get_sovits_dir()
    if not sovits_dir:
        raise RuntimeError("GPT-SoVITS not found")
    for p in [sovits_dir, os.path.join(sovits_dir, "GPT_SoVITS")]:
        if p not in sys.path:
            sys.path.insert(0, p)


def synthesize_local(
    text: str,
    slug: str,
    ref_audio: str,
    ref_text: str = "",
    output_path: str = "output.wav",
    use_finetuned_gpt: bool = False,
    top_k: int = 15,
    top_p: float = 0.8,
    temperature: float = 0.8,
    speed: float = 1.0,
) -> bool:
    """
    本地直接调用 GPT-SoVITS 推理（不需要启动 API 服务）。
    这是实测验证的最可靠方式。
    """
    _ensure_sovits_path()

    gpt_model = find_gpt_model(slug, use_finetuned=use_finetuned_gpt)
    sovits_model = find_sovits_model(slug)

    if not gpt_model:
        print("[x] GPT model not found")
        return False
    if not sovits_model:
        print("[x] SoVITS model not found")
        return False

    print(f"  GPT:    {os.path.basename(gpt_model)} {'(finetuned)' if use_finetuned_gpt else '(pretrained)'}")
    print(f"  SoVITS: {os.path.basename(sovits_model)} (finetuned)")
    print(f"  Ref:    {os.path.basename(ref_audio)}")

    from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav

    # 加载模型（如果和上次不同才重新加载）
    if _model_loaded["gpt"] != gpt_model:
        change_gpt_weights(gpt_model)
        _model_loaded["gpt"] = gpt_model
    if _model_loaded["sovits"] != sovits_model:
        change_sovits_weights(sovits_model)
        _model_loaded["sovits"] = sovits_model

    results = list(get_tts_wav(
        ref_wav_path=ref_audio,
        prompt_text=ref_text,
        prompt_language="中文",
        text=text,
        text_language="中文",
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        speed=speed,
    ))

    if not results:
        print("[x] No audio generated")
        return False

    import soundfile as sf
    import numpy as np

    sr, audio = results[-1]
    duration = len(audio) / sr

    if duration < 0.5 or np.max(np.abs(audio)) < 10:
        print(f"[!] Output too short ({duration:.1f}s) or silent")
        if not use_finetuned_gpt:
            print("    Try: --use-finetuned-gpt (if data is standard Mandarin)")
        return False

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    sf.write(output_path, audio, sr)
    print(f"[ok] {output_path} ({duration:.1f}s)")
    return True


# ── 批量合成 ──────────────────────────────────────────────────────────────────

def synthesize_batch(
    text_file: str, slug: str, outdir: str,
    ref_audio: str, ref_text: str = "",
    use_finetuned_gpt: bool = False,
) -> dict:
    """批量合成：每行一句。"""
    os.makedirs(outdir, exist_ok=True)

    with open(text_file, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    if not lines:
        print("[x] Text file is empty")
        return {"total": 0, "success": 0, "failed": 0}

    print(f"[batch] {len(lines)} sentences")
    stats = {"total": len(lines), "success": 0, "failed": 0}

    for i, text in enumerate(lines, 1):
        out_path = os.path.join(outdir, f"{i:03d}.wav")
        print(f"\n[{i}/{len(lines)}] {text[:40]}{'...' if len(text) > 40 else ''}")
        ok = synthesize_local(
            text, slug, ref_audio, ref_text, out_path,
            use_finetuned_gpt=use_finetuned_gpt,
        )
        stats["success" if ok else "failed"] += 1

    return stats


# ── Check ─────────────────────────────────────────────────────────────────────

def action_check(slug: str):
    """检查合成环境。"""
    print(f"=== {slug} voice synthesis status ===\n")

    sovits_dir = get_sovits_dir()
    print(f"GPT-SoVITS: {'[ok] ' + sovits_dir if sovits_dir else '[x] not found'}")

    sovits_model = find_sovits_model(slug)
    print(f"SoVITS model (finetuned): {'[ok] ' + os.path.basename(sovits_model) if sovits_model else '[x]'}")

    gpt_pretrained = find_gpt_model(slug, use_finetuned=False)
    print(f"GPT model (pretrained): {'[ok] ' + os.path.basename(gpt_pretrained) if gpt_pretrained else '[x]'}")

    gpt_finetuned = find_gpt_model(slug, use_finetuned=True)
    print(f"GPT model (finetuned): {'[ok] ' + os.path.basename(gpt_finetuned) if gpt_finetuned else '[x] none'}")

    ref = find_ref_audio(slug)
    print(f"Reference audio: {'[ok] ' + os.path.basename(ref) if ref else '[x]'}")

    if ref:
        ref_text = find_ref_text(ref, slug)
        if ref_text:
            print(f"  Transcript: {ref_text[:60]}{'...' if len(ref_text) > 60 else ''}")

    print()
    if sovits_model and gpt_pretrained and ref:
        print("[ok] Ready to synthesize")
        print(f"  Usage: python voice_synthesizer.py --slug {slug} --text \"your text here\"")
    else:
        missing = []
        if not sovits_dir:
            missing.append("GPT-SoVITS (run voice_trainer.py --action setup)")
        if not sovits_model:
            missing.append("SoVITS model (run voice_trainer.py --action full)")
        if not ref:
            missing.append("Reference audio (run voice_trainer.py --action prepare)")
        print("[x] Not ready. Missing:")
        for m in missing:
            print(f"  - {m}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Voice synthesizer - type text, hear your loved one's voice",
    )
    parser.add_argument("--slug", required=True, help="Memorial slug")
    parser.add_argument("--action", default="synthesize",
                        choices=["synthesize", "check"],
                        help="Action: synthesize (default) or check")

    parser.add_argument("--text", help="Text to synthesize")
    parser.add_argument("--text-file", help="Batch: one sentence per line")
    parser.add_argument("--output", default="output.wav", help="Output WAV path")
    parser.add_argument("--outdir", default="./audio_out", help="Batch output directory")

    parser.add_argument("--ref-audio", help="Reference audio (3-10s, auto-selected if omitted)")
    parser.add_argument("--ref-text", help="Reference audio transcript (auto-looked-up if omitted)")
    parser.add_argument("--use-finetuned-gpt", action="store_true",
                        help="Use finetuned GPT model instead of pretrained (better for standard Mandarin)")
    parser.add_argument("--speed", type=float, default=1.0, help="Speech speed (default 1.0)")
    parser.add_argument("--top-k", type=int, default=15)
    parser.add_argument("--top-p", type=float, default=0.8)
    parser.add_argument("--temperature", type=float, default=0.8)

    args = parser.parse_args()

    if args.action == "check":
        action_check(args.slug)
        return

    if not args.text and not args.text_file:
        parser.error("--text or --text-file required")

    # 自动查找参考音频和文本
    ref_audio = args.ref_audio or find_ref_audio(args.slug)
    if not ref_audio:
        print("[x] No reference audio found. Run voice_trainer.py --action prepare first.")
        sys.exit(1)

    ref_text = args.ref_text or find_ref_text(ref_audio, args.slug)

    if args.text_file:
        stats = synthesize_batch(
            args.text_file, args.slug, args.outdir,
            ref_audio, ref_text, args.use_finetuned_gpt,
        )
        print(f"\n[summary] {stats['success']}/{stats['total']} succeeded")
    else:
        print(f"[synthesize] \"{args.text}\"")
        ok = synthesize_local(
            args.text, args.slug, ref_audio, ref_text, args.output,
            use_finetuned_gpt=args.use_finetuned_gpt,
            top_k=args.top_k, top_p=args.top_p,
            temperature=args.temperature, speed=args.speed,
        )
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
