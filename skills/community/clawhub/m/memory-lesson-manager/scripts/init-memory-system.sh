#!/bin/bash
# 记忆系统初始化脚本
# 自动创建缺失的记忆文件和目录结构
# 用法：./init-memory-system.sh [--dry-run]

set -e

# 配置
# 支持环境变量或自动检测工作区
if [ -n "$OPENCLAW_WORKSPACE" ]; then
    WORKSPACE_DIR="$OPENCLAW_WORKSPACE"
elif [ -n "$CLAW_WORKSPACE" ]; then
    WORKSPACE_DIR="$CLAW_WORKSPACE"
else
    # 从 skill 目录向上两级找到 workspace
    WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
    # 验证是否包含 skills/memory-lesson-manager
    if [ ! -d "$WORKSPACE_DIR/skills/memory-lesson-manager" ]; then
        # 尝试从当前工作目录
        WORKSPACE_DIR="$(pwd)"
    fi
fi
MEMORY_DIR="$WORKSPACE_DIR/memory"
LESSONS_DIR="$MEMORY_DIR/lessons"
TEMPLATES_DIR="$MEMORY_DIR/templates"
STATE_DIR="$WORKSPACE_DIR/state"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
    cat << EOF
用法：$(basename "$0") [选项]

自动创建缺失的记忆文件和目录结构

选项:
  --dry-run      预览模式，不实际创建文件
  -h, --help     显示帮助信息

创建内容:
  - memory/lessons/{HOT,WARM/{errors,corrections,best-practices,feature-requests,decisions,projects,people},COLD/archive}
  - memory/templates/ (9 个模板)
  - state/ (2 个状态模板)
  - memory/lessons/README.md
  - memory/lessons/INDEX.md
  - 当日日记 memory/YYYY-MM-DD.md
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

log_dry() {
    echo -e "${YELLOW}[DRY-RUN]${NC} $1"
}

# 解析参数
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
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
            log_error "意外参数：$1"
            usage
            exit 1
            ;;
    esac
done

# 获取当前日期
TODAY=$(date +%Y-%m-%d)
TODAY_FULL=$(date +"%Y-%m-%d — 工作记录")

log_step "1/4 创建目录结构..."

# 目录列表
DIRS=(
    "$LESSONS_DIR/HOT"
    "$LESSONS_DIR/WARM/errors"
    "$LESSONS_DIR/WARM/corrections"
    "$LESSONS_DIR/WARM/best-practices"
    "$LESSONS_DIR/WARM/feature-requests"
    "$LESSONS_DIR/WARM/decisions"
    "$LESSONS_DIR/WARM/projects"
    "$LESSONS_DIR/WARM/people"
    "$LESSONS_DIR/COLD/archive"
    "$TEMPLATES_DIR"
    "$STATE_DIR"
)

for dir in "${DIRS[@]}"; do
    if [ -d "$dir" ]; then
        if [ "$DRY_RUN" = true ]; then
            log_dry "目录已存在：$dir"
        fi
    else
        if [ "$DRY_RUN" = true ]; then
            log_dry "将创建目录：$dir"
        else
            mkdir -p "$dir"
            log_info "已创建目录：$dir"
        fi
    fi
done

log_step "2/4 创建模板文件..."

# 模板文件列表
TEMPLATES=(
    "diary-template.md"
    "lesson-error-template.md"
    "lesson-correction-template.md"
    "lesson-feature-template.md"
    "lesson-best-practice-template.md"
    "lesson-decision-template.md"
    "lesson-project-template.md"
    "lesson-people-template.md"
    "memory-hot-template.md"
    "session-state-template.md"
    "working-buffer-template.md"
)

# 脚本目录
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

for template in "${TEMPLATES[@]}"; do
    TARGET_FILE=""
    
    # 确定目标位置
    if [[ "$template" == "session-state"* ]] || [[ "$template" == "working-buffer"* ]]; then
        TARGET_FILE="$STATE_DIR/$template"
    else
        TARGET_FILE="$TEMPLATES_DIR/$template"
    fi
    
    if [ -f "$TARGET_FILE" ]; then
        if [ "$DRY_RUN" = true ]; then
            log_dry "模板已存在：$TARGET_FILE"
        fi
    else
        # 检查 scripts 目录下是否有模板
        SOURCE_FILE="$SCRIPTS_DIR/templates/$template"
        
        if [ -f "$SOURCE_FILE" ]; then
            if [ "$DRY_RUN" = true ]; then
                log_dry "将复制模板：$SOURCE_FILE → $TARGET_FILE"
            else
                if ! cp "$SOURCE_FILE" "$TARGET_FILE" 2>/dev/null; then
                    log_error "模板复制失败：$SOURCE_FILE"
                    ((failed++)) || true
                    continue
                fi
                log_info "已创建模板：$TARGET_FILE"
            fi
        else
            if [ "$DRY_RUN" = true ]; then
                log_dry "将创建模板：$TARGET_FILE (从 skill 复制)"
            else
                # 从 skill 目录复制
                SKILL_TEMPLATE="$WORKSPACE_DIR/skills/memory-lesson-manager/templates/$template"
                if [ -f "$SKILL_TEMPLATE" ]; then
                    cp "$SKILL_TEMPLATE" "$TARGET_FILE"
                else
                    # 创建空模板
                    touch "$TARGET_FILE"
                fi
                log_info "已创建模板：$TARGET_FILE"
            fi
        fi
    fi
done

log_step "3/4 创建索引文件..."

# 创建 lessons/README.md
README_FILE="$LESSONS_DIR/README.md"
if [ -f "$README_FILE" ]; then
    if [ "$DRY_RUN" = true ]; then
        log_dry "README 已存在：$README_FILE"
    fi
else
    if [ "$DRY_RUN" = true ]; then
        log_dry "将创建 README: $README_FILE"
    else
        cat > "$README_FILE" << 'README'
# Lessons 索引 (WARM 层)

**最后更新：** YYYY-MM-DD  
**版本：** V2.0

---

## 三层记忆架构

```
lessons/
├── HOT/                        # 🔥 高频使用（≤20 条，自动加载）
│   └── memory-hot.md
│
├── WARM/                       # 🌡️ 按需加载（默认层级）
│   ├── README.md              # 本文件
│   ├── errors/                # 错误记录 (ERR-*)
│   ├── corrections/           # 纠正学习 (LRN-*)
│   ├── best-practices/        # 最佳实践 (LRN-*)
│   ├── feature-requests/      # 功能请求 (FEAT-*)
│   ├── decisions/             # 决策记录 (DEC-*)
│   ├── projects/              # 项目经验 (PRJ-*)
│   └── people/                # 人物档案 (PPL-*)
│
└── COLD/archive/               # ❄️ 归档（90 天未用）
    └── *.md
```

---

## 快速开始

### 创建学习条目

```bash
# 错误记录
cp memory/templates/lesson-error-template.md \
   memory/lessons/WARM/errors/ERR-YYYYMMDD-XXX.md

# 最佳实践
cp memory/templates/lesson-best-practice-template.md \
   memory/lessons/WARM/best-practices/LRN-YYYYMMDD-XXX.md
```

### 工具脚本

```bash
# 晋升高频条目
./skills/memory-lesson-manager/scripts/promote-lesson.sh

# 归档过期条目
./skills/memory-lesson-manager/scripts/archive-cold.sh

# 提取技能
./skills/memory-lesson-manager/scripts/extract-skill.sh <技能名称>
```

---

_规范详情：work-specs/docs/memory-system-v2-spec.md_
README
        log_info "已创建 README: $README_FILE"
    fi
fi

# 创建 lessons/INDEX.md
INDEX_FILE="$LESSONS_DIR/INDEX.md"
if [ -f "$INDEX_FILE" ]; then
    if [ "$DRY_RUN" = true ]; then
        log_dry "INDEX 已存在：$INDEX_FILE"
    fi
else
    if [ "$DRY_RUN" = true ]; then
        log_dry "将创建 INDEX: $INDEX_FILE"
    else
        cat > "$INDEX_FILE" << INDEX
# Lessons Index

**最后更新：** $TODAY  
**版本：** V2.0

---

## 按类型统计

| 类型 | 前缀 | 目录 | 数量 | 待处理 | 已解决 | 已晋升 |
|------|------|------|------|--------|--------|--------|
| errors | ERR | WARM/errors/ | 0 | 0 | 0 | 0 |
| corrections | LRN | WARM/corrections/ | 0 | 0 | 0 | 0 |
| best-practices | LRN | WARM/best-practices/ | 0 | 0 | 0 | 0 |
| feature-requests | FEAT | WARM/feature-requests/ | 0 | 0 | 0 | 0 |
| decisions | DEC | WARM/decisions/ | 0 | 0 | 0 | 0 |
| projects | PRJ | WARM/projects/ | 0 | 0 | 0 | 0 |
| people | PPL | WARM/people/ | 0 | 0 | 0 | 0 |
| **总计** | - | - | **0** | **0** | **0** | **0** |

---

## HOT Memory

**文件：** HOT/memory-hot.md  
**条目数量：** 0/20  
**最后更新：** $TODAY

*暂无高频条目*

---

## 最近添加

*暂无条目*

---

## 高频模式（出现≥3 次）

*暂无高频模式*

---

## 待处理条目

*暂无待处理条目*

---

## 维护记录

| 日期 | 操作 | 条目数 | 操作人 |
|------|------|--------|--------|
| $TODAY | 初始化 | 0 | $(whoami) |

---

## 快速链接

- [WARM/README.md](WARM/README.md) — WARM 层使用指南
- [HOT/memory-hot.md](HOT/memory-hot.md) — HOT 内存
- [memory/templates/](../templates/) — 模板文件
- [state/](../state/) — 状态恢复文件
- [skills/memory-lesson-manager/](../../skills/memory-lesson-manager/) — 技能目录
INDEX
        log_info "已创建 INDEX: $INDEX_FILE"
    fi
fi

log_step "4/4 创建当日日记..."

# 创建当日日记
DIARY_FILE="$MEMORY_DIR/$TODAY.md"
if [ -f "$DIARY_FILE" ]; then
    if [ "$DRY_RUN" = true ]; then
        log_dry "当日日记已存在：$DIARY_FILE"
    else
        log_info "当日日记已存在：$DIARY_FILE"
    fi
else
    if [ "$DRY_RUN" = true ]; then
        log_dry "将创建当日日记：$DIARY_FILE"
    else
        cat > "$DIARY_FILE" << DIARY
# $TODAY_FULL

---

## HH:MM — 上下文恢复 [P3]
- 新的一天开始
- 记忆系统检查启动

---

## 待办事项

### 待办
- [ ] 任务 1
- [ ] 任务 2

---

## 日记模板

使用 \`memory/templates/diary-template.md\` 记录每日工作。

**反思环节（强制）：**
- **做得好的：** 
- **可改进的：** 
- **学到的：** 
DIARY
        log_info "已创建当日日记：$DIARY_FILE"
    fi
fi

# 创建 state 文件
SESSION_STATE_FILE="$STATE_DIR/session-state.md"
if [ -f "$SESSION_STATE_FILE" ]; then
    if [ "$DRY_RUN" = true ]; then
        log_dry "session-state.md 已存在：$SESSION_STATE_FILE"
    fi
else
    if [ "$DRY_RUN" = true ]; then
        log_dry "将创建 session-state.md: $SESSION_STATE_FILE"
    else
        cp "$STATE_DIR/session-state-template.md" "$SESSION_STATE_FILE"
        log_info "已创建 session-state.md: $SESSION_STATE_FILE"
    fi
fi

WORKING_BUFFER_FILE="$STATE_DIR/working-buffer.md"
if [ -f "$WORKING_BUFFER_FILE" ]; then
    if [ "$DRY_RUN" = true ]; then
        log_dry "working-buffer.md 已存在：$WORKING_BUFFER_FILE"
    fi
else
    if [ "$DRY_RUN" = true ]; then
        log_dry "将创建 working-buffer.md: $WORKING_BUFFER_FILE"
    else
        cp "$STATE_DIR/working-buffer-template.md" "$WORKING_BUFFER_FILE"
        log_info "已创建 working-buffer.md: $WORKING_BUFFER_FILE"
    fi
fi

log_step "完成"

if [ "$DRY_RUN" = true ]; then
    echo ""
    log_info "预览模式 - 未实际创建文件"
    echo "运行不带 --dry-run 的参数执行实际初始化"
else
    echo ""
    log_info "✅ 记忆系统初始化完成！"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "已创建："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  目录结构：memory/lessons/{HOT,WARM,COLD}"
    echo "  模板文件：${#TEMPLATES[@]} 个"
    echo "  索引文件：README.md, INDEX.md"
    echo "  当日日记：$DIARY_FILE"
    echo "  状态文件：session-state.md, working-buffer.md"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "下一步："
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  1. 编辑当日日记：$DIARY_FILE"
    echo "  2. 更新 session-state.md: $SESSION_STATE_FILE"
    echo "  3. 开始记录学习条目"
    echo ""
fi
