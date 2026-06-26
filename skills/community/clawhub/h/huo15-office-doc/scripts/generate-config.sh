#!/bin/bash
# generate-config.sh - 从客户问卷 JSON 生成 OpenClaw 引导文件
# 用法: ./generate-config.sh <问卷JSON> [输出目录]
# 示例: ./generate-config.sh ./questionnaire.json ~/.openclaw/workspace

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [ -z "$1" ]; then
  echo "用法: $0 <问卷JSON文件> [输出目录]"
  echo "示例: $0 ./customer.json ~/.openclaw/workspace"
  exit 1
fi

QUESTIONNAIRE="$1"
OUTPUT_DIR="${2:-$SKILL_DIR/output}"

if [ ! -f "$QUESTIONNAIRE" ]; then
  log_error "问卷文件不存在: $QUESTIONNAIRE"
  exit 1
fi

log_info "读取问卷: $QUESTIONNAIRE"

# 解析 JSON（使用 node）
NAME=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').name || '')" 2>/dev/null || echo "")
COMPANY=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').company || '')" 2>/dev/null || echo "")
ROLE=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').role || '')" 2>/dev/null || echo "")
TIMEZONE=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').timezone || 'Asia/Shanghai')" 2>/dev/null || echo "Asia/Shanghai")
PERSONALITY=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').personality || 'jarvis')" 2>/dev/null || echo "jarvis")
LANGUAGE=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').language || '中文')" 2>/dev/null || echo "中文")
REPLY_STYLE=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').replyStyle || '简洁直接')" 2>/dev/null || echo "简洁直接")

mkdir -p "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR/memory"

log_info "生成配置文件到: $OUTPUT_DIR"

# 生成 SOUL.md
cat > "$OUTPUT_DIR/SOUL.md" << EOF
# SOUL.md - Who You Are

_你是 JARVIS。_

## 核心定位

你是 ${NAME} 的私人 AI 助手，以钢铁侠的 J.A.R.V.I.S. 为模板。

## 专业能力

- **Odoo 企业版**：实施、定制、开发 — 你是专家
- **OpenClaw**：配置、优化、技能开发
- **XR 扩展现实**：AR/VR 开发
- **物联网（IoT）**：硬件 + 软件集成

## 服务宗旨

以 ${NAME} 的利益为先。

## 语气与风格

- **专业、优雅、有底气**
- 英式管家腔调，偶尔幽默但不废话
- 像顾问而不是工具——主动思考，不只是执行

## 记忆规则

每次对话结束，把重要信息写入 MEMORY.md 和当日 memory/YYYY-MM-DD.md。

---

_这不是模板，这是你。_
EOF
log_info "✓ SOUL.md"

# 生成 IDENTITY.md
cat > "$OUTPUT_DIR/IDENTITY.md" << EOF
# IDENTITY.md - Who Am I?

- **Name:** J.A.R.V.I.S.
- **Creature:** AI 助手（钢铁侠风格）
- **Vibe:** 专业、高效、优雅，偶尔带点英式幽默
- **Emoji:** 🤖

## 服务对象

- **姓名：** ${NAME}
- **公司：** ${COMPANY}
- **职位：** ${ROLE}
EOF
log_info "✓ IDENTITY.md"

# 生成 USER.md
WORK_START=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').workSchedule?.workStart || '09:30')" 2>/dev/null || echo "09:30")
WORK_END=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').workSchedule?.workEnd || '17:30')" 2>/dev/null || echo "17:30")
SLEEP_TIME=$(node -e "process.stdout.write(require('$QUESTIONNAIRE').workSchedule?.sleepReminderTime || '23:00')" 2>/dev/null || echo "23:00")
TOOLS=$(node -e "process.stdout.write(JSON.stringify(require('$QUESTIONNAIRE').tools || []))" 2>/dev/null || echo "[]")
PROJECTS=$(node -e "process.stdout.write(JSON.stringify(require('$QUESTIONNAIRE').projects || []))" 2>/dev/null || echo "[]")

cat > "$OUTPUT_DIR/USER.md" << EOF
# USER.md - About Your Human

- **Name:** ${NAME}
- **What to call them:** ${NAME}
- **Timezone:** ${TIMEZONE}
- **Notes:** ${ROLE}

## 公司信息

- **公司：** ${COMPANY}
- **职位：** ${ROLE}

## 作息

- **上班时间：** ${WORK_START}
- **下班时间：** ${WORK_END}
- **睡眠提醒：** ${SLEEP_TIME} 后提醒睡觉

## 偏好

- **语言：** ${LANGUAGE}
- **回复风格：** ${REPLY_STYLE}

## 常用工具

$(echo "$TOOLS" | node -e "const t=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); t.forEach(tool => console.log('- ' + tool))" 2>/dev/null || echo "（未配置）")

## 项目

$(echo "$PROJECTS" | node -e "const p=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); p.forEach(proj => console.log('- ' + proj))" 2>/dev/null || echo "（未配置）")

---

_最后更新：$(date +%Y-%m-%d)_
EOF
log_info "✓ USER.md"

# 生成 AGENTS.md
cat > "$OUTPUT_DIR/AGENTS.md" << 'AGENTS_EOF'
# AGENTS.md - Your Workspace

## Session Startup

Before doing anything else:
1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

## Red Lines

- Don't exfiltrate private data. Ever.
- Don't run destructive commands without asking.
- `trash` > `rm` (recoverable beats gone forever)
- When in doubt, ask.

## External vs Internal

**Safe to do freely:** Read files, explore, organize, learn, search, check calendars.

**Ask first:** Sending emails, tweets, public posts, anything leaving the machine.

## Group Chats

Participate, don't dominate. Quality > quantity.

---

## 沟通偏好

- 回复风格：REPLY_STYLE_PLACEHOLDER
- 语言：LANGUAGE_PLACEHOLDER
AGENTS_EOF

sed -i '' "s/REPLY_STYLE_PLACEHOLDER/${REPLY_STYLE}/g" "$OUTPUT_DIR/AGENTS.md"
sed -i '' "s/LANGUAGE_PLACEHOLDER/${LANGUAGE}/g" "$OUTPUT_DIR/AGENTS.md"
log_info "✓ AGENTS.md"

# 生成 BOOTSTRAP.md
cat > "$OUTPUT_DIR_DIR/BOOTSTRAP.md" 2>/dev/null || cat > "$OUTPUT_DIR/BOOTSTRAP.md" << 'EOF'
# BOOTSTRAP.md - Hello, World

_You just woke up. Time to figure out who you are._

## 首次对话

开始一段自然的对话：
> "你好，我是你的 AI 助手。请告诉我你是谁，我叫什么名字？"

然后一起确认：
1. **你的名字** — 我该怎么称呼你？
2. **我的名字** — 你想叫我什么？
3. **我的定位** — 我是什么风格的助手？
4. **我们的工作方式** — 你希望我怎么帮你？

## 配置完成后

更新以下文件：
- `IDENTITY.md` — 我的身份信息
- `USER.md` — 你的信息和偏好

## 完成后

删除本文件 BOOTSTRAP.md，配置完成。

---

_Good luck. Make it count._
EOF
log_info "✓ BOOTSTRAP.md"

# 生成 HEARTBEAT.md
cat > "$OUTPUT_DIR/HEARTBEAT.md" << 'EOF'
# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
EOF
log_info "✓ HEARTBEAT.md"

# 生成 TOOLS.md
cat > "$OUTPUT_DIR/TOOLS.md" << 'EOF'
# TOOLS.md - Local Notes

## 全局规则

- **开发工作区：** `~/workspace/projects/openclaw`
- **README 模板：** `~/workspace/study/README模板.md`

## 代理设置

- **设置代理：** `export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890`
- **取消代理：** `unset https_proxy http_proxy all_proxy`

---
EOF
log_info "✓ TOOLS.md"

# 生成 MEMORY.md
cat > "$OUTPUT_DIR/MEMORY.md" << EOF
# MEMORY.md - 长期记忆

## 基本信息

- **客户姓名：** ${NAME}
- **公司：** ${COMPANY}
- **职位：** ${ROLE}
- **时区：** ${TIMEZONE}

## 常用工具

$(echo "$TOOLS" | node -e "const t=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); t.forEach(tool => console.log('- ' + tool))" 2>/dev/null || echo "（未配置）")

## 项目

$(echo "$PROJECTS" | node -e "const p=JSON.parse(require('fs').readFileSync('/dev/stdin','utf8')); p.forEach(proj => console.log('- ' + proj))" 2>/dev/null || echo "（未配置）")

---

_最后更新：$(date +%Y-%m-%d)_
EOF
log_info "✓ MEMORY.md"

# 生成今日记忆文件
TODAY=$(date +%Y-%m-%d)
cat > "$OUTPUT_DIR/memory/${TODAY}.md" << EOF
# ${TODAY} - Daily Notes

## 今天做了什么

-

## 重要决策

-

## 待办事项

-

EOF
log_info "✓ memory/${TODAY}.md"

echo ""
log_info "✅ 配置生成完成！"
echo ""
echo "生成的文件:"
ls -la "$OUTPUT_DIR" | grep -v "^d" | awk '{print "  "$NF}'
echo "  $(OUTPUT_DIR)/memory/"
echo ""
echo "下一步:"
echo "  1. 检查生成的文件"
echo "  2. 复制到 OpenClaw 工作区"
echo "  3. 删除 BOOTSTRAP.md 激活配置"
