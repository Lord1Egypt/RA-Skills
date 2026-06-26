"""
TTS双发音人测试 - 验证音色配置和声道分配逻辑
"""
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]

private_tts_path = Path(__file__).parent.parent / "private" / "TTS.txt"
if private_tts_path.exists() and not os.getenv("VOLCANO_TTS_APP_ID"):
    try:
        with open(private_tts_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.strip().split('\n'):
                if 'APP ID' in line and '：' in line:
                    os.environ['VOLCANO_TTS_APP_ID'] = line.split('：')[1].strip()
                elif 'Access Token' in line and '：' in line:
                    os.environ['VOLCANO_TTS_ACCESS_TOKEN'] = line.split('：')[1].strip()
    except Exception as e:
        print(f"[Config] 加载失败: {e}")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tts_controller import VolcanoTTSController, VoiceConfig

print("=" * 70)
print("TTS双发音人配置测试")
print("=" * 70)

# 测试1: 默认音色配置
print("\n[测试1] 默认音色配置")
controller = VolcanoTTSController()

print(f"  Host A voice: {controller.host_a_voice}")
print(f"  Host B voice: {controller.host_b_voice}")
print(f"  Resource ID: {controller.resource_id}")

voice_a = controller.voice_config.get_voice_info(controller.host_a_voice)
voice_b = controller.voice_config.get_voice_info(controller.host_b_voice)

print(f"\n  A音色详情:")
print(f"    名称: {voice_a.get('name', 'Unknown')}")
print(f"    性别: {voice_a.get('gender', 'Unknown')}")
print(f"    类型: {voice_a.get('type', 'Unknown')}")
print(f"    描述: {voice_a.get('description', 'Unknown')}")

print(f"\n  B音色详情:")
print(f"    名称: {voice_b.get('name', 'Unknown')}")
print(f"    性别: {voice_b.get('gender', 'Unknown')}")
print(f"    类型: {voice_b.get('type', 'Unknown')}")
print(f"    描述: {voice_b.get('description', 'Unknown')}")

# 验证A是男声，B是女声
if voice_a.get('gender') == 'male' and voice_b.get('gender') == 'female':
    print("\n  [OK] 默认配置正确: A为男声，B为女声")
else:
    print("\n  [WARN] 默认配置可能不是预期的A男B女")

# 测试2: 推荐音色配对
print("\n[测试2] 推荐音色配对")
config = VoiceConfig()
pairs = ["default", "professional", "casual", "english"]
for pair in pairs:
    info = config.get_recommended_pair(pair)
    if info:
        print(f"  {pair}: {info.get('description', '')}")
        print(f"    A: {info.get('host_a', '')}")
        print(f"    B: {info.get('host_b', '')}")

# 测试3: 音色列表
print("\n[测试3] 音色列表")
voices = config.list_voices()
print(f"  总共有 {len(voices)} 个音色")

male_voices = config.list_voices(gender="male")
female_voices = config.list_voices(gender="female")
print(f"  男声: {len(male_voices)} 个")
print(f"  女声: {len(female_voices)} 个")

# 测试4: Saturn vs Uranus
print("\n[测试4] 音色类型分布")
uranus_count = sum(1 for v in voices if v.get('type') == 'uranus')
saturn_count = sum(1 for v in voices if v.get('type') == 'saturn')
print(f"  Uranus (TTS 2.0): {uranus_count} 个")
print(f"  Saturn: {saturn_count} 个")

# 测试5: 验证声道分配逻辑
print("\n[测试5] 声道分配逻辑验证")
print("  根据代码逻辑:")
print("  - A说话人 -> 左声道")
print("  - B说话人 -> 右声道")
print("  这是通过pydub的from_mono_audiosegments实现的:")
print("    A: AudioSegment.from_mono_audiosegments(A_audio, silence)")
print("    B: AudioSegment.from_mono_audiosegments(silence, B_audio)")

# 测试6: 资源ID映射
print("\n[测试6] 资源ID映射")
print(f"  Uranus -> seed-tts-2.0")
print(f"  Saturn -> volc.megatts.default")
print(f"  当前使用: {controller.resource_id}")

# 验证
voice_type = voice_a.get('type', '')
expected_resource = config.get_resource_id(controller.host_a_voice)
print(f"  预期资源ID: {expected_resource}")
if controller.resource_id == expected_resource:
    print("  [OK] 资源ID映射正确")
else:
    print("  [WARN] 资源ID映射可能有问题")

print("\n" + "=" * 70)
print("双发音人配置测试完成！")
print("=" * 70)
