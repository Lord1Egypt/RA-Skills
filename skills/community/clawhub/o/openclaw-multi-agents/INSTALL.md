# 安装指南

**版本：** 6.0.0  
**架构：** v6 三层级架构（Planning → Manager → Workers）

> 本文件是给人类用户看的操作指南，说明如何在 OpenClaw 中配置持久多 Agent 团队。

---

## 核心概念：v6 三层级架构

```
用户 (User)
    ↓
主 Agent (Main Agent) - Pure Relay 角色
    ↓
Manager Agent (协调者)
    ↓
Worker Agents (执行者)
```

**v6 重大变化：**
- **必须先进行 Planning Phase**（用户访谈）才能创建 Agent
- **必须先创建 Manager Agent**，然后才能创建 Workers
- Main Agent 变为 Pure Relay 角色，不再直接管理 Workers
- Workers 的 session key 后缀从 `:main` 改为 `:manager`

---

## 两个目录，职责不同

| 目录 | 作用 | 放什么 |
|------|------|--------|
| `~/.openclaw/workspace-<agentId>/` | Agent 的**大脑**（workspace） | SOUL.md、AGENTS.md、skills/ |
| `~/.openclaw/agents/<agentId>/` | Agent 的**状态**（agentDir） | sessions/（会话历史）、agent/（auth） |

**常见误区：** 看到 `~/.openclaw/agents/` 下有 `claude-code/`、`gemini/` 等目录，**不代表有子 Agent 团队**。那些是编程工具的 session 目录，没有 workspace，也没有 SOUL.md。

**判断是否有子 Agent 团队的唯一正确方式**：查看 `~/.openclaw/openclaw.json` 的 `agents.list` 里是否有 main 之外的成员。

---

## 前提条件

### 1. OpenClaw 版本要求

OpenClaw CLI 使用**日历式版本号**（如 **2026.3.x**），请以你本机 `openclaw --version` 输出为准。

- **最低建议：** **2026.3.x** 及以上（需支持 v6：Manager Agent、`tools.agentToAgent`、`tools.sessions.visibility` 等）
- **若版本过旧：** 先升级 CLI，再按本指南配置；具体升级方式见官方文档

检查版本：

```bash
openclaw --version
```

```powershell
openclaw --version
```

### 2. 规划阶段准备

v6 架构要求**必须先完成 Planning Phase** 才能创建 Agent：

- 预留 15-30 分钟进行用户访谈
- 准备好描述你的工作流程和痛点
- 了解你的任务类型（创意型/分析型/执行型/审查型/协调型）

### 3. 基础环境

- Linux / macOS / Windows（PowerShell）
- **Bash**（用于 `run_planning_interview.sh`、`setup_team.sh`；Windows 可用 Git Bash 或 WSL）
- **PowerShell**：可用 `scripts\setup_team.ps1` / `setup_agent.ps1` 创建 v6 工作区（与 `setup_team.sh` 流程对齐）
- 已配置 OpenClaw CLI 认证

---

## v6 安装流程（5 步法）

### Step 1: Planning Phase（用户访谈）

**这是 v6 新增步骤，必须先完成才能创建 Agent。**

运行规划访谈脚本：

```bash
bash scripts/run_planning_interview.sh
```

脚本会引导你完成 10 个结构化问题：
1. 描述你的典型工作流程
2. 识别当前最大的 3 个痛点
3. 任务类型分类
4. 协作模式偏好
5. 质量要求
6. 成功案例分享
7. 失败案例分析
8. 与 AI 的理想关系
9. 特殊约束条件
10. 3 个月后的成功愿景

**输出：** `team-design.md`（团队设计文档）

**跳过规划（仅当你已有设计文档）：**
```bash
bash scripts/setup_team.sh --skip-planning --template product-dev
```

---

### Step 2: 审阅团队设计（用户确认）

打开生成的 `team-design.md`，确认以下内容：

- [ ] 工作流程描述准确
- [ ] 痛点分析符合实际情况
- [ ] 推荐的团队配置合理
- [ ] Manager Agent 选择恰当
- [ ] Worker Agents 分工明确
- [ ] 人格原型选择合适

**重要：** 必须获得用户确认后才能继续创建 Agent。

---

### Step 3: 创建 Manager Agent（必须先创建）

**v6 关键规则：必须先创建 Manager，然后才能创建 Workers。**

使用模板快速创建：

```bash
# 使用预定义模板（自动创建 Manager + Workers）
bash scripts/setup_team.sh --template product-dev

# 只创建 Manager（稍后手动添加 Workers）
bash scripts/setup_team.sh --manager-only --template product-dev
```

**手动创建 Manager：**

```bash
# 使用 setup_agent.sh 的 --type manager 参数
bash scripts/setup_agent.sh --type manager gantt '亨利·甘特' glm-5
```

**Manager Agent 配置要点：**
- Session key 后缀：`:main`（与 Main Agent 通信）
- 职责：规划、协调、验证、质量把关
- 必须配置在 openclaw.json 的 `agents.list` 中

---

### Step 4: 创建 Worker Agents（Manager 存在后才能创建）

**Worker 创建必须在 Manager 之后。**

如果使用 `setup_team.sh` 模板，Workers 会自动创建。

**手动创建 Worker：**

```bash
# 使用 --type worker 和 --manager-id 参数
bash scripts/setup_agent.sh \
  --type worker \
  --manager-id gantt \
  munger '查理·芒格' glm-5
```

**Worker Agent 配置要点：**
- Session key 后缀：`:manager`（与 Manager 通信，不是 `:main`）
- 职责：专注专业领域的任务执行
- 不直接与 Main Agent 通信

**创建多个 Workers：**

```bash
# 费曼 - 深度开发
bash scripts/setup_agent.sh \
  --type worker \
  --manager-id gantt \
  feynman '理查德·费曼' glm-5

# 德明 - 质量把关
bash scripts/setup_agent.sh \
  --type worker \
  --manager-id gantt \
  deming 'W. Edwards Deming' glm-5
```

---

### Step 5: 配置 openclaw.json

编辑 `~/.openclaw/openclaw.json`，添加所有 Agent：

```json5
{
  agents: {
    defaults: {
      model: {
        // 全局主模型
        primary: "anthropic/claude-opus-4-6",
        // 全局 Fallback Chain
        fallbacks: [
          "openrouter/moonshotai/kimi-k2",
          "openrouter/z-ai/glm-5",
          "anthropic/claude-sonnet-4-6",
        ],
      },
    },
    list: [
      // 主 Agent（已有）
      {
        id: "main",
        default: true,
        workspace: "~/.openclaw/workspace",
      },
      // Manager Agent（v6 新增，必须先创建）
      {
        id: "manager",
        name: "亨利·甘特",
        workspace: "~/.openclaw/workspace-manager",
        model: "anthropic/claude-opus-4-6",
      },
      // Worker Agents（在 Manager 之后创建）
      {
        id: "munger",
        name: "芒格",
        workspace: "~/.openclaw/workspace-munger",
        model: "anthropic/claude-opus-4-6",
      },
      {
        id: "feynman",
        name: "费曼",
        workspace: "~/.openclaw/workspace-feynman",
        model: "openai/gpt-5.3-codex",
      },
      {
        id: "deming",
        name: "德明",
        workspace: "~/.openclaw/workspace-deming",
        model: "anthropic/claude-opus-4-6",
      },
    ],
  },

  // 必须：启用 Agent 间通信
  tools: {
    sessions: {
      visibility: "all",
    },
    agentToAgent: {
      enabled: true,
      // v6: 必须包含 "main"，否则 Main Agent 无法发送消息
      allow: ["main", "manager", "munger", "feynman", "deming"],
    },
  },
}
```

**重启 gateway 使配置生效：**

```bash
openclaw gateway restart
```

**初始化 Wisdom 目录（推荐）：**

```bash
# 创建 wisdom 目录并复制样例文件
mkdir -p ~/.openclaw/workspace/memory/wisdom
SKILL_DIR="$(openclaw skills info openclaw-multi-agents --json 2>/dev/null | grep path | head -1 | sed 's/.*: "\(.*\)".*/\1/' || find ~/.openclaw/workspace/skills -name "SKILL.md" | grep multi-agents | xargs dirname)"
if [ -n "$SKILL_DIR" ] && [ -d "$SKILL_DIR/examples/wisdom" ]; then
  cp "$SKILL_DIR/examples/wisdom/"*.md ~/.openclaw/workspace/memory/wisdom/
  echo "✅ Wisdom 样例已复制"
else
  echo "⚠️ 请手动复制：cp <skill目录>/examples/wisdom/*.md ~/.openclaw/workspace/memory/wisdom/"
fi
```

> Wisdom 文件用于积累团队经验教训，Main Agent 派活时会注入相关内容给 Workers。

**验证团队配置：**

```bash
# 确认所有 Agent 已注册
openclaw agents list

# 期望输出：
# ID        Name      Workspace
# main      爱兔      ~/.openclaw/workspace
# manager   亨利·甘特  ~/.openclaw/workspace-manager
# munger    芒格      ~/.openclaw/workspace-munger
# feynman   费曼      ~/.openclaw/workspace-feynman
# deming    德明      ~/.openclaw/workspace-deming
```

---

## Planning Phase 详解

### 为什么需要规划阶段

v6 架构引入 Planning Phase 是为了解决以下问题：

1. **避免盲目配置** - 先理解需求，再设计团队
2. **定制化设计** - 每个团队都是根据用户 workflow 量身定制
3. **用户参与** - 用户参与决策，不是被动接受配置
4. **明确目标** - 3 个月后的成功标准在开始前就确定

### 访谈流程示例

```
═══════════════════════════════════════════════════════════════
  Multi-Agent Orchestration - v6 团队规划访谈
═══════════════════════════════════════════════════════════════

本访谈将帮助你设计最适合的 Agent 团队配置。
预计耗时：15-30 分钟
输出：team-design.md（团队设计文档）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  第一轮：Workflow 理解
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q1: 请描述你典型的工作流程（主要任务类型）
   例如：需求分析 → 开发 → 测试 → 部署
   回答: ________________________________

Q2: 你目前最大的 3 个痛点是什么？
   痛点 1: ________________________________
   痛点 2: ________________________________
   痛点 3: ________________________________

Q3: 你的任务可以分成哪几类？
   选项: 创意型 / 分析型 / 执行型 / 审查型 / 协调型
   回答: ________________________________

Q4: 你需要怎样的协作模式？
   1) 自主型 - 给目标，AI 自己探索
   2) 陪伴型 - 边做边讨论，实时反馈
   3) 流水线型 - 明确分工，按步骤执行
   4) 顾问型 - 先咨询建议，再决定
   选择 (1-4): ________________________________

Q5: 你对输出质量的要求是什么？
   1) 速度优先
   2) 平衡型
   3) 质量优先
   4) 零容忍
   选择 (1-4): ________________________________

[继续第二轮...]
```

### 团队设计文档内容

生成的 `team-design.md` 包含：

1. **项目/Workflow 摘要** - 工作流程描述、输入输出
2. **痛点识别** - 优先级排序的痛点列表
3. **推荐团队组成** - ASCII 架构图、Agent 详细配置
4. **通信流程** - Session keys、消息流向图
5. **任务类别映射** - 每个 Agent 的 Task Category 和 Model
6. **实施检查清单** - 分步骤的实施指南
7. **用户确认部分** - 需要用户勾选的确认项

---

## 创建你的团队（详细步骤）

### 方法 A：使用 setup_team.sh（推荐）

**完整流程（Planning + Manager + Workers）：**

```bash
# 1. 运行规划访谈（生成 team-design.md）
bash scripts/run_planning_interview.sh

# 2. 审阅 team-design.md，确认设计

# 3. 使用模板创建完整团队
bash scripts/setup_team.sh --template product-dev

# 4. 按脚本提示更新 openclaw.json

# 5. 重启 gateway
openclaw gateway restart
```

**可用模板：**

| 模板名 | Manager | Workers | 适用场景 |
|--------|---------|---------|----------|
| `product-dev` | 亨利·甘特 | 芒格 + 费曼 + 德明 + 德鲁克 | 产品开发团队 |
| `marketing` | 项目经理 | 乔布斯 + 芒格 + 卡尼曼 | 营销增长团队 |
| `research` | 研究主管 | 图灵 + 费曼 + 芒格 | 研究开发团队 |
| `content` | 内容总监 | 乔布斯 + 奥格威 + 德明 | 内容创作团队 |
| `small` | 亨利·甘特 | 费曼 + 德明 | 轻量级团队 |

**命令行选项：**

```bash
# 跳过规划（已有 team-design.md）
bash scripts/setup_team.sh --skip-planning --template product-dev

# 只创建 Manager
bash scripts/setup_team.sh --manager-only --template product-dev

# 显示帮助
bash scripts/setup_team.sh --help
```

---

### 方法 B：手动配置

**Step 1: 运行规划访谈**

```bash
bash scripts/run_planning_interview.sh
```

**Step 2: 创建 Manager Agent**

```bash
# 创建 Manager workspace
mkdir -p ~/.openclaw/workspace-manager

# 创建 Manager SOUL.md（参考 docs/team_templates.md）
# 创建 Manager AGENTS.md
```

**Step 3: 创建 Worker Agents（Manager 存在后）**

```bash
# 为每个 Worker 创建 workspace
mkdir -p ~/.openclaw/workspace-munger
mkdir -p ~/.openclaw/workspace-feynman
mkdir -p ~/.openclaw/workspace-deming

# 写入 SOUL.md（必须包含 v6 协调关系部分）
```

**Step 4: 配置 openclaw.json**

添加 Manager 和所有 Workers 到 `agents.list`。

**Step 5: 重启 gateway**

```bash
openclaw gateway restart
```

---

## v6 Session Key 参考

### 三层级架构通信模式

| 方向 | Session Key | 用途 |
|------|-------------|------|
| Main → Manager | `agent:manager:main` | 主 Agent 分发任务给 Manager |
| Manager → Main | `agent:main:manager` | Manager 向主 Agent 汇报状态 |
| Manager → Worker | `agent:<worker>:manager` | Manager 分配任务给 Worker |
| Worker → Manager | `agent:manager:<worker>` | Worker 向 Manager 汇报状态 |

### 示例通信流程

```typescript
// 1. 用户请求 → Main Agent
// Main Agent 直接回答或转交 Manager

// 2. Main Agent → Manager Agent
sessions_send({
  sessionKey: "agent:manager:main",
  message: "用户请求：...",
  timeoutSeconds: 0  // 绝不阻塞
})

// 3. Manager Agent → Worker Agent
sessions_send({
  sessionKey: "agent:munger:manager",
  message: "任务：...",
  timeoutSeconds: 0
})

// 4. Worker Agent → Manager Agent
sessions_send({
  sessionKey: "agent:manager:munger",
  message: "任务完成报告：..."
})

// 5. Manager Agent → Main Agent
sessions_send({
  sessionKey: "agent:main:manager",
  message: "整体进度：..."
})
```

---

## 故障排查（v6 特有问题）

### 问题：Worker 创建失败，提示 Manager 不存在

**症状：**
```
❌ 错误：Manager Agent 'manager' 不存在
请先创建 Manager Agent，然后再创建 Workers
```

**原因：**
v6 架构要求必须先创建 Manager Agent，Workers 依赖 Manager 进行协调。

**解决：**
```bash
# 1. 先创建 Manager
bash scripts/setup_agent.sh --type manager manager '亨利·甘特' glm-5

# 2. 确认 Manager workspace 存在
ls ~/.openclaw/workspace-manager/

# 3. 再创建 Workers
bash scripts/setup_agent.sh --type worker --manager-id manager munger '查理·芒格' glm-5
```

---

### 问题：Session key 不匹配

**症状：**
- Worker 收不到 Manager 的消息
- `sessions_list` 找不到 Worker 的 session

**原因：**
v6 中 Worker 的 session key 后缀从 `:main` 改为 `:manager`。

**检查清单：**

```bash
# 检查 Worker SOUL.md 中的协调关系部分
grep "协调关系" ~/.openclaw/workspace-munger/SOUL.md

# 应该显示：
# ## 协调关系（v6 架构）
# **我的协调者：** Manager Agent

# 检查 session key 格式
grep "agent:munger:manager" ~/.openclaw/workspace-munger/SOUL.md

# 应该使用 :manager 后缀，不是 :main
```

**修复：**
如果 Worker 使用旧的 `:main` 后缀，需要更新 SOUL.md：

```bash
# 将 :main 替换为 :manager
sed -i 's/agent:munger:main/agent:munger:manager/g' ~/.openclaw/workspace-munger/SOUL.md
```

---

### 问题：Planning Phase 被跳过

**症状：**
- 直接运行 `setup_team.sh` 而没有先运行 `run_planning_interview.sh`
- 生成的团队配置不符合实际需求

**解决：**
```bash
# 1. 删除可能存在的旧设计文档
rm -f team-design.md

# 2. 重新运行规划访谈
bash scripts/run_planning_interview.sh

# 3. 审阅生成的 team-design.md

# 4. 使用 --skip-planning 重新创建团队
bash scripts/setup_team.sh --skip-planning --template product-dev
```

---

### 问题：Main Agent 仍然尝试直接管理 Workers

**症状：**
- Main Agent 直接给 Worker 发任务，而不是通过 Manager
- 提示 "Conductor" 角色相关的内容

**原因：**
Main Agent 的 SOUL.md 仍是旧版「指挥者（Conductor）」设定，未按 Pure Relay 更新。

**解决：**
更新 Main Agent 的 SOUL.md，添加以下内容：

```markdown
## 身份定位

我是通信桥梁，不是执行者。

- 我不执行任务，只传递信息
- 我不做决策，只转达请求
- 我不管理 Workers，Manager 是我的执行伙伴

## 职责边界

**我绝不做的:**
- 直接给 Worker 发任务（只与 Manager 通信）
- 自己执行具体任务（写代码、出方案、做分析）
- 等待任务完成才回复用户（阻塞是禁止的）
- 管理任务依赖关系（Manager 负责编排）
```

---

### 问题：Manager 没有收到 Main Agent 的消息

**症状：**
- Main Agent 调用 `sessions_send` 到 `agent:manager:main` 但没有响应
- Manager 的 session 历史中没有记录

**检查清单：**

```bash
# 1. 检查 openclaw.json 配置
cat ~/.openclaw/openclaw.json | grep -A 5 "agentToAgent"

# 应该包含：
# "agentToAgent": {
#   "enabled": true,
#   "allow": ["manager", "munger", ...]
# }

# 2. 检查 Manager 是否已注册
openclaw agents list

# 3. 检查 Manager workspace 是否存在
ls ~/.openclaw/workspace-manager/SOUL.md

# 4. 重启 gateway
openclaw gateway restart
```

---

## 卸载子 Agent

```bash
# 1. 从 openclaw.json 的 agents.list 中移除该 Agent 条目
# 2. 重启 gateway
openclaw gateway restart

# 3. 可选：删除 workspace（会同时删除 SOUL.md 和记忆）
rm -rf ~/.openclaw/workspace-manager
rm -rf ~/.openclaw/workspace-munger

# 4. 可选：删除 session 历史
rm -rf ~/.openclaw/agents/manager
rm -rf ~/.openclaw/agents/munger
```

---

**最后更新：** 2026-03-19  
**版本：** 6.0.0
