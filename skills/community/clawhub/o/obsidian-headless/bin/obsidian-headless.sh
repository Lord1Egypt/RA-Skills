#!/bin/bash
# obsidian-headless.sh - 无头 Obsidian 自然语言控制工具
# 在无显示器环境下通过自然语言指令管理 Obsidian 笔记仓库

# 严格模式（除了未绑定变量检查，因为 OBSIDIAN_VAULT 可能未设置）
set -eo pipefail

# 检查依赖
check_dependencies() {
    local missing=()
    
    for cmd in find grep mkdir touch rm cat date chmod head tail cut awk; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done
    
    # realpath 检查（macOS 可能没有这个命令）
    if ! command -v realpath &>/dev/null; then
        printf '%b警告: realpath 命令未找到（macOS 用户可安装 coreutils）%b\n' "$YELLOW" "$NC" >&2
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        printf '%b错误: 缺少必要命令: %s%b\n' "$RED" "${missing[*]}" "$NC" >&2
        printf '请安装缺失的依赖后重试\n' >&2
        exit 1
    fi
}

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置文件路径
CONFIG_DIR="${HOME}/.config/obsidian-headless"
CONFIG_FILE="${CONFIG_DIR}/vault-path"

# 检查依赖
check_dependencies

# 获取仓库路径
get_vault_path() {
    # 1. 优先使用环境变量
    if [[ -n "${OBSIDIAN_VAULT}" ]]; then
        echo "${OBSIDIAN_VAULT}"
        return 0
    fi
    
    # 2. 使用保存的配置
    if [[ -f "${CONFIG_FILE}" ]]; then
        local saved_path=$(cat "${CONFIG_FILE}" 2>/dev/null | tr -d '\n')
        if [[ -d "${saved_path}" ]]; then
            echo "${saved_path}"
            return 0
        fi
    fi
    
    # 3. 首次使用，提示用户输入
    echo "首次使用 Obsidian Headless" >&2
    echo "==========================" >&2
    echo >&2
    
    while true; do
        read -p "请输入 Obsidian 仓库路径: " user_path
        
        # 展开 ~ 为 HOME
        user_path="${user_path/#\~/${HOME}}"
        
        if [[ -z "${user_path}" ]]; then
            echo "路径不能为空，请重新输入" >&2
            continue
        fi
        
        if [[ ! -d "${user_path}" ]]; then
            echo "目录不存在: ${user_path}" >&2
            read -p "是否创建该目录? (y/N): " create_dir
            if [[ "${create_dir}" == "y" || "${create_dir}" == "Y" ]]; then
                mkdir -p "${user_path}" && echo "已创建目录: ${user_path}" >&2
            else
                continue
            fi
        fi
        
        # 验证是否是有效的 Obsidian 仓库（检查是否有 .obsidian 文件夹或 .md 文件）
        if [[ -d "${user_path}/.obsidian" ]] || [[ $(find "${user_path}" -name "*.md" -type f 2>/dev/null | head -1) ]]; then
            echo "✓ 有效的 Obsidian 仓库" >&2
        else
            echo "警告: 该目录看起来不像 Obsidian 仓库（没有 .obsidian 文件夹或 .md 文件）" >&2
            read -p "仍要使用这个目录吗? (y/N): " confirm
            if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
                continue
            fi
        fi
        
        # 保存配置
        mkdir -p "${CONFIG_DIR}"
        echo "${user_path}" > "${CONFIG_FILE}"
        # 设置配置文件权限（644: 所有者可读写，其他人只读）
        chmod 644 "${CONFIG_FILE}"
        echo >&2
        echo "✓ 已保存配置到: ${CONFIG_FILE}" >&2
        echo "下次使用会自动加载此路径" >&2
        echo "如需更改，可: 1) 设置环境变量 OBSIDIAN_VAULT，或 2) 删除 ${CONFIG_FILE}" >&2
        echo >&2
        
        echo "${user_path}"
        return 0
    done
}

VAULT_PATH=$(get_vault_path)

TODAY=$(date +%Y-%m-%d)
DAILY_NOTE="${VAULT_PATH}/日记/${TODAY}.md"

# 安全函数：验证文件名
validate_filename() {
    local name="$1"
    # 检查是否包含路径遍历
    if [[ "$name" == *".."* ]]; then
        printf '%b错误: 文件名不能包含 ".."%b\n' "$RED" "$NC" >&2
        return 1
    fi
    # 检查是否包含控制字符
    if [[ "$name" =~ [[:cntrl:]] ]]; then
        printf '%b错误: 文件名包含非法字符%b\n' "$RED" "$NC" >&2
        return 1
    fi
    return 0
}

# 安全函数：验证路径在仓库内
validate_path_in_vault() {
    local filepath="$1"
    local abs_filepath
    local abs_vault
    
    abs_filepath=$(realpath -m "$filepath" 2>/dev/null || echo "$filepath")
    abs_vault=$(realpath "$VAULT_PATH" 2>/dev/null || echo "$VAULT_PATH")
    
    if [[ "$abs_filepath" != "$abs_vault"* ]]; then
        printf '%b错误: 文件路径必须在仓库内%b\n' "$RED" "$NC" >&2
        return 1
    fi
    return 0
}

# 错误退出函数
error_exit() {
    printf '%b错误: %s%b\n' "$RED" "$1" "$NC" >&2
    exit 1
}

# 显示帮助
show_help() {
    cat << 'EOF'
Obsidian Headless - 无头 Obsidian 自然语言控制工具

在无显示器/无 GUI 环境下管理 Obsidian 笔记仓库

支持的指令格式（obs 前缀可选，大小写不敏感）:
  obs创建笔记 [文件名] [内容]     或  obs 创建笔记 / obs-创建笔记 / OBS创建笔记
  obs删除笔记 [文件名]            或  obs 删除笔记 / obs-删除笔记
  obs查看笔记 [文件名]            或  obs 查看笔记 / obs-查看笔记
  obs搜索标题 [关键词]            或  obs 搜索标题 / obs-搜索标题
  obs搜索内容 [关键词]            或  obs 搜索内容 / obs-搜索内容
  obs模糊搜索 [关键词]            或  obs 模糊搜索 / obs-模糊搜索
  obs今天日记 [可选内容]          或  obs 今天日记 / obs-今天日记
  obs列出所有                     或  obs 列出所有 / obs-列出所有
  obs列出文件夹                   或  obs 列出文件夹 / obs-列出文件夹
  obs最近笔记                     或  obs 最近笔记 / obs-最近笔记
  obs修改库路径                   或  obs 修改库路径 / obs-修改库路径

配置方式（优先级从高到低）:
  1. 环境变量 OBSIDIAN_VAULT
  2. 配置文件 ~/.config/obsidian-headless/vault-path
  3. 首次使用时交互式输入

示例:
  obs创建笔记 待办清单 今天要完成: 1. xxx 2. yyy
  obs 搜索内容 home assistant
  OBS-模糊搜索 openclaw
  obs今天日记
  obs 删除笔记 旧笔记
  obs-修改库路径
EOF
}

# 创建笔记
create_note() {
    local title="$1"
    local content="${2:-}"
    
    if [[ -z "$title" ]]; then
        printf '%b错误: 需要提供文件名%b\n' "$RED" "$NC" >&2
        return 1
    fi
    
    # 安全验证：检查文件名
    if ! validate_filename "$title"; then
        return 1
    fi
    
    # 添加 .md 后缀（如果没有）
    [[ "$title" != *.md ]] && title="${title}.md"
    
    local filepath="${VAULT_PATH}/${title}"
    
    # 安全验证：确保路径在仓库内
    if ! validate_path_in_vault "$filepath"; then
        return 1
    fi
    
    # 检查是否已存在
    if [[ -f "$filepath" ]]; then
        printf '%b警告: 笔记已存在: %s%b\n' "$YELLOW" "$title" "$NC" >&2
        printf '文件路径: %s\n' "$filepath" >&2
        return 1
    fi
    
    # 创建目录（如果不存在）
    mkdir -p "$(dirname "$filepath")"
    
    # 提取文件名（不含路径）用于显示
    local note_title=$(basename "$title" .md)
    
    # 创建笔记
    # 如果内容为空，创建空文件；如果有内容，直接使用用户内容
    if [[ -n "$content" ]]; then
        printf '%s\n' "$content" > "$filepath"
    else
        touch "$filepath"
    fi
    
    echo -e "${GREEN}✓ 创建笔记成功${NC}"
    echo "文件名: ${note_title}"
    echo "路径: $filepath"
}

# 查找笔记（返回文件路径）
find_note() {
    local title="$1"
    local exact="${2:-false}"
    
    if [[ -z "$title" ]]; then
        return 1
    fi
    
    # 尝试精确匹配
    [[ "$title" != *.md ]] && local title_md="${title}.md" || local title_md="$title"
    
    local exact_match=$(find "$VAULT_PATH" -name "$title_md" -type f 2>/dev/null | head -1)
    
    if [[ -n "$exact_match" ]]; then
        echo "$exact_match"
        return 0
    fi
    
    # 模糊匹配
    if [[ "$exact" != "true" ]]; then
        local fuzzy_matches=$(find "$VAULT_PATH" -iname "*${title}*" -name "*.md" -type f 2>/dev/null)
        
        if [[ -n "$fuzzy_matches" ]]; then
            local count=$(echo "$fuzzy_matches" | wc -l)
            
            if [[ $count -eq 1 ]]; then
                echo "$fuzzy_matches"
                return 0
            else
                # 返回多个匹配（用于删除确认）
                echo "$fuzzy_matches"
                return 2
            fi
        fi
    fi
    
    return 1
}

# 删除笔记（带确认）
delete_note() {
    local title="$1"
    
    if [[ -z "$title" ]]; then
        echo -e "${RED}错误: 需要提供笔记标题${NC}"
        return 1
    fi
    
    local result=$(find_note "$title" false)
    local exit_code=$?
    
    if [[ $exit_code -eq 1 ]]; then
        echo -e "${RED}未找到笔记: $title${NC}"
        return 1
    fi
    
    if [[ $exit_code -eq 0 ]]; then
        # 只有一个匹配
        local filepath="$result"
        local basename=$(basename "$filepath" .md)
        
        echo -e "${YELLOW}即将删除笔记:${NC}"
        echo "  标题: $basename"
        echo "  路径: $filepath"
        echo
        
        # 显示笔记内容预览
        local lines=$(wc -l < "$filepath")
        echo "  内容预览 (共 $lines 行):"
        head -3 "$filepath" | sed 's/^/    /'
        [[ $lines -gt 3 ]] && echo "    ..."
        echo
        
        echo "请回复确认:"
        echo "  [Y] 确认删除"
        echo "  [N] 取消"
        echo
        echo "DELETE_CONFIRM:$filepath"
        return 0
    fi
    
    if [[ $exit_code -eq 2 ]]; then
        # 多个匹配
        echo -e "${YELLOW}找到多个匹配的笔记:${NC}"
        echo
        
        local i=1
        while IFS= read -r filepath; do
            local basename=$(basename "$filepath" .md)
            local dir=$(dirname "$filepath" | sed "s|${VAULT_PATH}/||")
            local lines=$(wc -l < "$filepath")
            
            echo "  [$i] $basename"
            echo "      位置: $dir/"
            echo "      大小: $lines 行"
            echo
            
            ((i++))
        done <<< "$result"
        
        echo "请回复要删除的笔记编号 (或 0 取消):"
        echo "MULTI_DELETE_CONFIRM:$result"
        return 0
    fi
}

# 执行删除（由 agent 调用）
execute_delete() {
    local filepath="$1"
    
    # 安全验证：确保路径在仓库内
    if ! validate_path_in_vault "$filepath"; then
        return 1
    fi
    
    if [[ ! -f "$filepath" ]]; then
        printf '%b错误: 文件不存在: %s%b\n' "$RED" "$filepath" "$NC" >&2
        return 1
    fi
    
    # 使用 -- 防止文件名以 - 开头
    rm -- "$filepath"
    
    if [[ $? -eq 0 ]]; then
        printf '%b✓ 已删除笔记%b\n' "$GREEN" "$NC"
        printf '  路径: %s\n' "$filepath"
        return 0
    else
        printf '%b✗ 删除失败%b\n' "$RED" "$NC" >&2
        return 1
    fi
}

# 查看笔记内容
view_note() {
    local title="$1"
    
    if [[ -z "$title" ]]; then
        echo -e "${RED}错误: 需要提供笔记标题${NC}"
        return 1
    fi
    
    local result=$(find_note "$title" false)
    local exit_code=$?
    
    if [[ $exit_code -eq 1 ]]; then
        echo -e "${RED}未找到笔记: $title${NC}"
        return 1
    fi
    
    if [[ $exit_code -eq 2 ]]; then
        # 多个匹配
        echo -e "${YELLOW}找到多个匹配的笔记，请指定更精确的标题:${NC}"
        echo "$result" | sed "s|${VAULT_PATH}/||" | nl
        return 1
    fi
    
    local filepath="$result"
    local basename=$(basename "$filepath")
    
    echo -e "${GREEN}=== $basename ===${NC}"
    echo
    cat "$filepath"
}

# 搜索标题
search_titles() {
    local keyword="$1"
    
    if [[ -z "$keyword" ]]; then
        echo -e "${RED}错误: 需要提供搜索关键词${NC}"
        return 1
    fi
    
    echo -e "${GREEN}搜索标题包含 '$keyword' 的笔记:${NC}"
    echo
    
    local results=$(find "$VAULT_PATH" -iname "*${keyword}*" -name "*.md" -type f 2>/dev/null)
    
    if [[ -z "$results" ]]; then
        echo "  (未找到匹配)"
        return 0
    fi
    
    echo "$results" | sed "s|${VAULT_PATH}/||" | nl
}

# 搜索内容
search_content() {
    local keyword="$1"
    
    if [[ -z "$keyword" ]]; then
        echo -e "${RED}错误: 需要提供搜索关键词${NC}"
        return 1
    fi
    
    echo -e "${GREEN}搜索内容包含 '$keyword' 的笔记:${NC}"
    echo
    
    local results
    if command -v rg &>/dev/null; then
        results=$(rg -i "$keyword" "$VAULT_PATH" -t md -l 2>/dev/null)
    else
        results=$(grep -ril "$keyword" "$VAULT_PATH" --include="*.md" 2>/dev/null)
    fi
    
    if [[ -z "$results" ]]; then
        echo "  (未找到匹配)"
        return 0
    fi
    
    echo "$results" | sed "s|${VAULT_PATH}/||" | nl
}

# 模糊搜索（标题+内容）
fuzzy_search() {
    local keyword="$1"
    
    if [[ -z "$keyword" ]]; then
        echo -e "${RED}错误: 需要提供搜索关键词${NC}"
        return 1
    fi
    
    echo -e "${GREEN}模糊搜索 '$keyword':${NC}"
    echo
    
    # 标题匹配
    echo -e "${YELLOW}--- 标题匹配 ---${NC}"
    local title_results=$(find "$VAULT_PATH" -iname "*${keyword}*" -name "*.md" -type f 2>/dev/null | head -10)
    
    if [[ -z "$title_results" ]]; then
        echo "  (无)"
    else
        echo "$title_results" | sed "s|${VAULT_PATH}/||" | nl
    fi
    
    echo
    
    # 内容匹配
    echo -e "${YELLOW}--- 内容匹配 ---${NC}"
    local content_results
    if command -v rg &>/dev/null; then
        content_results=$(rg -i "$keyword" "$VAULT_PATH" -t md -l 2>/dev/null | head -10)
    else
        content_results=$(grep -ril "$keyword" "$VAULT_PATH" --include="*.md" 2>/dev/null | head -10)
    fi
    
    if [[ -z "$content_results" ]]; then
        echo "  (无)"
    else
        echo "$content_results" | sed "s|${VAULT_PATH}/||" | nl
    fi
}

# 创建今天的日记
daily_note() {
    local content="${1:-}"
    
    # 创建日记文件夹（如果不存在）
    mkdir -p "$(dirname "$DAILY_NOTE")"
    
    if [[ -f "$DAILY_NOTE" ]]; then
        echo -e "${YELLOW}今天的日记已存在${NC}"
        if [[ -n "$content" ]]; then
            echo -e "\n$content" >> "$DAILY_NOTE"
            echo -e "${GREEN}✓ 已追加内容${NC}"
        fi
    else
        cat > "$DAILY_NOTE" << EOF
# ${TODAY}

${content}

## 待办事项
- [ ] 

## 笔记

EOF
        echo -e "${GREEN}✓ 创建今天日记${NC}"
    fi
    
    echo "  路径: $DAILY_NOTE"
}

# 列出所有笔记
list_all() {
    echo -e "${GREEN}所有笔记 (${VAULT_PATH}):${NC}"
    echo
    
    local count=$(find "$VAULT_PATH" -name "*.md" -type f 2>/dev/null | wc -l)
    echo "共 $count 篇笔记"
    echo
    
    find "$VAULT_PATH" -name "*.md" -type f 2>/dev/null | sed "s|${VAULT_PATH}/||" | sort | nl
}

# 列出文件夹
list_folders() {
    echo -e "${GREEN}所有文件夹:${NC}"
    echo
    
    find "$VAULT_PATH" -type d 2>/dev/null | \
        sed "s|${VAULT_PATH}/||" | \
        grep -v '^$' | \
        grep -v '^\.obsidian' | \
        sort | nl
}

# 最近笔记
recent_notes() {
    echo -e "${GREEN}最近修改的笔记 (前10):${NC}"
    echo
    
    find "$VAULT_PATH" -name "*.md" -type f -printf '%T@ %p\n' 2>/dev/null | \
        sort -rn | \
        head -10 | \
        cut -d' ' -f2- | \
        sed "s|${VAULT_PATH}/||" | \
        nl
}

# 修改库路径
change_vault_path() {
    echo -e "${YELLOW}修改 Obsidian 仓库路径${NC}"
    echo "========================"
    echo
    
    # 显示当前路径
    local current_path=""
    if [[ -n "${OBSIDIAN_VAULT}" ]]; then
        current_path="${OBSIDIAN_VAULT}"
        echo "当前路径（环境变量）: ${current_path}"
    elif [[ -f "${CONFIG_FILE}" ]]; then
        current_path=$(cat "${CONFIG_FILE}" 2>/dev/null | tr -d '\n')
        echo "当前路径（配置文件）: ${current_path}"
    else
        echo "当前未配置路径"
    fi
    echo
    
    # 提示输入新路径
    while true; do
        read -p "请输入新的仓库路径 (留空取消): " new_path
        
        # 检查是否留空
        if [[ -z "${new_path}" ]]; then
            echo "已取消，保持当前路径"
            return 0
        fi
        
        # 展开 ~ 为 HOME
        new_path="${new_path/#\~/${HOME}}"
        
        if [[ ! -d "${new_path}" ]]; then
            echo "目录不存在: ${new_path}"
            read -p "是否创建该目录? (y/N): " create_dir
            if [[ "${create_dir}" == "y" || "${create_dir}" == "Y" ]]; then
                mkdir -p "${new_path}" && echo "已创建目录: ${new_path}"
            else
                continue
            fi
        fi
        
        # 验证是否是有效的 Obsidian 仓库
        if [[ -d "${new_path}/.obsidian" ]] || [[ $(find "${new_path}" -name "*.md" -type f 2>/dev/null | head -1) ]]; then
            echo -e "${GREEN}✓ 有效的 Obsidian 仓库${NC}"
        else
            echo -e "${YELLOW}警告: 该目录看起来不像 Obsidian 仓库${NC}"
            read -p "仍要使用这个目录吗? (y/N): " confirm
            if [[ "${confirm}" != "y" && "${confirm}" != "Y" ]]; then
                continue
            fi
        fi
        
        # 保存配置
        mkdir -p "${CONFIG_DIR}"
        echo "${new_path}" > "${CONFIG_FILE}"
        # 设置配置文件权限（644: 所有者可读写，其他人只读）
        chmod 644 "${CONFIG_FILE}"
        echo
        echo -e "${GREEN}✓ 已更新仓库路径${NC}"
        echo "新路径: ${new_path}"
        echo
        echo "注意: 本次会话仍使用旧路径，下次运行命令时生效"
        echo "或重新加载配置: export OBSIDIAN_VAULT=${new_path}"
        
        return 0
    done
}

# 解析自然语言指令
# 支持的格式: obs创建笔记, obs 创建笔记, obs-创建笔记, OBS创建笔记 等
parse_command() {
    local input="$1"
    
    # 检查是否以 obs 开头（大小写不敏感）
    # 支持格式: obs指令, obs 指令, obs-指令, OBS指令 等
    local lower_input_check=$(echo "$input" | tr '[:upper:]' '[:lower:]')
    
    if [[ "$lower_input_check" == obs* ]]; then
        # 去除 obs 前缀（3个字符）
        local clean_input="${input:3}"
        # 去除后续的各种连接符（空格、-、_、: 等）
        # 注意：- 必须放在字符类开头或结尾
        while [[ "$clean_input" =~ ^[-[:space:]_\:\/] ]]; do
            clean_input="${clean_input:1}"
        done
        input="$clean_input"
    fi
    
    local lower_input=$(echo "$input" | tr '[:upper:]' '[:lower:]')
    
    case "$lower_input" in
        # 帮助
        帮助|help|"?"|-h|--help)
            show_help
            ;;
            
        # 创建笔记
        创建笔记*|新建笔记*|添加笔记*)
            # 提取 "笔记" 之后的所有内容
            local rest="${input#*笔记}"
            # 去除开头的空格和换行
            rest=$(echo "$rest" | sed 's/^[[:space:]]*//')
            
            # 获取第一行
            local first_line=$(echo "$rest" | head -1)
            # 从第一行提取文件名（第一个空格或换行前的内容）
            local title=$(echo "$first_line" | awk '{print $1}')
            
            # 获取文件名之后的所有内容
            local content=""
            # 获取第一行中文件名之后的内容（如果有空格）
            local first_line_after_title=$(echo "$first_line" | cut -s -d' ' -f2-)
            # 获取后续所有行
            local other_lines=$(echo "$rest" | tail -n +2)
            
            # 合并内容
            if [[ -n "$first_line_after_title" && -n "$other_lines" ]]; then
                # 第一行有内容，且还有后续行
                content="${first_line_after_title}
${other_lines}"
            elif [[ -n "$first_line_after_title" ]]; then
                # 只有第一行有内容
                content="$first_line_after_title"
            elif [[ -n "$other_lines" ]]; then
                # 第一行只有文件名，内容在后续行
                content="$other_lines"
            fi
            
            create_note "$title" "$content"
            ;;
            
        # 删除笔记
        删除笔记*|移除笔记*)
            local title="${input#*笔记}"
            title=$(echo "$title" | sed 's/^[[:space:]]*//')
            delete_note "$title"
            ;;
            
        # 查看笔记
        查看笔记*|打开笔记*|读取笔记*|显示笔记*)
            local title="${input#*笔记}"
            title=$(echo "$title" | sed 's/^[[:space:]]*//')
            view_note "$title"
            ;;
            
        # 搜索标题
        搜索标题*|查找标题*|标题搜索*)
            local keyword="${input#*标题}"
            keyword=$(echo "$keyword" | sed 's/^[[:space:]]*//')
            search_titles "$keyword"
            ;;
            
        # 搜索内容
        搜索内容*|查找内容*|内容搜索*)
            local keyword="${input#*搜索}"
            keyword=$(echo "$keyword" | sed 's/^[[:space:]]*//')
            keyword=$(echo "$keyword" | sed 's/^内容//;s/^[[:space:]]*//')
            search_content "$keyword"
            ;;
            
        # 模糊搜索
        模糊搜索*|快速搜索*)
            local keyword="${input#*搜索}"
            keyword=$(echo "$keyword" | sed 's/^[[:space:]]*//;s/^模糊//;s/^[[:space:]]*//')
            fuzzy_search "$keyword"
            ;;
            
        # 今天日记
        今天日记*|今日日记*|daily*)
            local content="${input#*日记}"
            content=$(echo "$content" | sed 's/^[[:space:]]*//')
            daily_note "$content"
            ;;
            
        # 列出所有
        列出所有|所有笔记)
            list_all
            ;;
            
        # 列出文件夹
        列出文件夹|所有文件夹)
            list_folders
            ;;
            
        # 最近笔记
        最近笔记|最近修改)
            recent_notes
            ;;
            
        # 修改库路径
        修改库路径|修改库目录|更改路径|切换仓库)
            change_vault_path
            ;;
            
        # 执行删除（内部使用）
        EXECUTE_DELETE:*)
            local filepath="${input#EXECUTE_DELETE:}"
            execute_delete "$filepath"
            ;;
            
        # 未知命令
        *)
            echo -e "${RED}无法理解的指令: $input${NC}"
            echo "试试: 创建笔记, 搜索内容, 今天日记, 帮助"
            return 1
            ;;
    esac
}

# 主程序
main() {
    if [[ $# -eq 0 ]]; then
        echo -e "${YELLOW}Obsidian Headless - 无头 Obsidian 自然语言控制工具${NC}"
        echo "仓库: $VAULT_PATH"
        echo
        show_help
        exit 0
    fi
    
    local input="$*"
    
    if [[ ! -d "$VAULT_PATH" ]]; then
        echo -e "${RED}错误: 仓库路径不存在: $VAULT_PATH${NC}"
        echo "设置环境变量: export OBSIDIAN_VAULT=/path/to/vault"
        exit 1
    fi
    
    parse_command "$input"
}

main "$@"
