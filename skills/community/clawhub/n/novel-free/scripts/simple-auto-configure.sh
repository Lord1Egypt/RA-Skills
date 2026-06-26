#!/usr/bin/env bash
#
# 简化的自动模型配置脚本
# 无颜色代码，更可靠
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 主函数
main() {
    local project_dir="$1"
    
    if [[ -z "$project_dir" ]] || [[ ! -d "$project_dir" ]]; then
        echo "用法: $0 <项目目录>"
        echo "示例: $0 /path/to/novel-project"
        exit 1
    fi
    
    local config_file="$project_dir/meta/config.md"
    if [[ ! -f "$config_file" ]]; then
        echo "错误: 未找到配置文件 $config_file"
        exit 1
    fi
    
    echo "开始自动配置模型..."
    echo "项目目录: $project_dir"
    
    # 使用当前会话的模型作为默认
    local default_model="infini-ai/deepseek-v3.2-thinking"
    
    echo "使用默认模型: $default_model"
    
    # 创建备份
    cp "$config_file" "$config_file.bak"
    
    # 替换占位符 - 使用不同的分隔符避免转义问题
    sed -i "s|provider/model-id|$default_model|g" "$config_file"
    
    # 更新 agent-registry.json
    local registry_file="$project_dir/meta/agent-registry.json"
    if [[ -f "$registry_file" ]]; then
        cp "$registry_file" "$registry_file.bak"
        sed -i "s|{{worldbuilder_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{characterDesigner_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{outlinePlanner_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{chapterOutliner_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{mainWriter_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{oocGuardian_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{battleAgent_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{finalReviewer_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{readerSimulator_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{styleAnchorGenerator_model}}|$default_model|g" "$registry_file"
        sed -i "s|{{rollingSummarizer_model}}|$default_model|g" "$registry_file"
    fi
    
    echo "✅ 模型配置完成！"
    echo "备份文件: $config_file.bak"
    echo "配置摘要:"
    echo "  所有Agent使用同一模型: $default_model"
    echo "  如需差异化配置，请手动编辑 $config_file"
}

main "$@"