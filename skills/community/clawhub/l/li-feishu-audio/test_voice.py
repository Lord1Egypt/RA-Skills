#!/usr/bin/env python3
"""完整的语音功能测试脚本"""

import os
import sys
import subprocess
import tempfile

# 动态检测技能目录（支持不同用户和环境）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == "scripts" else SCRIPT_DIR

# 优先使用环境变量，否则使用默认路径
VENV_DIR = os.environ.get("VENV_DIR", f"{SKILL_DIR}/.venv")
VENV_PYTHON = f"{VENV_DIR}/bin/python"

def test_component(name, cmd, timeout=30):
    """测试单个组件"""
    print(f"\n[测试] {name}")
    print(f"  命令: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            print(f"  ✅ 成功")
            return True
        else:
            print(f"  ❌ 失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ 异常: {e}")
        return False

def main():
    print("=" * 60)
    print("Li Feishu Audio - 完整功能测试")
    print("=" * 60)

    results = []

    # 1. 测试模型是否存在
    model_dir = os.path.expanduser("~/.fast-whisper-models/models--Systran--faster-whisper-tiny")
    if os.path.exists(model_dir):
        print(f"\n[检查] faster-whisper tiny 模型")
        print(f"  路径: {model_dir}")
        print(f"  ✅ 存在")
        results.append(True)
    else:
        print(f"\n[检查] faster-whisper tiny 模型")
        print(f"  路径: {model_dir}")
        print(f"  ❌ 不存在")
        results.append(False)

    # 2. 测试 edge-tts
    temp_mp3 = tempfile.mktemp(suffix=".mp3")
    tts_script = f"""
import asyncio
import edge_tts
async def main():
    communicate = edge_tts.Communicate("测试", "zh-CN-XiaoxiaoNeural")
    await communicate.save("{temp_mp3}")
asyncio.run(main())
"""
    results.append(test_component("edge-tts 语音生成",
        [VENV_PYTHON, "-c", tts_script]))

    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)

    # 3. 测试 ffmpeg
    results.append(test_component("ffmpeg 格式转换",
        ["ffmpeg", "-version"]))

    # 4. 测试 ffprobe
    results.append(test_component("ffprobe 时长检测",
        ["ffprobe", "-version"]))

    # 5. 测试 handler
    print(f"\n[测试] voice.py Handler")
    handler_input = '{"message": "你好"}'
    try:
        result = subprocess.run(
            [VENV_PYTHON, f"{SKILL_DIR}/src/handlers/voice.py"],
            input=handler_input,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"  输出: {result.stdout.strip()}")
            if '"voice_path"' in result.stdout and '"voice_duration"' in result.stdout:
                print(f"  ✅ Handler 工作正常")
                results.append(True)
            else:
                print(f"  ❌ Handler 输出格式不正确")
                results.append(False)
        else:
            print(f"  ❌ Handler 失败: {result.stderr}")
            results.append(False)
    except Exception as e:
        print(f"  ❌ Handler 异常: {e}")
        results.append(False)

    # 6. 检查最终语音文件
    print(f"\n[检查] 生成的语音文件")
    if os.path.exists("/tmp/reply.opus"):
        size = os.path.getsize("/tmp/reply.opus")
        print(f"  路径: /tmp/reply.opus")
        print(f"  大小: {size} bytes")
        print(f"  ✅ 文件存在")
        results.append(True)
    else:
        print(f"  路径: /tmp/reply.opus")
        print(f"  ❌ 文件不存在")
        results.append(False)

    # 总结
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"测试结果: {passed}/{total} 通过")

    if passed == total:
        print("✅ 所有组件工作正常！Li Feishu Audio 技能已就绪。")
        return 0
    else:
        print("❌ 部分组件有问题，请检查上方日志。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
