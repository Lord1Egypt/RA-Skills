#!/usr/bin/env python3
"""
测试脚本

测试龙虾电台Skill的基本功能。
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from providers.qwen3_tts import Qwen3TTSProvider
from providers.tts_base import Emotion
from utils.content_generator import ContentGenerator
from utils.content_generator_v2 import ContentGeneratorV2
from utils.audio_manager import AudioManager
from utils.config_manager import ConfigManager
from utils.platform_adapter import get_current_platform


async def test_tts_model_availability():
    """测试TTS模型可用性"""
    print("🔍 测试Qwen3-TTS模型可用性...")
    
    tts_provider = Qwen3TTSProvider()
    is_available = await tts_provider.check_availability()
    
    if is_available:
        print("✅ Qwen3-TTS模型可用")
        return True
    else:
        print("❌ Qwen3-TTS模型未下载")
        print("   请下载模型:")
        print("   huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-Base")
        return False


async def test_tts_synthesis():
    """测试TTS合成"""
    print("\n🎤 测试TTS合成...")
    
    tts_provider = Qwen3TTSProvider()
    
    # 检查模型是否可用
    is_available = await tts_provider.check_availability()
    if not is_available:
        print("⚠️  模型未下载，跳过TTS合成测试")
        return True  # 返回True，因为这不是错误，只是模型未下载
    
    test_text = "这是一个测试音频，欢迎使用龙虾电台。"
    print(f"   测试文本: {test_text}")
    
    try:
        audio_data = await tts_provider.synthesize(
            text=test_text,
            voice_id="xiaoxiao",
            emotion=Emotion.NEUTRAL,
            speed=1.0,
            pitch=1.0
        )
        
        print(f"✅ 音频生成成功")
        print(f"   格式: {audio_data.format}")
        print(f"   时长: {audio_data.duration:.1f}秒")
        print(f"   大小: {len(audio_data.data)}字节")
        
        return True
    except Exception as e:
        print(f"❌ 音频生成失败: {e}")
        return False


def test_content_generator():
    """测试内容生成器V1"""
    print("\n📝 测试内容生成器V1...")
    
    content_generator = ContentGenerator()
    
    try:
        radio_content = content_generator.generate(
            topics=["人工智能"],
            tags=["科技"],
            duration=2
        )
        
        print(f"✅ 内容生成成功")
        print(f"   标题: {radio_content.title}")
        print(f"   摘要: {radio_content.summary[:50]}...")
        print(f"   内容长度: {len(radio_content.content)}字符")
        
        return True
    except Exception as e:
        print(f"❌ 内容生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_content_generator_v2():
    """测试内容生成器V2"""
    print("\n📝 测试内容生成器V2 (新闻搜索+LLM处理)...")
    
    content_generator = ContentGeneratorV2()
    
    try:
        # 使用平台搜索（或模拟数据）
        radio_content = await content_generator.generate(
            topics=["人工智能"],
            tags=["科技"],
            max_segments=3,
            use_platform_search=True
        )
        
        print(f"✅ 内容生成成功")
        print(f"   主标题: {radio_content.main_title}")
        print(f"   摘要: {radio_content.summary}")
        print(f"   新闻条数: {len(radio_content.segments)}条")
        
        if radio_content.segments:
            print(f"\n   第一条新闻:")
            print(f"   - 标题: {radio_content.segments[0].title}")
            print(f"   - 内容: {radio_content.segments[0].content[:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ 内容生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_audio_manager():
    """测试音频管理器"""
    print("\n💾 测试音频管理器...")
    
    audio_manager = AudioManager()
    
    try:
        test_audio = b"test audio data"
        audio_url = audio_manager.save(
            audio_data=test_audio,
            user_id="test_user",
            format="wav",
            metadata={'test': True}
        )
        
        print(f"✅ 音频保存成功")
        print(f"   URL: {audio_url}")
        
        storage_info = audio_manager.get_storage_info()
        print(f"   文件总数: {storage_info['total_files']}")
        print(f"   总大小: {storage_info['total_size_mb']} MB")
        
        return True
    except Exception as e:
        print(f"❌ 音频管理失败: {e}")
        return False


def test_config_manager():
    """测试配置管理器"""
    print("\n⚙️ 测试配置管理器...")
    
    config_manager = ConfigManager()
    
    try:
        tts_config = config_manager.get_tts_config()
        print(f"✅ TTS配置读取成功")
        print(f"   提供商: {tts_config.provider}")
        print(f"   模型: {tts_config.model}")
        print(f"   音色: {tts_config.voice}")
        
        user_prefs = config_manager.get_user_preferences()
        print(f"✅ 用户偏好读取成功")
        print(f"   语言: {user_prefs.language}")
        
        return True
    except Exception as e:
        print(f"❌ 配置管理失败: {e}")
        return False


def test_platform_detection():
    """测试平台检测"""
    print("\n🔍 测试平台检测...")
    
    try:
        platform = get_current_platform()
        print(f"✅ 平台检测成功")
        print(f"   当前平台: {platform}")
        
        return True
    except Exception as e:
        print(f"❌ 平台检测失败: {e}")
        return False


async def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 龙虾电台Skill测试")
    print("=" * 60)
    
    results = []
    
    results.append(("TTS模型可用性", await test_tts_model_availability()))
    results.append(("TTS合成", await test_tts_synthesis()))
    results.append(("内容生成器V1", test_content_generator()))
    results.append(("内容生成器V2", await test_content_generator_v2()))
    results.append(("音频管理器", test_audio_manager()))
    results.append(("配置管理器", test_config_manager()))
    results.append(("平台检测", test_platform_detection()))
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
