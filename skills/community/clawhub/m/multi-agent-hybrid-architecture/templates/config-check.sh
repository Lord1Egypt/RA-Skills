#!/bin/bash

# 混合层级隔离架构 1.0 - 配置检查脚本
# 用于验证 Agent 配置是否正确

set -e

echo "🖤 混合层级隔离架构 1.0 - 配置检查"
echo "======================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 统计
PASS=0
FAIL=0
WARN=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASS++))
}

check_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAIL++))
}

check_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((WARN++))
}

# 1. 检查 Agent 目录
echo "📁 检查 Agent 目录..."
echo "-------------------"

WRITER_DIR="$HOME/Documents/openclaw/agents/writer"
MEDIA_DIR="$HOME/Documents/openclaw/agents/media"

if [ -d "$WRITER_DIR" ]; then
    check_pass "Writer Agent 目录存在：$WRITER_DIR"
else
    check_fail "Writer Agent 目录不存在：$WRITER_DIR"
    echo "  提示：请确认你的 writer Agent 目录路径"
fi

if [ -d "$MEDIA_DIR" ]; then
    check_pass "Media Agent 目录存在：$MEDIA_DIR"
else
    check_warn "Media Agent 目录不存在：$MEDIA_DIR"
    echo "  提示：如果还没创建 media Agent，请先创建"
fi

echo ""

# 2. 检查 SOUL.md 配置
echo "📜 检查 SOUL.md 配置..."
echo "---------------------"

if [ -f "$WRITER_DIR/SOUL.md" ]; then
    check_pass "Writer SOUL.md 存在"
    
    # 检查是否包含 baoyu 限制
    if grep -q "禁止.*baoyu\|baoyu.*禁止\|❌.*baoyu" "$WRITER_DIR/SOUL.md" 2>/dev/null; then
        check_pass "Writer SOUL.md 包含 baoyu-* 技能限制"
    else
        check_warn "Writer SOUL.md 可能缺少 baoyu-* 技能限制"
        echo "  提示：请确保包含'禁止执行 baoyu-* 技能'的约束"
    fi
else
    check_fail "Writer SOUL.md 不存在"
    echo "  提示：请复制 templates/writer-soul-template.md 到 $WRITER_DIR/SOUL.md"
fi

if [ -f "$MEDIA_DIR/SOUL.md" ]; then
    check_pass "Media SOUL.md 存在"
    
    # 检查是否包含 baoyu 权限
    if grep -q "baoyu.*权限\|✅.*baoyu\|允许.*baoyu" "$MEDIA_DIR/SOUL.md" 2>/dev/null; then
        check_pass "Media SOUL.md 包含 baoyu-* 技能权限"
    else
        check_warn "Media SOUL.md 可能缺少 baoyu-* 技能权限说明"
        echo "  提示：请确保包含'允许执行 baoyu-* 技能'的说明"
    fi
else
    check_warn "Media SOUL.md 不存在（如已创建 media Agent）"
    echo "  提示：请复制 templates/media-soul-template.md 到 $MEDIA_DIR/SOUL.md"
fi

echo ""

# 3. 检查技能目录
echo "🔧 检查技能目录..."
echo "-----------------"

# 检查 baoyu 技能是否存在
BAOYU_SKILLS=(
    "baoyu-image-gen"
    "baoyu-cover-image"
    "baoyu-infographic"
    "baoyu-post-to-wechat"
    "baoyu-post-to-weibo"
)

SKILLS_FOUND=0
SKILLS_TOTAL=${#BAOYU_SKILLS[@]}

for skill in "${BAOYU_SKILLS[@]}"; do
    # 检查常见技能路径
    if [ -d "$HOME/Documents/openclaw/agents/writer/skills/$skill" ] || \
       [ -d "$HOME/Documents/openclaw/agents/media/skills/$skill" ] || \
       [ -d "$HOME/.openclaw/skills/$skill" ]; then
        ((SKILLS_FOUND++))
    fi
done

if [ $SKILLS_FOUND -ge 3 ]; then
    check_pass "已找到 $SKILLS_FOUND/$SKILLS_TOTAL 个 baoyu-* 技能"
else
    check_warn "只找到 $SKILLS_FOUND/$SKILLS_TOTAL 个 baoyu-* 技能"
    echo "  提示：请确保已安装必要的 baoyu-* 技能"
fi

echo ""

# 4. 检查 openclaw.json 配置
echo "⚙️  检查 openclaw.json 配置..."
echo "---------------------------"

OPENCLAW_JSON="$HOME/.openclaw/openclaw.json"

if [ -f "$OPENCLAW_JSON" ]; then
    check_pass "openclaw.json 存在"
    
    # 检查 JSON 格式
    if python3 -m json.tool "$OPENCLAW_JSON" > /dev/null 2>&1; then
        check_pass "openclaw.json 格式正确"
    else
        check_fail "openclaw.json 格式错误"
        echo "  提示：请运行 'cat $OPENCLAW_JSON | python3 -m json.tool' 检查"
    fi
    
    # 检查是否包含多 bot 配置
    if grep -q "bots\[\]" "$OPENCLAW_JSON" 2>/dev/null || \
       grep -q "\"writer\"\|\"media\"" "$OPENCLAW_JSON" 2>/dev/null; then
        check_pass "openclaw.json 包含多 Agent 配置"
    else
        check_warn "openclaw.json 可能缺少多 Agent 配置"
        echo "  提示：如需多 Agent 协作，请配置 bots 数组"
    fi
else
    check_warn "openclaw.json 不存在（使用默认配置）"
fi

echo ""

# 5. 检查 Gateway 状态
echo "🚀 检查 Gateway 状态..."
echo "--------------------"

if command -v openclaw &> /dev/null; then
    if openclaw status &> /dev/null; then
        check_pass "OpenClaw Gateway 运行正常"
    else
        check_warn "OpenClaw Gateway 可能未运行"
        echo "  提示：运行 'openclaw gateway start' 启动"
    fi
else
    check_fail "未找到 openclaw 命令"
    echo "  提示：请确认 OpenClaw 已正确安装"
fi

echo ""

# 6. 检查模板文件
echo "📋 检查模板文件..."
echo "-----------------"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/writer-soul-template.md" ]; then
    check_pass "writer-soul-template.md 存在"
else
    check_fail "writer-soul-template.md 不存在"
fi

if [ -f "$SCRIPT_DIR/media-soul-template.md" ]; then
    check_pass "media-soul-template.md 存在"
else
    check_fail "media-soul-template.md 不存在"
fi

echo ""

# 总结
echo "======================================"
echo "📊 检查结果汇总"
echo "======================================"
echo -e "${GREEN}通过${NC}: $PASS"
echo -e "${RED}失败${NC}: $FAIL"
echo -e "${YELLOW}警告${NC}: $WARN"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ 配置检查通过！可以开始使用混合层级隔离架构~${NC}"
    echo ""
    echo "下一步："
    echo "1. 重启 Gateway: openclaw gateway restart"
    echo "2. 测试任务流转：@墨墨 帮我生成一张图片"
    echo "3. 验证约束：确认墨墨不会直接调用 baoyu-* 技能"
    exit 0
else
    echo -e "${RED}❌ 存在配置问题，请先修复上述失败项${NC}"
    echo ""
    echo "修复建议："
    echo "1. 确保 Agent 目录存在"
    echo "2. 复制 SOUL.md 模板到对应目录"
    echo "3. 确认 openclaw.json 配置正确"
    exit 1
fi
