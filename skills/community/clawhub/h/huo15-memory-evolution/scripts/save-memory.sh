#!/bin/bash
#===============================================================================
# huo15-memory-evolution: 主动记忆写入工具
#
# 用法:
#   ./save-memory.sh <type> <name> <description> << 'EOF'
#   记忆内容
#   EOF
#
# 示例:
#   ./save-memory.sh feedback wecom-media-send "企微群聊发图片必须用chatid" << 'EOF'
#   ## 规则
#   企微群聊发图片必须用 chatid，不是 touser
#
#   ## 为什么值得记忆
#   之前用 touser 发送图片失败，报错 86008
#
#   ## 如何应用
#   在企微群聊场景下，媒体发送一律使用 chatid 参数
#   EOF
#
# 或交互模式:
#   ./save-memory.sh --interactive
#===============================================================================

set -e

SKILL_DIR="$(cd "$(dirname "$(dirname "$0")")" && pwd)"

# 动态路由：优先使用 PWD 检测 > OC_AGENT_ID > 默认
if [ -d "${PWD}/memory" ] && [[ "$PWD" == *".openclaw/workspace"* ]]; then
    WORKSPACE_DIR="$PWD"
elif [ -n "${OC_AGENT_ID:-}" ]; then
    WORKSPACE_DIR="$HOME/.openclaw/workspace-${OC_AGENT_ID}"
else
    WORKSPACE_DIR="$HOME/.openclaw/workspace"
fi

MEMORY_DIR="$WORKSPACE_DIR/memory"
TODAY=$(date +%Y-%m-%d)

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $*"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

usage() {
    cat << USAGE
用法:
    $0 <type> <name> <description> << 'EOF'
    记忆内容
    EOF

参数:
    type        记忆类型: user|feedback|project|reference
    name        记忆名称（英文，无空格）
    description 一句话描述（用于判断相关性）

示例:
    $0 feedback wecom-media-send "企微群聊发图片必须用chatid" << 'EOF'
    ## 规则
    企微群聊发图片必须用 chatid，不是 touser
    EOF

交互模式:
    $0 --interactive
USAGE
}

# 交互模式
interactive_mode() {
    log "🖊️  主动记忆写入 - 交互模式"
    echo ""
    
    # 选择类型
    echo "选择记忆类型:"
    echo "  1) user      - 用户偏好、习惯"
    echo "  2) feedback   - 纠正反馈、确认偏好"
    echo "  3) project   - 项目进展、决策"
    echo "  4) reference - 外部系统指针"
    read -p "请输入选项 (1-4): " type_choice
    
    case "$type_choice" in
        1) TYPE="user" ;;
        2) TYPE="feedback" ;;
        3) TYPE="project" ;;
        4) TYPE="reference" ;;
        *) error "无效选择"; exit 1 ;;
    esac
    
    # 输入名称
    read -p "记忆名称（英文，无空格）: " NAME
    
    # 输入描述
    read -p "一句话描述: " DESCRIPTION
    
    # 输入内容
    echo ""
    echo "请输入记忆内容（输入完成后按 Ctrl+D）:"
    echo "---"
    CONTENT=$(cat)
    echo "---"
    
    # 确认
    echo ""
    echo "请确认:"
    echo "  类型: $TYPE"
    echo "  名称: $NAME"
    echo "  描述: $DESCRIPTION"
    read -p "确认保存? (y/n): " confirm
    
    if [ "$confirm" != "y" ]; then
        log "已取消"
        exit 0
    fi
    
    save_memory "$TYPE" "$NAME" "$DESCRIPTION" "$CONTENT"
}

# 保存记忆
save_memory() {
    local TYPE="$1"
    local NAME="$2"
    local DESCRIPTION="$3"
    local CONTENT="$4"
    
    # 验证参数
    if [ -z "$TYPE" ] || [ -z "$NAME" ] || [ -z "$DESCRIPTION" ] || [ -z "$CONTENT" ]; then
        error "缺少必要参数"
        usage
        exit 1
    fi
    
    # 验证类型
    case "$TYPE" in
        user|feedback|project|reference) ;;
        *)
            error "无效类型: $TYPE"
            echo "有效类型: user, feedback, project, reference"
            exit 1
            ;;
    esac
    
    # 检查目录
    TYPE_DIR="$MEMORY_DIR/$TYPE"
    if [ ! -d "$TYPE_DIR" ]; then
        mkdir -p "$TYPE_DIR"
        log "创建目录: $TYPE_DIR"
    fi
    
    # 生成文件名
    FILENAME="${NAME}.md"
    FILEPATH="$TYPE_DIR/$FILENAME"
    
    # 如果文件已存在，询问是否覆盖
    if [ -f "$FILEPATH" ]; then
        warn "文件已存在: $FILEPATH"
        read -p "覆盖? (y/n): " overwrite
        if [ "$overwrite" != "y" ]; then
            log "已取消"
            exit 0
        fi
    fi
    
    # 写入记忆文件
    cat << EOF > "$FILEPATH"
---
name: ${NAME}
type: ${TYPE}
description: ${DESCRIPTION}
created: ${TODAY}
updated: ${TODAY}
---

${CONTENT}
EOF
    
    log "✅ 记忆已保存: $TYPE/$FILENAME"
    
    # 更新 MEMORY.md 索引
    update_index "$TYPE" "$NAME" "$DESCRIPTION" "$TYPE/$FILENAME"
}

# 更新索引
update_index() {
    local TYPE="$1"
    local NAME="$2"
    local DESCRIPTION="$3"
    local MEMORY_PATH="$4"
    
    local INDEX_FILE="$WORKSPACE_DIR/MEMORY.md"
    
    # 检查是否已在索引中
    if grep -q "$MEMORY_PATH" "$INDEX_FILE" 2>/dev/null; then
        log "   ↩  已在索引中: $MEMORY_PATH"
        return
    fi
    
    # 构建新条目
    local NEW_ENTRY="- [${NAME}](memory/${MEMORY_PATH}) — ${DESCRIPTION}"
    
    # 使用 awk 在对应 section 后插入
    local SECTION_MARKER=""
    case "$TYPE" in
        user) SECTION_MARKER="^## user$" ;;
        feedback) SECTION_MARKER="^## feedback$" ;;
        project) SECTION_MARKER="^## project$" ;;
        reference) SECTION_MARKER="^## reference$" ;;
    esac
    
    if [ -n "$SECTION_MARKER" ]; then
        awk -v pattern="$SECTION_MARKER" -v entry="$NEW_ENTRY" '
            $0 ~ pattern { found=1; print; next }
            found && /^$/ { print entry; print; found=0; next }
            { print }
        ' "$INDEX_FILE" > "$INDEX_FILE.tmp" && mv "$INDEX_FILE.tmp" "$INDEX_FILE"
        log "   ✅ 索引已更新"
    fi
}

# 主逻辑
main() {
    if [ "$1" = "--interactive" ] || [ "$1" = "-i" ]; then
        interactive_mode
    elif [ "$#" -ge 3 ]; then
        TYPE="$1"
        NAME="$2"
        DESCRIPTION="$3"
        
        # 从 stdin 读取内容
        CONTENT=$(cat)
        
        if [ -z "$CONTENT" ]; then
            error "记忆内容为空"
            exit 1
        fi
        
        save_memory "$TYPE" "$NAME" "$DESCRIPTION" "$CONTENT"
    else
        usage
        exit 1
    fi
}

main "$@"
