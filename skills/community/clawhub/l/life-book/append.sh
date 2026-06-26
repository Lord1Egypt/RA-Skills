#!/usr/bin/env bash
# 生命之书 - 对话式内容追加工具
# 用于在 OpenClaw 对话中快速沉淀内容

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace/life-books"

# 初始化用户目录
init_user() {
    local user_name="${1:-default}"
    local user_dir="${WORKSPACE}/${user_name}"
    
    if [[ ! -d "${user_dir}" ]]; then
        mkdir -p "${user_dir}"/{chapters,materials,raw}
        
        cat > "${user_dir}/metadata.json" <<EOF
{
  "name": "${user_name}",
  "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "chapters": [],
  "timeline": []
}
EOF
    fi
    
    echo "${user_dir}"
}

# 追加内容到章节
append_to_chapter() {
    local user_name="$1"
    local chapter_name="$2"
    local content="$3"
    
    local user_dir=$(init_user "${user_name}")
    local chapter_file="${user_dir}/chapters/${chapter_name}.md"
    
    # 如果章节文件不存在，创建它
    if [[ ! -f "${chapter_file}" ]]; then
        cat > "${chapter_file}" <<EOF
# ${chapter_name}

记录开始时间: $(date '+%Y-%m-%d %H:%M:%S')

---

EOF
    fi
    
    # 追加内容
    cat >> "${chapter_file}" <<EOF
### $(date '+%Y-%m-%d %H:%M')

${content}

---

EOF
    
    echo "✓ 内容已追加到: ${chapter_name}"
}

# 获取章节字数统计
get_chapter_stats() {
    local user_name="${1:-default}"
    local user_dir="${WORKSPACE}/${user_name}"
    
    if [[ ! -d "${user_dir}/chapters" ]]; then
        echo "0"
        return
    fi
    
    local total_words=0
    for chapter_file in "${user_dir}"/chapters/*.md; do
        [[ ! -f "${chapter_file}" ]] && continue
        local words=$(wc -w < "${chapter_file}" | tr -d ' ')
        total_words=$((total_words + words))
    done
    
    echo "${total_words}"
}

# 主函数
main() {
    local action="${1:-help}"
    
    case "${action}" in
        append)
            local user_name="${2:-default}"
            local chapter_name="$3"
            local content="$4"
            append_to_chapter "${user_name}" "${chapter_name}" "${content}"
            ;;
        init)
            local user_name="${2:-default}"
            init_user "${user_name}"
            echo "✓ 用户目录已初始化"
            ;;
        stats)
            local user_name="${2:-default}"
            local words=$(get_chapter_stats "${user_name}")
            echo "已记录: ${words} 字"
            ;;
        *)
            cat <<EOF
生命之书 - 对话式追加工具

用法:
  append [用户名] <章节名> <内容>    追加内容到章节
  init [用户名]                     初始化用户目录
  stats [用户名]                    查看字数统计

示例:
  append default "出生与童年" "我出生在北京..."
  stats default
EOF
            ;;
    esac
}

main "$@"
