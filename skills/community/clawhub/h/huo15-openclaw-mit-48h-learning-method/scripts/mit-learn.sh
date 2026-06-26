#!/bin/bash
#===============================================================================
# 火一五 MIT 48 小时学习法 - 核心脚本 (v3.0.0)
# MIT 48-Hour Learning Method - Core Script
#
# 精髓来源：Ihtesham Ali 原始推文（X @ihtesham2005，3M+ views）
# 原始三问（精确措辞）：
#   Q1: "What are the 5 core mental models that every expert in this field shares?"
#   Q2: "Show me the 3 places where experts in this field fundamentally disagree,
#        and what each side's strongest argument is."
#   Q3: "Generate 10 questions that would expose whether someone deeply
#        understands this subject versus someone who just memorized facts."
# 反馈循环：错误回答时 →
#   "Explain why this is wrong and what I'm missing."
#
# 三大学习科学原理：
#   - Active Recall（主动回忆）
#   - Desirable Difficulty（必要难度）
#   - Conceptual Frameworks First（先框架后细节）
#
# 完整 48h 时间线：
#   Phase 1 (0-1h)  : context stacking → 三问 → 智识地图
#   Phase 2 (1-7h)  : 用 6 小时主动回忆回答 probing questions + 反馈循环
#   Phase 3 (7-48h) : synthesis + practice exam + audio/video 巩固
#
# 依赖：notebooklm-mcp-cli（~/.venv/notebooklm/bin/nlm）
#===============================================================================

set -euo pipefail

# 配置
NLM="${NLM:-${HOME}/.venv/notebooklm/bin/nlm}"
PROFILE="${NOTEBOOKLM_PROFILE:-default}"
LEARN_LANG="${MIT_LEARN_LANG:-zh-CN}"
KB_DIR="${MIT_LEARN_KB_DIR:-${HOME}/knowledge/huo15/learning}"
NOTEBOOK_ID_FILE="${HOME}/.mit-learn-notebook-id"
ENV_FILE="${HOME}/.mit-learn-env"

# 颜色输出
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; MAGENTA='\033[0;35m'; NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC}   $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; }
phase()   { echo -e "${MAGENTA}[PHASE]${NC} $1"; }
debug()   { [ "${DEBUG:-0}" = "1" ] && echo -e "${CYAN}[DEBUG]${NC} $1" || true; }

# 命令是否需要登录（list/help 等本地命令不需要）
NETWORK_COMMANDS=("init" "add" "ask" "audio" "video" "full" "marathon" "status" "list" \
                  "synthesize" "contradictions" "gaps" "feynman" "weakness" "exam" \
                  "flashcards" "quiz" "mindmap" "chat-config" "download" "export")

needs_network() {
  local cmd="$1"
  local n
  for n in "${NETWORK_COMMANDS[@]}"; do
    [ "${cmd}" = "${n}" ] && return 0
  done
  return 1
}

#-------------------------------------------------------------------------------
# 自动登录检测与续登录
#-------------------------------------------------------------------------------
auto_login() {
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

#-------------------------------------------------------------------------------
# 辅助函数
#-------------------------------------------------------------------------------

convert_file_url() {
  local input="$1"
  if [[ "$input" =~ ^file:// ]]; then
    local path="${input#file://}"
    path=$(python3 -c "import urllib.parse; print(urllib.parse.unquote('${path}'))" 2>/dev/null || echo "${path}")
    echo "$path"
  else
    echo "$input"
  fi
}

get_notebook_id() {
  local nid
  nid=$(cat "${NOTEBOOK_ID_FILE}" 2>/dev/null || echo "")
  if [ -z "${nid}" ]; then
    error "未找到 notebook ID，请先运行 mit-learn.sh init <主题>"
    return 1
  fi
  echo "${nid}"
}

get_topic() {
  grep -E '^TOPIC=' "${ENV_FILE}" 2>/dev/null | tail -1 | cut -d= -f2- || echo "unknown"
}

# 等待资料处理
wait_for_processing() {
  local notebook_id="$1"
  info "等待资料处理完成..."
  local max_wait=300 waited=0 status
  while true; do
    status=$(${NLM} notebook get "${notebook_id}" --profile "${PROFILE}" 2>/dev/null | \
      grep -i "status\|state\|progress" | head -3 || echo "unknown")
    if echo "${status}" | grep -qi "ready\|complete\|done\|success"; then
      success "资料处理完成"; break
    fi
    [ ${waited} -ge ${max_wait} ] && { warn "处理超时（${max_wait}s）"; break; }
    echo -n "."; sleep 10; waited=$((waited + 10))
  done
  echo ""
}

# 等待音频生成
wait_for_audio() {
  local notebook_id="$1" artifact_id="$2"
  info "等待音频生成完成..."
  local max_wait=300 waited=0 status
  while true; do
    status=$(${NLM} studio status "${notebook_id}" --profile "${PROFILE}" 2>/dev/null | \
      grep -i "${artifact_id}" | head -1 || echo "")
    if echo "${status}" | grep -qi "ready\|complete\|done\|success\|completed"; then
      success "音频生成完成"; break
    fi
    if echo "${status}" | grep -qi "failed\|error\|timeout"; then
      error "音频生成失败"; return 1
    fi
    [ ${waited} -ge ${max_wait} ] && { warn "生成超时（${max_wait}s），请手动检查"; break; }
    echo -n "."; sleep 10; waited=$((waited + 10))
  done
  echo ""
}

get_or_create_notebook() {
  local title="$1" notebook_id=""
  info "检查现有笔记本: ${title}"
  notebook_id=$(${NLM} notebook list --profile "${PROFILE}" 2>/dev/null | \
    grep -i "${title}" | grep -oE '([a-zA-Z0-9_-]+)' | tr -d '()' | head -1)
  if [ -n "${notebook_id}" ]; then
    success "找到现有笔记本: ${notebook_id}"
    echo "${notebook_id}"; return 0
  fi
  info "创建笔记本: ${title}"
  local create_output
  create_output=$(${NLM} notebook create "${title}" --profile "${PROFILE}" 2>&1) || {
    error "创建失败: ${create_output}"
    sleep 2
    notebook_id=$(${NLM} notebook list --profile "${PROFILE}" 2>/dev/null | \
      grep -i "${title}" | grep -oE '([a-zA-Z0-9_-]+)' | tr -d '()' | head -1)
    [ -n "${notebook_id}" ] && { echo "${notebook_id}"; return 0; }
    return 1
  }
  notebook_id=$(echo "${create_output}" | grep -oE '[a-zA-Z0-9]{20,}' | head -1)
  if [ -z "${notebook_id}" ]; then
    sleep 1
    notebook_id=$(${NLM} notebook list --profile "${PROFILE}" 2>/dev/null | \
      grep -i "${title}" | grep -oE '([a-zA-Z0-9_-]+)' | tr -d '()' | head -1)
  fi
  if [ -n "${notebook_id}" ]; then
    success "笔记本创建成功: ${notebook_id}"
    echo "${notebook_id}" > "${NOTEBOOK_ID_FILE}"
    {
      echo "NOTEBOOK_ID=${notebook_id}"
      echo "TOPIC=${title}"
      echo "CREATED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    } > "${ENV_FILE}"
    echo "${notebook_id}"
  else
    error "无法获取 notebook ID"; return 1
  fi
}

list_notebooks() {
  info "笔记本列表:"
  ${NLM} notebook list --profile "${PROFILE}" 2>/dev/null || error "获取笔记本列表失败"
}

# 通用 query 包装器：可选保存输出到知识库
run_query() {
  local notebook_id="$1" prompt="$2" save_name="${3:-}"
  local output_file=""
  if [ -n "${save_name}" ]; then
    local topic kb_topic_dir
    topic=$(get_topic)
    kb_topic_dir="${KB_DIR}/${topic}"
    mkdir -p "${kb_topic_dir}"
    output_file="${kb_topic_dir}/$(date +%Y-%m-%d)-${save_name}.md"
  fi
  info "请稍候，NotebookLM 正在分析..."
  local result
  result=$(${NLM} notebook query "${notebook_id}" "${prompt}" --profile "${PROFILE}" 2>/dev/null)
  echo "${result}"
  if [ -n "${output_file}" ]; then
    {
      echo "# ${save_name}"
      echo ""
      echo "- Notebook: ${notebook_id}"
      echo "- Topic: $(get_topic)"
      echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
      echo ""
      echo "## Prompt"
      echo ""
      echo '```'
      echo "${prompt}"
      echo '```'
      echo ""
      echo "## Response"
      echo ""
      echo "${result}"
    } > "${output_file}"
    success "已保存到: ${output_file}"
  fi
}

#-------------------------------------------------------------------------------
# 三问 prompts（基于 Ihtesham Ali 原始措辞 + 中文化）
#-------------------------------------------------------------------------------

# 中文版本（默认使用）
ASK_MENTAL_MODELS_PROMPT_ZH="你是一个领域专家。请基于提供的所有资料，回答这个核心问题：

**该领域每位专家都共享的 5 个核心心智模型（mental models）是什么？**

要求：
1. 不要泛泛而谈，必须是该领域专家在思考问题时实际使用的思维框架
2. 每个心智模型用一句话精确解释其本质
3. 每个心智模型给出一个能展示该框架威力的具体应用例子
4. 优先选择能跨越多个子领域、被反复使用的根本性框架

输出格式：
### 心智模型 1：[名称]
- **本质**：（一句话）
- **应用例子**：（具体场景）
- **为什么它是核心**：（为什么专家离不开它）

（依次列出 5 个）

最后总结：这 5 个心智模型如何相互嵌套，构成该领域专家的'思维操作系统'？"

ASK_DISAGREEMENTS_PROMPT_ZH="你是一个领域思想史专家。请基于提供的所有资料，回答这个核心问题：

**该领域专家在哪 3 个根本问题上彻底不同意？请给出每一方最强的论证。**

要求：
1. 必须是根本性分歧（涉及理论基础、方法论或终极目标），而非细枝末节
2. 每一方的论证必须是其立场上最强的版本（steelman），而非稻草人
3. 解释分歧的根源（不同的本体论假设？不同的价值观？不同的证据偏好？）
4. 说明为什么这些分歧至今未解决

输出格式：
### 分歧 1：[问题描述]
- **甲方立场**：
- **甲方最强论证**：
- **乙方立场**：
- **乙方最强论证**：
- **分歧根源**：（本体论 / 方法论 / 价值观 / 证据偏好）
- **对学习者的启示**：理解这个分歧后，你应该如何不被任何一派洗脑？

（依次列出 3 个）"

ASK_PROBING_PROMPT_ZH="你是苏格拉底式追问者。请基于提供的所有资料，生成 10 个能彻底区分'真懂'和'假背'的暴露性问题。

**判定标准：**
- 假背者：能复述定义、能列出步骤，但无法解释 why、无法迁移、无法应对反例
- 真懂者：能解释 why、能从第一性原理推导、能举出非平凡的反例、能识别问题的边界

**要求：**
1. 问题必须是开放式，无法靠记忆模板回答
2. 至少 3 个问题涉及'反直觉'情境
3. 至少 2 个问题要求识别问题的隐含假设
4. 至少 2 个问题要求跨领域迁移
5. 至少 1 个问题要求识别教科书的简化或谎言

输出格式：
**问题 1：** [问题内容]
- 假背者会怎么错：（典型错误回答）
- 真懂者会怎么答：（真懂的关键点 + why）
- 这个问题暴露的能力维度：（理解 / 推理 / 迁移 / 边界识别）

（依次列出 10 个，不要省略）"

ASK_FOLLOWUP_PROMPT_ZH="我刚才回答了一个 probing question。请基于提供的资料，做以下事情：

1. **诊断我的回答**：我说了什么？这个回答的核心思路是什么？
2. **指出错误或缺失**：我哪里错了？我遗漏了什么关键点？为什么我会这样错（认知盲点是什么）？
3. **给出真懂者的回答**：从第一性原理出发，真懂的人会如何思考这个问题？
4. **生成一个'追击问题'**：基于我刚才暴露的盲点，给我一个更深的问题，迫使我面对这个盲点。

我的回答如下：
---
{ANSWER}
---"

# 进阶 prompts（来自 Ihtesham 全集 + 网上最佳实践）

ASK_SYNTHESIZE_PROMPT_ZH="基于提供的所有资料，把所有最重要的洞见综合为一个统一的思维框架——任何人都能用它来思考这个领域。

要求：
1. 不要罗列要点，要构建一个有内部逻辑的框架
2. 框架应包含：核心概念（最多 5 个）、核心概念之间的关系、应用流程、边界条件
3. 用一句话概括这个框架的灵魂
4. 给出 3 个用这个框架成功分析问题的例子
5. 给出 1 个这个框架失效的边界例子

输出结构：
## 框架名称
## 一句话灵魂
## 核心概念（最多 5 个）
## 概念关系图（用文字描述）
## 应用流程（步骤化）
## 成功例子 ×3
## 失效边界 ×1
## 与领域内其他框架的关系"

ASK_CONTRADICTIONS_PROMPT_ZH="比较提供的所有资料，找出资料之间所有的矛盾和分歧。

对每个矛盾，给出：
1. **矛盾内容**：哪两条资料怎么说？（精确引用）
2. **矛盾性质**：是事实分歧、定义分歧、方法分歧、还是价值分歧？
3. **可能解释**：为什么会出现这个矛盾？（不同语境？不同时代？不同假设？）
4. **谁更可信**：基于资料的权威性、新近度、证据支持，倾向于哪一方？
5. **对学习者的指导**：你应该怎么记忆这个矛盾点？

如果资料没有明显矛盾，请找出'隐含矛盾'——表面一致但深层假设不同的地方。"

ASK_GAPS_PROMPT_ZH="基于提供的所有资料，对照该领域的当前业界标准（最新 12 个月），识别这些资料中**没有覆盖**的关键内容。

要求：
1. 不是列出资料里有什么，而是找出**资料里没有但应该有**的内容
2. 按重要性排序：
   - **致命缺口**：不知道这些会做出错误决策
   - **重要缺口**：不知道这些会被该领域专家立刻识破
   - **次要缺口**：知道更好但不知道也不致命
3. 每个缺口给出补充建议（具体到资料类型、关键词、推荐来源）

输出格式：
### 致命缺口（按严重度排序）
- 缺口 1：[内容] / 为什么致命 / 如何补
- 缺口 2：...

### 重要缺口
...

### 次要缺口
..."

ASK_FEYNMAN_PROMPT_ZH="我们要做 Feynman 学习法的角色反转。

**新角色分配：**
- 你是学生（一个聪明但完全不懂这个领域的 12 岁孩子）
- 我是老师

我会向你解释一个概念。你的任务：
1. 用一个 12 岁孩子的语言反问我：'你说的 X 是什么意思？'
2. 找出我解释中的术语、跳跃和模糊之处
3. 用'但是这样的话...'追问我的逻辑漏洞
4. 当我使用专业术语时，问'能不能用我能听懂的话说？'

请基于提供的资料知识，扮演这个聪明的 12 岁学生，准备好挑战我。
我现在要解释的概念是：**{CONCEPT}**

我的解释：
---
{EXPLANATION}
---"

ASK_WEAKNESS_PROMPT_ZH="基于提供的所有资料，假设我是一个'刚学完这个领域'的学习者。请预测我最可能存在的 5 个知识弱点和盲区。

每个弱点给出：
1. **弱点内容**：我大概率不懂或会搞错的具体知识点
2. **诊断证据**：为什么大多数学习者会卡在这里？（认知偏差 / 教学惯性 / 概念隐蔽）
3. **暴露这个弱点的测试题**：一个能立刻看出我懂没懂的问题
4. **针对性补救**：具体到哪本书/哪段视频/哪个练习
5. **优先级**：（高/中/低）—— 不补会不会影响其他知识的吸收？

按优先级倒序输出。"

ASK_EXAM_PROMPT_ZH="基于提供的所有资料，给我生成一份模拟期末考试。

要求：
- **总题数**：15 题
- **题型分布**：5 道选择题 + 5 道简答题 + 3 道分析题 + 2 道开放论述题
- **难度分布**：3 道送分题 + 7 道中等题 + 5 道难题
- **考点覆盖**：覆盖资料中所有核心心智模型 + 至少 1 个专家分歧 + 至少 2 个跨章节综合
- **格式**：每道题独立编号，给出题目、参考答案、评分要点

最后给出：
- **预计完成时间**：90 分钟
- **及格标准**：60% / 优秀标准：85%
- **如果你做完后觉得 X 题最难**，说明你需要重点复习哪部分"

#-------------------------------------------------------------------------------
# 命令实现
#-------------------------------------------------------------------------------

cmd_init() {
  local title="${1:-}"
  if [ -z "${title}" ]; then
    read -r -p "输入笔记本标题: " title
  fi
  [ -z "${title}" ] && { error "标题不能为空"; return 1; }
  local notebook_id
  notebook_id=$(get_or_create_notebook "${title}")
  if [ -n "${notebook_id}" ]; then
    echo "${notebook_id}" > "${NOTEBOOK_ID_FILE}"
    echo "${notebook_id}"
  else
    return 1
  fi
}

cmd_add() {
  local notebook_id files=() urls=() yt_urls=() title="" wait_flag=false
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file|-f)    files+=("$2"); shift 2 ;;
      --url|-u)     urls+=("$2"); shift 2 ;;
      --youtube|-y) yt_urls+=("$2"); shift 2 ;;
      --title|-t)   title="$2"; shift 2 ;;
      --wait|-w)    wait_flag=true; shift ;;
      *)            urls+=("$1"); shift ;;
    esac
  done
  notebook_id=$(get_notebook_id) || return 1

  for url in "${urls[@]+"${urls[@]}"}"; do
    [ -z "${url}" ] && continue
    if [[ "${url}" =~ ^file:// ]]; then
      local real_path; real_path=$(convert_file_url "${url}")
      if [ -f "${real_path}" ]; then
        info "添加文件: ${real_path}"
        local result
        result=$(${NLM} source add "${notebook_id}" --file "${real_path}" \
          --title "${title:-$(basename "${real_path}")}" --profile "${PROFILE}" 2>&1)
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
      result=$(${NLM} source add "${notebook_id}" --url "${url}" \
        --title "${title:-${url}}" --profile "${PROFILE}" 2>&1)
      if echo "${result}" | grep -qi "error\|failed"; then
        error "添加失败: ${result}"
      else
        success "已添加: ${url}"
      fi
    fi
  done

  for yt in "${yt_urls[@]+"${yt_urls[@]}"}"; do
    [ -z "${yt}" ] && continue
    info "添加 YouTube: ${yt}"
    local result
    result=$(${NLM} source add "${notebook_id}" --youtube "${yt}" \
      --title "${title:-YouTube}" --profile "${PROFILE}" 2>&1)
    if echo "${result}" | grep -qi "error\|failed"; then
      error "添加失败: ${result}"
    else
      success "已添加: ${yt}"
    fi
  done

  for file in "${files[@]+"${files[@]}"}"; do
    [ -z "${file}" ] && continue
    [[ "${file}" =~ ^file:// ]] && file=$(convert_file_url "${file}")
    if [ -f "${file}" ]; then
      info "添加文件: ${file}"
      local result
      result=$(${NLM} source add "${notebook_id}" --file "${file}" \
        --title "${title:-$(basename "${file}")}" --profile "${PROFILE}" 2>&1)
      if echo "${result}" | grep -qi "error\|failed"; then
        error "添加失败: ${result}"
      else
        success "已添加: $(basename "${file}")"
      fi
    else
      warn "文件不存在: ${file}"
    fi
  done

  [ "${wait_flag}" = true ] && wait_for_processing "${notebook_id}"
}

cmd_ask() {
  local question_type="${1:-}"
  local notebook_id; notebook_id=$(get_notebook_id) || return 1

  case "${question_type}" in
    mental-models|mental|q1)
      info "=== Q1: 问心智模型（Mental Models）==="
      run_query "${notebook_id}" "${ASK_MENTAL_MODELS_PROMPT_ZH}" "q1-mental-models"
      ;;
    disagreements|disagree|q2)
      info "=== Q2: 问专家分歧（Expert Disagreements）==="
      run_query "${notebook_id}" "${ASK_DISAGREEMENTS_PROMPT_ZH}" "q2-disagreements"
      ;;
    probing|probing-questions|q3)
      info "=== Q3: 问暴露性问题（Probing Questions）==="
      run_query "${notebook_id}" "${ASK_PROBING_PROMPT_ZH}" "q3-probing-questions"
      ;;
    followup)
      shift
      local answer="${*:-}"
      [ -z "${answer}" ] && { error "用法: ask followup <你的回答>"; return 1; }
      info "=== Feedback Loop: 诊断你的回答 ==="
      local prompt="${ASK_FOLLOWUP_PROMPT_ZH//\{ANSWER\}/${answer}}"
      run_query "${notebook_id}" "${prompt}" "followup-$(date +%H%M%S)"
      ;;
    all)
      cmd_ask "mental-models"; echo ""
      cmd_ask "disagreements"; echo ""
      cmd_ask "probing-questions"
      ;;
    *)
      cat <<EOF
请指定问题类型:
  mental-models (q1)  - 问心智模型（5 个核心思维框架）
  disagreements (q2)  - 问专家分歧（3 个根本不同意的问题）
  probing       (q3)  - 问暴露性问题（10 个区分真懂假背的问题）
  followup <answer>   - 反馈循环：诊断你的回答 + 追击问题
  all                 - 完整三问（q1 → q2 → q3）
EOF
      ;;
  esac
}

cmd_synthesize() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "=== Synthesis: 把所有资料综合为一个统一框架 ==="
  run_query "${notebook_id}" "${ASK_SYNTHESIZE_PROMPT_ZH}" "synthesis"
}

cmd_contradictions() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "=== Contradictions: 找出资料之间的矛盾 ==="
  run_query "${notebook_id}" "${ASK_CONTRADICTIONS_PROMPT_ZH}" "contradictions"
}

cmd_gaps() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "=== Gaps: 识别资料中的知识缺口 ==="
  run_query "${notebook_id}" "${ASK_GAPS_PROMPT_ZH}" "gaps"
}

cmd_feynman() {
  local concept="${1:-}" explanation="${2:-}"
  if [ -z "${concept}" ] || [ -z "${explanation}" ]; then
    error "用法: feynman <概念名> <你的解释>"
    return 1
  fi
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "=== Feynman Teach-Back: 角色反转 ==="
  local prompt="${ASK_FEYNMAN_PROMPT_ZH//\{CONCEPT\}/${concept}}"
  prompt="${prompt//\{EXPLANATION\}/${explanation}}"
  run_query "${notebook_id}" "${prompt}" "feynman-${concept// /-}"
}

cmd_weakness() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "=== Weakness Analysis: 预测学习者的知识盲区 ==="
  run_query "${notebook_id}" "${ASK_WEAKNESS_PROMPT_ZH}" "weakness-analysis"
}

cmd_exam() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "=== Practice Exam: 生成模拟期末考试 ==="
  run_query "${notebook_id}" "${ASK_EXAM_PROMPT_ZH}" "practice-exam"
}

cmd_audio() {
  local format="${1:-deep_dive}" wait_flag="${2:-yes}"
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "生成音频概览 (format: ${format}, language: ${LEARN_LANG})..."
  local result
  result=$(${NLM} audio create "${notebook_id}" \
    --format "${format}" --language "${LEARN_LANG}" \
    --profile "${PROFILE}" --confirm 2>&1)
  echo "${result}"
  local artifact_id
  artifact_id=$(echo "${result}" | grep -oE '[a-f0-9-]{36}' | head -1)
  if [ -n "${artifact_id}" ] && [ "${wait_flag}" = "yes" ]; then
    wait_for_audio "${notebook_id}" "${artifact_id}"
    echo ""
    info "下载: mit-learn.sh download audio --id ${artifact_id}"
  elif [ -n "${artifact_id}" ]; then
    info "Artifact ID: ${artifact_id}"
  fi
}

cmd_video() {
  local style="${1:-auto_select}" format="${2:-explainer}"
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "生成视频概览 (style: ${style}, format: ${format})..."
  ${NLM} video create "${notebook_id}" \
    --style "${style}" --format "${format}" --language "${LEARN_LANG}" \
    --profile "${PROFILE}" --confirm 2>&1
}

cmd_flashcards() {
  local difficulty="${1:-medium}" focus="${2:-}"
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "生成抽认卡 (difficulty: ${difficulty})..."
  if [ -n "${focus}" ]; then
    ${NLM} flashcards create "${notebook_id}" \
      --difficulty "${difficulty}" --focus "${focus}" \
      --profile "${PROFILE}" --confirm 2>&1
  else
    ${NLM} flashcards create "${notebook_id}" \
      --difficulty "${difficulty}" \
      --profile "${PROFILE}" --confirm 2>&1
  fi
}

cmd_quiz() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "生成测验..."
  ${NLM} quiz create "${notebook_id}" --profile "${PROFILE}" --confirm 2>&1
}

cmd_mindmap() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "生成思维导图..."
  ${NLM} mindmap create "${notebook_id}" --profile "${PROFILE}" --confirm 2>&1
}

cmd_chat_config() {
  local goal="${1:-learning_guide}"
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  info "配置 chat goal 为: ${goal}"
  if [ "${goal}" = "custom" ]; then
    local custom_prompt="${2:-你是一个苏格拉底式追问者。永远不要直接给答案，而是用问题引导我自己想出答案。当我答错时，问\"你为什么这么想？\"当我答对时，问\"还有别的可能吗？\"}"
    ${NLM} chat configure "${notebook_id}" --goal custom \
      --prompt "${custom_prompt}" --profile "${PROFILE}" 2>&1
  else
    ${NLM} chat configure "${notebook_id}" --goal "${goal}" --profile "${PROFILE}" 2>&1
  fi
}

cmd_download() {
  local kind="${1:-}"
  shift || true
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  case "${kind}" in
    audio|video|slide-deck|infographic|report|mind-map|data-table|quiz|flashcards)
      info "下载 ${kind}..."
      ${NLM} download "${kind}" "${notebook_id}" "$@" --profile "${PROFILE}" 2>&1
      ;;
    *)
      cat <<EOF
用法: download <类型> [--id <artifact_id>] [-o <output_path>]
类型: audio | video | slide-deck | infographic | report | mind-map | data-table | quiz | flashcards
EOF
      ;;
  esac
}

cmd_export() {
  local notebook_id; notebook_id=$(get_notebook_id) || return 1
  local topic; topic=$(get_topic)
  local kb_topic_dir="${KB_DIR}/${topic}"
  mkdir -p "${kb_topic_dir}"
  local index="${kb_topic_dir}/INDEX.md"
  info "导出学习成果到 ${kb_topic_dir}/"
  {
    echo "# ${topic} - MIT 48h 学习档案"
    echo ""
    echo "- Notebook ID: ${notebook_id}"
    echo "- Created: $(grep CREATED_AT "${ENV_FILE}" 2>/dev/null | cut -d= -f2-)"
    echo "- Exported: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo ""
    echo "## 资料源"
    echo ""
    ${NLM} source list "${notebook_id}" --profile "${PROFILE}" 2>/dev/null || echo "（无法获取）"
    echo ""
    echo "## 已生成的产物"
    echo ""
    ls -1 "${kb_topic_dir}/" | grep -v INDEX.md | sed 's/^/- /'
  } > "${index}"
  success "导出完成: ${index}"
}

cmd_status() {
  local notebook_id; notebook_id=$(cat "${NOTEBOOK_ID_FILE}" 2>/dev/null || echo "")
  if [ -z "${notebook_id}" ]; then
    info "当前没有活跃的 notebook"
    list_notebooks; return
  fi
  info "Notebook ID: ${notebook_id}"
  info "Topic: $(get_topic)"
  echo ""
  ${NLM} notebook get "${notebook_id}" --profile "${PROFILE}" 2>/dev/null || \
    ${NLM} notebook describe "${notebook_id}" --profile "${PROFILE}" 2>&1
  echo ""
  info "资料源:"
  ${NLM} source list "${notebook_id}" --profile "${PROFILE}" 2>/dev/null || echo "无"
}

#-------------------------------------------------------------------------------
# full：原快捷流程（保持向后兼容）
#-------------------------------------------------------------------------------
cmd_full() {
  local title="${1:-}" urls=() files=() yt_urls=() skip_audio=false
  shift || true
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file|-f)    files+=("$2"); shift 2 ;;
      --url|-u)     urls+=("$2"); shift 2 ;;
      --youtube|-y) yt_urls+=("$2"); shift 2 ;;
      --skip-audio) skip_audio=true; shift ;;
      *)            urls+=("$1"); shift ;;
    esac
  done
  [ -z "${title}" ] && read -r -p "输入学习主题: " title

  echo ""
  info "=== 火一五 MIT 48 小时学习法（快捷流程）==="
  info "主题: ${title}"
  echo ""

  info "[Step 1/4] 创建笔记本..."
  cmd_init "${title}"; echo ""

  if [ ${#urls[@]} -gt 0 ] || [ ${#files[@]} -gt 0 ] || [ ${#yt_urls[@]} -gt 0 ]; then
    info "[Step 2/4] 添加资料..."
    local args=()
    for u in "${urls[@]+"${urls[@]}"}"; do args+=(--url "${u}"); done
    for f in "${files[@]+"${files[@]}"}"; do args+=(--file "${f}"); done
    for y in "${yt_urls[@]+"${yt_urls[@]}"}"; do args+=(--youtube "${y}"); done
    args+=(--wait)
    cmd_add "${args[@]}"
  else
    warn "[Step 2/4] 跳过（无资料）"
  fi
  echo ""

  info "[Step 3/4] 三问框架..."
  cmd_ask "mental-models"; echo ""
  cmd_ask "disagreements"; echo ""
  cmd_ask "probing-questions"; echo ""

  info "[Step 4/4] 生成音频概览..."
  if [ "${skip_audio}" = true ]; then
    warn "跳过音频生成（--skip-audio）"
  else
    cmd_audio
  fi

  echo ""
  success "快捷流程完成！"
  info "建议接下来: mit-learn.sh export  # 导出到本地知识库"
}

#-------------------------------------------------------------------------------
# marathon：完整 48h 三阶段时间线
#-------------------------------------------------------------------------------
cmd_marathon() {
  local title="${1:-}" urls=() files=() yt_urls=()
  shift || true
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file|-f)    files+=("$2"); shift 2 ;;
      --url|-u)     urls+=("$2"); shift 2 ;;
      --youtube|-y) yt_urls+=("$2"); shift 2 ;;
      *)            urls+=("$1"); shift ;;
    esac
  done
  [ -z "${title}" ] && read -r -p "输入学习主题: " title

  echo ""
  phase "═══ 火一五 MIT 48 小时学习马拉松 ═══"
  phase "主题: ${title}"
  phase "完整三阶段时间线"
  echo ""

  # ========== Phase 1: 0-1h ==========
  phase "─── Phase 1 (0-1h): Context Stacking + 智识地图 ───"
  info "原理: Conceptual Frameworks First（先框架后细节）"
  echo ""
  cmd_init "${title}"

  if [ ${#urls[@]} -gt 0 ] || [ ${#files[@]} -gt 0 ] || [ ${#yt_urls[@]} -gt 0 ]; then
    local args=()
    for u in "${urls[@]+"${urls[@]}"}"; do args+=(--url "${u}"); done
    for f in "${files[@]+"${files[@]}"}"; do args+=(--file "${f}"); done
    for y in "${yt_urls[@]+"${yt_urls[@]}"}"; do args+=(--youtube "${y}"); done
    args+=(--wait)
    cmd_add "${args[@]}"
  else
    warn "未提供资料 - Ihtesham 原方案：6 教科书 + 15 论文 + 全部 lecture transcript"
    warn "请通过 --url / --file / --youtube 添加，或先单独运行 add 命令"
  fi
  echo ""
  cmd_ask "mental-models"; echo ""
  cmd_ask "disagreements"; echo ""
  cmd_ask "probing-questions"; echo ""

  # ========== Phase 2: 1-7h ==========
  phase "─── Phase 2 (1-7h): 主动回忆 + 反馈循环 ───"
  info "原理: Active Recall + Desirable Difficulty"
  info "做法：用 6 小时回答上面 10 个 probing questions"
  info "每答错一题，立即用: mit-learn.sh ask followup '<你的回答>'"
  info "（这一阶段需要你自己执行，脚本不能替你回答）"
  echo ""

  # ========== Phase 3: 7-48h ==========
  phase "─── Phase 3 (7-48h): 综合 + 模拟考 + 巩固 ───"
  info "原理: 综合 → 测试 → 多模态强化"
  echo ""
  cmd_synthesize; echo ""
  cmd_weakness; echo ""
  cmd_exam; echo ""

  info "生成多模态学习产物..."
  cmd_audio "deep_dive" "no"; echo ""
  cmd_mindmap || true; echo ""
  cmd_flashcards "medium" || true; echo ""

  echo ""
  cmd_export
  echo ""
  phase "═══ 48h 马拉松准备完成 ═══"
  success "下一步：用 6 小时认真回答 probing questions，每错必 ask followup"
}

#-------------------------------------------------------------------------------
# usage
#-------------------------------------------------------------------------------
usage() {
  cat <<EOF
火一五 MIT 48 小时学习法 v3.0.0
基于 Ihtesham Ali 原始三问框架 + 完整 48h 时间线

用法: mit-learn.sh <command> [args]

═══ 笔记本管理 ═══
  init <title>         创建/复用同名笔记本
  add [opts]           添加资料: --url / --file / --youtube / --wait
  status               当前 notebook 状态
  list                 列出所有 notebooks

═══ 三问框架（核心精髓）═══
  ask mental-models    Q1: 5 个核心心智模型
  ask disagreements    Q2: 3 个专家根本分歧
  ask probing          Q3: 10 个暴露性问题
  ask followup <答案>  反馈循环：诊断你的回答 + 追击问题
  ask all              完整三问

═══ 进阶分析（Ihtesham 全集）═══
  synthesize           综合所有资料为一个统一框架
  contradictions       找出资料间的矛盾
  gaps                 识别资料的知识缺口
  feynman <概念> <解释> Feynman 角色反转 teach-back
  weakness             预测学习者的知识盲区
  exam                 生成 15 题模拟期末考

═══ NotebookLM 多模态产物 ═══
  audio [format]       播客 (deep_dive/brief/critique/debate)
  video [style] [fmt]  视频 (style/format)
  flashcards [diff]    抽认卡 (easy/medium/hard)
  quiz                 测验
  mindmap              思维导图
  chat-config [goal]   配置 chat (learning_guide/custom)
  download <type>      下载产物

═══ 完整流程 ═══
  full <title> [opts]      快捷流程（init→add→三问→audio）
  marathon <title> [opts]  完整 48h 三阶段马拉松

═══ 知识库整合 ═══
  export               导出到 ~/knowledge/huo15/learning/<topic>/

═══ 环境变量 ═══
  NLM                 nlm CLI 路径（默认 ~/.venv/notebooklm/bin/nlm）
  NOTEBOOKLM_PROFILE  Profile 名（默认 default）
  MIT_LEARN_LANG      输出语言（默认 zh-CN）
  MIT_LEARN_KB_DIR    知识库目录（默认 ~/knowledge/huo15/learning）

例：
  mit-learn.sh init "强化学习"
  mit-learn.sh add --file paper.pdf --youtube https://yt.com/x --wait
  mit-learn.sh ask all
  mit-learn.sh marathon "强化学习" --file ./book.pdf --url https://...
EOF
}

#-------------------------------------------------------------------------------
# 主入口
#-------------------------------------------------------------------------------
COMMAND="${1:-}"

# 仅对网络命令做登录检查
if needs_network "${COMMAND}"; then
  auto_login || exit 1
fi

case "${COMMAND}" in
  init)            shift; cmd_init "$@" ;;
  add)             shift; cmd_add "$@" ;;
  ask)             shift; cmd_ask "$@" ;;
  audio)           shift; cmd_audio "$@" ;;
  video)           shift; cmd_video "$@" ;;
  flashcards)      shift; cmd_flashcards "$@" ;;
  quiz)            shift; cmd_quiz "$@" ;;
  mindmap)         shift; cmd_mindmap "$@" ;;
  chat-config)     shift; cmd_chat_config "$@" ;;
  download)        shift; cmd_download "$@" ;;
  synthesize)      shift; cmd_synthesize "$@" ;;
  contradictions)  shift; cmd_contradictions "$@" ;;
  gaps)            shift; cmd_gaps "$@" ;;
  feynman)         shift; cmd_feynman "$@" ;;
  weakness)        shift; cmd_weakness "$@" ;;
  exam)            shift; cmd_exam "$@" ;;
  full)            shift; cmd_full "$@" ;;
  marathon)        shift; cmd_marathon "$@" ;;
  status)          cmd_status ;;
  list)            list_notebooks ;;
  export)          cmd_export ;;
  help|--help|-h|"") usage ;;
  *)
    error "未知命令: ${COMMAND}"
    echo ""
    usage
    exit 1
    ;;
esac
