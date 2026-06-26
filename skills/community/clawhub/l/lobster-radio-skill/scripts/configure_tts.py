#!/usr/bin/env python3
"""
TTS配置脚本

配置TTS音色和参数。
"""

import sys
import asyncio
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.qwen3_tts import Qwen3TTSProvider
from utils.config_manager import ConfigManager, TTSConfig


async def configure_tts(
    voice: str = None,
    emotion: str = None,
    speed: float = None,
    pitch: float = None,
    model: str = None
):
    """
    配置TTS
    
    Args:
        voice: 音色ID
        emotion: 情感类型
        speed: 语速
        pitch: 音调
        model: 模型名称
    """
    config_manager = ConfigManager()
    current_config = config_manager.get_tts_config()
    
    print("🎙️ 当前TTS配置:")
    print(f"   提供商: {current_config.provider}")
    print(f"   模型: {current_config.model}")
    print(f"   音色: {current_config.voice}")
    print(f"   情感: {current_config.emotion}")
    print(f"   语速: {current_config.speed}")
    print(f"   音调: {current_config.pitch}")
    
    if any([voice, emotion, speed, pitch, model]):
        if voice:
            current_config.voice = voice
        if emotion:
            current_config.emotion = emotion
        if speed:
            current_config.speed = speed
        if pitch:
            current_config.pitch = pitch
        if model:
            current_config.model = model
        
        config_manager.save_tts_config(current_config)
        
        print("\n✅ TTS配置已更新:")
        print(f"   提供商: {current_config.provider}")
        print(f"   模型: {current_config.model}")
        print(f"   音色: {current_config.voice}")
        print(f"   情感: {current_config.emotion}")
        print(f"   语速: {current_config.speed}")
        print(f"   音调: {current_config.pitch}")
    else:
        print("\n💡 可用音色:")
        tts_provider = Qwen3TTSProvider(model_name=current_config.model)
        voices = await tts_provider.get_voices()
        
        for i, v in enumerate(voices, 1):
            print(f"   {i}. {v.name} ({v.gender.value}) - {v.description}")
        
        print("\n💡 可用情感:")
        from providers.tts_base import Emotion
        for i, e in enumerate(Emotion, 1):
            print(f"   {i}. {e.value}")
        
        print("\n💡 使用示例:")
        print("   python configure_tts.py --voice xiaoxiao --emotion neutral --speed 1.0")


async def test_tts():
    """测试TTS"""
    print("\n🎤 测试TTS...")
    
    config_manager = ConfigManager()
    tts_config = config_manager.get_tts_config()
    
    tts_provider = Qwen3TTSProvider(model_name=tts_config.model)
    
    is_available = await tts_provider.check_availability()
    if not is_available:
        print("❌ Qwen3-TTS模型未下载")
        print("   正在下载模型，请稍候...")
        print("   这可能需要几分钟时间，取决于您的网络速度")
        
        try:
            await tts_provider.download_model()
            print("✅ 模型下载完成")
        except Exception as e:
            print(f"❌ 模型下载失败: {e}")
            print("\n请手动下载模型：")
            print("   方法1: 从HuggingFace下载")
            print("   pip install huggingface_hub")
            print("   huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base")
            print("\n   方法2: 从ModelScope下载（国内用户推荐）")
            print("   pip install modelscope")
            print("   python -c \"from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-Base', cache_dir='./models')\"")
            print("\n   详细说明请查看: QWEN3TTS_GUIDE.md")
            return False
    
    print("✅ Qwen3-TTS模型可用")
    
    test_text = "这是一个测试音频，欢迎使用龙虾电台。"
    print(f"\n📝 测试文本: {test_text}")
    
    try:
        audio_data = await tts_provider.synthesize(
            text=test_text,
            voice_id=tts_config.voice,
            emotion=tts_config.emotion,
            speed=tts_config.speed,
            pitch=tts_config.pitch
        )
        
        print(f"✅ 音频生成成功")
        print(f"   格式: {audio_data.format}")
        print(f"   时长: {audio_data.duration:.1f}秒")
        print(f"   大小: {len(audio_data.data)}字节")
        
        return True
    except Exception as e:
        print(f"❌ 音频生成失败: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='配置TTS')
    parser.add_argument('--voice', type=str, help='音色ID')
    parser.add_argument('--emotion', type=str, help='情感类型')
    parser.add_argument('--speed', type=float, help='语速（0.5-2.0）')
    parser.add_argument('--pitch', type=float, help='音调（0.5-2.0）')
    parser.add_argument('--model', type=str, help='模型名称')
    parser.add_argument('--test', action='store_true', help='测试TTS')
    
    args = parser.parse_args()
    
    if args.test:
        asyncio.run(test_tts())
    else:
        asyncio.run(configure_tts(
            voice=args.voice,
            emotion=args.emotion,
            speed=args.speed,
            pitch=args.pitch,
            model=args.model
        ))


if __name__ == "__main__":
    main()
