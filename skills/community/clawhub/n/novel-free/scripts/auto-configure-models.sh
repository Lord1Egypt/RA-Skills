#!/usr/bin/env bash
#
# novel-free 自动模型配置脚本
# 自动从 openclaw.json 读取可用模型并配置项目
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 查找 openclaw.json
find_openclaw_json() {
    local paths=(
        "$HOME/.openclaw/openclaw.json"
        "/root/.openclaw/openclaw.json"
        "./openclaw.json"
        "/etc/openclaw/openclaw.json"
    )
    
    for path in "${paths[@]}"; do
        if [[ -f "$path" ]]; then
            echo "$path"
            return 0
        fi
    done
    return 1
}

# 从 openclaw.json 提取模型列表
extract_models() {
    local config_file="$1"
    
    if ! command -v jq &> /dev/null; then
        echo -e "${YELLOW}警告: jq 命令未安装，使用简化解析${NC}"
        # 简化解析
        grep -o '"id"[[:space:]]*:[[:space:]]*"[^"]*"' "$config_file" | \
            grep -v "default" | \
            sed 's/.*"id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/' | \
            sort -u
        return
    fi
    
    # 使用 jq 提取所有模型ID
    jq -r '
        .models.providers[]?.models[]?.id // empty
    ' "$config_file" 2>/dev/null || echo ""
}

# 选择模型
select_model() {
    local models=("$@")
    local selected=""
    
    if [[ ${#models[@]} -eq 0 ]]; then
        echo -e "${RED}错误: 未找到可用模型${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}可用模型列表:${NC}"
    for i in "${!models[@]}"; do
        echo "  $((i+1)). ${models[$i]}"
    done
    
    # 智能推荐
    echo ""
    echo -e "${YELLOW}智能推荐:${NC}"
    echo "  写作主模型：${models[0]} (通常第一个是主模型)"
    echo "  OOC检查模型：${models[0]} (同主模型)"
    echo "  终审模型：${models[0]} (同主模型)"
    
    # 自动选择第一个模型
    selected="${models[0]}"
    
    # 确定provider
    local provider=""
    if [[ "$selected" == *"/"* ]]; then
        echo "$selected"  # 已经是完整格式
    else
        # 从配置文件确定provider
        local config_file="$1"
        if [[ -f "$config_file" ]] && command -v jq &> /dev/null; then
            # 尝试查找provider
            provider=$(jq -r --arg model "$selected" '
                .models.providers | to_entries[] | 
                select(.value.models[]?.id == $model) | .key
            ' "$config_file" 2>/dev/null | head -1)
        fi
        
        if [[ -n "$provider" ]]; then
            echo "${provider}/${selected}"
        else
            echo "unknown/${selected}"
        fi
    fi
}

# 主函数
main() {
    local project_dir="$1"
    
    if [[ -z "$project_dir" ]] || [[ ! -d "$project_dir" ]]; then
        echo -e "${RED}用法: $0 <项目目录>${NC}"
        echo -e "${YELLOW}示例: $0 /path/to/novel-project${NC}"
        exit 1
    fi
    
    local config_file="$project_dir/meta/config.md"
    if [[ ! -f "$config_file" ]]; then
        echo -e "${RED}错误: 未找到配置文件 $config_file${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}开始自动配置模型...${NC}"
    echo -e "项目目录: $project_dir"
    
    # 查找 openclaw.json
    local openclaw_json
    openclaw_json=$(find_openclaw_json)
    if [[ -z "$openclaw_json" ]]; then
        echo -e "${YELLOW}警告: 未找到 openclaw.json，使用默认配置${NC}"
        return 0
    fi
    
    echo -e "找到配置文件: $openclaw_json"
    
    # 提取模型
    echo -e "${BLUE}提取可用模型...${NC}"
    local models
    mapfile -t models < <(extract_models "$openclaw_json")
    
    if [[ ${#models[@]} -eq 0 ]]; then
        echo -e "${YELLOW}警告: 未提取到模型，使用占位符${NC}"
        models=("provider/model-id")
    fi
    
    echo -e "${GREEN}找到 ${#models[@]} 个模型${NC}"
    
    # 选择主模型
    local main_model
    main_model=$(select_model "${models[@]}")
    echo -e "${GREEN}选择主模型: $main_model${NC}"
    
    # 更新配置文件
    echo -e "${BLUE}更新配置文件...${NC}"
    
    # 创建备份
    cp "$config_file" "$config_file.bak"
    
    # 替换占位符
    # 注意：需要转义斜杠
    local escaped_model="${main_model//\//\\/}"
    
    sed -i \
        -e "s/provider\/model-id/$escaped_model/g" \
        "$config_file"
    
    # 更新 agent-registry.json
    local registry_file="$project_dir/meta/agent-registry.json"
    if [[ -f "$registry_file" ]]; then
        sed -i "s/{{worldbuilder_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{characterDesigner_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{outlinePlanner_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{chapterOutliner_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{mainWriter_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{oocGuardian_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{battleAgent_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{finalReviewer_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{readerSimulator_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{styleAnchorGenerator_model}}/$escaped_model/g" "$registry_file"
        sed -i "s/{{rollingSummarizer_model}}/$escaped_model/g" "$registry_file"
    fi
    
    echo -e "${GREEN}✅ 模型配置完成！${NC}"
    echo -e "${YELLOW}备份文件: $config_file.bak${NC}"
    echo -e "${BLUE}配置摘要:${NC}"
    echo "  所有Agent使用同一模型: $main_model"
    echo "  如需差异化配置，请手动编辑 $config_file"
}

main "$@"