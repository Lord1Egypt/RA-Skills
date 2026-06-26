#!/usr/bin/env python3
"""
WhisperX 转写 + 说话人分离（Speaker Diarization）
用法: python transcribe_with_diarization.py <input.mp3> [--model base] [--language zh] [--hf_token TOKEN]

依赖: pip install whisperx
首次使用需获取 HuggingFace Token，详见 SKILL.md
"""

import sys
import os
import argparse
import whisperx


def main():
    parser = argparse.ArgumentParser(description="WhisperX 转写 + 说话人分离")
    parser.add_argument("audio_file", help="输入音频文件路径 (.mp3 / .wav)")
    parser.add_argument("--model", default="base", help="Whisper 模型 (tiny/base/small/medium/large, 默认 base)")
    parser.add_argument("--language", default="zh", help="语言代码 (默认 zh)")
    parser.add_argument("--hf_token", default=None, help="HuggingFace Token（也可通过 HF_TOKEN 环境变量设置）")
    args = parser.parse_args()

    audio_file = args.audio_file
    if not os.path.isfile(audio_file):
        print(f"错误：文件不存在 - {audio_file}")
        sys.exit(1)

    # 获取 HF Token
    hf_token = args.hf_token or os.environ.get("HF_TOKEN", None)
    if not hf_token:
        print("错误：未设置 HuggingFace Token。请通过 --hf_token 参数或 HF_TOKEN 环境变量提供。")
        print("首次使用请参考 SKILL.md 中的指引获取 Token。")
        sys.exit(1)

    print(f"[INFO] 加载模型: {args.model}, 语言: {args.language}")

    # 1. 转写
    print("[INFO] Step 1/4: 语音转写...")
    model = whisperx.load_model(args.model, device="cpu", compute_type="int8")
    result = model.transcribe(audio_file, language=args.language)

    # 2. 对齐（词级时间戳）
    print("[INFO] Step 2/4: 词级对齐...")
    model_a, metadata = whisperx.load_align_model(language_code=args.language, device="cpu")
    result = whisperx.align(result["segments"], model_a, metadata, audio_file, device="cpu")

    # 3. 说话人分离
    print("[INFO] Step 3/4: 说话人分离 (Diarization)...")
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device="cpu")
    diarize_segments = diarize_model(audio_file)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    # 4. 输出带说话人标签的文本
    print("[INFO] Step 4/4: 输出结果")
    print("=" * 60)
    current_speaker = None
    for seg in result["segments"]:
        speaker = seg.get("speaker", "UNKNOWN")
        text = seg["text"].strip()
        if not text:
            continue
        if speaker != current_speaker:
            print(f"\n【{speaker}】", end=" ")
            current_speaker = speaker
        else:
            print(end=" ")
        print(text, end="")
    print()
    print("=" * 60)
    print("[INFO] 转写完成")


if __name__ == "__main__":
    raise SystemExit(main())
