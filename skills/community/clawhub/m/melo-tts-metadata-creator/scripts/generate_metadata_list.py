#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: melo-tts-metadata-creator
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: MeloTTS metadata.list 生成器（OpenClaw Skill 专用）
完全符合官方最新标准：路径|speaker|lang|text（无空格）。
支持 wav 和 txt 在不同目录 + 多级子目录完全符合 MeloTTS 官方最新标准。
"""

import argparse
from pathlib import Path
import gc
import sys
import env_manager
import ensure_package
from config import MODEL_DIR, SKILL_ROOT, VENV_DIR
from logger_manager import LoggerManager
ensure_package.pip("openai-whisper")
ensure_package.pip("torch")
ensure_package.pip("torchaudio")
import whisper
import torch

logger = LoggerManager.setup_logger(logger_name="melo-tts-metadata-creator")

def main():

    global args

    wav_dir = Path(args.wav_dir).resolve()
    txt_dir = Path(args.txt_dir).resolve()

    if not wav_dir.exists():
        logger.error(f"❌ 错误：wav_dir 不存在 {wav_dir}")
        sys.exit(1)
    if not txt_dir.exists():
        logger.error(f"❌ 错误：txt_dir 不存在 {txt_dir}")
        sys.exit(1)

    # 创建本地 models 目录
    local_models_dir = MODEL_DIR
    local_models_dir.mkdir(parents=True, exist_ok=True)

    # 查找所有 .wav
    pattern = "**/*.wav" if args.recursive else "*.wav"
    wav_files = sorted(wav_dir.glob(pattern))

    if not wav_files:
        logger.error("❌ 错误：未找到任何 .wav 文件")
        sys.exit(1)

    logger.info(f"🔍 找到 {len(wav_files)} 个 .wav 文件")
    if args.speaker:
        logger.info(f"🎯 单音色模式 - 统一 speaker: {args.speaker}")
    else:
        logger.info("🎯 多音色模式 - 将自动提取每个子目录名称作为 speaker")

    # Whisper 模型加载（失败时优雅降级）
    model = None
    if args.use_whisper:
        try:
            logger.info(f"🚀 加载 Whisper base 模型（下载到: {local_models_dir}）...")
            model = whisper.load_model("base", download_root=str(local_models_dir))
            logger.info("✅ Whisper 模型加载成功")
        except Exception as e:
            logger.error(f"⚠️ Whisper 模型加载失败: {e}")
            logger.error("⚠️ 将跳过没有 .txt 的音频，继续处理已有转录的文件...")
            model = None

    lines = []
    skipped = 0
    transcribed = 0

    for wav_path in wav_files:
        rel_path = wav_path.relative_to(wav_dir)
        
        # ==================== 核心逻辑：speaker 处理 ====================
        if args.speaker:
            speaker = args.speaker.strip()
        else:
            # 未传入 speaker 时，提取第一级子目录名
            speaker = rel_path.parts[0] if len(rel_path.parts) > 1 else "default_speaker"
        # ============================================================

        txt_path = (txt_dir / rel_path).with_suffix(".txt")
        abs_wav = str(wav_path.resolve())

        if txt_path.exists():
            text = txt_path.read_text(encoding="utf-8").strip()
            source = "from .txt"
        elif args.use_whisper and model is not None:
            logger.info(f"🎤 Whisper 转录 [{speaker}]: {rel_path}")
            try:
                result = model.transcribe(str(wav_path), language=args.lang.lower())
                text = result["text"].strip()
                txt_path.parent.mkdir(parents=True, exist_ok=True)
                txt_path.write_text(text, encoding="utf-8")
                source = "Whisper"
                transcribed += 1
            except Exception as e:
                logger.error(f"⚠️ 转录失败 {rel_path}: {e}，跳过")
                skipped += 1
                continue
        else:
            logger.info(f"⚠️ 跳过（无 txt 且 Whisper 不可用）: {rel_path}")
            skipped += 1
            continue

        line = f"{abs_wav}|{speaker}|{args.lang}|{text}"
        lines.append(line)
        logger.info(f"✅ {rel_path} → speaker: {speaker} | {source}")

    # 显存释放
    if model is not None:
        print("🔄 正在释放 Whisper 模型和显存...", file=sys.stderr)
        del model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        print("✅ 显存已释放", file=sys.stderr)

    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    speaker_count = len({line.split('|')[1] for line in lines})
    logger.info(f"\n🎉 metadata.list 生成完成！共 {len(lines)} 行，{speaker_count} 个 speaker")
    logger.info(f"   - Whisper 转录数量: {transcribed}")
    logger.info(f"   - 跳过数量: {skipped}")
    logger.info(f"📁 文件保存至：{output_path}")


if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()

    parser = argparse.ArgumentParser(description="生成 MeloTTS metadata.list（支持 wav 和 txt 分离目录）")
    parser.add_argument("--wav_dir", type=str, required=True, help="wav 文件根目录（必须）")
    parser.add_argument("--txt_dir", type=str, required=True, help="txt 转录文件根目录（必须，和 wav 目录结构一致）")
    parser.add_argument("--speaker", type=str, default=None, help="说话人名字。如果不传，则自动使用第一级子目录名作为 speaker（多音色模式）")
    parser.add_argument("--lang", type=str, default="ZH", choices=["ZH", "EN"], help="语言代码")
    parser.add_argument("--output", type=str, default="metadata.list", help="输出 metadata.list 路径")
    parser.add_argument("--recursive", action="store_true", help="递归搜索（默认开启多级目录）")
    parser.add_argument("--use_whisper", action="store_true", help="没有找到 txt 时自动用 Whisper 转录")
    args = parser.parse_args()


    main()