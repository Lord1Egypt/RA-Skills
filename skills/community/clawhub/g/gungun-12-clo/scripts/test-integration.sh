#!/bin/bash
# 🌪️ 滚滚 Self-Reflection 集成测试脚本

echo "🌪️ 滚滚 Self-Reflection 集成测试"
echo "================================="
echo ""

WORKSPACE="/home/admin/.openclaw/workspace"
cd "$WORKSPACE"

# 测试 1：检查配置文件
echo "✅ 测试 1：检查配置文件"
if [ -f ".openclaw/self-reflection.json" ]; then
    echo "   ✓ self-reflection.json 存在"
else
    echo "   ✗ self-reflection.json 不存在"
fi

if [ -f "HEARTBEAT.md" ]; then
    echo "   ✓ HEARTBEAT.md 存在且已配置"
else
    echo "   ✗ HEARTBEAT.md 不存在"
fi

echo ""

# 测试 2：检查 .learnings/ 目录
echo "✅ 测试 2：检查 .learnings/ 目录"
if [ -d ".learnings" ]; then
    echo "   ✓ .learnings/ 目录存在"
    echo "   - LEARNINGS.md: $(wc -l < .learnings/LEARNINGS.md) 行"
    echo "   - ERRORS.md: $(wc -l < .learnings/ERRORS.md) 行"
    echo "   - FEATURE_REQUESTS.md: $(wc -l < .learnings/FEATURE_REQUESTS.md) 行"
else
    echo "   ✗ .learnings/ 目录不存在"
fi

echo ""

# 测试 3：检查 memory tiering
echo "✅ 测试 3：检查 memory tiering"
if [ -f "memory/hot/HOT_MEMORY.md" ]; then
    echo "   ✓ HOT_MEMORY.md 存在"
else
    echo "   ✗ HOT_MEMORY.md 不存在"
fi

if [ -f "memory/warm/WARM_MEMORY.md" ]; then
    echo "   ✓ WARM_MEMORY.md 存在"
else
    echo "   ✗ WARM_MEMORY.md 不存在"
fi

if [ -f "memory/self-review.md" ]; then
    echo "   ✓ self-review.md 存在"
else
    echo "   ✗ self-review.md 不存在"
fi

echo ""

# 测试 4：检查 12 号滚滚脚本
echo "✅ 测试 4：检查 12 号滚滚脚本"
if [ -f "skills/gungun-12-clo/scripts/learning_recorder.py" ]; then
    echo "   ✓ learning_recorder.py 存在"
else
    echo "   ✗ learning_recorder.py 不存在"
fi

if [ -f "skills/gungun-12-clo/scripts/error_detector.py" ]; then
    echo "   ✓ error_detector.py 存在"
else
    echo "   ✗ error_detector.py 不存在"
fi

if [ -f "skills/gungun-12-clo/scripts/learning_promoter.py" ]; then
    echo "   ✓ learning_promoter.py 存在"
else
    echo "   ✗ learning_promoter.py 不存在"
fi

echo ""

# 测试 5：测试 learning_recorder.py
echo "✅ 测试 5：测试 learning_recorder.py"
python3 skills/gungun-12-clo/scripts/learning_recorder.py learning "test" "集成测试" "测试学习记录功能" "low" "test" 2>&1

echo ""

# 测试 6：检查已安装的反思技能
echo "✅ 测试 6：检查已安装的反思技能"
skills=("self-improving-agent" "self-reflection" "auto-reflection" "memory-tiering" "gungun-12-clo")
for skill in "${skills[@]}"; do
    if [ -d "skills/$skill" ]; then
        echo "   ✓ $skill 已安装"
    else
        echo "   ✗ $skill 未安装"
    fi
done

echo ""

# 测试 7：检查 jq 和 date（self-reflection 依赖）
echo "✅ 测试 7：检查系统依赖"
if command -v jq &> /dev/null; then
    echo "   ✓ jq 已安装"
else
    echo "   ✗ jq 未安装（需要安装：sudo yum install jq）"
fi

if command -v date &> /dev/null; then
    echo "   ✓ date 已安装"
else
    echo "   ✗ date 未安装"
fi

echo ""
echo "================================="
echo "🎉 测试完成！"
echo ""
echo "📊 学习统计："
grep -h "### \[LRN-" .learnings/LEARNINGS.md 2>/dev/null | wc -l | xargs echo "   - 学习记录数："
grep -h "Status\*\*: pending" .learnings/LEARNINGS.md 2>/dev/null | wc -l | xargs echo "   - Pending 学习："
grep -h "Status\*\*: resolved" .learnings/LEARNINGS.md 2>/dev/null | wc -l | xargs echo "   - 已解决："
grep -h "Status\*\*: promoted" .learnings/LEARNINGS.md 2>/dev/null | wc -l | xargs echo "   - 已推广："

echo ""
echo "💡 下一步："
echo "   1. 运行 self-reflection check（如果可用）"
echo "   2. 推广 pending 学习到 AGENTS.md/SOUL.md/TOOLS.md"
echo "   3. 生成第一次学习周报"
