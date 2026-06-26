#!/bin/bash
# check-writing-state.sh
# 检查写作状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# 项目根目录
PROJECT_ROOT="${1:-.}"

# 检查必要文件
check_state() {
  local missing=0
  
  log_info "检查项目状态: $PROJECT_ROOT"
  
  # 检查宪法
  if [ -f "$PROJECT_ROOT/memory/constitution.md" ]; then
    log_info "✅ 宪法已创建"
  else
    log_warn "⚠️ 宪法未创建"
    missing=$((missing + 1))
  fi
  
  # 检查规格
  spec_file=$(find "$PROJECT_ROOT/stories" -name "specification.md" 2>/dev/null | head -1)
  if [ -n "$spec_file" ]; then
    log_info "✅ 故事规格已创建"
  else
    log_warn "⚠️ 故事规格未创建"
    missing=$((missing + 1))
  fi
  
  # 检查计划
  plan_file=$(find "$PROJECT_ROOT/stories" -name "creative-plan.md" 2>/dev/null | head -1)
  if [ -n "$plan_file" ]; then
    log_info "✅ 创作计划已创建"
  else
    log_warn "⚠️ 创作计划未创建"
    missing=$((missing + 1))
  fi
  
  # 检查任务
  tasks_file=$(find "$PROJECT_ROOT/stories" -name "tasks.md" 2>/dev/null | head -1)
  if [ -n "$tasks_file" ]; then
    log_info "✅ 任务清单已创建"
  else
    log_warn "⚠️ 任务清单未创建"
    missing=$((missing + 1))
  fi
  
  echo ""
  if [ $missing -eq 0 ]; then
    log_info "✅ 所有前置步骤已完成，可以开始写作"
    return 0
  else
    log_warn "⚠️ 还有 $missing 个前置步骤未完成"
    return 1
  fi
}

# 统计进度
show_progress() {
  log_info "进度统计"
  
  # 章节数
  total_chapters=$(find "$PROJECT_ROOT/stories" -name "chapter-*.md" 2>/dev/null | wc -l)
  log_info "已完成章节: $total_chapters"
  
  # 总字数
  total_words=0
  for f in $(find "$PROJECT_ROOT/stories" -name "chapter-*.md" 2>/dev/null); do
    words=$(count_chinese_words "$f")
    total_words=$((total_words + words))
  done
  log_info "已完成字数: $total_words"
}

if [ "$1" = "--check" ]; then
  check_state
elif [ "$1" = "--progress" ]; then
  show_progress
else
  check_state
  echo ""
  show_progress
fi
