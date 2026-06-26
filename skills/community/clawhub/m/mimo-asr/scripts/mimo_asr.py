"""
MiMo-V2.5-ASR 命令行语音识别 / Command-line Speech Recognition (中文/English)

基于小米 MiMo-V2.5-ASR 模型的离线语音转文字脚本。
Offline speech-to-text using Xiaomi MiMo-V2.5-ASR.

用法 / Usage:
  python scripts/mimo_asr.py audio.wav              # 自动检测语言 / auto language
  python scripts/mimo_asr.py audio.wav --language zh  # 指定中文 / Chinese
  python scripts/mimo_asr.py audio.wav --language en  # 指定英文 / English
  python scripts/mimo_asr.py audio.wav --output result.txt  # 输出到文件 / to file
"""

import argparse
import sys
import os

# Windows GBK 兼容
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def main():
    parser = argparse.ArgumentParser(
        description="MiMo-V2.5-ASR 语音识别 / Speech Recognition"
    )
    parser.add_argument("audio", help="音频文件路径 / Audio file path (wav, mp3, etc.)")
    parser.add_argument("--language", choices=["auto", "zh", "en"], default="auto",
                        help="语言：auto=自动检测 / auto detect, zh=中文/Chinese, en=英文/English")
    parser.add_argument("--output", help="输出文本文件路径 / Output text file (optional)")
    parser.add_argument("--model-dir", default="./models/MiMo-V2.5-ASR",
                        help="ASR 模型目录 / ASR model directory")
    parser.add_argument("--tokenizer-dir", default="./models/MiMo-Audio-Tokenizer",
                        help="音频分词器目录 / Audio tokenizer directory")
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu",
                        help="运行设备 / Device: cpu 或 / or cuda")

    args = parser.parse_args()

    # 检查音频文件是否存在
    if not os.path.exists(args.audio):
        print(f"错误 / Error: 音频文件不存在 / Audio file not found: {args.audio}",
              file=sys.stderr)
        sys.exit(1)

    # 构建 audio_tag
    lang_map = {"zh": "<chinese>", "en": "<english>", "auto": None}
    audio_tag = lang_map[args.language]

    print(f"加载模型 / Loading model...", flush=True)
    try:
        from src.mimo_audio.mimo_audio import MimoAudio
        model = MimoAudio(
            model_path=args.model_dir,
            tokenizer_path=args.tokenizer_dir,
        )
    except ImportError:
        print("❌ 请安装 mimo-audio 包 / Install: pip install mimo-audio", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 模型加载失败 / Model load failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"转录中 / Transcribing... ({args.audio})", flush=True)
    try:
        text = model.asr_sft(args.audio, audio_tag=audio_tag) if audio_tag else model.asr_sft(args.audio)
    except Exception as e:
        print(f"❌ 转录失败 / Transcription failed: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"✅ 已保存到 / Saved to: {args.output}", flush=True)
    else:
        print(f"\n📝 {text}", flush=True)


if __name__ == "__main__":
    main()
