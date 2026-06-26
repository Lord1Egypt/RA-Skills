"""
TTS引用上文功能测试 - 验证TTS 2.0的上下文缓存
"""
import os
import sys
import time
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
                elif 'secret key' in line and '：' in line:
                    os.environ['VOLCANO_TTS_SECRET_KEY'] = line.split('：')[1].strip()
        print("[Config] 已从private/TTS.txt加载配置\n")
    except Exception as e:
        print(f"[Config] 加载失败: {e}")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tts_controller import VolcanoTTSController
from src.schema import ScriptVersion, DialogueLine, TokenUsage

print("=" * 70)
print("TTS引用上文功能测试")
print("=" * 70)
print("测试场景: 对话需要依赖前文语境")
print("功能原理: TTS 2.0的additions.context字段传递上文")
print("=" * 70)

# 设计测试场景：对话需要依赖前文语境
lines = [
    DialogueLine(speaker="A", text="你听说过那个消息吗？"),
    DialogueLine(speaker="B", text="什么消息？"),
    DialogueLine(speaker="A", text="就是我们公司要上市的事情。"),  # 承接前文
    DialogueLine(speaker="B", text="真的吗？那太好了！恭喜你啊！"),  # 需要理解前文
    DialogueLine(speaker="A", text="是啊，准备了这么多年，终于有结果了。"),  # 延续话题
]

script = ScriptVersion(
    session_id="test_context_001",
    outline_checksum="test",
    lines=lines,
    word_count=500,
    estimated_duration_sec=120,
    token_usage=TokenUsage(input=100, output=200, total=300)
)

try:
    # 测试启用上下文
    cost_tracker = {}
    controller = VolcanoTTSController(
        enable_context=True,
        cost_tracker=cost_tracker,
    )

    print(f"\n[TTS配置]")
    print(f"  TTS 2.0: {'是' if controller._is_tts_v2 else '否'}")
    print(f"  引用上文: {'启用' if controller.enable_context else '禁用'}")
    print(f"  缓存大小: {controller._max_context_lines}句")

    output_path = Path("./test_outputs/tts_test/context_test.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[上下文缓存验证]")
    print(f"  生成前缓存状态:")
    print(f"    A: {controller._context_cache.get('A', [])}")
    print(f"    B: {controller._context_cache.get('B', [])}")

    print(f"\n[开始生成]")
    result = controller.generate_dual_audio(script, output_path)

    print(f"\n[生成后缓存状态]")
    print(f"  A: {controller._context_cache.get('A', [])}")
    print(f"  B: {controller._context_cache.get('B', [])}")

    print(f"\n[验证结果]")
    # 验证缓存是否正确更新
    # A说了第1、3、5句，缓存应该有最近2句（第3和第5句的前两句中A说的）
    # 实际上A说的是索引0、2、4，最后两句是索引2和4的内容
    # 但由于交替对话，缓存逻辑是按说话人独立计算的

    a_cache = controller._context_cache.get('A', [])
    b_cache = controller._context_cache.get('B', [])

    # A应该缓存了最近说的（但最多_max_context_lines=2句）
    if len(a_cache) > 0:
        print(f"  [OK] A说话人缓存非空: {len(a_cache)}句")
    else:
        print(f"  [WARN] A说话人缓存为空")

    if len(b_cache) > 0:
        print(f"  [OK] B说话人缓存非空: {len(b_cache)}句")
    else:
        print(f"  [WARN] B说话人缓存为空")

    print(f"\n[成本统计]")
    for k, v in cost_tracker.items():
        print(f"  {k}: {v}")

    print(f"\n[生成结果]")
    print(f"  文件: {result}")
    print(f"  大小: {result.stat().st_size} bytes")

    print("\n" + "=" * 70)
    print("引用上文功能测试完成！")
    print("=" * 70)
    print("\n说明:")
    print("- TTS 2.0的引用上文通过additions.context字段实现")
    print("- 每句合成时自动包含前几句作为上下文")
    print("- 帮助模型理解语境，生成更连贯的情感")
    print("=" * 70)

except Exception as e:
    print(f"\n[错误] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
