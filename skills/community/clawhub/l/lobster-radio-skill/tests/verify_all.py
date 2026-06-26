#!/usr/bin/env python3
"""
完整验证脚本

验证龙虾电台Skill的所有组件是否正确安装和配置。
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def check_dependencies():
    """检查依赖包"""
    print("📦 检查依赖包...")
    
    required_packages = {
        'torch': 'PyTorch',
        'transformers': 'Transformers',
        'accelerate': 'Accelerate',
        'huggingface_hub': 'HuggingFace Hub',
        'aiohttp': 'aiohttp',
        'pydub': 'pydub'
    }
    
    missing = []
    installed = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            installed.append(name)
            print(f"   ✅ {name}")
        except ImportError:
            missing.append(name)
            print(f"   ❌ {name} - 未安装")
    
    if missing:
        print(f"\n❌ 缺少依赖包: {', '.join(missing)}")
        print("   请运行: pip install -r requirements.txt")
        return False
    
    print("\n✅ 所有依赖包已安装")
    return True


def check_model_files():
    """检查模型文件"""
    print("\n🔍 检查Qwen3-TTS模型文件...")
    
    # 检查 CustomVoice 模型路径（优先）
    customvoice_paths = [
        Path("./models/Qwen3-TTS-12Hz-0.6B-CustomVoice"),
        Path("./models/Qwen3-TTS-12Hz-1.7B-CustomVoice"),
        Path.home() / ".cache" / "huggingface" / "hub" / "models--Qwen--Qwen3-TTS-12Hz-0.6B-CustomVoice",
    ]
    
    # CustomVoice 模型文件结构
    customvoice_files = ['config.json', 'model.safetensors', 'vocab.json']
    
    for model_path in customvoice_paths:
        if model_path.exists():
            print(f"   ✅ 找到CustomVoice模型: {model_path}")
            
            missing_files = []
            for file in customvoice_files:
                if not (model_path / file).exists():
                    missing_files.append(file)
            
            if missing_files:
                print(f"   ⚠️  缺少文件: {', '.join(missing_files)}")
            else:
                print(f"   ✅ CustomVoice模型文件完整")
                return True
    
    print("\n❌ 未找到Qwen3-TTS CustomVoice模型")
    print("\n请下载CustomVoice模型：")
    print("   方法1（HuggingFace）:")
    print("   huggingface-cli download Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice --local-dir ./models/Qwen3-TTS-12Hz-0.6B-CustomVoice")
    print("\n   方法2（ModelScope，国内推荐）:")
    print("   python -c \"from modelscope import snapshot_download; snapshot_download('qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice', cache_dir='./models')\"")
    return False


async def check_tts_provider():
    """检查TTS Provider"""
    print("\n🎤 检查TTS Provider...")
    
    try:
        from providers.qwen3_tts import Qwen3TTSProvider
        
        provider = Qwen3TTSProvider()
        is_available = await provider.check_availability()
        
        if is_available:
            print("   ✅ Qwen3-TTS Provider可用")
            
            voices = await provider.get_voices()
            print(f"   ✅ 可用音色: {len(voices)}个")
            
            return True
        else:
            print("   ❌ Qwen3-TTS Provider不可用")
            return False
            
    except Exception as e:
        print(f"   ❌ TTS Provider错误: {e}")
        return False


def check_content_generator():
    """检查内容生成器"""
    print("\n📝 检查内容生成器...")
    
    try:
        from utils.content_generator import ContentGenerator
        
        generator = ContentGenerator()
        
        radio_content = generator.generate(
            topics=["测试"],
            tags=["测试"],
            duration=1
        )
        
        print(f"   ✅ 内容生成器正常")
        print(f"   ✅ 生成标题: {radio_content.title}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 内容生成器错误: {e}")
        return False


def check_audio_manager():
    """检查音频管理器"""
    print("\n💾 检查音频管理器...")
    
    try:
        from utils.audio_manager import AudioManager
        
        manager = AudioManager()
        
        test_audio = b"test audio data"
        audio_url = manager.save(
            audio_data=test_audio,
            user_id="test",
            format="wav",
            metadata={'test': True}
        )
        
        print(f"   ✅ 音频管理器正常")
        print(f"   ✅ 测试文件: {audio_url}")
        
        storage_info = manager.get_storage_info()
        print(f"   ✅ 存储目录: {storage_info['storage_dir']}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 音频管理器错误: {e}")
        return False


def check_config_manager():
    """检查配置管理器"""
    print("\n⚙️  检查配置管理器...")
    
    try:
        from utils.config_manager import ConfigManager
        
        manager = ConfigManager()
        
        tts_config = manager.get_tts_config()
        print(f"   ✅ TTS配置: {tts_config.model}")
        
        user_prefs = manager.get_user_preferences()
        print(f"   ✅ 用户偏好: {user_prefs.language}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 配置管理器错误: {e}")
        return False


async def test_synthesis():
    """测试语音合成"""
    print("\n🧪 测试语音合成...")
    
    try:
        from providers.qwen3_tts import Qwen3TTSProvider
        
        provider = Qwen3TTSProvider()
        
        if not await provider.check_availability():
            print("   ⚠️  模型未下载，跳过合成测试")
            return True
        
        test_text = "这是一个测试。"
        
        print(f"   测试文本: {test_text}")
        print("   正在生成音频...")
        
        audio_data = await provider.synthesize(
            text=test_text,
            voice_id="xiaoxiao",
            emotion="neutral",
            speed=1.0,
            pitch=1.0
        )
        
        print(f"   ✅ 音频生成成功")
        print(f"   ✅ 时长: {audio_data.duration:.1f}秒")
        print(f"   ✅ 大小: {len(audio_data.data)}字节")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 语音合成错误: {e}")
        return False


async def run_all_checks():
    """运行所有检查"""
    print("=" * 60)
    print("🧪 龙虾电台Skill完整验证")
    print("=" * 60)
    
    results = []
    
    results.append(("依赖包", check_dependencies()))
    results.append(("模型文件", check_model_files()))
    results.append(("TTS Provider", await check_tts_provider()))
    results.append(("内容生成器", check_content_generator()))
    results.append(("音频管理器", check_audio_manager()))
    results.append(("配置管理器", check_config_manager()))
    results.append(("语音合成测试", await test_synthesis()))
    
    print("\n" + "=" * 60)
    print("📊 验证结果汇总")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有检查通过！Skill已准备就绪。")
        print("\n使用方法:")
        print("   python scripts/generate_radio.py --topics '人工智能' --tags '科技'")
    else:
        print("\n⚠️  部分检查未通过，请根据上述提示解决问题。")
    
    return all(result for _, result in results)


if __name__ == "__main__":
    success = asyncio.run(run_all_checks())
    sys.exit(0 if success else 1)
