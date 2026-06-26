#!/usr/bin/env bash
# 生命之书 - Life Book Generator
# 引导用户创建个人生命故事

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="${HOME}/.openclaw/workspace/life-books"
CONFIG_FILE="${WORKSPACE}/config.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✓${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $*"
}

log_error() {
    echo -e "${RED}✗${NC} $*" >&2
}

# 初始化工作空间
init_workspace() {
    local user_name="${1:-default}"
    local user_dir="${WORKSPACE}/${user_name}"
    
    if [[ -d "${user_dir}" ]]; then
        log_warn "项目已存在: ${user_dir}"
        read -p "是否继续？(y/N) " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
    fi
    
    log_info "创建项目结构..."
    mkdir -p "${user_dir}"/{raw,materials,chapters}
    
    # 创建配置文件
    if [[ ! -f "${CONFIG_FILE}" ]]; then
        cat > "${CONFIG_FILE}" <<EOF
{
  "language": "zh-CN",
  "style": "narrative",
  "includePhotos": true,
  "privacyLevel": "private",
  "autoBackup": true,
  "currentUser": "${user_name}"
}
EOF
    fi
    
    # 创建元数据文件
    cat > "${user_dir}/metadata.json" <<EOF
{
  "name": "${user_name}",
  "created": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "chapters": [],
  "timeline": []
}
EOF
    
    log_success "项目初始化完成: ${user_dir}"
}

# 交互式引导
start_interview() {
    local user_name="${1:-default}"
    local user_dir="${WORKSPACE}/${user_name}"
    
    [[ ! -d "${user_dir}" ]] && init_workspace "${user_name}"
    
    log_info "开始生命故事记录..."
    echo
    echo "我会通过一系列问题引导你记录人生经历。"
    echo "你可以随时输入 'skip' 跳过问题，'save' 保存进度，'quit' 退出。"
    echo
    
    local chapters=(
        "出生与童年"
        "求学经历"
        "职业生涯"
        "重要关系"
        "人生转折"
        "当下与展望"
    )
    
    for chapter in "${chapters[@]}"; do
        echo
        log_info "=== ${chapter} ==="
        echo
        
        local chapter_file="${user_dir}/chapters/$(echo "${chapter}" | tr ' ' '_').md"
        echo "# ${chapter}" > "${chapter_file}"
        echo >> "${chapter_file}"
        echo "记录时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "${chapter_file}"
        echo >> "${chapter_file}"
        
        case "${chapter}" in
            "出生与童年")
                ask_question "${chapter_file}" "你出生在哪一年？哪个地方？"
                ask_question "${chapter_file}" "你的童年是在哪里度过的？"
                ask_question "${chapter_file}" "有哪些童年记忆让你印象深刻？"
                ask_question "${chapter_file}" "你的家庭是什么样的？"
                ;;
            "求学经历")
                ask_question "${chapter_file}" "你在哪里上的小学/中学/大学？"
                ask_question "${chapter_file}" "有哪些老师或同学对你影响深远？"
                ask_question "${chapter_file}" "求学期间有什么难忘的经历？"
                ;;
            "职业生涯")
                ask_question "${chapter_file}" "你的第一份工作是什么？"
                ask_question "${chapter_file}" "职业生涯中有哪些重要的转折点？"
                ask_question "${chapter_file}" "你最自豪的职业成就是什么？"
                ;;
            "重要关系")
                ask_question "${chapter_file}" "谁是你生命中最重要的人？"
                ask_question "${chapter_file}" "有哪些友谊让你珍惜？"
                ask_question "${chapter_file}" "你如何看待家庭关系？"
                ;;
            "人生转折")
                ask_question "${chapter_file}" "有哪些事件改变了你的人生轨迹？"
                ask_question "${chapter_file}" "你如何应对人生的挑战？"
                ask_question "${chapter_file}" "哪些决定让你成为现在的自己？"
                ;;
            "当下与展望")
                ask_question "${chapter_file}" "你现在的生活状态如何？"
                ask_question "${chapter_file}" "你对未来有什么期待？"
                ask_question "${chapter_file}" "你想对未来的自己说什么？"
                ;;
        esac
        
        log_success "章节 '${chapter}' 记录完成"
    done
    
    echo
    log_success "所有章节记录完成！"
    log_info "你可以运行 'life-book generate ${user_name}' 生成完整的生命之书"
}

# 提问并记录
ask_question() {
    local output_file="$1"
    local question="$2"
    
    echo
    echo -e "${BLUE}Q:${NC} ${question}"
    echo -n "A: "
    
    local answer
    read -r answer
    
    case "${answer}" in
        skip)
            log_warn "跳过此问题"
            return
            ;;
        save)
            log_success "进度已保存"
            return
            ;;
        quit)
            log_info "退出记录"
            exit 0
            ;;
        "")
            log_warn "未输入内容，跳过"
            return
            ;;
    esac
    
    echo "## ${question}" >> "${output_file}"
    echo >> "${output_file}"
    echo "${answer}" >> "${output_file}"
    echo >> "${output_file}"
}

# 添加章节
add_chapter() {
    local user_name="${1:-default}"
    local chapter_name="$2"
    local user_dir="${WORKSPACE}/${user_name}"
    
    [[ ! -d "${user_dir}" ]] && log_error "项目不存在，请先运行 'life-book start'" && exit 1
    
    local chapter_file="${user_dir}/chapters/$(echo "${chapter_name}" | tr ' ' '_').md"
    
    if [[ -f "${chapter_file}" ]]; then
        log_warn "章节已存在: ${chapter_name}"
        read -p "是否覆盖？(y/N) " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && exit 0
    fi
    
    echo "# ${chapter_name}" > "${chapter_file}"
    echo >> "${chapter_file}"
    echo "记录时间: $(date '+%Y-%m-%d %H:%M:%S')" >> "${chapter_file}"
    echo >> "${chapter_file}"
    
    log_success "章节创建完成: ${chapter_file}"
    log_info "请编辑文件添加内容"
}

# 导入资料
import_materials() {
    local user_name="${1:-default}"
    local source="$2"
    local user_dir="${WORKSPACE}/${user_name}"
    
    [[ ! -d "${user_dir}" ]] && log_error "项目不存在" && exit 1
    
    if [[ -f "${source}" ]] || [[ -d "${source}" ]]; then
        log_info "导入本地资料: ${source}"
        cp -r "${source}" "${user_dir}/materials/"
        log_success "导入完成"
    elif [[ "${source}" =~ ^https?:// ]]; then
        log_info "导入网络资料: ${source}"
        local filename=$(basename "${source}")
        curl -sL "${source}" -o "${user_dir}/materials/${filename}"
        log_success "导入完成"
    else
        log_error "无效的资料源: ${source}"
        exit 1
    fi
}

# 生成生命之书
generate_book() {
    local user_name="${1:-default}"
    local user_dir="${WORKSPACE}/${user_name}"
    
    [[ ! -d "${user_dir}" ]] && log_error "项目不存在" && exit 1
    
    log_info "生成生命之书..."
    
    local book_file="${user_dir}/book.md"
    
    # 书籍头部
    cat > "${book_file}" <<EOF
# 我的生命之书

> 生成时间: $(date '+%Y年%m月%d日')

---

## 目录

EOF
    
    # 生成目录
    local chapter_num=1
    for chapter_file in "${user_dir}"/chapters/*.md; do
        [[ ! -f "${chapter_file}" ]] && continue
        local chapter_name=$(basename "${chapter_file}" .md | tr '_' ' ')
        echo "${chapter_num}. ${chapter_name}" >> "${book_file}"
        ((chapter_num++))
    done
    
    echo >> "${book_file}"
    echo "---" >> "${book_file}"
    echo >> "${book_file}"
    
    # 合并章节
    chapter_num=1
    for chapter_file in "${user_dir}"/chapters/*.md; do
        [[ ! -f "${chapter_file}" ]] && continue
        
        echo "## 第${chapter_num}章" >> "${book_file}"
        echo >> "${book_file}"
        
        # 跳过原文件的标题行
        tail -n +2 "${chapter_file}" >> "${book_file}"
        
        echo >> "${book_file}"
        echo "---" >> "${book_file}"
        echo >> "${book_file}"
        
        ((chapter_num++))
    done
    
    # 添加资料索引
    if [[ -d "${user_dir}/materials" ]] && [[ -n "$(ls -A "${user_dir}/materials")" ]]; then
        echo "## 附录：资料索引" >> "${book_file}"
        echo >> "${book_file}"
        
        for material in "${user_dir}"/materials/*; do
            [[ ! -e "${material}" ]] && continue
            local material_name=$(basename "${material}")
            echo "- ${material_name}" >> "${book_file}"
        done
        
        echo >> "${book_file}"
    fi
    
    log_success "生命之书生成完成: ${book_file}"
    log_info "文件大小: $(du -h "${book_file}" | cut -f1)"
}

# 查看状态
show_status() {
    local user_name="${1:-default}"
    local user_dir="${WORKSPACE}/${user_name}"
    
    [[ ! -d "${user_dir}" ]] && log_error "项目不存在" && exit 1
    
    echo
    log_info "=== 生命之书项目状态 ==="
    echo
    echo "用户: ${user_name}"
    echo "路径: ${user_dir}"
    echo
    
    local chapter_count=$(find "${user_dir}/chapters" -name "*.md" 2>/dev/null | wc -l)
    echo "已完成章节: ${chapter_count}"
    
    if [[ ${chapter_count} -gt 0 ]]; then
        echo
        echo "章节列表:"
        for chapter_file in "${user_dir}"/chapters/*.md; do
            [[ ! -f "${chapter_file}" ]] && continue
            local chapter_name=$(basename "${chapter_file}" .md | tr '_' ' ')
            local word_count=$(wc -w < "${chapter_file}")
            echo "  - ${chapter_name} (${word_count} 字)"
        done
    fi
    
    echo
    local material_count=$(find "${user_dir}/materials" -type f 2>/dev/null | wc -l)
    echo "收集资料: ${material_count} 个文件"
    
    if [[ -f "${user_dir}/book.md" ]]; then
        echo
        local book_size=$(du -h "${user_dir}/book.md" | cut -f1)
        echo "生命之书: 已生成 (${book_size})"
    else
        echo
        echo "生命之书: 未生成"
    fi
    
    echo
}

# 主函数
main() {
    local command="${1:-help}"
    
    case "${command}" in
        start)
            local user_name="${2:-default}"
            start_interview "${user_name}"
            ;;
        add-chapter)
            local user_name="${2:-default}"
            local chapter_name="${3:-}"
            [[ -z "${chapter_name}" ]] && log_error "请指定章节名称" && exit 1
            add_chapter "${user_name}" "${chapter_name}"
            ;;
        import)
            local user_name="${2:-default}"
            local source="${3:-}"
            [[ -z "${source}" ]] && log_error "请指定资料源" && exit 1
            import_materials "${user_name}" "${source}"
            ;;
        generate)
            local user_name="${2:-default}"
            generate_book "${user_name}"
            ;;
        status)
            local user_name="${2:-default}"
            show_status "${user_name}"
            ;;
        help|--help|-h)
            cat <<EOF
生命之书 (Life Book) - 个人传记生成工具

用法:
  life-book start [用户名]              开始交互式记录
  life-book add-chapter [用户名] <章节>  添加新章节
  life-book import [用户名] <路径|URL>   导入资料
  life-book generate [用户名]            生成生命之书
  life-book status [用户名]              查看项目状态
  life-book help                        显示此帮助

示例:
  life-book start                       # 开始记录（默认用户）
  life-book start zhangsan              # 为 zhangsan 开始记录
  life-book add-chapter "大学时光"       # 添加章节
  life-book import ~/photos             # 导入照片
  life-book generate                    # 生成成书
  life-book status                      # 查看状态

所有数据存储在: ${WORKSPACE}
EOF
            ;;
        *)
            log_error "未知命令: ${command}"
            echo "运行 'life-book help' 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"
