---
name: openclaw-soul
description: OpenClaw 自我进化框架一键部署。安装宪法(AGENTS.md)、可进化灵魂(SOUL.md)、心跳系统、PARA三层记忆架构、目标管理，并通过场景化对话引导用户定义 Agent 性格。自动配置 EvoClaw（审批制进化）和 Self-Improving Agent（自主学习）。触发场景："setup openclaw-soul"、"安装进化框架"、"部署灵魂系统"、"openclaw-soul"。
metadata:
  clawdbot:
    emoji: "🧬"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# openclaw-soul — Self-Evolution Framework

为 OpenClaw 安装完整的自我进化框架：宪法 + 可进化灵魂 + 结构化心跳协议 + PARA 三层记忆 + 目标管理 + 治理配置。

**安装内容**：
- 9 个工作区文件（AGENTS.md, SOUL.md, HEARTBEAT.md, BOOTSTRAP.md, USER.md, IDENTITY.md, GOALS.md, working-memory.md, long-term-memory.md）
- 2 个依赖 skill（evoclaw, self-improving）
- Heartbeat 定时任务配置
- EvoClaw 治理配置（advisory 模式 + soul-revisions 回滚）
- PARA 三层记忆目录结构
- 引导对话启动（BOOTSTRAP.md）

---

## §1 [GATE] 确认安装环境

**在执行任何操作之前，必须先完成此步骤。跳过此步骤是禁止的。**

询问用户：

> "准备部署 openclaw-soul 自我进化框架。请确认：
> 1. 工作区路径是什么？（默认：`~/.openclaw/workspace/`）
> 2. 如有自定义路径请告知。"

将用户确认的路径记为 `$WORKSPACE`。如果用户说"默认"或不指定，使用 `~/.openclaw/workspace/`。

---

## §2 [GATE] 环境检查

**必须先通过环境检查，否则禁止继续后续步骤。**

运行预检脚本：

```bash
python3 "$(dirname "$0")/../scripts/preflight_check.py"
```

如果脚本不可用，手动执行以下检查：

1. **工作区目录存在**：`$WORKSPACE` 路径必须存在且可写
2. **openclaw.json 可读**：检查 `$WORKSPACE/../openclaw.json` 是否存在且为有效 JSON
3. **clawhub CLI 可用**：`which clawhub` 或检查 `~/.openclaw/bin/clawhub`
4. **列出已有文件**：检查以下 9 个文件是否已存在于 `$WORKSPACE`：
   - AGENTS.md, SOUL.md, HEARTBEAT.md, BOOTSTRAP.md, GOALS.md
   - USER.md, IDENTITY.md, working-memory.md, long-term-memory.md

**输出格式**：逐项报告 pass/warn/fail，标记需要备份的文件。

**判断逻辑**：
- 任何 `fail` → 报告问题并**停止**，告知用户如何修复
- 只有 `warn` → 告知用户限制，确认是否继续
- 全部 `pass` → 继续下一步

---

## §3 [REQUIRED] 备份已有文件

对每个即将部署的文件，如果已存在于 `$WORKSPACE`：

```bash
cp "$WORKSPACE/{filename}" "$WORKSPACE/{filename}.backup.$(date +%Y%m%d-%H%M%S)"
```

列出所有被备份的文件告知用户。如果没有需要备份的文件，跳过此步骤并告知用户。

**保证非破坏性**：原文件在备份完成后才会被覆盖。

---

## §4 [REQUIRED] 模板部署

从 `references/` 目录读取模板，写入 `$WORKSPACE`：

| 模板文件 | 目标位置 |
|---------|---------|
| `references/agents-template.md` | `$WORKSPACE/AGENTS.md` |
| `references/soul-template.md` | `$WORKSPACE/SOUL.md` |
| `references/heartbeat-template.md` | `$WORKSPACE/HEARTBEAT.md` |
| `references/bootstrap-guide.md` | `$WORKSPACE/BOOTSTRAP.md` |
| `references/user-template.md` | `$WORKSPACE/USER.md` |
| `references/identity-template.md` | `$WORKSPACE/IDENTITY.md` |
| `references/goals-template.md` | `$WORKSPACE/GOALS.md` |
| `references/working-memory-template.md` | `$WORKSPACE/working-memory.md` |
| `references/long-term-memory-template.md` | `$WORKSPACE/long-term-memory.md` |

**部署步骤**：
1. 读取 `references/` 中的模板文件内容
2. 写入对应的 `$WORKSPACE` 目标路径
3. 创建目录结构（如不存在）：
   ```
   $WORKSPACE/
   ├── memory/
   │   ├── daily/              # Layer 2: daily notes
   │   ├── entities/           # Layer 1: knowledge graph
   │   ├── experiences/        # EvoClaw
   │   ├── significant/        # EvoClaw
   │   ├── reflections/        # EvoClaw
   │   ├── proposals/          # EvoClaw
   │   └── pipeline/           # EvoClaw
   └── soul-revisions/         # SOUL.md version snapshots
   ```
4. 每个文件写入后读回验证——确认文件非空且内容完整

如果任何文件写入失败，立即停止并报告错误。

---

## §5 [REQUIRED] 依赖 Skill 安装（三级 Fallback）

### 5a. 检查 clawhub 可用性

```bash
which clawhub || test -f ~/.openclaw/bin/clawhub
CLAWHUB_AVAILABLE=$?
```

记录 clawhub 是否可用。

### 5b. 安装 EvoClaw

检查 `$WORKSPACE/skills/evoclaw/SKILL.md` 是否存在：

**已安装** → 跳过，告知用户

**未安装** → 按优先级尝试：

1. **Level 1 - clawhub 安装**（如果可用）
   ```bash
   clawhub install evoclaw --force
   ```
   如果成功，告知用户已从 clawhub 安装。

2. **Level 2 - 离线 Fallback**（如果 Level 1 失败或 clawhub 不可用）
   - 检查本 skill 所在目录的 `fallback/evoclaw/SKILL.md` 是否存在
   - 如果存在：
     ```bash
     cp -r "$(dirname "$0")/../fallback/evoclaw" "$WORKSPACE/skills/"
     ```
   - 如果 fallback 文件也不存在，记录警告继续下一步

3. **Level 3 - AGENTS.md 内联版本**
   > "⚠️ EvoClaw 离线安装不可用。openclaw-soul 将使用 AGENTS.md 中的内联 Identity Evolution 机制。
   >
   > 功能对标：
   > - 核心 Identity 变更需要用户批准
   > - Working Style 和 User Understanding 可自主更新
   > - SOUL.md 变更前自动创建快照
   >
   > 如需完整 EvoClaw：稍后执行 `clawhub install evoclaw` 或从服务器复制 fallback 文件。"

### 5c. 安装 Self-Improving Agent

检查 `$WORKSPACE/skills/self-improving/SKILL.md` 是否存在：

**已安装** → 跳过，告知用户

**未安装** → 按优先级尝试：

1. **Level 1 - clawhub 安装**（如果可用）
   ```bash
   clawhub install self-improving --force
   ```
   如果成功，告知用户已从 clawhub 安装。

2. **Level 2 - 离线 Fallback**（如果 Level 1 失败或 clawhub 不可用）
   - 检查本 skill 所在目录的 `fallback/self-improving/SKILL.md` 是否存在
   - 如果存在：
     ```bash
     cp -r "$(dirname "$0")/../fallback/self-improving" "$WORKSPACE/skills/"
     ```
   - 如果 fallback 文件也不存在，记录警告继续下一步

3. **Level 3 - AGENTS.md 内联版本**
   > "⚠️ Self-Improving 离线安装不可用。openclaw-soul 将使用 AGENTS.md 中的内联 Self-Improving Protocol。
   >
   > 功能对标：
   > - 加载已学规则：从 ~/self-improving/memory.md 读取
   > - 用户纠正 → ~/self-improving/corrections.md
   > - 同一模式重复 3 次 → 升级为永久规则
   > - 30 天未使用 → 降级到 archive/
   >
   > 如需完整 Self-Improving Agent：稍后执行 `clawhub install self-improving` 或从服务器复制 fallback 文件。"

### 5d. 验证结果

安装完成后，逐项报告：

```
✓ EvoClaw: [installed from clawhub | installed from fallback | using inline version]
✓ Self-Improving: [installed from clawhub | installed from fallback | using inline version]
```

- 如果两个都"using inline version"，提示用户可随时升级到完整版本
- 如果有 fallback 或 Level 1 安装，验证对应的 SKILL.md 文件存在且非空

---

## §6 [REQUIRED] EvoClaw 治理配置

### 6a. 治理配置

写入 `$WORKSPACE/memory/evoclaw-state.json`：

```json
{
  "mode": "advisory",
  "require_approval": ["Core Identity", "Capability Tree", "Value Function"],
  "auto_sections": ["Working Style", "User Understanding", "Evolution Log"],
  "revision_dir": "soul-revisions",
  "initialized": true
}
```

### 6b. 验证

确认 evoclaw-state.json 存在且可解析为有效 JSON。

---

## §7 [REQUIRED] Self-Improving Agent 初始化

### 7a. 目录结构

确保以下目录存在：
```
~/self-improving/
├── projects/
├── domains/
└── archive/
```

### 7b. 初始化文件

如果以下文件不存在，创建初始版本：

**~/self-improving/memory.md**:
```markdown
# Self-Improving Memory

> Execution patterns and learned rules. Updated after corrections and lessons.

(empty — will accumulate through use)
```

**~/self-improving/corrections.md**:
```markdown
# Corrections Log

> Failed attempts and their fixes. Each entry prevents the same mistake twice.

(empty — will accumulate through use)
```

**~/self-improving/index.md**:
```markdown
# Self-Improving Index

> Quick reference to all domains, projects, and archived knowledge.

## Domains
(none yet)

## Projects
(none yet)

## Archive
(none yet)
```

如果文件已存在，**不要覆盖**——它们可能包含已积累的学习内容。

---

## §8 [REQUIRED] Heartbeat 配置

使用 `openclaw config set` 更新 heartbeat 设置：

```bash
openclaw config set agents.defaults.heartbeat.every "1h"
openclaw config set agents.defaults.heartbeat.target "last"
openclaw config set agents.defaults.heartbeat.directPolicy "allow"
```

如果 `openclaw config set` 命令不可用，直接编辑 `openclaw.json`：

1. 读取当前 openclaw.json
2. 确保 `agents.defaults.heartbeat` 对象存在
3. 设置：
   - `every`: `"1h"`
   - `target`: `"last"`
   - `directPolicy`: `"allow"`
4. 写回文件

---

## §9 [REQUIRED] 验证清单

逐项检查并报告 pass/fail：

| # | 检查项 | 验证方法 |
|---|--------|---------|
| 1 | AGENTS.md 存在且非空 | `test -s $WORKSPACE/AGENTS.md` |
| 2 | SOUL.md 存在且非空 | `test -s $WORKSPACE/SOUL.md` |
| 3 | HEARTBEAT.md 存在且非空 | `test -s $WORKSPACE/HEARTBEAT.md` |
| 4 | BOOTSTRAP.md 存在且非空 | `test -s $WORKSPACE/BOOTSTRAP.md` |
| 5 | GOALS.md 存在且非空 | `test -s $WORKSPACE/GOALS.md` |
| 6 | USER.md 存在且非空 | `test -s $WORKSPACE/USER.md` |
| 7 | IDENTITY.md 存在且非空 | `test -s $WORKSPACE/IDENTITY.md` |
| 8 | working-memory.md 存在且非空 | `test -s $WORKSPACE/working-memory.md` |
| 9 | long-term-memory.md 存在且非空 | `test -s $WORKSPACE/long-term-memory.md` |
| 10 | EvoClaw skill 已安装 | `test -f $WORKSPACE/skills/evoclaw/SKILL.md` |
| 11 | evoclaw-state.json 配置正确 | 读取并验证 mode=advisory |
| 12 | Self-Improving skill 已安装 | `test -f $WORKSPACE/skills/self-improving/SKILL.md` |
| 13 | ~/self-improving/ 目录就绪 | 检查 memory.md, corrections.md, index.md |
| 14 | Heartbeat 配置已写入 | 读取 openclaw.json 确认 heartbeat 字段 |
| 15 | memory/entities/ 目录存在 | `test -d $WORKSPACE/memory/entities` |
| 16 | memory/daily/ 目录存在 | `test -d $WORKSPACE/memory/daily` |
| 17 | soul-revisions/ 目录存在 | `test -d $WORKSPACE/soul-revisions` |

**输出格式**：

```
✓ AGENTS.md — pass
✓ SOUL.md — pass
✓ GOALS.md — pass
...
✗ EvoClaw — fail (SKILL.md not found)
```

**判断**：
- 全部 pass → 继续 §10
- 任何 fail → 列出失败项，提示用户手动修复

---

## §10 [FINAL] 触发引导对话

**只有 §9 全部通过后才执行此步骤。**

1. 读取 `$WORKSPACE/BOOTSTRAP.md`
2. 告知用户：

> "🧬 openclaw-soul 部署完成！
>
> 已安装：
> - 宪法（AGENTS.md）— 含 Conductor 协议和委派规范
> - 可进化灵魂（SOUL.md）— 带版本快照回滚
> - 结构化心跳协议（HEARTBEAT.md）— 唤醒上下文 + 阻塞去重 + 预算感知
> - PARA 三层记忆（entities 知识图谱 + daily 日记 + 隐性知识）
> - 目标管理（GOALS.md）— 任务追溯到目标
> - EvoClaw 治理（advisory 模式）
> - Self-Improving Agent
>
> 现在开始你的第一次深度对话——我要认识你，然后定义我自己的性格。"

3. **立即开始执行 BOOTSTRAP.md 的 Phase 1**——从这里开始就是 BOOTSTRAP 的流程接管
4. 此 skill 的使命到此结束。后续由 BOOTSTRAP.md + AGENTS.md + SOUL.md 接管运行

---

_openclaw-soul v1.2.0 — Zero-dependency deployment with three-level fallback. Give your AI a soul that grows._
