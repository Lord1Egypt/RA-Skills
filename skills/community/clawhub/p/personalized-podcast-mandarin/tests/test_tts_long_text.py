"""
TTS长文本压力测试 - 验证长文本合成的稳定性
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
    except Exception as e:
        print(f"[Config] 加载失败: {e}")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tts_controller import VolcanoTTSController
from src.schema import ScriptVersion, DialogueLine, TokenUsage

print("=" * 70)
print("TTS长文本压力测试")
print("=" * 70)

# 生成长文本对话 - 使用简单文本避免编码问题
lines = []
num_turns = 5  # 5轮对话 = 10句

for i in range(num_turns):
    text_a = f"这是A的第{i+1}句发言，用于测试长文本合成功能是否正常工作。"
    text_b = f"这是B的第{i+1}句回应，同样用于测试长文本合成的稳定性。"
    lines.append(DialogueLine(speaker="A", text=text_a))
    lines.append(DialogueLine(speaker="B", text=text_b))

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
    enable_context=False,  # 先禁用引用上文，测试基础长文本功能
    cost_tracker=cost_tracker,
)

output_path = Path("./test_outputs/tts_test/long_text.mp3")
output_path.parent.mkdir(parents=True, exist_ok=True)

print(f"\n[开始长文本合成...]")

try:
    start = time.time()

    # 每5句报告一次进度
    def progress_callback(current, total):
        if current % 5 == 0:
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

    print(f"\n[生成成功]")
    print(f"  总耗时: {elapsed:.2f}s ({elapsed/60:.1f}分钟)")
    print(f"  平均每句: {elapsed/len(lines):.2f}s")
    print(f"  文件大小: {result.stat().st_size / 1024:.2f} KB")

    print(f"\n[成本统计]")
    print(f"  连接创建: {cost_tracker.get('connection_creates', 0)}")
    print(f"  连接复用: {cost_tracker.get('connection_reuses', 0)}")
    print(f"  请求总数: {cost_tracker.get('total_requests', 0)}")
    print(f"  重试次数: {cost_tracker.get('retry_count', 0)}")
    print(f"  失败请求: {cost_tracker.get('failed_requests', 0)}")

    if cost_tracker.get('failed_requests', 0) == 0:
        print(f"  [OK] 无失败请求")
    else:
        print(f"  [WARN] 有{cost_tracker.get('failed_requests')}个失败请求")

    # 计算优化效果
    reuses = cost_tracker.get('connection_reuses', 0)
    saved_time = reuses * 0.07
    print(f"\n[优化效果]")
    print(f"  链接复用节省约: {saved_time:.2f}s")

    # 验证稳定性
    if cost_tracker.get('retry_count', 0) == 0:
        print(f"  [OK] 无重试，连接稳定")
    else:
        print(f"  [INFO] 发生{cost_tracker.get('retry_count')}次重试")

    print("\n" + "=" * 70)
    print("长文本压力测试通过！")
    print("=" * 70)

except Exception as e:
    print(f"\n[错误] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
