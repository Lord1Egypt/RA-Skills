#!/usr/bin/env bash
#============================================================
# auto-capture.sh - Claude Code 风格的自动记忆捕获
#============================================================
# 功能：自动识别会话中的"高光时刻"并写入记忆
# 触发条件：
#   1. 完成后（✅ 完成 / 🏆 超越 / v1.0.0 发布）
#   2. 修正后（用户纠正了 AI 的错误）
#   3. 错误解决后（从错误中学习）
#   4. 重要决策（用户做出了重要决定）
#   5. 发现新模式（重复出现的信息）
#============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 自动检测 workspace 路径
# 优先级：WORKSPACE_DIR 环境变量 > PWD > 基于脚本位置推断
if [ -n "${WORKSPACE_DIR:-}" ]; then
    : # 使用环境变量
elif [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
else
    # 回退：从脚本位置推断（适用于主 workspace）
    WORKSPACE_DIR="$(cd "$SKILL_DIR/../.." && pwd)"
fi
MEMORY_DIR="$WORKSPACE_DIR/memory"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_capture(){ echo -e "${GREEN}[CAPTURE]${NC} $*"; }

#----------------------------------------------------------
# 模式定义
#----------------------------------------------------------

# 完成类模式（优先级最高）
PATTERN_COMPLETION=(
  "已完成|完成|✅|v[0-9]+\.[0-9]+|发布|突破|超越"
  "实现了|实现了|已实现|功能完成|100%|全部完成"
)

# 修正类模式
PATTERN_CORRECTION=(
  "不对|不是这样|错了|重新|纠正|修正"
  "你忘了|你忘记了|你应该|记住"
)

# 错误解决模式
PATTERN_ERROR_FIXED=(
  "错误已修复|解决了|修好了|找到原因了"
  "Root cause|根本原因|是因为"
)

# 决策类模式
PATTERN_DECISION=(
  "决定用|选用|采用|选择"
  "就这样|就这样定了|方案是"
)

# 任务指令模式（v3.1.0 新增）
PATTERN_TASK=(
  "@贾维斯|@JARVIS"
  "帮我|帮我把|帮我做"
  "fork.*到|fork.*into"
  "创建.*仓库|新建.*项目"
  "安装.*技能|发布.*技能"
  "拆分成|分拆成"
  "同步到|上传到|部署到"
  "给我.*取个.*别名"
)

# 异步任务开始模式（v3.4.5 新增 - 对标 Claude Code async task tracking）
PATTERN_ASYNC_START=(
  "生成已启动|任务已启动|ID：[a-f0-9-]+"
  "正在生成|开始生成|启动生成"
  "video.*生成|audio.*生成|导出开始"
  "上传中|上传开始|发送中"
)

#----------------------------------------------------------
# 核心：检查内容是否匹配任何模式
#----------------------------------------------------------
match_patterns() {
  local content="$1"
  local pattern_list="$2"
  local pattern
  echo "$pattern_list" | tr '|' '\n' | while IFS= read -r pattern; do
    if echo "$content" | grep -qiE "$pattern" 2>/dev/null; then
      echo "MATCH:$pattern"
      return 0
    fi
  done
  return 1
}

#----------------------------------------------------------
# 提取关键信息
#----------------------------------------------------------
extract_key_info() {
  local content="$1"
  local type="$2"
  
  # 清理内容，保留关键部分
  echo "$content" | head -20 | grep -v "^[[:space:]]*$" | head -10
}

#----------------------------------------------------------
# 分类记忆类型
#----------------------------------------------------------
classify_memory() {
  local content="$1"
  
  # 优先级：异步任务开始 > 任务指令 > 纠正 > 完成 > 决策 > 错误解决
  # 异步任务开始模式（第一时间检测，防止丢失进行中任务状态）
  if echo "$content" | grep -qiE "生成已启动|任务已启动|ID：[a-f0-9-]{10,}|正在生成|开始生成|启动生成|video.*生成|audio.*生成|导出开始|上传中|上传开始|发送中"; then
    echo "async-start"
  # 任务指令模式
  elif echo "$content" | grep -qiE "@贾维斯|@JARVIS|帮我|帮我把|帮我做|fork.*到|fork.*into|创建.*仓库|新建.*项目|安装.*技能|发布.*技能|拆分成|分拆成|同步到|上传到|部署到|给我.*取个.*别名"; then
    echo "task"
  # 修正类
  elif echo "$content" | grep -qiE "你错了|不对|不是这样|错了|重新|纠正|修正|你忘了|你忘记了|实际上|正确的是"; then
    echo "feedback"
  # 完成类
  elif echo "$content" | grep -qiE "已完成|完成|✅|v[0-9]+\.[0-9]+|发布|突破|超越|实现了|已实现|100%|全部完成"; then
    echo "project"
  # 决策类
  elif echo "$content" | grep -qiE "决定用|选用|采用|选择|就这样|就这样定了|方案是"; then
    echo "project"
  # 错误解决类
  elif echo "$content" | grep -qiE "错误已修复|解决了|修好了|找到原因了|Root cause|根本原因|是因为"; then
    echo "feedback"
  else
    echo "reference"
  fi
}

#----------------------------------------------------------
# 主函数：自动捕获
#----------------------------------------------------------
auto_capture() {
  local content="${1:-}"
  local manual_type="${2:-}"
  
  if [[ -z "$content" ]]; then
    log_warn "用法: auto-capture.sh <内容> [类型]"
    return 1
  fi
  
  local type="${manual_type:-$(classify_memory "$content")}"
  local timestamp
  timestamp=$(date '+%Y-%m-%d %H:%M')
  
  # 如果是异步任务开始类型，先添加到待追踪任务列表
  if [[ "$type" == "async-start" ]]; then
    # 提取任务 ID（匹配 UUID 或类似 ID）
    local task_id
    task_id=$(echo "$content" | grep -oE "[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}" | head -1)
    if [[ -z "$task_id" ]]; then
      # 如果没找到 UUID，生成一个基于时间和内容的 ID
      task_id="async-$(date +%Y%m%d%H%M%S)-$(echo "$content" | md5 | cut -c1-8)"
    fi
    
    # 提取任务描述（取前50字符）
    local task_desc
    task_desc=$(echo "$content" | head -1 | cut -c1-50)
    
    # 调用 session-state.sh 添加待追踪任务
    "$SCRIPT_DIR/session-state.sh" add-pending "$task_id" "$task_desc" async 2>/dev/null || true
    
    # 类型改为 project 存储
    type="project"
    log_capture "检测到异步任务开始，已添加到待追踪列表: $task_id"
  fi
  
  # 生成记忆文件名
  local safe_content
  safe_content=$(echo "$content" | head -1 | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/_/g' | cut -c1-30)
  local filename="${timestamp//:/}_${safe_content}.md"
  local filepath="$MEMORY_DIR/$type/$filename"
  
  # 写入记忆文件
  mkdir -p "$MEMORY_DIR/$type"
  cat > "$filepath" << EOF
---
name: "$safe_content"
type: $type
source: auto-capture
created: $timestamp
tags: [auto, captured]
---

$(extract_key_info "$content" "$type")

## 原始内容
\`\`\`
$(echo "$content" | head -50)
\`\`\`

*由 auto-capture 自动捕获于 $timestamp*
EOF
  
  log_capture "已自动捕获记忆: $type/$filename"
  echo "$filepath"
}

#----------------------------------------------------------
# 交互式检查：分析最后 N 条消息是否值得捕获
#----------------------------------------------------------
check_recent() {
  local lines="${1:-100}"
  
  log_info "检查最近 $lines 行对话是否需要捕获..."
  
  # 这个函数用于 AI 在会话中主动调用
  # 检查当前上下文是否有值得记忆的内容
  return 0
}

#----------------------------------------------------------
# 启动时调用：加载最近的自动捕获记忆
#----------------------------------------------------------
load_recent() {
  local limit="${1:-5}"
  local type="${2:-}"
  
  local search_dir="$MEMORY_DIR"
  [[ -n "$type" ]] && search_dir="$MEMORY_DIR/$type"
  
  find "$search_dir" -name "*.md" -newer "$SKILL_DIR/SKILL.md" 2>/dev/null \
    | head -"$limit" \
    | while read -r f; do
        echo "=== $(basename "$f") ==="
        grep -A5 "^---$" "$f" | tail -6
        echo ""
      done
}

#----------------------------------------------------------
# 显示帮助
#----------------------------------------------------------
show_help() {
  cat << 'EOF'
auto-capture.sh - 自动记忆捕获工具

用法:
  auto-capture.sh <内容>           # 自动识别类型并捕获
  auto-capture.sh <内容> project    # 指定类型为 project
  auto-capture.sh <内容> feedback   # 指定类型为 feedback
  auto-capture.sh load [数量]       # 加载最近的自动记忆
  auto-capture.sh check             # 检查是否需要捕获
  auto-capture.sh -h                # 显示帮助

触发条件:
  ✅ 完成标志: "已完成"、"v1.0.0"、"发布"
  🔧 修正标志: "不对"、"错了"、"纠正"
  🐛 错误解决: "解决了"、"修好了"
  📋 决策标志: "决定用"、"选用"

示例:
  auto-capture.sh "多智能体协同 v2.0.0 已完成"
  auto-capture.sh "用户纠正了我对 Cost Tracker 的理解"
  auto-capture.sh load 10
EOF
}

#----------------------------------------------------------
# 入口
#----------------------------------------------------------
main() {
  # 支持 stdin 输入（心跳时管道传入）
  if [[ "${1:-}" == "--stdin" ]] || [[ -p /dev/stdin ]]; then
    local content
    content=$(cat -)
    if [[ -n "$content" ]]; then
      auto_capture "$content"
      return $?
    fi
  fi
  
  case "${1:-}" in
    load)
      load_recent "${2:-5}" "${3:-}"
      ;;
    check)
      check_recent "${2:-100}"
      ;;
    -h|--help|help)
      show_help
      ;;
    *)
      auto_capture "$@"
      ;;
  esac
}

main "$@"
