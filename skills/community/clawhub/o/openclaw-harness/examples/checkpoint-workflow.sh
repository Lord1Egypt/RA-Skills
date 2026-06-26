#!/bin/bash
# =============================================================================
# checkpoint-workflow.sh — openclaw-harness 检查点工作流示例
#
# 描述：演示完整的检查点生命周期 — 创建、列出、恢复、删除
# 依赖：harness, openclaw-harness 已安装
#
# 使用场景：
#   - 开发过程中频繁存档，防止工作丢失
#   - 危险操作前创建安全快照
#   - 回滚到之前的稳定版本
# =============================================================================

set -e

HARNESS="/data/openclaw-harness/bin/harness"
PROJECT="${PROJECT:-$HOME/tmp/checkpoint-demo}"

# -----------------------------------------------------------------------------
# 颜色输出
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}    $*"; }
success() { echo -e "${GREEN}[PASS]${NC}   $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}   $*"; }
error()   { echo -e "${RED}[ERROR]${NC}  $*"; exit 1; }
step()    { echo -e "${MAGENTA}[STEP]${NC}  $*"; }
highlight() { echo -e "${CYAN}  $*{NC}"; }

# -----------------------------------------------------------------------------
# 辅助函数
# -----------------------------------------------------------------------------

# 等待用户确认（用于交互模式）
confirm() {
  local prompt="${1:-继续？}"
  read -p "$(echo -e "${YELLOW}[CONFIRM]${NC} $prompt (y/N): ")" -n 1 -r
  echo
  [[ $REPLY =~ ^[Yy]$ ]] || { warn "已取消"; return 1; }
  return 0
}

# 打印分隔线
divider() {
  echo ""
  echo "──────────────────────────────────────────────"
  echo ""
}

# -----------------------------------------------------------------------------
# 主流程
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "  openclaw-harness 检查点工作流演示"
echo "=============================================="
echo ""

# 创建演示目录
info "创建演示项目: $PROJECT"
mkdir -p "$PROJECT"
cd "$PROJECT"

# 初始化 Harness
step "初始化 Harness"
"$HARNESS" init --quiet && success "初始化完成"

# 创建示例任务文件
cat > TASKS.md <<'EOF'
# TASKS.md - 检查点工作流演示

## 阶段

| ID | 名称 | 状态 |
|----|------|------|
| 1 | 需求分析 | ✅ 完成 |
| 2 | 架构设计 | 🔄 进行中 |
| 3 | 开发实现 | ⏳ 待开始 |
| 4 | 测试验证 | ⏳ 待开始 |

## 当前: Phase 2 - 架构设计

- [ACTIVE] 检查点工作流演示
EOF

cat > MEMORY.md <<'EOF'
# MEMORY.md

## 重要决策

- 2026-03-27: 使用检查点管理开发进度
EOF

success "示例文件已创建 (TASKS.md, MEMORY.md)"

# -----------------------------------------------------------------------------
# 场景 1: 正常存档流程
# -----------------------------------------------------------------------------
divider
step "场景 1: 正常存档流程"

info "创建检查点 'before-dangerous-change'"
CP1=$("$HARNESS" checkpoint create "before-dangerous-change" --tag "safe-point" 2>/dev/null | grep -o '[a-f0-9]\{16,\}' | head -1 || echo "")
if [[ -n "$CP1" ]]; then
  success "检查点 ID: $CP1"
else
  warn "获取检查点 ID 失败，继续演示"
fi

info "模拟正常开发修改..."
echo "# 新增功能" >> TASKS.md
echo "- 新增：检查点功能" >> TASKS.md
success "文件已修改"

# -----------------------------------------------------------------------------
# 场景 2: 危险操作前的安全快照
# -----------------------------------------------------------------------------
divider
step "场景 2: 危险操作前的安全快照"

info "创建 'pre-refactor' 安全快照"
CP_SAFE=$("$HARNESS" checkpoint create "pre-refactor-safety" --tag "refactor" --tag "safe" 2>/dev/null | grep -o '[a-f0-9]\{16,\}' | head -1 || echo "")
[[ -n "$CP_SAFE" ]] && success "安全快照 ID: $CP_SAFE" || warn "获取 ID 失败"

info "模拟危险重构操作..."
# 模拟修改（实际会破坏文件）
echo "" >> TASKS.md
echo "## 重构中（模拟危险操作）" >> TASKS.md
echo "⚠️  大规模重构中，功能可能不稳定" >> TASKS.md
success "文件已修改（危险操作）"

# 列出当前所有检查点
info "当前检查点列表："
echo ""
"$HARNESS" checkpoint list 2>/dev/null | grep -E "^(ID|label|---|\|)" || true
echo ""

# -----------------------------------------------------------------------------
# 场景 3: 从安全快照恢复
# -----------------------------------------------------------------------------
divider
step "场景 3: 从安全快照恢复"

if [[ -n "$CP_SAFE" ]]; then
  warn "发现文件已被破坏，准备从安全快照恢复..."
  # confirm "确认从检查点 $CP_SAFE 恢复？" || true
  
  highlight "执行: harness checkpoint restore $CP_SAFE"
  "$HARNESS" checkpoint restore "$CP_SAFE" --force 2>/dev/null && \
    success "已恢复到 'pre-refactor-safety' 检查点" || \
    warn "恢复命令执行完成（请手动验证文件）"
  
  info "验证恢复后的 TASKS.md："
  grep -c "危险操作" TASKS.md >/dev/null 2>&1 && \
    warn "文件仍包含危险操作标记" || \
    success "TASKS.md 已恢复正常"
else
  warn "无安全快照，跳过恢复演示"
fi

# -----------------------------------------------------------------------------
# 场景 4: 检查点生命周期管理
# -----------------------------------------------------------------------------
divider
step "场景 4: 检查点生命周期管理"

info "创建多个检查点模拟生命周期..."
for label in "milestone-1" "milestone-2" "milestone-3"; do
  "$HARNESS" checkpoint create "$label" --tag "milestone" 2>/dev/null && \
    success "创建: $label" || warn "创建失败: $label"
done

info "查看所有检查点："
echo ""
"$HARNESS" checkpoint list 2>/dev/null | head -30 || true
echo ""

# -----------------------------------------------------------------------------
# 场景 5: 清理旧检查点
# -----------------------------------------------------------------------------
divider
step "场景 5: GC 清理（干运行）"

info "预览 GC 将清理的内容："
"$HARNESS" gc --dry-run --max-cp 3 2>/dev/null || warn "GC 干运行完成"

# -----------------------------------------------------------------------------
# 总结
# -----------------------------------------------------------------------------
divider
highlight "检查点工作流核心命令："
echo ""
echo "  # 创建检查点（推荐在每次重要变更前）"
echo "  harness checkpoint create <标签> --tag <标签名>"
echo ""
echo "  # 危险操作前务必存档"
echo "  harness checkpoint create pre-refactor-safety"
echo ""
echo "  # 列出所有检查点"
echo "  harness checkpoint list"
echo ""
echo "  # 恢复到安全快照"
echo "  harness checkpoint restore <cp-id>"
echo ""
echo "  # 自动清理旧检查点"
echo "  harness gc --dry-run  # 先预览"
echo "  harness gc --max-cp 5  # 限制数量"

echo ""
success "检查点工作流演示完成！"
echo ""
info "清理演示目录: rm -rf $PROJECT"
echo ""
