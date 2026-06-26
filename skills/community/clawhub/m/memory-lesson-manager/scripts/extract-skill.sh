#!/bin/bash
# 技能提取助手 - Extract Skill Helper
# 从学习条目创建新的技能
# 用法：./extract-skill.sh <技能名称> [--dry-run]

set -e

# 配置
SKILLS_DIR="./skills"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    cat << EOF
用法：$(basename "$0") <技能名称> [选项]

从学习条目创建新的技能。

参数:
  技能名称     技能名称（小写，连字符分隔，支持中文拼音）

选项:
  --dry-run      预览将创建的内容但不实际创建文件
  --output-dir   输出目录（相对于当前路径，默认：./skills）
  -h, --help     显示帮助信息

示例:
  $(basename "$0") docker-m1-fixes
  $(basename "$0") api-timeout-patterns --dry-run
  $(basename "$0") pnpm-setup --output-dir ./skills/custom

技能将创建在：\$SKILLS_DIR/<技能名称>/
EOF
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# 解析参数
SKILL_NAME=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --output-dir)
            if [ -z "${2:-}" ] || [[ "${2:-}" == -* ]]; then
                log_error "--output-dir 需要相对路径参数"
                usage
                exit 1
            fi
            SKILLS_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            log_error "未知选项：$1"
            usage
            exit 1
            ;;
        *)
            if [ -z "$SKILL_NAME" ]; then
                SKILL_NAME="$1"
            else
                log_error "意外参数：$1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

# 验证技能名称
if [ -z "$SKILL_NAME" ]; then
    log_error "技能名称不能为空"
    usage
    exit 1
fi

# 验证技能名称格式（小写、连字符、无空格）
if ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    log_error "技能名称格式无效。请使用小写字母、数字和连字符。"
    log_error "示例：'docker-fixes', 'api-patterns', 'pnpm-setup'"
    exit 1
fi

# 验证输出路径
if [[ "$SKILLS_DIR" = /* ]]; then
    log_error "输出目录必须是相对路径"
    exit 1
fi

if [[ "$SKILLS_DIR" =~ (^|/)\.\.(/|$) ]]; then
    log_error "输出目录不能包含 '..' 路径段"
    exit 1
fi

SKILLS_DIR="${SKILLS_DIR#./}"
SKILLS_DIR="./$SKILLS_DIR"

SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

# 检查技能是否已存在
if [ -d "$SKILL_PATH" ] && [ "$DRY_RUN" = false ]; then
    log_error "技能已存在：$SKILL_PATH"
    log_error "请使用不同的名称或先删除现有技能"
    exit 1
fi

# Dry run 输出
if [ "$DRY_RUN" = true ]; then
    log_info "预览模式 - 将创建："
    echo "  $SKILL_PATH/"
    echo "  $SKILL_PATH/SKILL.md"
    echo ""
    echo "模板内容预览："
    echo "---"
    cat << TEMPLATE
name: $SKILL_NAME
description: "[待填写：简洁描述此技能的功能和使用场景]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[待填写：简要介绍技能目的]

## 快速参考

| 场景 | 操作 |
|------|------|
| [触发条件] | [执行操作] |

## 使用方法

[待填写：详细使用说明]

## 示例

[待填写：具体示例]

## 来源学习

此技能从学习条目提取。
- 学习 ID: [待填写原始学习 ID]
- 原始文件：memory/lessons/XXX.md
TEMPLATE
    echo "---"
    exit 0
fi

# 创建技能目录结构
log_info "创建技能：$SKILL_NAME"
log_step "1/4 创建目录结构"

mkdir -p "$SKILL_PATH"

log_step "2/4 创建 SKILL.md"

# 创建 SKILL.md
cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[待填写：简洁描述此技能的功能和使用场景]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[待填写：简要介绍技能目的]

## 快速参考

| 场景 | 操作 |
|------|------|
| [触发条件] | [执行操作] |

## 使用方法

[待填写：详细使用说明]

## 示例

[待填写：具体示例]

## 来源学习

此技能从学习条目提取。
- 学习 ID: [待填写原始学习 ID]
- 原始文件：memory/lessons/XXX.md

## 相关文件

- [ ] 是否需要 references/ 目录存放详细文档？
- [ ] 是否需要 scripts/ 目录存放可执行代码？
- [ ] 是否需要 assets/ 目录存放静态资源？
TEMPLATE

log_info "已创建：$SKILL_PATH/SKILL.md"

log_step "3/4 创建 references 目录"
mkdir -p "$SKILL_PATH/references"
cat > "$SKILL_PATH/references/.gitkeep" << 'EOF'
# References Directory

放置详细文档、规范链接、参考资料等。

## 建议文件

- `spec.md` - 相关技术规范
- `examples.md` - 使用示例集合
- `changelog.md` - 技能更新日志
EOF

log_step "4/4 创建 scripts 目录"
mkdir -p "$SKILL_PATH/scripts"
cat > "$SKILL_PATH/scripts/.gitkeep" << 'EOF'
# Scripts Directory

放置可执行脚本、自动化工具等。

## 规范

- 脚本必须有 shebang (#!/bin/bash 或 #!/usr/bin/env node)
- 脚本必须有执行权限 (chmod +x)
- 脚本必须有错误处理 (set -e)
EOF

# 输出下一步提示
echo ""
log_info "✅ 技能框架创建成功！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "下一步操作："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  1. 编辑 $SKILL_PATH/SKILL.md"
echo "     填写所有 [待填写] 部分"
echo ""
echo "  2. 从学习条目复制内容"
echo "     来源：memory/lessons/XXX.md"
echo ""
echo "  3. 添加参考资料（如需要）"
echo "     位置：$SKILL_PATH/references/"
echo ""
echo "  4. 添加可执行脚本（如需要）"
echo "     位置：$SKILL_PATH/scripts/"
echo ""
echo "  5. 更新原始学习条目"
echo "     添加：**状态**: promoted_to_skill"
echo "     添加：**技能路径**: skills/$SKILL_NAME"
echo ""
echo "  6. 验证技能"
echo "     在新会话中读取技能确保自包含"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
log_info "提示：使用 clawhub publish $SKILL_PATH 发布到 ClawHub"
