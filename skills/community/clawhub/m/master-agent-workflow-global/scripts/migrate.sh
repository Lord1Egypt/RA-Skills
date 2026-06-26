#!/bin/bash
# master-agent-workflow-global 迁移工具
# 版本: 2.0.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 技能目录
MAW_HOME="${MAW_HOME:-$HOME/.openclaw/global-skills/master-agent-workflow}"
CONFIG_DIR="$MAW_HOME/config"
TEMPLATE_DIR="$MAW_HOME/templates"
BACKUP_DIR="$MAW_HOME/backups"

# 确保目录存在
mkdir -p "$CONFIG_DIR" "$TEMPLATE_DIR" "$BACKUP_DIR"

# 帮助信息
show_help() {
    cat << EOF
master-agent-workflow-global 迁移工具 v2.0.0

用法: $0 [命令] [参数]

命令:
  export [名称]      导出配置到文件
  import <文件>      从文件导入配置
  backup             创建完整备份
  restore <备份>     从备份恢复
  list               列出所有备份
  clean [天数]       清理旧备份
  help               显示帮助信息

参数:
  --output <文件>    指定输出文件
  --include-state    包含运行状态
  --exclude-state    排除运行状态
  --force            强制操作
  --dry-run          试运行

示例:
  $0 export my-config --output config.json
  $0 import config.json
  $0 backup
  $0 list
  $0 clean 30

环境变量:
  MAW_HOME           技能根目录
  MAW_BACKUP_DIR     备份目录
EOF
}

# 导出配置
export_config() {
    local config_name="${1:-all}"
    local output_file="${2:-$BACKUP_DIR/maw-export-$(date +%Y%m%d-%H%M%S).json}"
    local include_state=false
    
    # 解析选项
    shift 2
    while [[ $# -gt 0 ]]; do
        case $1 in
            --include-state) include_state=true ;;
            --output) output_file="$2"; shift ;;
        esac
        shift
    done
    
    echo -e "${BLUE}导出配置: $config_name -> $output_file${NC}"
    
    # 创建导出数据
    local export_data="{
  \"version\": \"2.0.0\",
  \"export_time\": \"$(date -Iseconds)\",
  \"config_name\": \"$config_name\",
  \"include_state\": $include_state,
  \"configs\": {},
  \"templates\": []
}"
    
    # 导出配置
    if [[ "$config_name" == "all" || "$config_name" == "*" ]]; then
        # 导出所有配置
        for config_file in "$CONFIG_DIR"/*.json; do
            if [ -f "$config_file" ]; then
                local name=$(basename "$config_file" .json)
                local content=$(cat "$config_file")
                export_data=$(echo "$export_data" | jq --arg name "$name" --argjson content "$content" '.configs[$name] = $content')
            fi
        done
    elif [ -f "$CONFIG_DIR/$config_name.json" ]; then
        # 导出单个配置
        local content=$(cat "$CONFIG_DIR/$config_name.json")
        export_data=$(echo "$export_data" | jq --argjson content "$content" '.configs["'"$config_name"'"] = $content')
    else
        echo -e "${RED}配置不存在: $config_name${NC}"
        return 1
    fi
    
    # 导出模板
    for template_file in "$TEMPLATE_DIR"/*.json; do
        if [ -f "$template_file" ]; then
            local content=$(cat "$template_file")
            export_data=$(echo "$export_data" | jq --argjson content "$content" '.templates += [$content]')
        fi
    done
    
    # 导出状态（如果包含）
    if [ "$include_state" = true ]; then
        # 这里可以添加状态导出逻辑
        export_data=$(echo "$export_data" | jq '.state = {}')
    fi
    
    # 写入文件
    echo "$export_data" | jq '.' > "$output_file"
    
    echo -e "${GREEN}✓ 配置已导出到: $output_file${NC}"
    echo -e "  大小: $(wc -c < "$output_file") 字节"
    echo -e "  配置数: $(echo "$export_data" | jq '.configs | length')"
    echo -e "  模板数: $(echo "$export_data" | jq '.templates | length')"
}

# 导入配置
import_config() {
    local input_file="$1"
    local force=false
    
    # 解析选项
    shift
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force) force=true ;;
        esac
        shift
    done
    
    if [ ! -f "$input_file" ]; then
        echo -e "${RED}文件不存在: $input_file${NC}"
        return 1
    fi
    
    echo -e "${BLUE}导入配置: $input_file${NC}"
    
    # 读取导入数据
    local import_data=$(cat "$input_file")
    local version=$(echo "$import_data" | jq -r '.version // "unknown"')
    
    # 检查版本兼容性
    if [[ "$version" != "2.0.0" && "$version" != "1.0.0" ]]; then
        echo -e "${YELLOW}⚠ 警告: 不兼容的版本: $version${NC}"
        if [ "$force" != true ]; then
            read -p "是否继续? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                echo "导入取消"
                return 1
            fi
        fi
    fi
    
    # 导入配置
    local config_count=0
    echo "$import_data" | jq -r '.configs | to_entries[] | "\(.key)=\(.value | @json)"' | while IFS='=' read -r key value; do
        if [ -n "$key" ] && [ -n "$value" ]; then
            echo "$value" | jq '.' > "$CONFIG_DIR/$key.json"
            config_count=$((config_count + 1))
            echo -e "  ${GREEN}✓${NC} 导入配置: $key"
        fi
    done
    
    # 导入模板
    local template_count=0
    echo "$import_data" | jq -r '.templates[] | @json' | while read -r template; do
        if [ -n "$template" ]; then
            local name=$(echo "$template" | jq -r '.name')
            if [ -n "$name" ]; then
                echo "$template" | jq '.' > "$TEMPLATE_DIR/$name.json"
                template_count=$((template_count + 1))
                echo -e "  ${GREEN}✓${NC} 导入模板: $name"
            fi
        fi
    done
    
    echo -e "${GREEN}✓ 配置导入完成${NC}"
    echo -e "  导入配置数: $config_count"
    echo -e "  导入模板数: $template_count"
    echo -e "  版本: $version"
}

# 创建备份
create_backup() {
    local backup_name="maw-backup-$(date +%Y%m%d-%H%M%S)"
    local backup_file="$BACKUP_DIR/$backup_name.tar.gz"
    
    echo -e "${BLUE}创建完整备份: $backup_file${NC}"
    
    # 创建临时目录
    local temp_dir=$(mktemp -d)
    
    # 复制配置
    mkdir -p "$temp_dir/config"
    cp -r "$CONFIG_DIR"/* "$temp_dir/config/" 2>/dev/null || true
    
    # 复制模板
    mkdir -p "$temp_dir/templates"
    cp -r "$TEMPLATE_DIR"/* "$temp_dir/templates/" 2>/dev/null || true
    
    # 复制日志（可选）
    mkdir -p "$temp_dir/logs"
    cp -r "$MAW_HOME/logs"/* "$temp_dir/logs/" 2>/dev/null || true
    
    # 创建元数据
    cat > "$temp_dir/metadata.json" << EOF
{
  "backup_name": "$backup_name",
  "backup_time": "$(date -Iseconds)",
  "version": "2.0.0",
  "config_count": $(find "$temp_dir/config" -name "*.json" 2>/dev/null | wc -l),
  "template_count": $(find "$temp_dir/templates" -name "*.json" 2>/dev/null | wc -l)
}
EOF
    
    # 打包
    tar -czf "$backup_file" -C "$temp_dir" .
    
    # 清理临时目录
    rm -rf "$temp_dir"
    
    # 计算大小
    local size=$(du -h "$backup_file" | cut -f1)
    
    echo -e "${GREEN}✓ 备份创建完成${NC}"
    echo -e "  文件: $backup_file"
    echo -e "  大小: $size"
    echo -e "  配置数: $(find "$CONFIG_DIR" -name "*.json" 2>/dev/null | wc -l)"
    echo -e "  模板数: $(find "$TEMPLATE_DIR" -name "*.json" 2>/dev/null | wc -l)"
}

# 列出备份
list_backups() {
    echo -e "${BLUE}可用备份:${NC}"
    
    if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
        echo -e "  ${YELLOW}暂无备份${NC}"
        return
    fi
    
    for backup in "$BACKUP_DIR"/*.tar.gz; do
        if [ -f "$backup" ]; then
            local name=$(basename "$backup" .tar.gz)
            local size=$(du -h "$backup" | cut -f1)
            local mtime=$(stat -c %y "$backup" | cut -d' ' -f1)
            echo -e "  ${GREEN}•${NC} $name"
            echo -e "    大小: $size, 日期: $mtime"
        fi
    done
}

# 清理旧备份
clean_backups() {
    local days="${1:-30}"
    
    echo -e "${BLUE}清理 $days 天前的备份...${NC}"
    
    local count=0
    find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$days -type f | while read -r backup; do
        echo -e "  ${YELLOW}删除: $(basename "$backup")${NC}"
        rm "$backup"
        count=$((count + 1))
    done
    
    echo -e "${GREEN}✓ 清理完成，删除了 $count 个备份${NC}"
}

# 主函数
main() {
    local command="$1"
    
    case "$command" in
        export)
            shift
            export_config "$@"
            ;;
        import)
            shift
            import_config "$@"
            ;;
        backup)
            create_backup
            ;;
        restore)
            shift
            restore_backup "$@"
            ;;
        list)
            list_backups
            ;;
        clean)
            shift
            clean_backups "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}未知命令: $command${NC}"
            show_help
            exit 1
            ;;
    esac
}

# 检查依赖
if ! command -v jq &> /dev/null; then
    echo -e "${RED}错误: 需要 jq 命令${NC}"
    echo "请安装: brew install jq 或 apt-get install jq"
    exit 1
fi

# 运行主函数
main "$@"