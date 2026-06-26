#!/bin/bash
#===============================================================================
# PromptBuddy Lite v3.0.0
# 基于《The Prompt Report》+ HMAW 层级式架构
# 采用 4 层分层模板结构
#
# L1 角色层 - Who (身份设定)
# L2 任务层 - What (核心任务)
# L3 格式层 - How (输出格式)
# L4 约束层 - Constraints (上下文约束)
#===============================================================================

# ==================== L1: 角色层模板 ====================

declare -A ROLE_TEMPLATES=(
    # 通用型
    ["通用助手"]="你是一位专业助手，擅长理解用户需求并提供精准帮助"
    ["通用顾问"]="你是一位资深顾问，专注于解决实际问题"
    ["领域专家"]="你是一位领域专家，具备丰富的实践经验"
    
    # 分析类
    ["分析师"]="你是一位资深分析师，善于从数据中提炼洞察"
    ["策略分析师"]="你是一位策略分析师，擅长深度思考和逻辑推演"
    ["商业分析师"]="你是一位商业分析师，专注于市场洞察和竞争分析"
    
    # 创意类
    ["创意专家"]="你是一位创意专家，善于头脑风暴和创新思维"
    ["策划专家"]="你是一位策划专家，擅长活动/项目策划"
    
    # 执行类
    ["技术专家"]="你是一位技术专家，具备扎实的编程和架构能力"
    ["运营专家"]="你是一位运营专家，精通业务流程优化"
    ["项目经理"]="你是一位资深项目经理，擅长项目规划与执行"
    
    # 审核类
    ["审核专家"]="你是一位资深审核专家，严格把控质量和风险"
    ["优化专家"]="你是一位精益求精的优化专家，持续改进"
    
    # 决策类
    ["决策顾问"]="你是一位理性决策顾问，帮助权衡利弊"
    ["战略顾问"]="你是一位战略顾问，具备全局视野"
)

# ==================== L2: 任务层模板 ====================

declare -A TASK_TEMPLATES=(
    # 通用任务
    ["通用"]="理解用户需求并提供专业解答"
    
    # 分析类
    ["分析"]="深入分析问题，识别核心要素和关键变量"
    ["调研"]="全面调研背景信息，提供系统性报告"
    ["评估"]="客观评估现状，给出专业判断和建议"
    
    # 生成类
    ["生成"]="根据需求生成完整方案或内容"
    ["创作"]="运用创意能力，创作独特内容"
    ["规划"]="制定详细的行动计划和时间表"
    
    # 优化类
    ["优化"]="识别改进空间，提出优化方案"
    ["改进"]="分析现有方案，提供具体改进建议"
    ["完善"]="补充遗漏，完善方案完整性"
    
    # 审核类
    ["审核"]="全面检查，识别问题和风险"
    ["审查"]="严谨审查，给出客观评价"
    ["验证"]="验证可行性和效果"
    
    # 决策类
    ["建议"]="综合分析，提供最佳建议"
    ["推荐"]="基于专业判断，推荐最优方案"
    ["选择"]="对比分析，帮助做出明智选择"
)

# ==================== L3: 格式层模板 ====================

declare -A FORMAT_TEMPLATES=(
    # 通用格式
    ["简洁"]="语言简洁，直击要点"
    ["详细"]="内容详尽，面面俱到"
    ["结构化"]="使用标题、分点等结构化表达"
    
    # 列表类
    ["清单"]="以清单形式呈现，便于执行"
    ["步骤"]="分步骤说明，每步清晰可操作"
    
    # 报告类
    ["摘要"]="先总结核心结论，再展开说明"
    ["报告"]="采用正式报告格式：背景、分析、结论、建议"
    
    # 对比类
    ["对比"]="采用表格对比，突出差异和优劣"
    ["矩阵"]="使用矩阵/二维表呈现多元关系"
    
    # 专业格式
    ["专业"]="使用专业术语，保持严谨性"
    ["易懂"]="用通俗语言解释专业概念"
)

# ==================== L4: 约束层模板 ====================

declare -A CONSTRAINT_TEMPLATES=(
    # 无约束
    ["无特定约束"]=""
    
    # 行业约束
    ["SaaS行业"]="聚焦SaaS产品特性、订阅模式、客户成功"
    ["电商行业"]="考虑电商流量、转化、复购等核心指标"
    ["金融行业"]="注重合规、风险控制、数据安全"
    ["教育行业"]="关注学习效果、用户体验、教育公平"
    ["医疗行业"]="遵守医疗法规、注重信息准确性"
    
    # 角色约束
    ["B端视角"]="面向企业客户，强调效率和投入产出比"
    ["C端视角"]="面向个人用户，注重体验和情感连接"
    ["管理层视角"]="面向决策者，聚焦战略价值和顶层设计"
    ["执行层视角"]="面向执行者，注重可操作性和细节"
    
    # 范围约束
    ["短期视角"]="聚焦当下问题和近期效果"
    ["长期视角"]="考虑可持续发展和尚期影响"
    ["成本敏感"]="优先考虑成本控制和资源效率"
    ["质量优先"]="质量为首要目标，成本次之"
    
    # 风格约束
    ["保守"]="稳健为主，控制风险"
    ["创新"]="鼓励创新突破，容忍合理风险"
    ["客观中立"]="保持客观，不偏不倚"
)

# ==================== 行业词典 ====================

declare -A INDUSTRY_MAP=(
    ["SaaS"]="SaaS行业" ["saas"]="SaaS行业"
    ["软件"]="软件行业" ["互联网"]="互联网行业"
    ["金融"]="金融行业" ["银行"]="金融行业" ["保险"]="金融行业"
    ["教育"]="教育行业" ["培训"]="教育行业"
    ["医疗"]="医疗行业" ["医药"]="医疗行业"
    ["电商"]="电商行业" ["零售"]="零售行业"
    ["制造"]="制造业" ["工厂"]="制造业"
    ["科技"]="科技行业" ["AI"]="科技行业"
    ["汽车"]="汽车行业"
    ["房地产"]="房地产行业"
    ["能源"]="能源行业"
    ["物流"]="物流行业"
    ["餐饮"]="餐饮行业"
    ["旅游"]="旅游行业"
    ["媒体"]="传媒行业"
    ["游戏"]="游戏行业"
)

# ==================== 领域词典 ====================

declare -A DOMAIN_MAP=(
    ["销售"]="销售管理" ["营销"]="市场营销"
    ["产品"]="产品设计" ["设计"]="产品设计"
    ["技术"]="技术研发" ["开发"]="技术研发"
    ["管理"]="团队管理" ["运营"]="运营优化"
    ["增长"]="业务增长" ["数据"]="数据分析"
    ["人力"]="人力资源" ["财务"]="财务管理"
    ["法务"]="法律合规"
)

# ==================== 场景词典 ====================

declare -A SCENE_MAP=(
    ["B端"]="B端视角" ["企业"]="B端视角" ["公司"]="B端视角"
    ["C端"]="C端视角" ["个人"]="C端视角"
    ["老板"]="管理层视角" ["领导"]="管理层视角" ["管理"]="管理层视角"
    ["执行"]="执行层视角" ["落地"]="执行层视角"
)

# ==================== 任务关键词映射 ====================

declare -A TASK_KEYWORDS=(
    ["分析"]="分析" ["分析一下"]="分析" ["评析"]="分析"
    ["调研"]="调研" ["调查"]="调研" ["研究"]="调研"
    ["评估"]="评估" ["评价"]="评估" ["判断"]="评估"
    ["生成"]="生成" ["写"]="生成" ["创作"]="生成" ["制定"]="生成"
    ["规划"]="规划" ["计划"]="规划" ["策划"]="规划"
    ["优化"]="优化" ["改进"]="优化" ["提升"]="优化"
    ["完善"]="完善" ["补充"]="完善"
    ["审核"]="审核" ["审查"]="审核" ["检查"]="审核"
    ["验证"]="验证" ["确认"]="验证"
    ["建议"]="建议" ["推荐"]="建议"
    ["帮我"]="通用" ["请"]="通用"
)

# ==================== 格式关键词映射 ====================

declare -A FORMAT_KEYWORDS=(
    ["简洁"]="简洁" ["简单"]="简洁" ["扼要"]="简洁"
    ["详细"]="详细" ["全面"]="详细"
    ["清单"]="清单" ["列表"]="清单" ["条目"]="清单"
    ["步骤"]="步骤" ["分步"]="步骤" ["流程"]="步骤"
    ["报告"]="报告" ["分析报告"]="报告"
    ["表格"]="对比" ["对比"]="对比"
)

# ==================== 约束关键词映射 ====================

declare -A CONSTRAINT_KEYWORDS=(
    ["短期"]="短期视角" ["近期"]="短期视角"
    ["长期"]="长期视角" ["长远"]="长期视角"
    ["成本"]="成本敏感" ["预算"]="成本敏感" ["省钱"]="成本敏感"
    ["质量"]="质量优先" ["品质"]="质量优先"
    ["创新"]="创新" ["突破"]="创新" ["新"]="创新"
    ["保守"]="保守" ["稳健"]="保守" ["稳妥"]="保守"
)

# ==================== 核心函数 ====================

# 提取实体
extract_entities() {
    local text="$1"
    local industry="" domain="" scene="" constraint=""
    
    # 提取行业
    for key in "${!INDUSTRY_MAP[@]}"; do
        if [[ "$text" == *"$key"* ]]; then
            industry="${INDUSTRY_MAP[$key]}"
            break
        fi
    done
    
    # 提取领域
    for key in "${!DOMAIN_MAP[@]}"; do
        if [[ "$text" == *"$key"* ]]; then
            domain="${DOMAIN_MAP[$key]}"
            break
        fi
    done
    
    # 提取场景
    for key in "${!SCENE_MAP[@]}"; do
        if [[ "$text" == *"$key"* ]]; then
            scene="${SCENE_MAP[$key]}"
            break
        fi
    done
    
    echo "${industry}|${domain}|${scene}"
}

# 识别任务类型
recognize_task() {
    local text="$1"
    local task="通用"
    
    for key in "${!TASK_KEYWORDS[@]}"; do
        if [[ "$text" == *"$key"* ]]; then
            task="${TASK_KEYWORDS[$key]}"
            break
        fi
    done
    
    echo "$task"
}

# 识别输出格式
recognize_format() {
    local text="$1"
    local format="结构化"
    
    for key in "${!FORMAT_KEYWORDS[@]}"; do
        if [[ "$text" == *"$key"* ]]; then
            format="${FORMAT_KEYWORDS[$key]}"
            break
        fi
    done
    
    echo "$format"
}

# 识别约束
recognize_constraint() {
    local text="$1"
    local constraint="无特定约束"
    
    for key in "${!CONSTRAINT_KEYWORDS[@]}"; do
        if [[ "$text" == *"$key"* ]]; then
            constraint="${CONSTRAINT_KEYWORDS[$key]}"
            break
        fi
    done
    
    echo "$constraint"
}

# 推断角色
infer_role() {
    local text="$1"
    local role="通用顾问"
    
    if [[ "$text" =~ 分析|评估|评测 ]]; then
        role="分析师"
    elif [[ "$text" =~ 策略|战略 ]]; then
        role="策略分析师"
    elif [[ "$text" =~ 营销|推广|品牌 ]]; then
        role="营销专家"
    elif [[ "$text" =~ 销售|客户 ]]; then
        role="销售顾问"
    elif [[ "$text" =~ 技术|开发|代码|程序 ]]; then
        role="技术专家"
    elif [[ "$text" =~ 运营|流程 ]]; then
        role="运营专家"
    elif [[ "$text" =~ 项目|计划|规划 ]]; then
        role="项目经理"
    elif [[ "$text" =~ 审核|审查|检查 ]]; then
        role="审核专家"
    elif [[ "$text" =~ 优化|改进|提升 ]]; then
        role="优化专家"
    elif [[ "$text" =~ 创意|策划|头脑风暴 ]]; then
        role="创意专家"
    fi
    
    echo "$role"
}

# 构建4层prompt
build_hierarchical_prompt() {
    local role="$1"
    local task="$2"
    local format="$3"
    local constraint="$4"
    local input="$5"
    local industry="$6"
    local domain="$7"
    
    # L1: 角色
    local l1="${ROLE_TEMPLATES[$role]:-${ROLE_TEMPLATES[通用顾问]}}"
    
    # L2: 任务
    local l2="${TASK_TEMPLATES[$task]:-${TASK_TEMPLATES[通用]}}"
    
    # L3: 格式
    local l3="${FORMAT_TEMPLATES[$format]:-${FORMAT_TEMPLATES[结构化]}}"
    
    # L4: 约束
    local l4=""
    if [[ -n "$constraint" && "$constraint" != "无特定约束" ]]; then
        l4="${CONSTRAINT_TEMPLATES[$constraint]}"
    fi
    
    # 构建上下文
    local context=""
    [[ -n "$industry" ]] && context="${industry}；"
    [[ -n "$domain" ]] && context="${context}${domain}；"
    [[ -n "$l4" ]] && context="${context}${l4}；"
    [[ -z "$context" ]] && context="无特定背景"
    
    # 组装4层prompt
    cat << EOF
[角色设定] ${l1}
[核心任务] ${l2}
[背景信息] ${context}
[输出要求] ${l3}
[用户需求] ${input}
EOF
}

# ==================== 主程序 ====================

main() {
    local input="$*"
    
    [ -z "$input" ] && { echo '{"need_optimization":false}'; exit 0; }
    
    local text_lower=$(echo "$input" | tr '[:upper:]' '[:lower:]')
    
    # 排除模式
    echo "$text_lower" | grep -qE "^你好|^在吗|^谢谢|^好的|^ok$|^hi$|^hello|^是$|^否$|^对$|^不$|^天气" && {
        echo "{\"need_optimization\":false,\"reason\":\"skip\"}"
        exit 0
    }
    
    # 提取实体
    local entity_result=$(extract_entities "$text_lower")
    local industry=$(echo "$entity_result" | cut -d'|' -f1)
    local domain=$(echo "$entity_result" | cut -d'|' -f2)
    local scene=$(echo "$entity_result" | cut -d'|' -f3)
    
    # 识别各层
    local task=$(recognize_task "$text_lower")
    local format=$(recognize_format "$text_lower")
    local constraint=$(recognize_constraint "$text_lower")
    local role=$(infer_role "$text_lower")
    
    # 如果场景被识别，优先级高于角色推断
    if [[ -n "$scene" ]]; then
        constraint="$scene"
    fi
    
    # 构建层级prompt
    local hierarchical_prompt
    hierarchical_prompt=$(build_hierarchical_prompt "$role" "$task" "$format" "$constraint" "$input" "$industry" "$domain")
    
    # 输出JSON
    local prompt_one=$(echo "$hierarchical_prompt" | tr '\n' ' ')
    
    # 返回结构化信息
    cat << EOF
{
  "need_optimization": true,
  "intent": "$task",
  "role": "$role",
  "format": "$format", 
  "constraint": "$constraint",
  "industry": "$industry",
  "domain": "$domain",
  "architecture": "hierarchical_4layer",
  "layers": {
    "L1_role": "$role",
    "L2_task": "$task",
    "L3_format": "$format",
    "L4_constraint": "$constraint"
  },
  "optimized_prompt": "$prompt_one"
}
EOF
}

main "$@"
