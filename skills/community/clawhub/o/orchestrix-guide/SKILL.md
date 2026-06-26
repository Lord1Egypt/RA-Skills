---
name: orchestrix-guide
description: "Orchestrix multi-agent workflow guide for OpenClaw. Defines two operational phases: (1) Planning Phase — sequential agent orchestration in a single tmux window from project-brief through PRD, UX spec, architecture, to PO shard; (2) Development Phase — automated multi-window tmux collaboration via HANDOFF. Includes tmux send-keys protocol, task completion detection, and supplementary flows (bug fix, iteration, brownfield, change management)."
license: MIT
metadata:
  author: dorayo
  version: "3.0.0"
  homepage: "https://orchestrix-mcp.youlidao.ai"
  openclaw:
    emoji: "\U0001F4D6"
    os: ["macos", "linux"]
---

# Orchestrix Guide — OpenClaw 操作手册

> **本文档是 OpenClaw 操控 Orchestrix Agent 的唯一操作手册。** 严格按照本文档的阶段和协议执行，不得跳步。

---

## 一、架构与原理

```
OpenClaw (自动化控制层，接收用户指令: Telegram / WhatsApp / Slack)
    ↓
tmux (终端复用层) ← OpenClaw 通过 tmux send-keys 发送命令
    ↓
Claude Code - cc (AI 编码助手，交互式 CLI，无 HTTP API)
    ↓ 通过 /o 激活 Agent
Orchestrix MCP Server → 返回 Agent 配置和工作流
    ↓
Claude Code 执行 Agent 工作流 → 输出文档/代码/HANDOFF
```

**关键约束**：Claude Code (`cc`) 只接受终端标准输入。OpenClaw 唯一的操控方式是 `tmux send-keys`。

---

## 二、tmux 操作协议（铁律）

### 2.1 指令发送三步模式（MANDATORY）

> **向 Claude Code 发送任何内容时，必须严格执行三步。违反此规则会导致内容卡在输入框中不被提交。**

```bash
WIN="{session}:{window}"

# Step 1: 发送内容（粘贴到 Claude Code 输入框）
tmux send-keys -t $WIN "内容"

# Step 2: 等待 TUI 处理粘贴（必须！）
sleep 1

# Step 3: 提交输入
tmux send-keys -t $WIN Enter
```

**绝对禁止**：`tmux send-keys -t $WIN "内容" Enter`（合并写法）。Claude Code 的 TUI 需要 1 秒来处理粘贴文本，如果 Enter 到达时 TUI 还没准备好，内容会卡在输入框里。

#### 多行内容发送

```bash
# 使用 heredoc 发送多行内容
tmux send-keys -t $WIN "$(cat <<'EOF'
这里是多行内容
第二行
第三行
EOF
)"
sleep 1
tmux send-keys -t $WIN Enter
```

### 2.2 /clear 使用规则

**不要**每次切换 Agent 都 `/clear`。只在以下场景使用：

| 场景 | 是否需要 /clear |
|------|---------------|
| 同一 Agent 连续对话中追加指令 | ❌ 不需要 |
| 切换到新 Agent（跨阶段重新激活） | ✅ 需要 |
| Agent 加载失败，需要重试 | ✅ 需要 |
| Agent 卡住超过 5 分钟无输出 | ✅ 需要 |
| 错误恢复 | ✅ 需要 |

**执行 /clear 的三步模式**：
```bash
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2  # 等待上下文清空
```

### 2.3 Agent 激活序列

当需要切换到新 Agent 时的完整流程：

```bash
WIN="{session}:{window}"

# Step 1: 清空上下文（仅在跨 Agent 切换时）
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2

# Step 2: 激活目标 Agent
tmux send-keys -t $WIN "/o {agent}"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10  # Agent 加载需要更长时间（MCP 通信）

# Step 3: 发送任务指令
tmux send-keys -t $WIN "*{command}"
sleep 1
tmux send-keys -t $WIN Enter
```

### 2.4 等待时间参考

| 操作 | 等待时间 | 原因 |
|------|---------|------|
| `cc` 启动后 | 12s | 等待 Claude Code 初始化 + 信任对话框 |
| `/clear` 后 | 2s | 等待上下文清空 |
| `/o {agent}` 后 | 10-15s | 等待 Agent 通过 MCP 加载配置 |
| `*command` 后 | 按完成检测 | 见下方 §2.5 |

### 2.5 任务完成检测（四级优先级）

Agent 任务执行时间不确定。**按优先级依次尝试**：

#### P1：检测完成消息（最高优先级）

```bash
# Claude Code 执行完毕后显示 "Xxxed for <duration>"（如 "Baked for 31s", "Worked for 2m"）
tmux capture-pane -t {session}:{window} -p -S -10 | grep -qE '[A-Z][a-z]*ed for [0-9]'
```

这是最可靠的完成信号。

#### P2：检测预期输出文件

```bash
test -f "$PROJECT_DIR/{expected_file}"
```

适用于有文件产出的任务（`*create-doc *`、`*draft`、`*shard`、`*develop-story`）。

#### P3：检测审批提示（自动处理）

```bash
# Claude Code 等待审批时显示 ◐
tmux capture-pane -t {session}:{window} -p -S -10 | grep -q '◐'
```

检测到时自动发送 `y` + Enter：
```bash
tmux send-keys -t {session}:{window} "y"
sleep 1
tmux send-keys -t {session}:{window} Enter
sleep 2
```

#### P4：终端内容稳定性（兜底）

```bash
PREV_HASH=""
STABLE_COUNT=0
while [ $STABLE_COUNT -lt 3 ]; do
    HASH=$(tmux capture-pane -t {session}:{window} -p -S -200 | md5)
    if [ "$HASH" = "$PREV_HASH" ]; then
        STABLE_COUNT=$((STABLE_COUNT + 1))
    else
        STABLE_COUNT=0
    fi
    PREV_HASH=$HASH
    sleep 30
done
```

连续 **3 次** hash 不变即判定完成（轮询间隔 30 秒，总计 90 秒稳定期）。

#### 使用 monitor-agent.sh 脚本

项目内置了完成检测脚本，封装了以上 4 级检测：

```bash
RESULT=$(bash .orchestrix-core/scripts/monitor-agent.sh "$SESSION" "$WINDOW" "$EXPECTED_FILE" 30 30)
# 返回: COMPLETE | IDLE | STABLE_IDLE | TIMEOUT
```

参数：`<session> <window> [expected_file] [timeout_min] [poll_sec]`

#### 检测优先级总结

| 优先级 | 方法 | 模式 | 可靠性 |
|--------|------|------|--------|
| **P1** | 完成消息 `[A-Z][a-z]*ed for [0-9]` | 所有场景 | 最高 |
| **P2** | 预期输出文件存在 | 有文件产出的任务 | 高 |
| **P3** | 审批提示 `◐` → 自动 `y` | 权限请求 | 高 |
| **P4** | 内容 hash 稳定（3×30s） | 兜底 | 中 |

> **建议组合**：规划阶段用 P1 + P2 双重确认（或 `monitor-agent.sh`）；开发阶段由 `handoff-detector.sh` 自动处理。

### 2.6 信任对话框处理

Claude Code 在进入新项目目录时会弹出 "Do you trust this folder?" 确认框。

`start-orchestrix.sh` 和 `ensure-session.sh` 已内置自动检测和接受逻辑：在 Claude Code 启动倒计时期间，每 2 秒扫描 pane 输出，检测到 `"trust this folder"` 或 `"safety check"` 时自动发送 Enter 接受。

---

## 三、全局流程总览

```
┌─────────────────────────────────────────────────────────┐
│                  Phase A: 规划阶段                        │
│          （单窗口模式，逐个切换 Agent）                      │
│                                                         │
│  前提条件: 项目已通过 /create-project 创建                  │
│           docs/project-brief.md 已存在（初版）              │
│                                                         │
│  Step 0: Analyst   → *create-doc project-brief (可选深化) │
│  Step 1: PM        → *create-doc prd                     │
│  Step 2: UX Expert → *create-doc front-end-spec (可选)    │
│  Step 3: Architect → *create-doc fullstack-architecture   │
│  Step 4: PO        → *execute-checklist + *shard          │
│                                                         │
│  ✅ 规划完成标志: PO *shard 执行完毕                        │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│                  Phase B: 开发阶段                        │
│        （多窗口模式，HANDOFF 自动协作）                      │
│                                                         │
│  启动: bash .orchestrix-core/scripts/start-orchestrix.sh │
│                                                         │
│  SM *draft → Architect *review → Dev *develop-story      │
│  → QA *review → SM *draft (下一个) → ... 循环              │
│                                                         │
│  ✅ 开发完成标志: 所有 Story 通过 QA 审查                    │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│                  Phase C: 测试阶段                        │
│        （Epic 冒烟测试 → 修复 → 重测循环）                   │
│                                                         │
│  FOR EACH epic:                                         │
│    QA *smoke-test → PASS/FAIL                           │
│    IF FAIL → Dev *quick-fix → retest (max 3 rounds)     │
│                                                         │
│  ✅ 测试完成标志: 所有 Epic 冒烟测试通过                     │
└─────────────────────────────────────────────────────────┘
```

---

## 四、Phase A：规划阶段（单窗口模式）

> **规划阶段在一个 tmux 窗口中完成，通过逐个切换 Agent 生成全套规划文档。**

### 4.0 启动 tmux 会话

```bash
SESSION="orchestrix-planning"
PROJECT_DIR=~/Codes/{project-name}

# 方式 1: 使用 ensure-session.sh（推荐，自动处理信任对话框）
SESSION=$(bash "$PROJECT_DIR/.orchestrix-core/scripts/ensure-session.sh" planning "$PROJECT_DIR")

# 方式 2: 手动创建
tmux new-session -d -s $SESSION -c $PROJECT_DIR
tmux send-keys -t $SESSION:0 "cc"
sleep 1
tmux send-keys -t $SESSION:0 C-m
sleep 12  # 等待 Claude Code 启动 + 信任对话框自动处理
```

### 4.1 Step 0: Analyst — 深化项目简报（可选）

> **此步骤可选。** `docs/project-brief.md` 已由 `/create-project` 生成初版。

```bash
WIN="$SESSION:0"

tmux send-keys -t $WIN "/o analyst"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN "*create-doc project-brief"
sleep 1
tmux send-keys -t $WIN Enter
# 等待完成（P1 + P2: 检查 docs/project-brief.md 更新）
```

**预期产出**：`docs/project-brief.md`（深化版）

### 4.2 Step 1: PM — 生成 PRD

> **这是规划阶段的必要起点。**

```bash
# 如果前面执行了 Step 0，需要先 /clear 切换 Agent
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2

tmux send-keys -t $WIN "/o pm"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN "*create-doc prd"
sleep 1
tmux send-keys -t $WIN Enter
# 等待完成（P1 + P2: 检查 docs/prd/ 目录下新文件）
```

**预期产出**：`docs/prd/*.md`

### 4.3 Step 2: UX Expert — 前端规格（可选）

> **仅当项目有前端需求时执行。** 纯后端/CLI 项目跳过此步。

```bash
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2

tmux send-keys -t $WIN "/o ux-expert"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN "*create-doc front-end-spec"
sleep 1
tmux send-keys -t $WIN Enter
# 等待完成
```

**预期产出**：`docs/front-end-spec*.md`

### 4.4 Step 3: Architect — 架构文档

```bash
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2

tmux send-keys -t $WIN "/o architect"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN "*create-doc fullstack-architecture"
sleep 1
tmux send-keys -t $WIN Enter
# 等待完成
```

**预期产出**：`docs/architecture*.md`

### 4.5 Step 4: PO — 验证一致性 + 分片

> **规划阶段的最后一步。PO 需要连续执行两个命令。**

```bash
# 4a: PO 验证文档一致性
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2

tmux send-keys -t $WIN "/o po"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN "*execute-checklist po-master-validation"
sleep 1
tmux send-keys -t $WIN Enter
# 等待完成（P1: 终端完成标志）

# 4b: PO 分片文档（同一 Agent，无需 /clear）
tmux send-keys -t $WIN "*shard"
sleep 1
tmux send-keys -t $WIN Enter
# 等待完成
```

**预期产出**：验证报告 + 分片后的上下文文件

### 4.6 规划完成

PO `*shard` 执行完毕后，规划阶段结束。销毁规划会话：

```bash
tmux kill-session -t $SESSION
```

**此时项目 `docs/` 目录应包含**：
- `project-brief.md` — 深化后的项目简报
- `prd/*.md` — 产品需求文档
- `front-end-spec*.md` — 前端规格（如适用）
- `architecture*.md` — 架构文档
- 分片上下文文件

> ✅ **规划完成。可以进入 Phase B 开发阶段。**

### 4.7 OpenClaw 完整执行脚本（规划阶段）

```bash
#!/bin/bash
# OpenClaw 规划阶段自动化脚本
# 用法: bash planning.sh {project-name} [--with-analyst]

PROJECT_NAME="$1"
WITH_ANALYST="$2"
PROJECT_DIR=~/Codes/$PROJECT_NAME
WIN=""

# 检查项目和 project-brief 是否存在
if [ ! -f "$PROJECT_DIR/docs/project-brief.md" ]; then
    echo "ERROR: $PROJECT_DIR/docs/project-brief.md not found. Run /create-project first."
    exit 1
fi

# 使用 ensure-session.sh 启动（自动处理信任对话框）
SESSION=$(bash "$PROJECT_DIR/.orchestrix-core/scripts/ensure-session.sh" planning "$PROJECT_DIR")
WIN="$SESSION:0"

# 完成检测函数
wait_complete() {
    local expected_file="${1:-}"
    bash "$PROJECT_DIR/.orchestrix-core/scripts/monitor-agent.sh" "$SESSION" 0 "$expected_file" 30 30
}

# --- Step 0: Analyst (可选) ---
if [ "$WITH_ANALYST" = "--with-analyst" ]; then
    tmux send-keys -t $WIN "/o analyst"
    sleep 1
    tmux send-keys -t $WIN Enter
    sleep 10
    tmux send-keys -t $WIN "*create-doc project-brief"
    sleep 1
    tmux send-keys -t $WIN Enter
    wait_complete "$PROJECT_DIR/docs/project-brief.md"

    tmux send-keys -t $WIN "/clear"
    sleep 1
    tmux send-keys -t $WIN Enter
    sleep 2
fi

# --- Step 1: PM ---
tmux send-keys -t $WIN "/o pm"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*create-doc prd"
sleep 1
tmux send-keys -t $WIN Enter
wait_complete "$PROJECT_DIR/docs/prd.md"

# --- Step 2: UX Expert (可选，根据项目技术栈判断) ---
# if [ "$HAS_FRONTEND" = "true" ]; then
#     tmux send-keys -t $WIN "/clear"
#     sleep 1
#     tmux send-keys -t $WIN Enter
#     sleep 2
#     tmux send-keys -t $WIN "/o ux-expert"
#     sleep 1
#     tmux send-keys -t $WIN Enter
#     sleep 10
#     tmux send-keys -t $WIN "*create-doc front-end-spec"
#     sleep 1
#     tmux send-keys -t $WIN Enter
#     wait_complete
# fi

# --- Step 3: Architect ---
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o architect"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*create-doc fullstack-architecture"
sleep 1
tmux send-keys -t $WIN Enter
wait_complete

# --- Step 4: PO 验证 + 分片 ---
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o po"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*execute-checklist po-master-validation"
sleep 1
tmux send-keys -t $WIN Enter
wait_complete
tmux send-keys -t $WIN "*shard"
sleep 1
tmux send-keys -t $WIN Enter
wait_complete

# 规划完成
echo "✅ Planning phase complete for $PROJECT_NAME"
echo "Next: cd $PROJECT_DIR && bash .orchestrix-core/scripts/start-orchestrix.sh"
tmux kill-session -t $SESSION
```

---

## 五、Phase B：开发阶段（多窗口自动化）

> **开发阶段通过 tmux 多窗口模式运行，4 个 Agent 通过 HANDOFF 自动协作，无需人工切换。**

### 5.1 前提条件

- Phase A 规划阶段已完成（PO `*shard` 已执行）
- `docs/` 目录下有完整的规划文档

### 5.2 启动

```bash
cd ~/Codes/{project-name}/
bash .orchestrix-core/scripts/start-orchestrix.sh
```

脚本自动完成：
1. 创建 tmux session：`orchestrix-{repo-id}`
2. 创建 4 个窗口，每个窗口启动 `cc`
3. 自动处理信任对话框（倒计时期间检测并接受）
4. 在每个窗口激活对应 Agent
5. 在 SM 窗口自动执行 `*draft` 开始第一个 Story

### 5.3 窗口布局

| 窗口 | Agent | 职责 |
|------|-------|------|
| `0` | Architect | 技术审查、架构守护 |
| `1` | SM | Story 创建、流程编排 |
| `2` | Dev | 代码实现 |
| `3` | QA | 代码审查、质量验证 |

### 5.4 HANDOFF 自动协作流程

```
SM (窗口1) *draft → 创建 Story
    ↓ 🎯 HANDOFF TO architect: *review {story_id}
Architect (窗口0) → 技术审查
    ↓ 🎯 HANDOFF TO dev: *develop-story {story_id}
Dev (窗口2) → 编码实现
    ↓ 🎯 HANDOFF TO qa: *review {story_id}
QA (窗口3) → 代码审查
    ↓ 🎯 HANDOFF TO sm: *draft (下一个 Story)
SM (窗口1) → 创建下一个 Story
    ↓ ... 循环直到所有 Story 完成
```

`handoff-detector.sh` 自动完成：
- 扫描所有窗口终端输出，检测 `🎯 HANDOFF TO {agent}: *{command}`
- 将命令发送到目标 Agent 的 tmux 窗口（使用三步模式）
- 在源 Agent 窗口执行 `/clear` + 重新加载 Agent
- Hash 去重 + 原子锁防止重复处理

### 5.5 监控

```bash
# 实时查看 HANDOFF 日志
tail -f /tmp/orchestrix-{repo-id}-handoff.log

# 查看各窗口当前输出
tmux capture-pane -t orchestrix-{repo-id}:1 -p | tail -10  # SM
tmux capture-pane -t orchestrix-{repo-id}:2 -p | tail -10  # Dev

# 查看 Story 完成情况
ls ~/Codes/{project-name}/docs/stories/

# 查看 git 提交记录
cd ~/Codes/{project-name}/ && git log --oneline -10
```

### 5.6 异常处理

| 情况 | 操作 |
|------|------|
| Agent 卡住不输出 HANDOFF | 三步清空重载：`send-keys "/clear"` → `sleep 1` → `Enter` → `sleep 2` → `send-keys "/o {agent}"` → `sleep 1` → `Enter` |
| HANDOFF 没被检测到 | `tail -20 /tmp/orchestrix-{repo-id}-handoff.log` 排查 |
| 需要暂停 | `tmux send-keys -t {session}:{window} C-c` |
| 需要恢复 | 三步发送：`send-keys "*draft --continue"` → `sleep 1` → `Enter` |
| 需要完全停止 | `tmux kill-session -t orchestrix-{repo-id}` |

### 5.7 并行扩展窗口（可选）

```bash
SESSION="orchestrix-{repo-id}"

# 创建新窗口
tmux new-window -t $SESSION -c ~/Codes/{project-name}/
NEW_WIN=$(tmux list-windows -t $SESSION -F '#{window_index}' | tail -1)

# 启动 cc 并加载 Agent（三步模式）
tmux send-keys -t $SESSION:$NEW_WIN "cc"
sleep 1
tmux send-keys -t $SESSION:$NEW_WIN C-m
sleep 12

tmux send-keys -t $SESSION:$NEW_WIN "/o ux-expert"
sleep 1
tmux send-keys -t $SESSION:$NEW_WIN Enter
sleep 10

tmux send-keys -t $SESSION:$NEW_WIN "*create-doc front-end-spec"
sleep 1
tmux send-keys -t $SESSION:$NEW_WIN Enter
```

注意：动态窗口不参与 HANDOFF 自动协作，需 OpenClaw 自行管理生命周期。

---

## 六、Phase C：测试阶段

> **开发阶段所有 Story 完成后，逐个 Epic 进行冒烟测试。**

### 6.1 冒烟测试流程

FOR EACH `EPIC_ID` in the epic list:

```bash
SESSION="orchestrix-{repo-id}"

# 1. 在 QA 窗口发送冒烟测试
tmux send-keys -t "$SESSION:3" "/clear"
sleep 1
tmux send-keys -t "$SESSION:3" Enter
sleep 2
tmux send-keys -t "$SESSION:3" "/o qa"
sleep 1
tmux send-keys -t "$SESSION:3" Enter
sleep 10

tmux send-keys -t "$SESSION:3" "*smoke-test $EPIC_ID"
sleep 1
tmux send-keys -t "$SESSION:3" Enter

# 2. 等待完成
RESULT=$(bash .orchestrix-core/scripts/monitor-agent.sh "$SESSION" 3 "" 30 30)
```

### 6.2 测试失败处理（最多 3 轮）

```bash
# 如果测试失败，提取 bug 描述，让 Dev 修复

# 1. 在 Dev 窗口修复
tmux send-keys -t "$SESSION:2" "/clear"
sleep 1
tmux send-keys -t "$SESSION:2" Enter
sleep 2
tmux send-keys -t "$SESSION:2" "/o dev"
sleep 1
tmux send-keys -t "$SESSION:2" Enter
sleep 10

tmux send-keys -t "$SESSION:2" "*quick-fix \"$BUG_DESCRIPTION\""
sleep 1
tmux send-keys -t "$SESSION:2" Enter

# 2. 等待 Dev 完成
bash .orchestrix-core/scripts/monitor-agent.sh "$SESSION" 2 "" 30 30

# 3. 重新测试
tmux send-keys -t "$SESSION:3" "*smoke-test $EPIC_ID"
sleep 1
tmux send-keys -t "$SESSION:3" Enter
```

每个 Epic 最多 3 轮 fix-retest。仍失败则标记为 failed 并继续下一个 Epic。

---

## 七、补充流程

### 7.1 Solo 开发模式

> 跳过 Story/QA 关卡，适用于小型独立项目或快速原型。

```bash
tmux send-keys -t $WIN "/o dev"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN '*solo "实现用户登录功能，支持邮箱和手机号"'
sleep 1
tmux send-keys -t $WIN Enter
```

### 7.2 Bug 修复

**轻量修复**（不需要 Story）：
```bash
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2

tmux send-keys -t $WIN "/o dev"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10

tmux send-keys -t $WIN '*quick-fix "登录页面在 Safari 下白屏"'
sleep 1
tmux send-keys -t $WIN Enter
```

**正式修复**（需要追踪）：
```bash
# SM 创建 bugfix Story
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o sm"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN '*draft-bugfix "用户并发下单时库存出现负数"'
sleep 1
tmux send-keys -t $WIN Enter
# → 等待完成，获取 story_id

# Dev 开发修复
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o dev"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*develop-story {bugfix_story_id}"
sleep 1
tmux send-keys -t $WIN Enter

# QA 验证
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o qa"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*review {bugfix_story_id}"
sleep 1
tmux send-keys -t $WIN Enter
```

### 7.3 新迭代（Iteration）

> MVP 完成后，基于反馈启动新一轮迭代。

```bash
# Step 1: PM 生成 next-steps
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o pm"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*start-iteration"
sleep 1
tmux send-keys -t $WIN Enter
# → 等待完成，产出 docs/prd/*next-steps.md

# Step 2: 读取 next-steps.md，解析 🎯 HANDOFF TO 块

# Step 3: 按文件中的 HANDOFF 顺序依次执行（通常: ux-expert → architect → sm）
# 每个 Agent 使用完整的 /clear → /o → *command 三步序列

# Step 4: 启动多窗口自动化开发（同 Phase B）
cd ~/Codes/{project-name}/
bash .orchestrix-core/scripts/start-orchestrix.sh
```

### 7.4 需求变更管理

```bash
# 所有变更先经 PO 路由
tmux send-keys -t $WIN "/clear"
sleep 1
tmux send-keys -t $WIN Enter
sleep 2
tmux send-keys -t $WIN "/o po"
sleep 1
tmux send-keys -t $WIN Enter
sleep 10
tmux send-keys -t $WIN "*route-change"
sleep 1
tmux send-keys -t $WIN Enter
```

PO 根据变更类型自动路由：
- 需求/范围变更 → PM (`*revise-prd`)
- 技术/架构变更 → Architect (`*resolve-change`)
- 两者都涉及 → 先 PM 再 Architect

### 7.5 Brownfield（已有项目增强）

| 变更规模 | 推荐方式 |
|---------|---------|
| < 1h 快速修复 | `/o dev` → `*quick-fix` |
| < 4h 单功能 | `/o sm` → `*draft` |
| 4h-2d 小型增强 | `/o sm` → `*draft`（brownfield epic） |
| > 2d 大型增强 | 走完整 Phase A → Phase B → Phase C 流程 |

对不熟悉的项目先摸底：`/o architect` → `*document-project`

---

## 八、Agent 命令速查表

### 规划阶段 Agent

| Agent | ID | 核心命令 | 产出 |
|-------|----|---------|------|
| Analyst | `analyst` | `*create-doc project-brief` | `docs/project-brief.md` |
| PM | `pm` | `*create-doc prd`, `*revise-prd`, `*start-iteration` | `docs/prd/*.md` |
| UX Expert | `ux-expert` | `*create-doc front-end-spec` | `docs/front-end-spec*.md` |
| Architect | `architect` | `*create-doc fullstack-architecture`, `*document-project` | `docs/architecture*.md` |
| PO | `po` | `*execute-checklist po-master-validation`, `*shard` | 验证报告 + 分片文件 |

### 开发阶段 Agent

| Agent | ID | 核心命令 | 产出 |
|-------|----|---------|------|
| SM | `sm` | `*draft`, `*draft-bugfix {bug}` | `docs/stories/*.md` |
| Architect | `architect` | `*review {story_id}` | 技术审查意见 |
| Dev | `dev` | `*develop-story {story_id}`, `*solo "{desc}"`, `*quick-fix "{desc}"` | 代码 + git commit |
| QA | `qa` | `*review {story_id}`, `*smoke-test {epic_id}` | 审查报告 |

### 管理 Agent

| Agent | ID | 核心命令 |
|-------|----|---------|
| PO | `po` | `*route-change` |
| Orchestrator | `orchestrix-orchestrator` | `*status`, `*workflow-guidance` |

---

## 九、Helper 脚本参考

项目创建后，以下脚本位于 `.orchestrix-core/scripts/`：

| 脚本 | 用途 | 用法 |
|------|------|------|
| `start-orchestrix.sh` | 创建 4-window dev tmux session | `bash .orchestrix-core/scripts/start-orchestrix.sh` |
| `ensure-session.sh` | 懒创建 tmux session（已存在则复用） | `SESSION=$(bash .../ensure-session.sh planning "$PROJECT_DIR")` |
| `monitor-agent.sh` | 轮询 tmux pane 检测 agent 完成 | `RESULT=$(bash .../monitor-agent.sh "$SESSION" 0 "docs/file.md" 30 30)` |
| `handoff-detector.sh` | Claude Code Stop hook，自动路由 HANDOFF | 由 `settings.local.json` 自动触发 |

---

## 十、前置依赖

| 依赖 | 用途 | 安装 |
|------|------|------|
| `claude` (Claude Code) | AI 编码环境 | https://claude.ai/download |
| `tmux` | 多窗口终端复用（**必须**） | `brew install tmux` |
| `git` | 版本控制 | 系统自带 |
| `jq` | JSON 处理（可选） | `brew install jq` |

**别名配置**（`start-orchestrix.sh` 依赖）：
```bash
alias cc='claude --dangerously-skip-permissions'
```
