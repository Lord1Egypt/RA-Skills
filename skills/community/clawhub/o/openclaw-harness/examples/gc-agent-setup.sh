#!/bin/bash
# =============================================================================
# gc-agent-setup.sh — GC Agent 配置与使用示例
#
# 描述：演示 GC Agent 的完整配置流程，包括 config.json 设置、daemon 模式、
#       单次执行、干运行预览
# 依赖：harness, gc-agent.sh（位于 /data/openclaw-harness/bin/）
#
# 使用场景：
#   - 设置自动清理规则
#   - 启动后台 GC 守护进程
#   - 手动触发 GC 清理
# =============================================================================

set -e

HARNESS_BIN="/data/openclaw-harness/bin"
GC_AGENT="${HARNESS_BIN}/gc-agent.sh"
HARNESS_CMD="${HARNESS_BIN}/harness"
PROJECT="${PROJECT:-$HOME/tmp/gc-agent-demo}"

# -----------------------------------------------------------------------------
# 颜色输出
# -----------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}    $*"; }
success() { echo -e "${GREEN}[PASS]${NC}   $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}   $*"; }
error()   { echo -e "${RED}[ERROR]${NC}  $*"; exit 1; }
section() { echo -e "\n${CYAN}==== $* ====${NC}"; }

# -----------------------------------------------------------------------------
# 清理演示目录（幂等）
# -----------------------------------------------------------------------------
cleanup_demo() {
  [[ -d "$PROJECT" ]] && rm -rf "$PROJECT"
  info "演示目录已清理"
}

# trap cleanup_demo EXIT

# -----------------------------------------------------------------------------
# 主流程
# -----------------------------------------------------------------------------
echo ""
echo "=============================================="
echo "  openclaw-harness GC Agent 配置与使用"
echo "=============================================="
echo ""

# 创建演示项目
info "创建演示项目: $PROJECT"
mkdir -p "$PROJECT"
cd "$PROJECT"

# 初始化 Harness
section "Step 1: 初始化 Harness"
"$HARNESS_CMD" init --quiet && success "Harness 初始化完成"

# 创建示例文件
cat > TASKS.md <<'EOF'
# TASKS.md - GC Agent 演示

## 状态
- [ACTIVE] GC Agent 配置演示

## 阶段
- [DONE] 初始化
- [ACTIVE] GC Agent 配置
- [PENDING] 测试清理
EOF
success "示例 TASKS.md 已创建"

# 创建多个检查点（用于测试 GC 数量限制）
section "Step 2: 创建多个检查点（测试 GC 数量限制）"
for i in 1 2 3 4 5 6 7 8; do
  "$HARNESS_CMD" checkpoint create "checkpoint-$i" --tag "test" 2>/dev/null && \
    info "  创建 checkpoint-$i" || warn "  创建失败: checkpoint-$i"
done
success "测试检查点已创建"

# 创建多个验证报告（用于测试报告保留）
section "Step 3: 创建多个验证报告（测试报告保留）"
for i in 1 2 3 4 5 6; do
  "$HARNESS_CMD" verify 2>/dev/null && info "  验证 $i" || true
done
success "测试验证报告已创建"

# -----------------------------------------------------------------------------
# 场景 1: 查看 GC 配置
# -----------------------------------------------------------------------------
section "场景 1: 查看当前 GC 配置"
info "配置文件位置: .harness/config.json"
if [[ -f ".harness/config.json" ]]; then
  info "当前配置内容："
  cat .harness/config.json | head -20
else
  info "配置文件尚未创建，首次 gc-agent 运行将使用默认配置"
fi

# -----------------------------------------------------------------------------
# 场景 2: GC 规则配置说明
# -----------------------------------------------------------------------------
section "场景 2: GC 规则配置说明"
highlight() { echo -e "  ${CYAN}$1${NC}"; }
highlight "可配置的 GC 规则（在 .harness/config.json 中）："
echo ""
echo "  gc.max_checkpoints       每任务最大检查点数（默认 10）"
echo "  gc.max_age_days          检查点最大保留天数（默认 7）"
echo "  gc.report_retention      报告保留数量（默认 20）"
echo "  gc.compress_trigger_lines MEMORY.md 压缩触发行数（默认 200）"
echo "  gc.daemon_interval       Daemon 轮询间隔秒数（默认 3600）"
echo "  gc.trash_retention_days  .trash 永久删除天数（默认 30）"
echo "  gc.archive_priority      归档优先级：memory-palace | local"
echo "  gc.skip_compress         跳过 memory 压缩（默认 false）"
echo "  gc.skip_checkpoint       跳过检查点清理（默认 false）"
echo "  gc.skip_report           跳过报告清理（默认 false）"
echo ""

# -----------------------------------------------------------------------------
# 场景 3: 单次 GC 干运行（预览）
# -----------------------------------------------------------------------------
section "场景 3: 单次 GC 干运行（预览）"
info "执行: gc-agent.sh --once --dry-run"
echo ""
"$GC_AGENT" --once --dry-run --verbose 2>&1 || true
echo ""

# -----------------------------------------------------------------------------
# 场景 4: 单次 GC 实际执行（限制数量）
# -----------------------------------------------------------------------------
section "场景 4: 单次 GC 实际执行（限制 max_cp=3）"
info "执行: gc-agent.sh --once --run --dry-run（先预览）"
"$GC_AGENT" --once --run --dry-run --verbose --max-cp 3 2>&1 || true
echo ""

read -p "$(echo -e "${YELLOW}[INPUT]${NC} 是否实际执行清理 max_cp=3？(y/N): ")" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  info "执行: gc-agent.sh --once --run --max-cp 3"
  "$GC_AGENT" --once --run --max-cp 3 --verbose 2>&1 || true
  success "GC 执行完成"
  
  info "清理后的检查点列表："
  "$HARNESS_CMD" checkpoint list 2>/dev/null | grep -E "ID|label|---|cp-" || true
else
  warn "跳过实际执行"
fi

# -----------------------------------------------------------------------------
# 场景 5: Daemon 模式说明
# -----------------------------------------------------------------------------
section "场景 5: Daemon 模式配置"
echo ""
highlight "启动 GC Agent 守护进程（后台常驻）："
echo ""
echo "  # 方式 1: 直接后台启动"
echo "  gc-agent.sh --daemon --run &"
echo ""
echo "  # 方式 2: 指定轮询间隔（每 30 分钟）"
echo "  gc-agent.sh --daemon --run --interval 1800 &"
echo ""
echo "  # 方式 3: 仅干运行守护（不实际清理）"
echo "  gc-agent.sh --daemon --dry-run --interval 600 &"
echo ""
echo "  # 查看 GC Agent 日志"
echo "  tail -f .harness/gc-agent.log"
echo ""

# -----------------------------------------------------------------------------
# 场景 6: 部分清理选项
# -----------------------------------------------------------------------------
section "场景 6: 部分清理（选择性跳过）"
highlight "选择性跳过某些清理项："
echo ""
echo "  # 仅清理检查点，跳过报告和 memory 压缩"
echo "  gc-agent.sh --once --run --no-report --no-compress"
echo ""
echo "  # 仅清理旧检查点（按时间），不限制数量"
echo "  gc-agent.sh --once --run --max-cp 999"
echo ""
echo "  # 跳过 .trash 清理（保留所有已删除项直到过期）"
echo "  gc-agent.sh --once --run --no-trash"
echo ""

# -----------------------------------------------------------------------------
# 场景 7: GC 日志查看
# -----------------------------------------------------------------------------
section "场景 7: GC 日志查看"
info "GC 日志位置: .harness/gc.log"
info "GC Agent 日志位置: .harness/gc-agent.log"
if [[ -f ".harness/gc.log" ]]; then
  info "最近 GC 日志（最后 10 行）："
  tail -10 .harness/gc.log 2>/dev/null || echo "（暂无）"
else
  echo "  （暂无 GC 日志）"
fi

# -----------------------------------------------------------------------------
# 场景 8: 查看 Harness 状态
# -----------------------------------------------------------------------------
section "场景 8: 查看 Harness 状态"
"$HARNESS_CMD" status -s

# -----------------------------------------------------------------------------
# 总结
# -----------------------------------------------------------------------------
section "GC Agent 快速参考"
echo ""
echo "  # 单次干运行预览（最安全）"
echo "  gc-agent.sh --once --dry-run"
echo ""
echo "  # 单次实际执行"
echo "  gc-agent.sh --once --run"
echo ""
echo "  # 后台常驻守护进程"
echo "  gc-agent.sh --daemon --run &"
echo ""
echo "  # 通过 harness 命令"
echo "  harness gc --dry-run          # 预览"
echo "  harness gc                    # 执行"
echo "  harness gc --max-cp 5         # 限制数量"
echo "  harness gc --max-age 7         # 按时间清理"
echo "  harness gc --aggressive        # 含 tmp 清理"
echo ""

success "GC Agent 配置演示完成！"
info "清理演示目录: rm -rf $PROJECT"
echo ""
