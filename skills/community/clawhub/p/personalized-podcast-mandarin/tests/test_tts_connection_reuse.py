"""
TTS链接复用测试 - 验证同一人连续多句时连接复用
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
print("TTS链接复用测试")
print("=" * 70)
print("测试场景: A连续说5句，然后B连续说5句")
print("预期结果: 连接创建2次，连接复用8次")
print("=" * 70)

# A连续5句，B连续5句
lines = []
for i in range(5):
    lines.append(DialogueLine(speaker="A", text=f"这是A的第{i+1}句连续发言，用于测试链接复用功能。"))
for i in range(5):
    lines.append(DialogueLine(speaker="B", text=f"这是B的第{i+1}句连续发言，同样测试链接复用。"))

script = ScriptVersion(
    session_id="test_reuse_001",
    outline_checksum="test",
    lines=lines,
    word_count=500,
    estimated_duration_sec=120,
    token_usage=TokenUsage(input=100, output=200, total=300)
)

try:
    cost_tracker = {}
    controller = VolcanoTTSController(
        enable_context=True,
        cost_tracker=cost_tracker,
    )

    print(f"\n[TTS配置]")
    print(f"  Host A: {controller.host_a_voice}")
    print(f"  Host B: {controller.host_b_voice}")
    print(f"  TTS 2.0: {'是' if controller._is_tts_v2 else '否'}")

    output_path = Path("./test_outputs/tts_test/connection_reuse.mp3")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n[开始生成]")
    start = time.time()

    def progress(current, total):
        print(f"  进度: {current}/{total}")

    result = controller.generate_dual_audio(script, output_path, progress_callback=progress)
    elapsed = time.time() - start

    print(f"\n[生成完成]")
    print(f"  总耗时: {elapsed:.2f}s")
    print(f"  平均每句: {elapsed/len(lines):.2f}s")
    print(f"  文件大小: {result.stat().st_size} bytes")

    print(f"\n[连接复用统计]")
    print(f"  连接创建: {cost_tracker.get('connection_creates', 0)} (预期: 2)")
    print(f"  连接复用: {cost_tracker.get('connection_reuses', 0)} (预期: 8)")
    print(f"  请求总数: {cost_tracker.get('total_requests', 0)}")
    print(f"  重试次数: {cost_tracker.get('retry_count', 0)}")

    # 验证
    creates = cost_tracker.get('connection_creates', 0)
    reuses = cost_tracker.get('connection_reuses', 0)

    print(f"\n[验证结果]")
    if creates == 2:
        print(f"  [OK] 连接创建次数正确: {creates}")
    else:
        print(f"  [FAIL] 连接创建次数异常: {creates} (预期: 2)")

    if reuses == 8:
        print(f"  [OK] 连接复用次数正确: {reuses}")
    else:
        print(f"  [WARN] 连接复用次数: {reuses} (预期: 8)")

    # 计算节省的时间
    saved_time = reuses * 0.07  # 每次复用节省约70ms
    print(f"\n[性能优化]")
    print(f"  链接复用节省约: {saved_time*1000:.0f}ms ({saved_time:.2f}s)")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)

except Exception as e:
    print(f"\n[错误] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
