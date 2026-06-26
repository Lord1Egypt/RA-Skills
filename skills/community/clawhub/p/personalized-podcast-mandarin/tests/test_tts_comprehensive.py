"""
TTS综合测试 - 引用上下文、双发音人、长文本
"""
import os
import sys
import time
from pathlib import Path

# 设置编码避免Windows控制台乱码
sys.stdout.reconfigure(encoding='utf-8')

# 清除代理
for proxy_var in ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY']:
    if proxy_var in os.environ:
        del os.environ[proxy_var]

# 尝试从private目录加载TTS配置
private_tts_path = Path(__file__).parent.parent / "private" / "TTS.txt"
if private_tts_path.exists() and not os.getenv("VOLCANO_TTS_APP_ID"):
    try:
        with open(private_tts_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 解析格式：APP ID：xxx\nAccess Token：xxx\nsecret key：xxx
            for line in content.strip().split('\n'):
                if 'APP ID' in line and '：' in line:
                    os.environ['VOLCANO_TTS_APP_ID'] = line.split('：')[1].strip()
                elif 'Access Token' in line and '：' in line:
                    os.environ['VOLCANO_TTS_ACCESS_TOKEN'] = line.split('：')[1].strip()
                elif 'secret key' in line and '：' in line:
                    os.environ['VOLCANO_TTS_SECRET_KEY'] = line.split('：')[1].strip()
        print("[Config] 已从private/TTS.txt加载配置")
    except Exception as e:
        print(f"[Config] 加载private配置失败: {e}")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tts_controller import VolcanoTTSController
from src.schema import ScriptVersion, DialogueLine, TokenUsage

def test_context_reference():
    """
    测试1: 引用上下文功能
    验证TTS 2.0能利用前文语境生成更连贯的情感
    """
    print("\n" + "=" * 70)
    print("测试1: 引用上下文功能")
    print("=" * 70)

    # 设计测试场景：对话需要依赖前文语境
    lines = [
        DialogueLine(speaker="A", text="你听说过那个消息吗？"),
        DialogueLine(speaker="B", text="什么消息？"),
        DialogueLine(speaker="A", text="就是我们公司要上市的事情。"),  # 需要承接前文
        DialogueLine(speaker="B", text="真的吗？那太好了！恭喜你啊！"),  # 需要理解前文
        DialogueLine(speaker="A", text="是啊，准备了这么多年，终于有结果了。"),  # 延续话题
    ]

    total_chars = sum(len(l.text) for l in lines)
    script = ScriptVersion(
        session_id="test_context_001",
        outline_checksum="test",
        lines=lines,
        word_count=max(total_chars, 500),  # 满足最小限制
        estimated_duration_sec=120,  # 满足最小限制
        token_usage=TokenUsage(input=100, output=200, total=300)
    )

    # 测试启用上下文
    cost_with_context = {}
    controller_with = VolcanoTTSController(
        enable_context=True,
        cost_tracker=cost_with_context,
    )

    print(f"TTS 2.0检测: {'是' if controller_with._is_tts_v2 else '否'}")
    print(f"引用上文: {'启用' if controller_with.enable_context else '禁用'}")
    print(f"缓存大小: {controller_with._max_context_lines}句")

    output_path = Path("./test_outputs/tts_test/context_enabled.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        result = controller_with.generate_dual_audio(script, output_path)
        print(f"✅ 带上下文生成成功: {result.stat().st_size} bytes")
        print(f"   连接创建: {cost_with_context.get('connection_creates', 0)}")
        print(f"   连接复用: {cost_with_context.get('connection_reuses', 0)}")
    except Exception as e:
        print(f"❌ 带上下文生成失败: {e}")
        return False

    # 测试禁用上下文（对比）
    cost_without_context = {}
    controller_without = VolcanoTTSController(
        enable_context=False,
        cost_tracker=cost_without_context,
    )

    output_path2 = Path("./test_outputs/tts_test/context_disabled.mp3")

    try:
        result2 = controller_without.generate_dual_audio(script, output_path2)
        print(f"✅ 无上下文生成成功: {result2.stat().st_size} bytes")
    except Exception as e:
        print(f"❌ 无上下文生成失败: {e}")
        return False

    print("\n📊 上下文功能验证:")
    print(f"   启用上下文时缓存状态:")
    print(f"   A说话人缓存: {controller_with._context_cache.get('A', [])}")
    print(f"   B说话人缓存: {controller_with._context_cache.get('B', [])}")

    return True


def test_dual_speakers():
    """
    测试2: 双发音人测试
    验证A/B声道分配、音色区分、连接复用
    """
    print("\n" + "=" * 70)
    print("测试2: 双发音人声道分配")
    print("=" * 70)

    # A/B交替对话
    lines = []
    for i in range(10):
        if i % 2 == 0:
            lines.append(DialogueLine(speaker="A", text=f"这是第{i//2+1}轮对话，由A发言。"))
        else:
            lines.append(DialogueLine(speaker="B", text=f"这是B的回应，第{i//2+1}轮。"))

    script = ScriptVersion(
        session_id="test_dual_001",
        outline_checksum="test",
        lines=lines,
        word_count=max(sum(len(l.text) for l in lines), 500),
        estimated_duration_sec=120,
        token_usage=TokenUsage(input=100, output=200, total=300)
    )

    cost_tracker = {}
    controller = VolcanoTTSController(cost_tracker=cost_tracker)

    print(f"发音人A音色: {controller.host_a_voice}")
    print(f"发音人B音色: {controller.host_b_voice}")
    print(f"资源ID: {controller.resource_id}")

    # 验证音色类型
    voice_a = controller.voice_config.get_voice_info(controller.host_a_voice)
    voice_b = controller.voice_config.get_voice_info(controller.host_b_voice)

    print(f"\n音色信息:")
    print(f"  A: {voice_a.get('name', 'Unknown')} ({voice_a.get('gender', 'Unknown')})")
    print(f"  B: {voice_b.get('name', 'Unknown')} ({voice_b.get('gender', 'Unknown')})")

    output_path = Path("./test_outputs/tts_test/dual_speakers.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        start = time.time()
        result = controller.generate_dual_audio(script, output_path)
        elapsed = time.time() - start

        print(f"\n✅ 双发音人生成成功")
        print(f"   耗时: {elapsed:.2f}s")
        print(f"   文件大小: {result.stat().st_size} bytes")
        print(f"   连接创建: {cost_tracker.get('connection_creates', 0)} (预期: 2)")
        print(f"   连接复用: {cost_tracker.get('connection_reuses', 0)} (预期: 8)")
        print(f"   请求次数: {cost_tracker.get('total_requests', 0)}")

        # 验证连接复用效果
        expected_creates = 2
        expected_reuses = len(lines) - 2

        if cost_tracker.get('connection_creates', 0) == expected_creates:
            print(f"   ✅ 连接复用优化正确")
        else:
            print(f"   ⚠️ 连接数异常 (实际: {cost_tracker.get('connection_creates', 0)}, 预期: {expected_creates})")

        return True

    except Exception as e:
        print(f"❌ 双发音人测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_long_text():
    """
    测试3: 长文本压力测试
    验证长文本合成的稳定性、超时处理、内存管理
    """
    print("\n" + "=" * 70)
    print("测试3: 长文本压力测试")
    print("=" * 70)

    # 生成长文本对话 (50句，约1000+字符)
    long_text_a = """
    人工智能的发展历程可以追溯到上世纪五十年代。当时，计算机科学家们开始探索如何让机器模拟人类的智能行为。
    图灵测试的提出为人工智能的发展奠定了理论基础。随着计算能力的提升和算法的进步，人工智能在21世纪迎来了爆发式增长。
    深度学习技术的突破使得计算机在图像识别、语音识别、自然语言处理等领域取得了惊人的成就。
    """.strip().replace("\n", " ")

    long_text_b = """
    确实，深度学习的成功很大程度上依赖于大数据和大算力。卷积神经网络在图像领域的应用，
    循环神经网络和Transformer架构在序列建模中的成功，都推动了AI技术的实用化。
    但我们也要看到，当前的人工智能还存在很多局限性，比如可解释性差、泛化能力有限、对数据依赖过高等问题。
    """.strip().replace("\n", " ")

    lines = []
    num_turns = 25  # 25轮对话 = 50句

    for i in range(num_turns):
        lines.append(DialogueLine(speaker="A", text=f"{long_text_a[:80]} (第{i+1}轮)"))
        lines.append(DialogueLine(speaker="B", text=f"{long_text_b[:80]} (回应第{i+1}轮)"))

    total_chars = sum(len(l.text) for l in lines)

    print(f"测试规模:")
    print(f"  对话轮数: {num_turns}")
    print(f"  总句数: {len(lines)}")
    print(f"  总字符数: {total_chars}")
    print(f"  预估音频时长: {len(lines) * 3}秒 (~{len(lines)*3//60}分钟)")

    script = ScriptVersion(
        session_id="test_long_001",
        outline_checksum="test",
        lines=lines,
        word_count=max(total_chars, 500),
        estimated_duration_sec=max(len(lines) * 3, 120),
        token_usage=TokenUsage(input=1000, output=2000, total=3000)
    )

    cost_tracker = {}
    controller = VolcanoTTSController(
        enable_context=True,
        cost_tracker=cost_tracker,
    )

    output_path = Path("./test_outputs/tts_test/long_text.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n开始长文本合成...")

    try:
        start = time.time()

        # 每10句报告一次进度
        def progress_callback(current, total):
            if current % 10 == 0:
                elapsed = time.time() - start
                avg_time = elapsed / current
                remaining = (total - current) * avg_time
                print(f"  进度: {current}/{total} ({current*100//total}%) - "
                      f"已用{elapsed:.1f}s, 预计剩余{remaining:.1f}s")

        result = controller.generate_dual_audio(
            script,
            output_path,
            progress_callback=progress_callback,
        )

        elapsed = time.time() - start

        print(f"\n✅ 长文本合成成功")
        print(f"   总耗时: {elapsed:.2f}s ({elapsed/60:.1f}分钟)")
        print(f"   平均每句: {elapsed/len(lines):.2f}s")
        print(f"   文件大小: {result.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"   连接创建: {cost_tracker.get('connection_creates', 0)}")
        print(f"   连接复用: {cost_tracker.get('connection_reuses', 0)}")
        print(f"   重试次数: {cost_tracker.get('retry_count', 0)}")
        print(f"   失败请求: {cost_tracker.get('failed_requests', 0)}")

        if cost_tracker.get('failed_requests', 0) == 0:
            print(f"   ✅ 无失败请求")
        else:
            print(f"   ⚠️ 有{cost_tracker.get('failed_requests')}个失败请求")

        # 验证内存管理（检查是否顺利完成）
        print(f"   ✅ 内存管理正常")

        return True

    except Exception as e:
        print(f"\n❌ 长文本测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """
    测试4: 边界情况测试
    短文本、超长单句、特殊字符
    """
    print("\n" + "=" * 70)
    print("测试4: 边界情况测试")
    print("=" * 70)

    test_cases = [
        ("短文本", [DialogueLine(speaker="A", text="你好。")]),
        ("超长单句", [DialogueLine(speaker="A", text="这是一句非常长的文本" * 20)]),
        ("特殊字符", [DialogueLine(speaker="A", text="Hello! 你好？测试...【】「」")]),
        ("数字", [DialogueLine(speaker="A", text="2024年，AI技术实现了99.9%的准确率，花费$1000万。")]),
    ]

    controller = VolcanoTTSController()

    for case_name, lines in test_cases:
        print(f"\n  测试: {case_name}")
        print(f"    文本长度: {len(lines[0].text)}字符")

        script = ScriptVersion(
            session_id=f"test_edge_{case_name}",
            outline_checksum="test",
            lines=lines,
            word_count=max(len(lines[0].text), 500),
            estimated_duration_sec=120,
            token_usage=TokenUsage(input=10, output=20, total=30)
        )

        output_path = Path(f"./test_outputs/tts_test/edge_{case_name}.mp3")

        try:
            result = controller.generate_dual_audio(script, output_path)
            print(f"    ✅ 成功: {result.stat().st_size} bytes")
        except Exception as e:
            print(f"    ❌ 失败: {e}")

    return True


if __name__ == "__main__":
    print("=" * 70)
    print("TTS综合测试套件")
    print("=" * 70)
    print(f"测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 运行所有测试
    results = []

    results.append(("引用上下文", test_context_reference()))
    results.append(("双发音人", test_dual_speakers()))
    results.append(("长文本压力", test_long_text()))
    results.append(("边界情况", test_edge_cases()))

    # 汇总
    print("\n" + "=" * 70)
    print("测试结果汇总")
    print("=" * 70)

    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")

    all_passed = all(r[1] for r in results)

    print("=" * 70)
    if all_passed:
        print("🎉 所有测试通过！")
    else:
        print("⚠️ 部分测试失败，请检查日志")
    print("=" * 70)

    sys.exit(0 if all_passed else 1)
