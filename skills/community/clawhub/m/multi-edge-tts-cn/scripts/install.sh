#!/bin/bash
# Edge-TTS Skill 安装脚本
# 用法: bash install.sh

set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "=== Edge-TTS Skill 安装 ==="
echo "技能路径: $SKILL_DIR"

# 1. 检查 Python 版本
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        ver=$("$cmd" --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        if python3 -c "import sys; assert sys.version_info >= (3, 8)" 2>/dev/null; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ 需要 Python 3.8+"
    exit 1
fi

echo "✅ Python: $($PYTHON --version)"

# 2. 安装 edge-tts
echo ""
echo "检查 edge-tts..."
if $PYTHON -c "import edge_tts" 2>/dev/null; then
    echo "✅ edge-tts 已安装"
else
    echo "安装 edge-tts..."
    pip3 install --break-system-packages edge-tts 2>/dev/null || \
    pip3 install --user edge-tts 2>/dev/null || \
    pip3 install edge-tts 2>/dev/null || {
        echo "❌ edge-tts 安装失败"
        exit 1
    }
    echo "✅ edge-tts 安装成功"
fi

# 3. 检查 ffmpeg
echo ""
if command -v ffmpeg &>/dev/null; then
    ffmpeg_ver=$(ffmpeg -version 2>&1 | head -1)
    echo "✅ ffmpeg: $ffmpeg_ver"
else
    echo "❌ 需要 ffmpeg，请安装: sudo apt install ffmpeg"
    exit 1
fi

# 4. 验证语音生成
echo ""
echo "测试语音生成..."
OUT_DIR="$HOME/.openclaw/workspace/tmp"
mkdir -p "$OUT_DIR"
TEST_OUTPUT="$OUT_DIR/edge_tts_test.ogg"

$PYTHON "$SKILL_DIR/scripts/engine.py" \
    --text "你好，我是小梦，语音系统正常喵" \
    --voice xiaoxiao \
    --output "$TEST_OUTPUT"

if [ -f "$TEST_OUTPUT" ] && [ $(stat -f%z "$TEST_OUTPUT" 2>/dev/null || stat -c%s "$TEST_OUTPUT" 2>/dev/null) -gt 1000 ]; then
    echo "✅ 测试成功: $TEST_OUTPUT"
else
    echo "❌ 测试失败"
    exit 1
fi

# 5. 列出音色
echo ""
echo "=== 可用音色 ==="
$PYTHON "$SKILL_DIR/scripts/engine.py" --list-voices

echo ""
echo "=== 安装完成 ==="
echo "默认音色: xiaoxiao（活泼偏高音女声）"
echo "输出路径: ~/.openclaw/workspace/tmp/"
echo "调用方式: python3 scripts/engine.py --text <文本> --voice <音色ID>"
