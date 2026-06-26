#!/bin/bash
#===============================================================================
# 火一五 MIT 48 小时学习法 - 核心脚本
# MIT 48-Hour Learning Method - Core Script
#
# 依赖：notebooklm-mcp-cli（~/.venv/notebooklm/bin/nlm）
# 流程：学什么 → 创建 notebook → 添加资料 → 三问框架 → 生成 audio/video
#
# v2.1.0 改进：
# - 新增自动续登录功能：登录失效前自动运行 nlm login
# - 支持 file:// URL 自动转真实路径
# - 修复 full 命令参数传递 bug
# - 音频生成增加等待确认
# - 改进重复 notebook 检测
# - 增强错误处理
#===============================================================================

set -euo pipefail

# 配置
NLM="${NLM:-${HOME}/.venv/notebooklm/bin/nlm}"
PROFILE="${NOTEBOOKLM_PROFILE:-default}"
LANG="${MIT_LEARN_LANG:-zh-CN}"

#-------------------------------------------------------------------------------
# 自动登录检测与续登录
#-------------------------------------------------------------------------------

# 检查 nlm 是否已登录，未登录或登录失效则自动重新登录
auto_login() {
  # 先用 list 命令测试登录状态（快速轻量）
  if ${NLM} notebook list --profile "${PROFILE}" >/dev/null 2>&1; then
    debug "登录状态正常"
    return 0
  fi

  warn "检测到登录已失效，正在重新登录..."
  ${NLM} login
  if ${NLM} notebook list --profile "${PROFILE}" >/dev/null 2>&1; then
    success "重新登录成功"
    return 0
  else
    error "重新登录失败，请检查账号权限"
    return 1
  fi
}

# 颜色输出
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC}   $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; }
debug()   { [ "${DEBUG:-0}" = "1" ] && echo -e "${CYAN}[DEBUG]${NC} $1" || true; }

#-------------------------------------------------------------------------------
# 辅助函数
#-------------------------------------------------------------------------------

# 转换 file:// URL 为真实路径
convert_file_url() {
  local input="$1"
  if [[ "$input" =~ ^file:// ]]; then
    # 移除 file:// 前缀并 URL 解码
    local path="${input#file://}"
    # URL 解码（%20 → 空格等）
    path=$(python3 -c "import urllib.parse; print(urllib.parse.unquote('${path}'))" 2>/dev/null || echo "${path}")
    echo "$path"
  else
    echo "$input"
  fi
}

# 等待 notebook 处理完成
wait_for_processing() {
  local notebook_id="$1"
  info "等待资料处理完成..."
  local max_wait=300
  local waited=0
  while true; do
    local status
    status=$(${NLM} notebook get "${notebook_id}" --profile "${PROFILE}" 2>/dev/null | \
      grep -i "status\|state\|progress" | head -3 || echo "unknown")
    if echo "${status}" | grep -qi "ready\|complete\|done\|success"; then
      success "资料处理完成"
      break
    fi
    if [ ${waited} -ge ${max_wait} ]; then
      warn "处理超时（${max_wait}s），继续下一步..."
      break
    fi
    echo -n "."
    sleep 10
    waited=$((waited + 10))
  done
  echo ""
}

# 等待音频生成完成
wait_for_audio() {
  local notebook_id="$1"
  local artifact_id="$2"
  info "等待音频生成完成..."
  local max_wait=300
  local waited=0
  while true; do
    local status
    status=$(${NLM} studio status "${notebook_id}" --profile "${PROFILE}" 2>/dev/null | \
      grep -i "${artifact_id}" | head -1 || echo "")
    if echo "${status}" | grep -qi "ready\|complete\|done\|success\|completed"; then
      success "音频生成完成"
      break
    fi
    if echo "${status}" | grep -qi "failed\|error\|timeout"; then
      error "音频生成失败"
      return 1
    fi
    if [ ${waited} -ge ${max_wait} ]; then
      warn "生成超时（${max_wait}s），请手动检查状态"
      break
    fi
    echo -n "."
    sleep 10
    waited=$((waited + 10))
  done
  echo ""
}

# 获取或创建 notebook ID（检测重复）
get_or_create_notebook() {
  local title="$1"
  local notebook_id=""

  # 先查找是否存在同名 notebook
  info "检查现有笔记本: ${title}"
  notebook_id=$(${NLM} notebook list --profile "${PROFILE}" 2>/dev/null | \
    grep -i "${title}" | grep -oE '([a-zA-Z0-9_-]+)' | tr -d '()' | head -1)

  if [ -n "${notebook_id}" ]; then
    success "找到现有笔记本: ${notebook_id}"
    echo "${notebook_id}"
    return 0
  fi

  # 创建新 notebook
  info "创建笔记本: ${title}"
  local create_output
  create_output=$(${NLM} notebook create "${title}" --profile "${PROFILE}" 2>&1)
  local exit_code=$?

  if [ ${exit_code} -ne 0 ]; then
    error "创建笔记本失败: ${create_output}"
    # 尝试再次查找
    sleep 2
    notebook_id=$(${NLM} notebook list --profile "${PROFILE}" 2>/dev/null | \
      grep -i "${title}" | grep -oE '([a-zA-Z0-9_-]+)' | tr -d '()' | head -1)
    if [ -n "${notebook_id}" ]; then
      success "找到刚创建的笔记本: ${notebook_id}"
      echo "${notebook_id}"
      return 0
    fi
    return 1
  fi

  # 从输出中提取 ID
  notebook_id=$(echo "${create_output}" | grep -oE '[a-zA-Z0-9]{20,}' | head -1)
  if [ -z "${notebook_id}" ]; then
    sleep 1
    notebook_id=$(${NLM} notebook list --profile "${PROFILE}" 2>/dev/null | \
      grep -i "${title}" | grep -oE '([a-zA-Z0-9_-]+)' | tr -d '()' | head -1)
  fi

  if [ -n "${notebook_id}" ]; then
    success "笔记本创建成功: ${notebook_id}"
    echo "${notebook_id}" > "${HOME}/.mit-learn-notebook-id"
    echo "NOTEBOOK_ID=${notebook_id}" >> "${HOME}/.mit-learn-env"
    echo "${notebook_id}"
  else
    error "无法获取 notebook ID"
    return 1
  fi
}

# 获取 notebook 列表
list_notebooks() {
  info "笔记本列表:"
  ${NLM} notebook list --profile "${PROFILE}" 2>/dev/null || error "获取笔记本列表失败"
}

#-------------------------------------------------------------------------------
# 命令：init - 创建 notebook
#-------------------------------------------------------------------------------
cmd_init() {
  local title="${1:-}"

  if [ -z "${title}" ]; then
    read -p "输入笔记本标题: " title
  fi

  if [ -z "${title}" ]; then
    error "标题不能为空"
    return 1
  fi

  local notebook_id
  notebook_id=$(get_or_create_notebook "${title}")
  if [ -n "${notebook_id}" ]; then
    echo "${notebook_id}" > "${HOME}/.mit-learn-notebook-id"
    echo "${notebook_id}"
  else
    return 1
  fi
}

#-------------------------------------------------------------------------------
# 命令：add - 添加资料
#-------------------------------------------------------------------------------
cmd_add() {
  local notebook_id
  local files=()
  local urls=()
  local yt_urls=()
  local title=""
  local wait_flag=false

  # 解析参数
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file|-f)
        files+=("$2"); shift 2 ;;
      --url|-u)
        urls+=("$2"); shift 2 ;;
      --youtube|-y)
        yt_urls+=("$2"); shift 2 ;;
      --title|-t)
        title="$2"; shift 2 ;;
      --wait|-w)
        wait_flag=true; shift ;;
      *)
        urls+=("$1"); shift ;;
    esac
  done

  # 获取 notebook_id
  notebook_id=$(cat "${HOME}/.mit-learn-notebook-id" 2>/dev/null || echo "")
  if [ -z "${notebook_id}" ]; then
    error "未找到 notebook ID，请先运行 mit-learn.sh init"
    return 1
  fi

  # 添加 URL（自动转换 file://）
  for url in "${urls[@]:-}"; do
    if [ -n "${url}" ]; then
      # 处理 file:// URL
      if [[ "${url}" =~ ^file:// ]]; then
        local real_path
        real_path=$(convert_file_url "${url}")
        if [ -f "${real_path}" ]; then
          info "添加文件: ${real_path}"
          local result
          result=$(${NLM} source add "${notebook_id}" \
            --file "${real_path}" \
            --title "${title:-$(basename "${real_path}")}" \
            --profile "${PROFILE}" 2>&1)
          if echo "${result}" | grep -qi "error\|failed"; then
            error "添加失败: ${result}"
          else
            success "已添加: $(basename "${real_path}")"
          fi
        else
          warn "文件不存在: ${real_path}"
        fi
      else
        info "添加 URL: ${url}"
        local result
        result=$(${NLM} source add "${notebook_id}" \
          --url "${url}" \
          --title "${title:-${url}}" \
          --profile "${PROFILE}" 2>&1)
        if echo "${result}" | grep -qi "error\|failed"; then
          error "添加失败: ${result}"
        else
          success "已添加: ${url}"
        fi
      fi
    fi
  done

  # 添加 YouTube
  for yt in "${yt_urls[@]:-}"; do
    if [ -n "${yt}" ]; then
      info "添加 YouTube: ${yt}"
      local result
      result=$(${NLM} source add "${notebook_id}" \
        --youtube "${yt}" \
        --title "${title:-YouTube}" \
        --profile "${PROFILE}" 2>&1)
      if echo "${result}" | grep -qi "error\|failed"; then
        error "添加失败: ${result}"
      else
        success "已添加: ${yt}"
      fi
    fi
  done

  # 添加文件
  for file in "${files[@]:-}"; do
    if [ -n "${file}" ]; then
      # 处理 file:// URL
      if [[ "${file}" =~ ^file:// ]]; then
        file=$(convert_file_url "${file}")
      fi
      if [ -f "${file}" ]; then
        info "添加文件: ${file}"
        local result
        result=$(${NLM} source add "${notebook_id}" \
          --file "${file}" \
          --title "${title:-$(basename "${file}")}" \
          --profile "${PROFILE}" 2>&1)
        if echo "${result}" | grep -qi "error\|failed"; then
          error "添加失败: ${result}"
        else
          success "已添加: $(basename "${file}")"
        fi
      else
        warn "文件不存在: ${file}"
      fi
    fi
  done

  if [ "${wait_flag}" = true ]; then
    wait_for_processing "${notebook_id}"
  fi
}

#-------------------------------------------------------------------------------
# 命令：ask - 三问框架
#-------------------------------------------------------------------------------

# 三问提示词（中文）
ASK_MENTAL_MODELS_PROMPT="你是一个领域专家。请基于提供的资料，回答以下问题：

**问题：列出该领域专家共享的 5 个基本心智模型/思维框架**

心智模型是指专家们在分析和解决问题时共同使用的核心思维框架。请：

1. 识别并列出 5 个该领域最基本、最重要的心智模型
2. 每个心智模型用一句话解释
3. 每个心智模型举一个具体应用例子

格式：
### 心智模型 1：[名称]
- 解释：
- 应用例子：

（以此类推）"

ASK_DISAGREEMENTS_PROMPT="你是一个领域专家。请基于提供的资料，回答以下问题：

**问题：在哪 3 个问题上，该领域专家根本不同意？**

专家分歧是指学者们在核心理论、方法或结论上存在根本性争议。请：

1. 识别并列出 3 个专家们存在根本分歧的核心问题
2. 每个分歧说明：各方的主要观点是什么？为什么会产生分歧？
3. 每个分歧解释：这对你的学习意味着什么？

格式：
### 分歧 1：[问题描述]
- 甲方观点：
- 乙方观点：
- 分歧根源：
- 对学习者的启示：

（以此类推）"

ASK_PROBING_PROMPT="你是一个苏格拉底式追问者。请基于提供的资料，生成能区分真懂和假背的 10 个暴露性问题。

**要求：**
- 问题必须能区分真正理解概念的人和只会背答案的人
- 问题应该是开放式的，不能通过简单回忆来回答
- 问题要有深度，需要真正的理解才能回答

请生成 10 个这样的问题：

格式：
1. [问题内容]
   预期假背者会：[他们可能的错误回答方向]
   真正懂的人会：[他们会如何正确回答]

（以此类推，编号 1-10）"

cmd_ask() {
  local question_type="${1:-}"
  local notebook_id

  notebook_id=$(cat "${HOME}/.mit-learn-notebook-id" 2>/dev/null || echo "")
  if [ -z "${notebook_id}" ]; then
    error "未找到 notebook ID，请先运行 mit-learn.sh init"
    return 1
  fi

  case "${question_type}" in
    mental-models|mental)
      info "=== 问心智模型 ==="
      info "请稍候，NotebookLM 正在分析..."
      ${NLM} notebook query "${notebook_id}" "${ASK_MENTAL_MODELS_PROMPT}" \
        --profile "${PROFILE}" 2>/dev/null
      ;;

    disagreements|disagree)
      info "=== 问专家分歧 ==="
      info "请稍候，NotebookLM 正在分析..."
      ${NLM} notebook query "${notebook_id}" "${ASK_DISAGREEMENTS_PROMPT}" \
        --profile "${PROFILE}" 2>/dev/null
      ;;

    probing|probing-questions)
      info "=== 问暴露性问题 ==="
      info "请稍候，NotebookLM 正在分析..."
      ${NLM} notebook query "${notebook_id}" "${ASK_PROBING_PROMPT}" \
        --profile "${PROFILE}" 2>/dev/null
      ;;

    all)
      cmd_ask "mental-models"
      echo ""
      cmd_ask "disagreements"
      echo ""
      cmd_ask "probing-questions"
      ;;

    *)
      cat <<EOF
请指定问题类型:
  mental-models   - 问心智模型（5个基本思维框架）
  disagreements   - 问专家分歧（3个根本性问题）
  probing         - 问暴露性问题（10个区分真懂假背的问题）
  all             - 完整三问（心智模型→专家分歧→暴露性问题）
EOF
      ;;
  esac
}

#-------------------------------------------------------------------------------
# 命令：audio - 生成音频概览
#-------------------------------------------------------------------------------
cmd_audio() {
  local notebook_id
  local format="${1:-deep_dive}"
  local wait_flag="${2:-yes}"

  notebook_id=$(cat "${HOME}/.mit-learn-notebook-id" 2>/dev/null || echo "")
  if [ -z "${notebook_id}" ]; then
    error "未找到 notebook ID，请先运行 mit-learn.sh init"
    return 1
  fi

  info "生成音频概览 (format: ${format})..."
  local result
  result=$(${NLM} audio create "${notebook_id}" \
    --format "${format}" \
    --language "${LANG}" \
    --profile "${PROFILE}" \
    --confirm 2>&1)
  echo "${result}"

  # 提取 artifact ID
  local artifact_id
  artifact_id=$(echo "${result}" | grep -oE '[a-f0-9-]{36}' | head -1)
  if [ -n "${artifact_id}" ] && [ "${wait_flag}" = "yes" ]; then
    wait_for_audio "${notebook_id}" "${artifact_id}"
    echo ""
    info "下载命令:"
    echo "  nlm download audio ${notebook_id} --id ${artifact_id} -o ~/Downloads/audio.m4a"
  elif [ -n "${artifact_id}" ]; then
    info "Artifact ID: ${artifact_id}"
  fi
}

#-------------------------------------------------------------------------------
# 命令：video - 生成视频概览
#-------------------------------------------------------------------------------
cmd_video() {
  local notebook_id
  local style="${1:-auto_select}"

  notebook_id=$(cat "${HOME}/.mit-learn-notebook-id" 2>/dev/null || echo "")
  if [ -z "${notebook_id}" ]; then
    error "未找到 notebook ID，请先运行 mit-learn.sh init"
    return 1
  fi

  info "生成视频概览 (style: ${style})..."
  ${NLM} video create "${notebook_id}" \
    --style "${style}" \
    --language "${LANG}" \
    --profile "${PROFILE}" \
    --confirm 2>&1
}

#-------------------------------------------------------------------------------
# 命令：status - 查看状态
#-------------------------------------------------------------------------------
cmd_status() {
  local notebook_id
  notebook_id=$(cat "${HOME}/.mit-learn-notebook-id" 2>/dev/null || echo "")

  if [ -z "${notebook_id}" ]; then
    info "当前没有活跃的 notebook"
    list_notebooks
    return
  fi

  info "Notebook ID: ${notebook_id}"
  echo ""
  ${NLM} notebook get "${notebook_id}" --profile "${PROFILE}" 2>/dev/null || \
    ${NLM} notebook describe "${notebook_id}" --profile "${PROFILE}" 2>&1

  echo ""
  info "资料源:"
  ${NLM} source list "${notebook_id}" --profile "${PROFILE}" 2>/dev/null || echo "无"
}

#-------------------------------------------------------------------------------
# 命令：full - 完整流程
#-------------------------------------------------------------------------------
cmd_full() {
  local title="${1:-}"
  local urls=()
  local files=()
  local yt_urls=()
  local skip_audio=false

  shift
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file|-f)
        files+=("$2"); shift 2 ;;
      --url|-u)
        urls+=("$2"); shift 2 ;;
      --youtube|-y)
        yt_urls+=("$2"); shift 2 ;;
      --skip-audio)
        skip_audio=true; shift ;;
      *)
        urls+=("$1"); shift ;;
    esac
  done

  if [ -z "${title}" ]; then
    read -p "输入学习主题: " title
  fi

  echo ""
  info "=== 火一五 MIT 48 小时学习法 ==="
  info "学习主题: ${title}"
  echo ""

  # Step 1: 创建 notebook
  echo ""
  info "[Step 1/4] 创建笔记本..."
  cmd_init "${title}"
  echo ""

  # Step 2: 添加资料
  if [ ${#urls[@]} -gt 0 ] || [ ${#files[@]} -gt 0 ] || [ ${#yt_urls[@]} -gt 0 ]; then
    echo ""
    info "[Step 2/4] 添加资料..."
    # 正确传递参数：每个数组用对应的 flag
    cmd_add \
      --url "${urls[@]:-}" \
      --youtube "${yt_urls[@]:-}" \
      --file "${files[@]:-}" \
      --wait
  else
    echo ""
    warn "[Step 2/4] 跳过（无资料）"
  fi

  # Step 3: 三问框架
  echo ""
  info "[Step 3/4] 三问框架..."
  echo ""

  info "--- 心智模型 ---"
  cmd_ask "mental-models"
  echo ""

  info "--- 专家分歧 ---"
  cmd_ask "disagreements"
  echo ""

  info "--- 暴露性问题 ---"
  cmd_ask "probing-questions"
  echo ""

  # Step 4: 生成 audio
  echo ""
  info "[Step 4/4] 生成音频概览..."
  if [ "${skip_audio}" = true ]; then
    warn "跳过音频生成（--skip-audio）"
    echo ""
    info "可稍后运行:"
    echo "  mit-learn.sh audio"
  else
    cmd_audio
  fi

  echo ""
  success "学习项目完成！"
}

#-------------------------------------------------------------------------------
# 主入口
#-------------------------------------------------------------------------------

# 所有命令执行前先检查并自动续登录
auto_login

COMMAND="${1:-}"

case "${COMMAND}" in
  init)      shift; cmd_init "$@" ;;
  add)       shift; cmd_add "$@" ;;
  ask)       shift; cmd_ask "$@" ;;
  audio)     shift; cmd_audio "$@" ;;
  video)     shift; cmd_video "$@" ;;
  full)      shift; cmd_full "$@" ;;
  status)    cmd_status ;;
  list)      list_notebooks ;;
  help|--help|-h) usage ;;
  *)
    if [ -n "${COMMAND}" ]; then
      error "未知命令: ${COMMAND}"
    fi
    usage
    ;;
esac
