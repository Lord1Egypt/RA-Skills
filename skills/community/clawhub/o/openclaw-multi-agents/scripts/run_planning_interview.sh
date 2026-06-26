#!/bin/bash
# run_planning_interview.sh - Interactive Planning Interview for Team Design
# Version: 6.0.0 (v6 Architecture - Planning Phase)
# Author: AiTu (OpenClaw)
#
# Purpose: Guide users through structured interview to design optimal Agent team
# Output: Team Design Document (team-design.md)
#
# Usage:
#   bash scripts/run_planning_interview.sh [--resume] [--output <path>]
#
# Options:
#   --resume    Resume from saved progress
#   --output    Custom output path for team-design.md (default: ./team-design.md)

set -e

# =============================================================================
# CONFIGURATION
# =============================================================================

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
PROGRESS_FILE="/tmp/planning_interview_progress.json"
DEFAULT_OUTPUT="./team-design.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Interview state
declare -A ANSWERS
CURRENT_QUESTION=1
TOTAL_QUESTIONS=10
OUTPUT_FILE=""

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

print_header() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║${NC} ${WHITE}Multi-Agent Orchestration - Planning Interview${NC}                       ${CYAN}║${NC}"
    echo -e "${CYAN}║${NC} ${YELLOW}v6 Architecture - Team Design Phase${NC}                                 ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_section() {
    local title="$1"
    echo ""
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${WHITE}  $title${NC}"
    echo -e "${MAGENTA}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

print_progress() {
    local current=$1
    local total=$2
    local percent=$((current * 100 / total))
    local filled=$((percent / 5))
    local empty=$((20 - filled))
    
    echo -e "${CYAN}进度: [${GREEN}$(printf '█%.0s' $(seq 1 $filled))${NC}$(printf '░%.0s' $(seq 1 $empty))${CYAN}] ${WHITE}${current}/${total}${NC} (${percent}%)"
    echo ""
}

print_question() {
    local num=$1
    local category="$2"
    local question="$3"
    
    echo -e "${YELLOW}【问题 ${num}/${TOTAL_QUESTIONS}】${NC} ${BLUE}[${category}]${NC}"
    echo -e "${WHITE}${question}${NC}"
    echo ""
}

print_hint() {
    echo -e "${CYAN}💡 提示: ${NC}$1"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# =============================================================================
# PROGRESS MANAGEMENT
# =============================================================================

save_progress() {
    local json="{"
    json+="\"timestamp\":\"$(date -Iseconds)\","
    json+="\"current_question\":${CURRENT_QUESTION},"
    json+="\"answers\":{"
    
    local first=true
    for key in "${!ANSWERS[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            json+=","
        fi
        # Escape quotes in answers
        local value="${ANSWERS[$key]}"
        value="${value//\"/\\\"}"
        json+="\"$key\":\"$value\""
    done
    
    json+="}}"
    
    echo "$json" > "$PROGRESS_FILE"
}

load_progress() {
    if [ -f "$PROGRESS_FILE" ]; then
        print_warning "发现未完成的访谈记录"
        echo -e "  时间: $(grep -o '"timestamp":"[^"]*"' "$PROGRESS_FILE" | cut -d'"' -f4)"
        echo ""
        read -p "是否继续上次进度? [Y/n]: " resume_choice
        
        if [[ "$resume_choice" =~ ^[Nn]$ ]]; then
            rm -f "$PROGRESS_FILE"
            print_success "已清除旧记录，开始新访谈"
            return 1
        fi
        
        # Parse JSON manually (simple extraction)
        CURRENT_QUESTION=$(grep -o '"current_question":[0-9]*' "$PROGRESS_FILE" | cut -d: -f2)
        
        # Load answers (simplified parsing)
        local answers_raw=$(grep -o '"answers":{.*}' "$PROGRESS_FILE" | sed 's/"answers"://')
        
        print_success "已加载进度 (问题 ${CURRENT_QUESTION}/${TOTAL_QUESTIONS})"
        return 0
    fi
    return 1
}

# =============================================================================
# INPUT FUNCTIONS
# =============================================================================

get_multiline_input() {
    local prompt="$1"
    local var_name="$2"
    local input=""
    local line=""
    
    echo -e "${WHITE}${prompt}${NC}"
    echo -e "${CYAN}(输入多行内容，单独输入 'END' 结束)${NC}"
    echo ""
    
    while IFS= read -r line; do
        if [ "$line" = "END" ]; then
            break
        fi
        if [ -z "$input" ]; then
            input="$line"
        else
            input="$input
$line"
        fi
    done
    
    ANSWERS[$var_name]="$input"
}

get_single_input() {
    local prompt="$1"
    local var_name="$2"
    local default="${3:-}"
    local input=""
    
    if [ -n "$default" ]; then
        echo -e "${WHITE}${prompt} ${CYAN}[默认: $default]${NC}"
    else
        echo -e "${WHITE}${prompt}${NC}"
    fi
    
    read -p "> " input
    
    if [ -z "$input" ] && [ -n "$default" ]; then
        input="$default"
    fi
    
    ANSWERS[$var_name]="$input"
}

get_choice_input() {
    local prompt="$1"
    local var_name="$2"
    shift 2
    local options=("$@")
    
    echo -e "${WHITE}${prompt}${NC}"
    echo ""
    
    local i=1
    for opt in "${options[@]}"; do
        echo -e "  ${CYAN}$i)${NC} $opt"
        ((i++))
    done
    echo ""
    
    local choice=""
    while true; do
        read -p "请选择 [1-${#options[@]}]: " choice
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#options[@]} ]; then
            ANSWERS[$var_name]="${options[$((choice-1))]}"
            break
        fi
        print_error "无效选择，请输入 1-${#options[@]} 之间的数字"
    done
}

get_rating_input() {
    local prompt="$1"
    local var_name="$2"
    local rating=""
    
    echo -e "${WHITE}${prompt}${NC}"
    echo -e "${CYAN}(1=最低, 5=最高)${NC}"
    echo ""
    
    while true; do
        read -p "评分 [1-5]: " rating
        if [[ "$rating" =~ ^[1-5]$ ]]; then
            ANSWERS[$var_name]="$rating"
            break
        fi
        print_error "请输入 1-5 之间的数字"
    done
}

# =============================================================================
# INTERVIEW QUESTIONS
# =============================================================================

run_interview() {
    print_section "第一部分: 工作流程理解 (Workflow Understanding)"
    
    # Q1: 典型工作流程
    print_progress 1 $TOTAL_QUESTIONS
    print_question 1 "工作流程" "请描述您典型的一天工作流程，从开始到结束。"
    print_hint "例如：早上检查邮件、上午开会、下午写代码、晚上整理文档..."
    get_multiline_input "请详细描述:" "workflow_description"
    echo ""
    print_success "已记录工作流程描述"
    save_progress
    ((CURRENT_QUESTION++))
    
    # Q2: 任务类型
    print_progress 2 $TOTAL_QUESTIONS
    print_question 2 "任务分类" "您的工作任务可以分成哪几类？请列出主要类型。"
    print_hint "例如：创意型（设计、写作）、分析型（数据分析、调研）、执行型（编码、制作）、审查型（review、质检）、协调型（项目管理、沟通）"
    get_multiline_input "请列出任务类型:" "task_types"
    echo ""
    print_success "已记录任务类型"
    save_progress
    ((CURRENT_QUESTION++))
    
    # Q3: 核心痛点
    print_progress 3 $TOTAL_QUESTIONS
    print_question 3 "痛点识别" "在当前工作流程中，最让您感到沮丧或低效的三个环节是什么？"
    print_hint "请描述具体问题、发生频率、造成的影响"
    get_multiline_input "请描述三个痛点:" "pain_points"
    echo ""
    print_success "已记录痛点"
    save_progress
    ((CURRENT_QUESTION++))
    
    print_section "第二部分: 协作与质量需求 (Collaboration & Quality)"
    
    # Q4: 协作模式偏好
    print_progress 4 $TOTAL_QUESTIONS
    print_question 4 "协作模式" "您希望AI Agents如何融入您的工作流程？理想的协作方式是什么？"
    get_choice_input "请选择您偏好的协作模式:" "collaboration_mode" \
        "自主型 - 给目标，AI自己探索完成" \
        "陪伴型 - 边做边讨论，实时反馈" \
        "流水线型 - 明确分工，按步骤执行" \
        "顾问型 - 先咨询建议，再决定"
    echo ""
    print_success "已选择: ${ANSWERS[collaboration_mode]}"
    save_progress
    ((CURRENT_QUESTION++))
    
    # Q5: 质量要求
    print_progress 5 $TOTAL_QUESTIONS
    print_question 5 "质量标准" "对于工作输出，您的质量标准是什么？"
    get_choice_input "请选择质量优先级:" "quality_priority" \
        "速度优先 - 快比完美重要" \
        "平衡型 - 合理时间内合理质量" \
        "质量优先 - 必须达到高标准" \
        "零容忍 - 错误不可接受"
    echo ""
    print_success "已选择: ${ANSWERS[quality_priority]}"
    save_progress
    ((CURRENT_QUESTION++))
    
    # Q6: 控制程度
    print_progress 6 $TOTAL_QUESTIONS
    print_question 6 "控制程度" "您希望保持多少控制权？什么情况下希望AI自主决策？"
    print_hint "例如：日常任务可自主，重大决策需征询"
    get_multiline_input "请描述您的期望:" "control_preference"
    echo ""
    print_success "已记录控制偏好"
    save_progress
    ((CURRENT_QUESTION++))
    
    print_section "第三部分: 深度挖掘 (Deep Dive)"
    
    # Q7: 成功案例
    print_progress 7 $TOTAL_QUESTIONS
    print_question 7 "成功案例" "请分享一个最近让您印象深刻的成功案例。"
    print_hint "是什么让这次成功？有没有可以复制的部分？"
    get_multiline_input "请描述成功案例:" "success_case"
    echo ""
    print_success "已记录成功案例"
    save_progress
    ((CURRENT_QUESTION++))
    
    # Q8: 失败案例
    print_progress 8 $TOTAL_QUESTIONS
    print_question 8 "失败案例" "请分享一个最近的失败或挫折案例。"
    print_hint "失败的根本原因是什么？当时缺少什么资源或能力？"
    get_multiline_input "请描述失败案例:" "failure_case"
    echo ""
    print_success "已记录失败案例"
    save_progress
    ((CURRENT_QUESTION++))
    
    # Q9: 特殊约束
    print_progress 9 $TOTAL_QUESTIONS
    print_question 9 "特殊约束" "您的团队/项目有什么特殊约束或要求？"
    print_hint "例如：合规要求、技术栈限制、安全要求、预算限制"
    get_multiline_input "请描述约束条件:" "constraints"
    echo ""
    print_success "已记录约束条件"
    save_progress
    ((CURRENT_QUESTION++))
    
    print_section "第四部分: 目标与期望 (Goals & Expectations)"
    
    # Q10: 3个月目标
    print_progress 10 $TOTAL_QUESTIONS
    print_question 10 "成功愿景" "3个月后，您希望这个Agent团队帮您实现什么？"
    print_hint "例如：节省时间、提升质量、扩展能力、减少焦虑"
    get_multiline_input "请描述您的期望:" "success_vision"
    echo ""
    print_success "已记录成功愿景"
    save_progress
    ((CURRENT_QUESTION++))
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

analyze_responses() {
    print_section "分析访谈结果"
    
    echo -e "${WHITE}正在分析您的回答...${NC}"
    echo ""
    
    # Analyze workflow complexity
    local workflow_complexity="medium"
    local workflow_text="${ANSWERS[workflow_description]}"
    local step_count=$(echo "$workflow_text" | grep -oE "(步骤|环节|阶段|然后|接着|之后)" | wc -l)
    
    if [ "$step_count" -lt 3 ]; then
        workflow_complexity="simple"
    elif [ "$step_count" -gt 6 ]; then
        workflow_complexity="complex"
    fi
    
    ANSWERS[workflow_complexity]="$workflow_complexity"
    
    # Analyze team size recommendation
    local team_size="medium"
    local task_types="${ANSWERS[task_types]}"
    local type_count=$(echo "$task_types" | grep -oE "(、|，|,|\n)" | wc -l)
    ((type_count++))
    
    if [ "$type_count" -le 2 ]; then
        team_size="small"
    elif [ "$type_count" -ge 5 ]; then
        team_size="large"
    fi
    
    ANSWERS[team_size]="$team_size"
    
    # Determine primary task category
    local primary_category="unspecified-high"
    local collaboration="${ANSWERS[collaboration_mode]}"
    
    if [[ "$collaboration" == *"自主"* ]]; then
        primary_category="deep"
    elif [[ "$collaboration" == *"顾问"* ]]; then
        primary_category="ultrabrain"
    elif [[ "$collaboration" == *"流水线"* ]]; then
        primary_category="quick"
    fi
    
    ANSWERS[primary_category]="$primary_category"
    
    # Print analysis summary
    echo -e "${GREEN}分析完成！${NC}"
    echo ""
    echo -e "${WHITE}📊 分析结果:${NC}"
    echo ""
    echo -e "  ${CYAN}工作流程复杂度:${NC} ${YELLOW}$workflow_complexity${NC}"
    echo -e "  ${CYAN}推荐团队规模:${NC} ${YELLOW}$team_size${NC}"
    echo -e "  ${CYAN}主要任务类别:${NC} ${YELLOW}$primary_category${NC}"
    echo -e "  ${CYAN}协作模式:${NC} ${YELLOW}${ANSWERS[collaboration_mode]}${NC}"
    echo -e "  ${CYAN}质量要求:${NC} ${YELLOW}${ANSWERS[quality_priority]}${NC}"
    echo ""
}

# =============================================================================
# RECOMMENDATION FUNCTIONS
# =============================================================================

generate_recommendations() {
    print_section "团队配置推荐"
    
    local team_size="${ANSWERS[team_size]}"
    local primary_category="${ANSWERS[primary_category]}"
    local quality="${ANSWERS[quality_priority]}"
    
    # Manager Agent recommendation
    local manager_persona="亨利·甘特"
    local manager_reasoning="甘特图思维，擅长多Agent编排、进度可视化、任务协调"
    
    ANSWERS[manager_persona]="$manager_persona"
    ANSWERS[manager_reasoning]="$manager_reasoning"
    
    echo -e "${WHITE}基于您的访谈结果，推荐以下团队配置:${NC}"
    echo ""
    
    # Display architecture
    echo -e "${CYAN}┌─────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${CYAN}│${NC}                     ${WHITE}三层架构设计${NC}                           ${CYAN}│${NC}"
    echo -e "${CYAN}├─────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${CYAN}│${NC}  ${YELLOW}用户 (User)${NC}                                              ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}       │                                                     ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}       ▼                                                     ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}  ${GREEN}主Agent (Main Agent)${NC} - Pure Relay                      ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}       │                                                     ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}       ▼                                                     ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}  ${BLUE}Manager Agent${NC} - ${manager_persona}                          ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}       │                                                     ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}       ▼                                                     ${CYAN}│${NC}"
    echo -e "${CYAN}│${NC}  ${MAGENTA}Worker Agents${NC} (根据团队规模配置)                      ${CYAN}│${NC}"
    echo -e "${CYAN}└─────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Recommend workers based on team size
    case "$team_size" in
        small)
            echo -e "${WHITE}推荐团队规模: ${GREEN}轻量级 (3人)${NC}"
            echo ""
            echo -e "  ${CYAN}Manager:${NC} 亨利·甘特 (任务编排)"
            echo -e "  ${CYAN}Worker 1:${NC} 费曼 (核心开发 - deep)"
            echo -e "  ${CYAN}Worker 2:${NC} 德明 (质量把关 - unspecified-high)"
            echo ""
            ANSWERS[worker1_persona]="费曼"
            ANSWERS[worker1_role]="核心开发"
            ANSWERS[worker1_category]="deep"
            ANSWERS[worker2_persona]="德明"
            ANSWERS[worker2_role]="质量把关"
            ANSWERS[worker2_category]="unspecified-high"
            ANSWERS[worker3_persona]=""
            ANSWERS[worker4_persona]=""
            ;;
        medium)
            echo -e "${WHITE}推荐团队规模: ${GREEN}标准 (5人)${NC}"
            echo ""
            echo -e "  ${CYAN}Manager:${NC} 亨利·甘特 (任务编排)"
            echo -e "  ${CYAN}Worker 1:${NC} 芒格 (战略规划 - ultrabrain)"
            echo -e "  ${CYAN}Worker 2:${NC} 费曼 (核心开发 - deep)"
            echo -e "  ${CYAN}Worker 3:${NC} 德明 (质量把关 - unspecified-high)"
            echo -e "  ${CYAN}Worker 4:${NC} 德鲁克 (项目管理 - unspecified-low)"
            echo ""
            ANSWERS[worker1_persona]="芒格"
            ANSWERS[worker1_role]="战略规划"
            ANSWERS[worker1_category]="ultrabrain"
            ANSWERS[worker2_persona]="费曼"
            ANSWERS[worker2_role]="核心开发"
            ANSWERS[worker2_category]="deep"
            ANSWERS[worker3_persona]="德明"
            ANSWERS[worker3_role]="质量把关"
            ANSWERS[worker3_category]="unspecified-high"
            ANSWERS[worker4_persona]="德鲁克"
            ANSWERS[worker4_role]="项目管理"
            ANSWERS[worker4_category]="unspecified-low"
            ;;
        large)
            echo -e "${WHITE}推荐团队规模: ${GREEN}企业级 (6+人)${NC}"
            echo ""
            echo -e "  ${CYAN}Manager:${NC} 亨利·甘特 (主管理)"
            echo -e "  ${CYAN}Sub-Manager:${NC} 项目经理 (专项管理)"
            echo -e "  ${CYAN}Worker 1:${NC} 芒格 (战略规划 - ultrabrain)"
            echo -e "  ${CYAN}Worker 2:${NC} 费曼 (核心开发 - deep)"
            echo -e "  ${CYAN}Worker 3:${NC} 乔布斯 (产品设计 - visual-engineering)"
            echo -e "  ${CYAN}Worker 4:${NC} 图灵 (架构设计 - deep)"
            echo -e "  ${CYAN}Worker 5:${NC} 德明 (质量把关 - unspecified-high)"
            echo -e "  ${CYAN}Worker 6:${NC} 德鲁克 (项目管理 - unspecified-low)"
            echo ""
            ANSWERS[worker1_persona]="芒格"
            ANSWERS[worker1_role]="战略规划"
            ANSWERS[worker1_category]="ultrabrain"
            ANSWERS[worker2_persona]="费曼"
            ANSWERS[worker2_role]="核心开发"
            ANSWERS[worker2_category]="deep"
            ANSWERS[worker3_persona]="乔布斯"
            ANSWERS[worker3_role]="产品设计"
            ANSWERS[worker3_category]="visual-engineering"
            ANSWERS[worker4_persona]="图灵"
            ANSWERS[worker4_role]="架构设计"
            ANSWERS[worker4_category]="deep"
            ANSWERS[worker5_persona]="德明"
            ANSWERS[worker5_role]="质量把关"
            ANSWERS[worker5_category]="unspecified-high"
            ANSWERS[worker6_persona]="德鲁克"
            ANSWERS[worker6_role]="项目管理"
            ANSWERS[worker6_category]="unspecified-low"
            ;;
    esac
    
    # Quality-based model recommendations
    echo -e "${WHITE}模型推荐 (基于质量要求):${NC}"
    echo ""
    
    case "$quality" in
        *"速度优先"*)
            echo -e "  ${CYAN}推荐模型:${NC} Grok / Haiku / Flash (快速响应)"
            ANSWERS[model_recommendation]="Grok/Haiku/Flash"
            ;;
        *"平衡型"*)
            echo -e "  ${CYAN}推荐模型:${NC} Claude Sonnet / GPT-4 (平衡性能)"
            ANSWERS[model_recommendation]="Claude Sonnet/GPT-4"
            ;;
        *"质量优先"*)
            echo -e "  ${CYAN}推荐模型:${NC} Claude Opus / GPT-5 (高质量)"
            ANSWERS[model_recommendation]="Claude Opus/GPT-5"
            ;;
        *"零容忍"*)
            echo -e "  ${CYAN}推荐模型:${NC} Claude Opus + 严格审查流程"
            ANSWERS[model_recommendation]="Claude Opus (strict review)"
            ;;
    esac
    echo ""
}

# =============================================================================
# OUTPUT GENERATION
# =============================================================================

generate_team_design_document() {
    print_section "生成团队设计文档"
    
    local output_path="${OUTPUT_FILE:-$DEFAULT_OUTPUT}"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    
    echo -e "${WHITE}正在生成 Team Design Document...${NC}"
    echo ""
    
    cat > "$output_path" << EOF
# Team Design Document

**Project:** Custom Agent Team  
**Workflow:** ${ANSWERS[task_types]}  
**Created:** $timestamp  
**Version:** 6.0.0 (v6 Architecture)

---

## 1. Project/Workflow Summary

### 1.1 核心目标 (Core Objectives)

${ANSWERS[success_vision]}

### 1.2 工作流程描述 (Workflow Description)

\`\`\`
${ANSWERS[workflow_description]}
\`\`\`

### 1.3 输入与输出 (Inputs & Outputs)

| 类型 | 内容 | 格式 |
|------|------|------|
| 输入 | 用户请求、任务描述 | 自然语言 |
| 输出 | 完成的任务、分析报告、代码等 | 多格式 |

### 1.4 当前状态 (Current State)

- **现有工具/系统:** 待补充
- **团队规模:** ${ANSWERS[team_size]} team
- **执行频率:** 待补充

---

## 2. Pain Points Identified

### 2.1 主要痛点 (Primary Pain Points)

${ANSWERS[pain_points]}

### 2.2 痛点详细分析

**痛点分析基于用户访谈，需要进一步细化。**

---

## 3. Recommended Team Composition

### 3.1 三层架构设计 (Three-Tier Architecture)

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                      用户 (User)                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              主Agent (Main Agent)                            │
│         角色: 纯中继 (Pure Relay)                            │
│         职责: 用户沟通、任务分发、状态汇报                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│            管理Agent (Manager Agent)                         │
│         角色: 规划与协调 (Planning & Orchestration)          │
│         人格: ${ANSWERS[manager_persona]}                                    │
│         职责: 任务分解、质量把关、Worker管理                  │
└───────────┬───────────┬───────────┬─────────────────────────┘
            │           │           │
            ▼           ▼           ▼
EOF

    # Add workers based on team size
    local team_size="${ANSWERS[team_size]}"
    
    case "$team_size" in
        small)
            cat >> "$output_path" << EOF
┌───────────────┐ ┌───────────┐
│  Worker 1     │ │ Worker 2  │
│  ${ANSWERS[worker1_persona]}           │ │ ${ANSWERS[worker2_persona]}         │
│  ${ANSWERS[worker1_role]}       │ │ ${ANSWERS[worker2_role]}       │
└───────────────┘ └───────────┘
\`\`\`
EOF
            ;;
        medium)
            cat >> "$output_path" << EOF
┌───────────────┐ ┌───────────┐ ┌───────────────┐ ┌───────────────┐
│  Worker 1     │ │ Worker 2  │ │  Worker 3     │ │  Worker 4     │
│  ${ANSWERS[worker1_persona]}           │ │ ${ANSWERS[worker2_persona]}         │ │  ${ANSWERS[worker3_persona]}           │ │  ${ANSWERS[worker4_persona]}           │
│  ${ANSWERS[worker1_role]}       │ │ ${ANSWERS[worker2_role]}       │ │  ${ANSWERS[worker3_role]}       │ │  ${ANSWERS[worker4_role]}       │
└───────────────┘ └───────────┘ └───────────────┘ └───────────────┘
\`\`\`
EOF
            ;;
        large)
            cat >> "$output_path" << EOF
┌───────────────┐ ┌───────────┐ ┌───────────────┐
│  Worker 1     │ │ Worker 2  │ │  Worker 3     │
│  ${ANSWERS[worker1_persona]}           │ │ ${ANSWERS[worker2_persona]}         │ │  ${ANSWERS[worker3_persona]}           │
│  ${ANSWERS[worker1_role]}       │ │ ${ANSWERS[worker2_role]}       │ │  ${ANSWERS[worker3_role]}       │
└───────────────┘ └───────────┘ └───────────────┘
┌───────────────┐ ┌───────────┐ ┌───────────────┐
│  Worker 4     │ │ Worker 5  │ │  Worker 6     │
│  ${ANSWERS[worker4_persona]}           │ │ ${ANSWERS[worker5_persona]}         │ │  ${ANSWERS[worker6_persona]}           │
│  ${ANSWERS[worker4_role]}       │ │ ${ANSWERS[worker5_role]}       │ │  ${ANSWERS[worker6_role]}       │
└───────────────┘ └───────────┘ └───────────────┘
\`\`\`
EOF
            ;;
    esac

    cat >> "$output_path" << EOF

### 3.2 Agent 详细配置

#### 主Agent (Main Agent)
| 属性 | 配置 |
|------|------|
| Agent ID | \`main\` |
| 人格原型 | 爱兔 (默认) |
| 任务类别 | - |
| 核心职责 | 用户沟通、智能分发、状态聚合 |
| 报告对象 | 用户 |

#### 管理Agent (Manager Agent)
| 属性 | 配置 |
|------|------|
| Agent ID | \`manager\` |
| 人格原型 | ${ANSWERS[manager_persona]} |
| 任务类别 | unspecified-high |
| 核心职责 | 规划、协调、验证、质量把关 |
| 报告对象 | 主Agent (高层状态) |
| 管理对象 | Worker Agents |

#### Worker Agents

EOF

    # Add worker table based on team size
    case "$team_size" in
        small)
            cat >> "$output_path" << EOF
| Agent ID | 人格原型 | 角色定位 | 任务类别 | 核心职责 |
|----------|----------|----------|----------|----------|
| worker-1 | ${ANSWERS[worker1_persona]} | ${ANSWERS[worker1_role]} | ${ANSWERS[worker1_category]} | 执行核心任务 |
| worker-2 | ${ANSWERS[worker2_persona]} | ${ANSWERS[worker2_role]} | ${ANSWERS[worker2_category]} | 质量审查 |
EOF
            ;;
        medium)
            cat >> "$output_path" << EOF
| Agent ID | 人格原型 | 角色定位 | 任务类别 | 核心职责 |
|----------|----------|----------|----------|----------|
| munger | ${ANSWERS[worker1_persona]} | ${ANSWERS[worker1_role]} | ${ANSWERS[worker1_category]} | 战略规划、PRD设计 |
| feynman | ${ANSWERS[worker2_persona]} | ${ANSWERS[worker2_role]} | ${ANSWERS[worker2_category]} | 核心开发、技术实现 |
| deming | ${ANSWERS[worker3_persona]} | ${ANSWERS[worker3_role]} | ${ANSWERS[worker3_category]} | 质量把关、代码审查 |
| drucker | ${ANSWERS[worker4_persona]} | ${ANSWERS[worker4_role]} | ${ANSWERS[worker4_category]} | 项目管理、进度跟踪 |
EOF
            ;;
        large)
            cat >> "$output_path" << EOF
| Agent ID | 人格原型 | 角色定位 | 任务类别 | 核心职责 |
|----------|----------|----------|----------|----------|
| munger | ${ANSWERS[worker1_persona]} | ${ANSWERS[worker1_role]} | ${ANSWERS[worker1_category]} | 战略规划 |
| feynman | ${ANSWERS[worker2_persona]} | ${ANSWERS[worker2_role]} | ${ANSWERS[worker2_category]} | 核心开发 |
| jobs | ${ANSWERS[worker3_persona]} | ${ANSWERS[worker3_role]} | ${ANSWERS[worker3_category]} | 产品设计 |
| turing | ${ANSWERS[worker4_persona]} | ${ANSWERS[worker4_role]} | ${ANSWERS[worker4_category]} | 架构设计 |
| deming | ${ANSWERS[worker5_persona]} | ${ANSWERS[worker5_role]} | ${ANSWERS[worker5_category]} | 质量把关 |
| drucker | ${ANSWERS[worker6_persona]} | ${ANSWERS[worker6_role]} | ${ANSWERS[worker6_category]} | 项目管理 |
EOF
            ;;
    esac

    cat >> "$output_path" << EOF

---

## 4. Communication Flow

### 4.1 消息流向图 (Message Flow Diagram)

\`\`\`
用户请求
    │
    ▼
┌────────────────────────────────────────────────────────────┐
│  主Agent (Main)                                             │
│  ├─ 解析用户意图                                             │
│  ├─ 判断是否需要Manager介入                                  │
│  └─ 转发给Manager或直接响应                                  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  Manager Agent                                              │
│  ├─ 接收任务                                                │
│  ├─ 分解子任务                                              │
│  ├─ 分发给Workers (sessions_send)                           │
│  ├─ 收集结果                                                │
│  ├─ 质量验证                                                │
│  └─ 汇总报告给Main Agent                                    │
└──────────┬─────────┬─────────┬──────────────────────────────┘
           │         │         │
           ▼         ▼         ▼
      Workers (并行执行)
           │         │         │
           └─────────┼─────────┘
                     │
                     ▼
             结果聚合与验证
                     │
                     ▼
             返回主Agent → 用户
\`\`\`

### 4.2 通信协议 (Communication Protocol)

#### 主Agent → Manager
\`\`\`typescript
sessions_send({
  sessionKey: "agent:manager:main",
  message: "任务描述 + 上下文 + 约束条件",
  timeoutSeconds: 0  // 异步，不阻塞
})
\`\`\`

#### Manager → Workers
\`\`\`typescript
sessions_send({
  sessionKey: "agent:<worker_id>:manager",
  message: "子任务 + 依赖关系 + 验收标准",
  timeoutSeconds: 0  // 异步，并行执行
})
\`\`\`

---

## 5. Task Category Mapping

### 5.1 任务类别分配

| Agent | 主要任务类别 | Fallback Chain | 说明 |
|-------|--------------|----------------|------|
| Main | - | - | 智能分发，不直接处理 |
| Manager | unspecified-high | Claude Opus → GPT-5 | 规划协调，质量把关 |
EOF

    # Add worker task categories
    case "$team_size" in
        small)
            cat >> "$output_path" << EOF
| Worker 1 | ${ANSWERS[worker1_category]} | GPT Codex → Claude Sonnet | 核心任务执行 |
| Worker 2 | ${ANSWERS[worker2_category]} | Claude Opus → GPT-5 | 质量审查 |
EOF
            ;;
        medium)
            cat >> "$output_path" << EOF
| 芒格 | ${ANSWERS[worker1_category]} | GPT-5 → Claude Opus | 战略规划 |
| 费曼 | ${ANSWERS[worker2_category]} | GPT Codex → Claude Sonnet | 核心开发 |
| 德明 | ${ANSWERS[worker3_category]} | Claude Opus → GPT-5 | 质量把关 |
| 德鲁克 | ${ANSWERS[worker4_category]} | Claude Sonnet → GPT-4 | 项目管理 |
EOF
            ;;
        large)
            cat >> "$output_path" << EOF
| 芒格 | ${ANSWERS[worker1_category]} | GPT-5 → Claude Opus | 战略规划 |
| 费曼 | ${ANSWERS[worker2_category]} | GPT Codex → Claude Sonnet | 核心开发 |
| 乔布斯 | ${ANSWERS[worker3_category]} | Gemini Pro → GPT-4V | 产品设计 |
| 图灵 | ${ANSWERS[worker4_category]} | GPT Codex → Claude Sonnet | 架构设计 |
| 德明 | ${ANSWERS[worker5_category]} | Claude Opus → GPT-5 | 质量把关 |
| 德鲁克 | ${ANSWERS[worker6_category]} | Claude Sonnet → GPT-4 | 项目管理 |
EOF
            ;;
    esac

    cat >> "$output_path" << EOF

---

## 6. User Preferences

### 6.1 协作模式
${ANSWERS[collaboration_mode]}

### 6.2 质量要求
${ANSWERS[quality_priority]}

### 6.3 控制偏好
${ANSWERS[control_preference]}

### 6.4 特殊约束
${ANSWERS[constraints]}

---

## 7. Implementation Checklist

### 7.1 预实施检查 (Pre-Implementation)

- [ ] 用户已确认团队设计方案
- [ ] 所有Agent ID已确定
- [ ] 人格原型已选定并记录
- [ ] 任务类别已分配
- [ ] Fallback Chain已配置
- [ ] 工作目录已创建
- [ ] openclaw.json 已备份

### 7.2 实施步骤 (Implementation Steps)

\`\`\`bash
# Step 1: 创建Manager Agent工作区
bash scripts/setup_agent.sh manager "${ANSWERS[manager_persona]}" glm-5

# Step 2: 创建Worker Agents工作区
EOF

    # Add worker setup commands
    case "$team_size" in
        small)
            cat >> "$output_path" << EOF
bash scripts/setup_agent.sh worker-1 "${ANSWERS[worker1_persona]}" glm-5
bash scripts/setup_agent.sh worker-2 "${ANSWERS[worker2_persona]}" glm-5
EOF
            ;;
        medium)
            cat >> "$output_path" << EOF
bash scripts/setup_agent.sh munger "${ANSWERS[worker1_persona]}" glm-5
bash scripts/setup_agent.sh feynman "${ANSWERS[worker2_persona]}" glm-5
bash scripts/setup_agent.sh deming "${ANSWERS[worker3_persona]}" glm-5
bash scripts/setup_agent.sh drucker "${ANSWERS[worker4_persona]}" kimi-k2.5
EOF
            ;;
        large)
            cat >> "$output_path" << EOF
bash scripts/setup_agent.sh munger "${ANSWERS[worker1_persona]}" glm-5
bash scripts/setup_agent.sh feynman "${ANSWERS[worker2_persona]}" glm-5
bash scripts/setup_agent.sh jobs "${ANSWERS[worker3_persona]}" kimi-k2.5
bash scripts/setup_agent.sh turing "${ANSWERS[worker4_persona]}" glm-5
bash scripts/setup_agent.sh deming "${ANSWERS[worker5_persona]}" glm-5
bash scripts/setup_agent.sh drucker "${ANSWERS[worker6_persona]}" kimi-k2.5
EOF
            ;;
    esac

    cat >> "$output_path" << EOF

# Step 3: 配置openclaw.json
# - 添加agents.list条目
# - 配置fallback chains
# - 设置默认模型

# Step 4: 重启OpenClaw Gateway
# ⚠️ AI cannot execute this — it would kill the current session
# Please run manually in your terminal:
# openclaw gateway restart

# Step 5: 验证Agents注册
openclaw agents list
\`\`\`

---

## 8. User Approval

### 8.1 方案确认

我已审阅上述团队设计方案，确认以下事项:

- [ ] 工作流程描述准确
- [ ] 痛点分析符合实际情况
- [ ] 推荐的团队配置合理
- [ ] 人格原型选择恰当
- [ ] 任务类别分配合适
- [ ] 实施计划可行

### 8.2 修改意见 (如有)

_在此记录任何修改意见_

### 8.3 批准签名

**批准人:** ___________________  
**日期:** ___________________  
**签名:** ___________________

---

## 9. Appendix

### 9.1 访谈记录摘要

**工作流程:**
${ANSWERS[workflow_description]}

**任务类型:**
${ANSWERS[task_types]}

**核心痛点:**
${ANSWERS[pain_points]}

**成功案例:**
${ANSWERS[success_case]}

**失败案例:**
${ANSWERS[failure_case]}

**成功愿景:**
${ANSWERS[success_vision]}

### 9.2 参考文档

- [SKILL.md](../SKILL.md) - 完整使用指南
- [docs/persona_library.md](../docs/persona_library.md) - 人格原型库
- [docs/task_categories_and_model_matching.md](../docs/task_categories_and_model_matching.md) - 任务类别系统
- [docs/architecture_guide.md](../docs/architecture_guide.md) - 架构详解
- [docs/planning_guide.md](../docs/planning_guide.md) - 规划方法论

---

**文档生成:** Multi-Agent Orchestration Skill v6.0.0  
**生成时间:** $timestamp  
**生成工具:** run_planning_interview.sh
EOF

    print_success "Team Design Document 已生成: $output_path"
    echo ""
}

# =============================================================================
# SUMMARY AND CLEANUP
# =============================================================================

print_summary() {
    print_section "访谈完成"
    
    echo -e "${GREEN}🎉 恭喜！规划访谈已完成！${NC}"
    echo ""
    echo -e "${WHITE}📋 访谈摘要:${NC}"
    echo ""
    echo -e "  ${CYAN}工作流程复杂度:${NC} ${ANSWERS[workflow_complexity]}"
    echo -e "  ${CYAN}推荐团队规模:${NC} ${ANSWERS[team_size]}"
    echo -e "  ${CYAN}协作模式:${NC} ${ANSWERS[collaboration_mode]}"
    echo -e "  ${CYAN}质量要求:${NC} ${ANSWERS[quality_priority]}"
    echo ""
    echo -e "${WHITE}📄 输出文件:${NC}"
    echo -e "  ${GREEN}${OUTPUT_FILE:-$DEFAULT_OUTPUT}${NC}"
    echo ""
    echo -e "${WHITE}📖 下一步:${NC}"
    echo ""
    echo -e "  1. ${CYAN}审阅 Team Design Document${NC}"
    echo -e "     cat ${OUTPUT_FILE:-$DEFAULT_OUTPUT}"
    echo ""
    echo -e "  2. ${CYAN}确认或修改团队配置${NC}"
    echo ""
    echo -e "  3. ${CYAN}运行团队创建脚本${NC}"
    echo -e "     bash scripts/setup_team.sh <template>"
    echo ""
    echo -e "  4. ${CYAN}配置 openclaw.json${NC}"
    echo ""
    echo -e "  5. ${CYAN}重启 Gateway${NC}"
    echo -e "     openclaw gateway restart"
    echo ""
    
    # Clean up progress file
    rm -f "$PROGRESS_FILE"
}

# =============================================================================
# HELP AND USAGE
# =============================================================================

show_help() {
    echo ""
    echo -e "${WHITE}Multi-Agent Orchestration - Planning Interview${NC}"
    echo ""
    echo -e "${CYAN}用法:${NC}"
    echo "  bash scripts/run_planning_interview.sh [选项]"
    echo ""
    echo -e "${CYAN}选项:${NC}"
    echo "  --resume        从上次中断处继续访谈"
    echo "  --output <path> 指定输出文件路径 (默认: ./team-design.md)"
    echo "  --help, -h      显示此帮助信息"
    echo ""
    echo -e "${CYAN}描述:${NC}"
    echo "  交互式访谈脚本，引导用户完成团队设计规划。"
    echo "  访谈包含10个问题，涵盖工作流程、痛点、协作需求、质量要求等。"
    echo "  完成后生成 Team Design Document。"
    echo ""
    echo -e "${CYAN}示例:${NC}"
    echo "  # 开始新访谈"
    echo "  bash scripts/run_planning_interview.sh"
    echo ""
    echo "  # 继续上次访谈"
    echo "  bash scripts/run_planning_interview.sh --resume"
    echo ""
    echo "  # 指定输出路径"
    echo "  bash scripts/run_planning_interview.sh --output ./docs/my-team-design.md"
    echo ""
    echo -e "${CYAN}参考文档:${NC}"
    echo "  - docs/planning_guide.md      - 规划方法论"
    echo "  - templates/interview_questions.md - 问题库"
    echo "  - templates/team_design_template.md - 输出模板"
    echo ""
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --resume)
                RESUME=true
                shift
                ;;
            --output)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                print_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Print header
    print_header
    
    # Show introduction
    echo -e "${WHITE}欢迎使用 Multi-Agent Orchestration 规划访谈工具！${NC}"
    echo ""
    echo -e "本工具将引导您完成 ${YELLOW}v6 架构${NC} 的团队设计规划。"
    echo ""
    echo -e "${CYAN}访谈包含以下部分:${NC}"
    echo -e "  1. ${WHITE}工作流程理解${NC} - 了解您的日常工作"
    echo -e "  2. ${WHITE}协作与质量需求${NC} - 明确协作模式和质量标准"
    echo -e "  3. ${WHITE}深度挖掘${NC} - 探索成功与失败案例"
    echo -e "  4. ${WHITE}目标与期望${NC} - 设定成功愿景"
    echo ""
    echo -e "${CYAN}预计时长:${NC} ${YELLOW}15-30 分钟${NC}"
    echo ""
    echo -e "${CYAN}输出:${NC} ${GREEN}Team Design Document (team-design.md)${NC}"
    echo ""
    
    # Check for resume
    if [ "$RESUME" = true ]; then
        load_progress
    fi
    
    # Confirm to start
    read -p "按 Enter 开始访谈 (或输入 'q' 退出): " start_choice
    if [ "$start_choice" = "q" ]; then
        echo -e "${YELLOW}访谈已取消。${NC}"
        exit 0
    fi
    
    # Run interview
    run_interview
    
    # Analyze responses
    analyze_responses
    
    # Generate recommendations
    generate_recommendations
    
    # Ask for approval
    echo ""
    echo -e "${WHITE}是否接受以上推荐配置？${NC}"
    read -p "[Y/n]: " approval
    
    if [[ "$approval" =~ ^[Nn]$ ]]; then
        echo ""
        echo -e "${YELLOW}您可以手动编辑生成的 Team Design Document 进行调整。${NC}"
    fi
    
    # Generate output document
    generate_team_design_document
    
    # Print summary
    print_summary
}

# Run main
main "$@"