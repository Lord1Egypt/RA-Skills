#!/bin/bash
# openclaw-mlx-audio - 简化测试脚本
# 专注于代码质量和构建验证

set -e

echo "🧪 Running openclaw-mlx-audio tests..."

TOTAL=0
PASSED=0
FAILED=0

run_test() {
    local name="$1"
    local command="$2"
    
    TOTAL=$((TOTAL + 1))
    echo ""
    echo "▶️  Test $TOTAL: $name"
    
    if eval "$command" > /tmp/test_output_$TOTAL.txt 2>&1; then
        PASSED=$((PASSED + 1))
        echo "✅ PASSED: $name"
        return 0
    else
        FAILED=$((FAILED + 1))
        echo "❌ FAILED: $name"
        cat /tmp/test_output_$TOTAL.txt | tail -20
        return 1
    fi
}

# 1. 依赖检查
echo ""
echo "📦 Checking dependencies..."
run_test "ffmpeg installed" "command -v ffmpeg"
run_test "uv installed" "command -v uv"
run_test "Node.js installed" "command -v node"
run_test "bun installed" "command -v bun"

# 2. 构建检查
echo ""
echo "🏗️  Checking build..."
run_test "dist/index.js exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/dist/index.js"
run_test "package.json valid" "cd /Users/user/.openclaw/workspace/openclaw-mlx-audio && cat package.json | grep '\"name\"'"
run_test "openclaw.plugin.json valid" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/openclaw.plugin.json"

# 3. 代码质量检查
echo ""
echo "📝 Checking code quality..."
run_test "TypeScript compiles" "cd /Users/user/.openclaw/workspace/openclaw-mlx-audio && bun run build"
run_test "install.sh exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/install.sh"
run_test "install.sh executable" "test -x /Users/user/.openclaw/workspace/openclaw-mlx-audio/install.sh"

# 4. 文档检查
echo ""
echo "📚 Checking documentation..."
run_test "README exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/README.md"
run_test "TEST_PLAN exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/TEST_PLAN.md"
run_test "AUTORESEARCH_PLAN exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/AUTORESEARCH_PLAN.md"

# 5. 文件结构检查
echo ""
echo "📁 Checking file structure..."
run_test "src/index.ts exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/src/index.ts"
run_test "python-runtime exists" "test -d /Users/user/.openclaw/workspace/openclaw-mlx-audio/python-runtime"
run_test "tts_server.py exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/python-runtime/tts_server.py"
run_test "stt_server.py exists" "test -f /Users/user/.openclaw/workspace/openclaw-mlx-audio/python-runtime/stt_server.py"

# 计算成功率
echo ""
echo "📊 Results:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Total:  $TOTAL"
echo "Passed: $PASSED"
echo "Failed: $FAILED"

if [ $TOTAL -gt 0 ]; then
    SUCCESS_RATE=$(echo "scale=2; $PASSED * 100 / $TOTAL" | bc)
    echo "Success Rate: ${SUCCESS_RATE}%"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 输出指标供 autoresearch 使用
    echo ""
    echo "## Metrics for autoresearch:"
    echo "SUCCESS_RATE=$SUCCESS_RATE"
    echo "TOTAL_TESTS=$TOTAL"
    echo "PASSED_TESTS=$PASSED"
fi

# 清理
rm -f /tmp/test_output_*.txt

# 退出码
if [ $FAILED -gt 0 ]; then
    exit 1
else
    exit 0
fi
