#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""语音转文字工具，支持本地 Whisper 模型（base / small / large-v3）。"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict

# 设置 UTF-8 编码输出（Windows 兼容）
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

CONFIG_PATH = Path.home() / ".workbuddy" / "meeting-notes-config.json"

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "zh": "中文",
    "en": "英语",
    "ja": "日语",
    "ko": "韩语",
}

WHISPER_MODELS = {
    "tiny": {
        "name": "Whisper tiny",
        "description": "最小模型，速度最快",
        "size": "~39MB",
        "accuracy": "约 80%",
        "speed": "最快（<1分钟/10分钟音频）",
        "use_case": "快速测试、简单对话"
    },
    "base": {
        "name": "Whisper base",
        "description": "基础模型，平衡速度与准确率",
        "size": "~140MB",
        "accuracy": "约 85%",
        "speed": "快（<2分钟/10分钟音频）",
        "use_case": "日常使用、快速预览"
    },
    "small": {
        "name": "Whisper small",
        "description": "小型模型，高准确率",
        "size": "~460MB",
        "accuracy": "约 90%",
        "speed": "中等（~5分钟/10分钟音频）",
        "use_case": "推荐日常使用，准确率足够"
    },
    "medium": {
        "name": "Whisper medium",
        "description": "中型模型，高准确率",
        "size": "~1.5GB",
        "accuracy": "约 92%",
        "speed": "慢（~8-10分钟/10分钟音频）",
        "use_case": "专业场景，高准确率要求"
    },
    "large-v3": {
        "name": "Whisper large-v3",
        "description": "最新大型模型，最高准确率",
        "size": "~3GB",
        "accuracy": "约 95%+",
        "speed": "慢（~15-30分钟/10分钟音频，GPU 可加速）",
        "use_case": "专业会议、长音频、最高准确率要求"
    }
}


def load_config() -> Dict:
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "whisper": {
            "default_model": "small",
            "device": "auto"  # auto, cpu, cuda
        }
    }


def save_config(config: Dict):
    """保存配置"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def check_dependencies():
    """检查依赖项"""
    try:
        import whisper
        print("✅ Whisper 已安装")
        return True
    except ImportError:
        print("❌ Whisper 未安装，请运行：pip install openai-whisper")
        return False


def check_gpu():
    """检查 GPU 是否可用"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ 检测到 GPU：{torch.cuda.get_device_name(0)}")
            print(f"   显存：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("⚠️  未检测到 GPU（将使用 CPU，速度较慢）")
            print("   推荐配置：高性能显卡（如 RTX 3060+）可加速 10-50 倍")
            return False
    except ImportError:
        print("⚠️  未安装 PyTorch 或 CUDA 不可用（将使用 CPU）")
        return False


def estimate_time(audio_path: Path, model_name: str, has_gpu: bool) -> float:
    """预估转写时间（分钟）"""
    # 获取音频时长
    try:
        import wave
        with wave.open(str(audio_path), 'rb') as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
    except:
        # 如果无法获取精确时长，使用文件大小估算
        # 假设 1MB ≈ 1 分钟音频
        file_size = audio_path.stat().st_size / 1024 / 1024
        duration = file_size * 60  # 秒

    # 根据模型和设备估算时间
    # 基准：small 模型 + CPU，10 分钟音频需要约 5 分钟转写
    if has_gpu:
        # GPU 加速 10-50 倍
        speed_factor = {
            "tiny": 50,
            "base": 40,
            "small": 30,
            "medium": 20,
            "large-v3": 15
        }.get(model_name, 20)
    else:
        # CPU 速度
        speed_factor = {
            "tiny": 3,
            "base": 2.5,
            "small": 2,
            "medium": 1.5,
            "large-v3": 0.5
        }.get(model_name, 2)

    estimated_minutes = duration / 60 / speed_factor
    return estimated_minutes


def transcribe_with_whisper(audio_path: Path, model_name: str, language: str = "zh", output_path: Path = None) -> str:
    """使用 Whisper 进行转写"""
    import whisper
    import zhconv  # 繁简转换

    # large-v3 模型下载提示
    if model_name == "large-v3":
        print(f"\n⚠️  您选择了 large-v3 模型（约 3GB）")
        print(f"   首次使用时将自动下载模型文件")
        print(f"   下载地址：https://openaipublic.azureedge.net/main/whisper/large-v3.pt")
        print(f"   预计下载时间：5-15 分钟（取决于网络速度）")
        confirm = input(f"\n是否继续下载并使用 large-v3 模型？(y/n): ").strip().lower()
        if confirm not in ["y", "yes", "是"]:
            print("❌ 已取消，建议使用 small 模型")
            print("   小模型命令：python scripts/transcribe_audio.py <音频文件> --model small")
            sys.exit(0)

    print(f"\n📥 正在加载 {model_name} 模型...")
    model = whisper.load_model(model_name)

    print(f"🎙️  正在转写音频...")
    result = model.transcribe(
        str(audio_path),
        language=language,
        task="transcribe",
        fp16=False  # 使用 FP32 确保兼容性
    )

    # 获取转写文本
    text = result["text"]

    # 繁体转简体
    if language == "zh":
        text = zhconv.convert(text, "zh-cn")

    # 保存到文件
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ 转写文本已保存：{output_path}")

    return text


def main():
    parser = argparse.ArgumentParser(description="语音转文字工具（本地 Whisper）")
    parser.add_argument("audio", type=str, help="音频文件路径")
    parser.add_argument("--model", type=str, choices=list(WHISPER_MODELS.keys()), 
                       default="small", help="Whisper 模型（默认：small）")
    parser.add_argument("--language", type=str, default="zh", 
                       help="语言代码（默认：zh，支持：zh/en/ja/ko）")
    parser.add_argument("--output", type=str, help="输出文本文件路径")
    parser.add_argument("--list-models", action="store_true", help="列出可用模型")

    args = parser.parse_args()

    # 列出模型
    if args.list_models:
        print("\n📊 可用 Whisper 模型：\n")
        print(f"{'模型':<15} {'大小':<12} {'准确率':<12} {'速度':<30} {'使用场景'}")
        print("-" * 90)
        for model_id, model_info in WHISPER_MODELS.items():
            print(f"{model_id:<15} {model_info['size']:<12} {model_info['accuracy']:<12} {model_info['speed']:<30} {model_info['use_case']}")
        print("\n💡 推荐：日常使用 small，专业会议使用 large-v3")
        return

    # 检查依赖
    if not check_dependencies():
        sys.exit(1)

    # 检查音频文件
    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"❌ 音频文件不存在：{audio_path}")
        sys.exit(1)

    # 显示文件信息
    file_size = audio_path.stat().st_size / 1024 / 1024
    print(f"\n📁 文件信息：")
    print(f"   文件名：{audio_path.name}")
    print(f"   文件大小：{file_size:.2f} MB")
    print(f"   音频格式：{audio_path.suffix.upper()}")

    # 检查 GPU
    has_gpu = check_gpu()

    # 显示模型信息
    model_info = WHISPER_MODELS[args.model]
    print(f"\n🎙️  选择模型：{model_info['name']}")
    print(f"   描述：{model_info['description']}")
    print(f"   准确率：{model_info['accuracy']}")
    print(f"   模型大小：{model_info['size']}")

    # 预估时间
    estimated_minutes = estimate_time(audio_path, args.model, has_gpu)
    print(f"\n⏱️  预估转写时间：约 {estimated_minutes:.1f} 分钟")

    # 确认
    print(f"\n⚠️  转写过程中请勿关闭程序...")
    confirm = input(f"\n开始转写？(y/n): ").strip().lower()
    if confirm not in ["y", "yes", "是"]:
        print("❌ 已取消")
        sys.exit(0)

    # 执行转写
    output_path = Path(args.output) if args.output else None
    try:
        text = transcribe_with_whisper(
            audio_path, 
            args.model, 
            args.language, 
            output_path
        )
        print(f"\n✅ 转写完成！")
        print(f"   转写字符数：{len(text)}")
        if output_path:
            print(f"   输出文件：{output_path}")
    except Exception as e:
        print(f"\n❌ 转写失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
