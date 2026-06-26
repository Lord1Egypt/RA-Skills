#!/bin/bash

# Hive Task Router - 蜂巢智能任务分发系统
# 用途：根据任务类型自动选择模型和执行方式
# 版本：1.0.0
# 作者：qiongcao

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 模型配置（支持环境变量覆盖，通用所有模型提供商）
# 默认模型（可被环境变量覆盖）
MODEL_CODE="${HIVE_MODEL_CODE:-auto}"
MODEL_WEB="${HIVE_MODEL_WEB:-auto}"
MODEL_CHAT="${HIVE_MODEL_CHAT:-auto}"
MODEL_DOC="${HIVE_MODEL_DOC:-auto}"
MODEL_DATA="${HIVE_MODEL_DATA:-auto}"

# 模型验证模式：
# - HIVE_VALIDATE_MODEL=auto    → 自动检测可用模型（推荐）
# - HIVE_VALIDATE_MODEL=cache   → 首次验证，缓存 24 小时
# - HIVE_VALIDATE_MODEL=1       → 每次验证
# - HIVE_VALIDATE_MODEL=0       → 跳过验证
HIVE_VALIDATE_MODEL="${HIVE_VALIDATE_MODEL:-auto}"

# 模型配置说明：
# - provider 替换为你的模型提供商（如 bailian, openai, anthropic 等）
# - 或者设置环境变量自定义：
#   export HIVE_MODEL_CODE="bailian/qwen3-coder-plus"
#   export HIVE_MODEL_WEB="bailian/qwen3-max-2026-01-23"
#   export HIVE_MODEL_CHAT="bailian/qwen3.5-plus"

# 关键词定义（支持中英文）
CODE_KEYWORDS="代码 编程 脚本 函数 nodejs react vue typescript javascript html css 前端 后端 api 接口 调试 bug 优化 重构 code programming script function debug"
WEB_KEYWORDS="搜索 查找 调研 研究 github 项目 趋势 报告 分析 对比 评测 最新 2026 新闻 动态 search research github project trend report analysis latest news"
CHAT_KEYWORDS="你好 谢谢 再见 今天 明天 安排 计划 汇报 总结 提醒 备忘 hello thanks goodbye today tomorrow plan schedule summary reminder"
DOC_KEYWORDS="文档 说明 教程 指南 手册 readme wiki 注释 文档化 documentation guide tutorial manual readme wiki comment"
DATA_KEYWORDS="数据 分析 统计 图表 可视化 excel csv json 处理 转换 data analysis statistics chart visualization excel csv json processing"

# 模糊任务关键词（触发智能追问）
VAGUE_KEYWORDS="任务 帮忙 处理 搞定 完成 做一下 弄一下 这个 那个 一件事 一个东西 task help deal finish complete"

# 缓存文件路径（用于模型验证缓存）
CACHE_DIR="${HIVE_CACHE_DIR:-$HOME/.hive-task-router}"
CACHE_FILE="$CACHE_DIR/model_validation.cache"
CACHE_TTL="${HIVE_CACHE_TTL:-86400}"  # 缓存有效期：默认 24 小时

# 函数：自动检测可用模型
auto_detect_models() {
    echo -e "${BLUE}🔍 自动检测可用模型...${NC}"
    
    # 尝试使用 openclaw models list 检测
    local models_output=$(openclaw models list 2>/dev/null)
    
    if [ -z "$models_output" ]; then
        echo -e "${YELLOW}⚠️  无法自动检测模型，使用默认配置${NC}"
        return 1
    fi
    
    # 检测代码模型（优先 qwen3-coder-plus）
    if echo "$models_output" | grep -q "qwen3-coder-plus"; then
        MODEL_CODE=$(echo "$models_output" | grep "qwen3-coder-plus" | awk '{print $1}')
        MODEL_DATA="$MODEL_CODE"
    elif echo "$models_output" | grep -q "qwen3-coder"; then
        MODEL_CODE=$(echo "$models_output" | grep "qwen3-coder" | head -1 | awk '{print $1}')
        MODEL_DATA="$MODEL_CODE"
    fi
    
    # 检测 Web 模型（优先 qwen3-max）
    if echo "$models_output" | grep -q "qwen3-max"; then
        MODEL_WEB=$(echo "$models_output" | grep "qwen3-max" | awk '{print $1}')
    elif echo "$models_output" | grep -q "qwen3.*plus"; then
        MODEL_WEB=$(echo "$models_output" | grep "qwen3" | grep "plus" | head -1 | awk '{print $1}')
    fi
    
    # 检测聊天模型（优先 qwen3.5-plus）
    if echo "$models_output" | grep -q "qwen3.5-plus"; then
        MODEL_CHAT=$(echo "$models_output" | grep "qwen3.5-plus" | awk '{print $1}')
        MODEL_DOC="$MODEL_CHAT"
    elif echo "$models_output" | grep -q "qwen3.*plus"; then
        MODEL_CHAT=$(echo "$models_output" | grep "qwen3" | grep "plus" | head -1 | awk '{print $1}')
        MODEL_DOC="$MODEL_CHAT"
    fi
    
    # 显示检测结果
    echo -e "${GREEN}✅ 检测到可用模型：${NC}"
    echo "  💻 Code:  $MODEL_CODE"
    echo "  🔍 Web:   $MODEL_WEB"
    echo "  💬 Chat:  $MODEL_CHAT"
    echo "  📄 Doc:   $MODEL_DOC"
    echo "  📊 Data:  $MODEL_DATA"
    echo ""
    
    # 保存到缓存
    mkdir -p "$CACHE_DIR"
    echo "validated_at=$(date +%s)" > "$CACHE_FILE"
    echo "MODEL_CODE=$MODEL_CODE" >> "$CACHE_FILE"
    echo "MODEL_WEB=$MODEL_WEB" >> "$CACHE_FILE"
    echo "MODEL_CHAT=$MODEL_CHAT" >> "$CACHE_FILE"
    echo "MODEL_DOC=$MODEL_DOC" >> "$CACHE_FILE"
    echo "MODEL_DATA=$MODEL_DATA" >> "$CACHE_FILE"
    echo "auto_detected=1" >> "$CACHE_FILE"
    
    return 0
}

# 函数：加载缓存的模型配置
load_cached_models() {
    if [ -f "$CACHE_FILE" ]; then
        local cache_age=$(($(date +%s) - $(stat -f%m "$CACHE_FILE" 2>/dev/null || stat -c%Y "$CACHE_FILE" 2>/dev/null || echo 0)))
        
        if [ "$cache_age" -lt "$CACHE_TTL" ]; then
            # 缓存有效，加载配置
            source "$CACHE_FILE" 2>/dev/null
            if [ "$auto_detected" == "1" ]; then
                echo -e "${BLUE}✅ 使用缓存的模型配置（剩余有效期：$((CACHE_TTL - cache_age)) 秒）${NC}"
                return 0
            fi
        fi
    fi
    
    return 1  # 缓存无效或不存在
}

# 函数：验证模型配置
validate_models() {
    local validate_mode="$1"
    
    # 跳过验证模式
    if [ "$validate_mode" == "0" ] || [ "$validate_mode" == "none" ]; then
        return 0
    fi
    
    # 自动检测模式（推荐）
    if [ "$validate_mode" == "auto" ]; then
        # 先尝试加载缓存
        if load_cached_models; then
            return 0
        fi
        
        # 缓存无效，自动检测
        auto_detect_models
        return $?
    fi
    
    # 缓存模式
    if [ "$validate_mode" == "cache" ]; then
        if load_cached_models; then
            return 0
        fi
        
        # 缓存无效，检查是否包含占位符
        mkdir -p "$CACHE_DIR"
        
        local has_placeholder=0
        if [[ "$MODEL_CODE" == *"provider/"* ]] || \
           [[ "$MODEL_WEB" == *"provider/"* ]] || \
           [[ "$MODEL_CHAT" == *"provider/"* ]]; then
            has_placeholder=1
        fi
        
        if [ "$has_placeholder" -eq 1 ]; then
            echo -e "${YELLOW}⚠️  警告：模型配置包含占位符 'provider/'${NC}"
            echo ""
            echo -e "${GREEN}请在 ~/.bashrc 或 ~/.zshrc 中配置：${NC}"
            echo "  export HIVE_MODEL_CODE=\"bailian/qwen3-coder-plus\""
            echo "  export HIVE_MODEL_WEB=\"bailian/qwen3-max-2026-01-23\""
            echo "  export HIVE_MODEL_CHAT=\"bailian/qwen3.5-plus\""
            echo ""
            
            echo "validated_at=$(date +%s)" > "$CACHE_FILE"
            echo "has_placeholder=1" >> "$CACHE_FILE"
        else
            echo "validated_at=$(date +%s)" > "$CACHE_FILE"
            echo "has_placeholder=0" >> "$CACHE_FILE"
        fi
        
        return 0
    fi
    
    # 每次验证模式
    if [ "$validate_mode" == "1" ]; then
        local has_placeholder=0
        
        if [[ "$MODEL_CODE" == *"provider/"* ]] || \
           [[ "$MODEL_WEB" == *"provider/"* ]] || \
           [[ "$MODEL_CHAT" == *"provider/"* ]]; then
            has_placeholder=1
        fi
        
        if [ "$has_placeholder" -eq 1 ]; then
            echo -e "${YELLOW}⚠️  警告：模型配置包含占位符 'provider/'${NC}"
            echo ""
            echo -e "${GREEN}请在 ~/.bashrc 或 ~/.zshrc 中配置：${NC}"
            echo "  export HIVE_MODEL_CODE=\"bailian/qwen3-coder-plus\""
            echo "  export HIVE_MODEL_WEB=\"bailian/qwen3-max-2026-01-23\""
            echo "  export HIVE_MODEL_CHAT=\"bailian/qwen3.5-plus\""
            echo ""
        fi
        
        return 0
    fi
    
    return 0
}

# 函数：检查是否是模糊任务
is_vague_task() {
    local task="$1"
    local task_lower=$(echo "$task" | tr '[:upper:]' '[:lower:]')
    
    for keyword in $VAGUE_KEYWORDS; do
        if [[ "$task_lower" == *"$keyword"* ]]; then
            # 检查是否同时包含具体关键词
            for specific_keyword in $CODE_KEYWORDS $WEB_KEYWORDS $DATA_KEYWORDS $DOC_KEYWORDS; do
                if [[ "$task_lower" == *"$specific_keyword"* ]]; then
                    echo "no"  # 包含具体关键词，不是模糊任务
                    return 0
                fi
            done
            echo "yes"  # 只包含模糊关键词，是模糊任务
            return 0
        fi
    done
    
    echo "no"  # 不包含模糊关键词
}

# 函数：显示智能追问帮助
show_clarification_help() {
    echo -e "${YELLOW}================================${NC}"
    echo -e "${YELLOW}🤔 任务类型不明确，请提供更多信息${NC}"
    echo -e "${YELLOW}================================${NC}"
    echo ""
    echo -e "${GREEN}请问是什么类型的任务？${NC}"
    echo ""
    echo -e "${CYAN}💻 写代码/脚本？${NC}"
    echo "   例如：\"写个 Python 脚本\"、\"开发一个 API\""
    echo ""
    echo -e "${CYAN}🔍 搜索调研？${NC}"
    echo "   例如：\"搜索最新趋势\"、\"调研竞品\""
    echo ""
    echo -e "${CYAN}📊 数据处理？${NC}"
    echo "   例如：\"分析 Excel 数据\"、\"转换 JSON 格式\""
    echo ""
    echo -e "${CYAN}📄 写文档？${NC}"
    echo "   例如：\"写 API 文档\"、\"编写教程\""
    echo ""
    echo -e "${CYAN}💬 还是只是聊天？${NC}"
    echo "   例如：\"今天有什么安排\"、\"帮我总结一下\""
    echo ""
    echo -e "${GREEN}或者您直接告诉我具体内容，我来判断！${NC}"
    echo ""
}

# 函数：识别任务类型（按优先级：web > code > data > doc > chat）
identify_task_type() {
    local task="$1"
    local task_lower=$(echo "$task" | tr '[:upper:]' '[:lower:]')
    
    # 优先级 1：web（搜索、调研等）- 优先匹配
    for keyword in $WEB_KEYWORDS; do
        if [[ "$task_lower" == *"$keyword"* ]]; then
            echo "web"
            return 0
        fi
    done
    
    # 优先级 2：code（代码、编程等）
    for keyword in $CODE_KEYWORDS; do
        if [[ "$task_lower" == *"$keyword"* ]]; then
            echo "code"
            return 0
        fi
    done
    
    # 优先级 3：data（数据分析）
    for keyword in $DATA_KEYWORDS; do
        if [[ "$task_lower" == *"$keyword"* ]]; then
            echo "data"
            return 0
        fi
    done
    
    # 优先级 4：doc（文档）
    for keyword in $DOC_KEYWORDS; do
        if [[ "$task_lower" == *"$keyword"* ]]; then
            echo "doc"
            return 0
        fi
    done
    
    # 优先级 5：chat（日常对话）
    for keyword in $CHAT_KEYWORDS; do
        if [[ "$task_lower" == *"$keyword"* ]]; then
            echo "chat"
            return 0
        fi
    done
    
    # 默认返回 chat
    echo "chat"
}

# 函数：获取推荐模型
get_model() {
    local task_type="$1"
    
    case "$task_type" in
        code)
            echo "$MODEL_CODE"
            ;;
        web)
            echo "$MODEL_WEB"
            ;;
        chat)
            echo "$MODEL_CHAT"
            ;;
        doc)
            echo "$MODEL_DOC"
            ;;
        data)
            echo "$MODEL_DATA"
            ;;
        *)
            echo "$MODEL_CHAT"
            ;;
    esac
}

# 函数：获取执行方式
get_execution_mode() {
    local task_type="$1"
    
    case "$task_type" in
        chat)
            echo "main_session"
            ;;
        *)
            echo "subagent"
            ;;
    esac
}

# 函数：获取任务类型图标和描述
get_task_description() {
    local task_type="$1"
    
    case "$task_type" in
        code)
            echo -e "${CYAN}📦 代码任务${NC} - 使用 qwen3-coder-plus 模型\n   适合：Node.js、前端代码、脚本编写、API 开发、调试优化"
            ;;
        web)
            echo -e "${CYAN}🔍 搜索调研${NC} - 使用 qwen3-max-2026-01-23 模型\n   适合：GitHub 搜索、技术调研、趋势分析、竞品对比"
            ;;
        chat)
            echo -e "${CYAN}💬 日常对话${NC} - 使用 qwen3.5-plus 模型\n   适合：聊天、汇报、协调、日常任务、日程管理"
            ;;
        doc)
            echo -e "${CYAN}📄 文档任务${NC} - 使用 qwen3.5-plus 模型\n   适合：文档编写、说明生成、教程整理、Wiki 编写"
            ;;
        data)
            echo -e "${CYAN}📊 数据分析${NC} - 使用 qwen3-coder-plus 模型\n   适合：数据处理、统计分析、图表生成、格式转换"
            ;;
    esac
}

# 函数：显示帮助信息
show_help() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}蜂巢智能任务分发系统 - 路由助手${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
    echo -e "${GREEN}用法:${NC} $0 <任务描述>"
    echo ""
    echo -e "${GREEN}示例:${NC}"
    echo "  $0 \"帮我写一个 Node.js 脚本\""
    echo "  $0 \"搜索最新的 React 趋势\""
    echo "  $0 \"分析这个 Excel 数据\""
    echo "  $0 \"为项目编写 README 文档\""
    echo "  $0 \"今天有什么安排\""
    echo ""
    echo -e "${GREEN}任务类型优先级:${NC} web > code > data > doc > chat"
    echo ""
    echo -e "${GREEN}相关文档:${NC}"
    echo "  SKILL.md - 完整技能文档"
    echo "  config.md - 配置说明"
    echo ""
}

# 函数：生成执行命令
generate_command() {
    local task_type="$1"
    local model="$2"
    local exec_mode="$3"
    local task="$4"
    
    echo ""
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}推荐执行命令:${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
    
    if [ "$exec_mode" == "subagent" ]; then
        echo -e "${YELLOW}# 子代理模式（并行执行，不阻塞主会话）${NC}"
        echo "openclaw sessions spawn \\"
        echo "  --mode run \\"
        echo "  --runtime subagent \\"
        echo "  --model $model \\"
        echo "  --task \"$task\""
    else
        echo -e "${YELLOW}# 主会话模式（快速响应）${NC}"
        echo "openclaw agent \\"
        echo "  --session-id agent:main:chat \\"
        echo "  --model $model \\"
        echo "  --message \"$task\""
    fi
    
    echo ""
}

# 主函数
main() {
    # 检查参数
    if [ -z "$1" ]; then
        show_help
        exit 0
    fi
    
    # 处理帮助参数
    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_help
        exit 0
    fi
    
    # 验证模型配置（根据 HIVE_VALIDATE_MODEL 设置）
    validate_models "$HIVE_VALIDATE_MODEL"
    
    local task="$*"
    
    # 检查是否是模糊任务
    local is_vague=$(is_vague_task "$task")
    if [ "$is_vague" == "yes" ]; then
        show_clarification_help
        exit 0
    fi
    
    local task_type=$(identify_task_type "$task")
    local model=$(get_model "$task_type")
    local exec_mode=$(get_execution_mode "$task_type")
    
    # 输出分析结果
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}蜂巢智能任务分发系统 - 路由分析${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
    echo -e "${GREEN}任务描述:${NC} $task"
    echo -e "${GREEN}任务类型:${NC} ${CYAN}$task_type${NC}"
    echo -e "${GREEN}推荐模型:${NC} ${YELLOW}$model${NC}"
    echo -e "${GREEN}执行方式:${NC} ${YELLOW}$exec_mode${NC}"
    echo ""
    
    # 输出任务描述
    get_task_description "$task_type"
    
    echo ""
    
    # 生成执行命令
    generate_command "$task_type" "$model" "$exec_mode" "$task"
    
    # 输出提示信息
    echo -e "${GREEN}💡 提示:${NC}"
    if [ "$exec_mode" == "subagent" ]; then
        echo "   - 子代理适合长任务，可并行执行多个任务"
        echo "   - 使用 & 符号可同时启动多个子代理"
        echo "   - 建议最大并发数：5-10 个子代理"
    else
        echo "   - 主会话适合短任务，快速响应"
        echo "   - 日常对话、简单查询使用此模式"
    fi
    echo ""
}

# 执行主函数
main "$@"
