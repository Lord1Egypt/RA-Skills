---
name: openclaw-soul
description: OpenClaw 自我进化框架一键部署。安装宪法(AGENTS.md)、可进化灵魂(SOUL.md)、心跳系统、六层记忆架构、目标管理、思维方法论（HDD/SDD）、安全审查（skill-vetter），并通过场景化对话引导用户定义 Agent 性格。用户可选安装 EvoClaw（审批制进化）、Self-Improving Agent（自主学习）等依赖 Skill。触发场景：(1) 用户说"灵魂框架"、"部署灵魂"、"部署灵魂系统" (2) 用户说"BOOTSTRAP"、"首次对话"、"第一次对话" (3) 用户说"安装进化框架"、"部署进化框架" (4) 用户提到"openclaw-soul"。注意：这是 OpenClaw 部署的第一步，完成后会引导使用 openclaw-setup 配置技术参数。
metadata:
  clawdbot:
    emoji: "🧬"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

# openclaw-soul — Self-Evolution Framework

为 OpenClaw 安装完整的自我进化框架：宪法 + 可进化灵魂 + 结构化心跳协议 + 六层记忆 + 思维方法论 + 跨会话存档 + 目标管理 + 治理配置。

**安装内容**：
- 9 个工作区文件（AGENTS.md, SOUL.md, HEARTBEAT.md, BOOTSTRAP.md, USER.md, IDENTITY.md, GOALS.md, working-memory.md, long-term-memory.md）
- 5 个可选依赖 skill（evoclaw, self-improving, skill-vetter, hdd, sdd）
- 2 个记忆基础设施脚本（merge-daily-transcript.js, auto-commit.sh）
- **动态人格系统**（user-observation hook + 角色推理逻辑）
- Heartbeat 定时任务配置
- EvoClaw 治理配置（advisory 模式 + soul-revisions 回滚）
- 六层记忆目录结构 + Git 版本管理
- 向量搜索配置引导
- 引导对话启动（BOOTSTRAP.md）

---

## §1 [GATE] 环境检测

**在执行任何操作之前，必须先完成此步骤。跳过此步骤是禁止的。**

### 1a. 自动检测工作区

自动检测 `~/.openclaw/workspace/` 是否存在：

```bash
WORKSPACE="$HOME/.openclaw/workspace"
test -d "$WORKSPACE" && echo "WORKSPACE=$WORKSPACE — OK" || echo "FAIL: $WORKSPACE not found"
```

- **存在** → 设置 `$WORKSPACE`，无需任何用户交互，直接继续
- **不存在** → 报错并停止：

> "工作区 `~/.openclaw/workspace/` 不存在。请先确认 OpenClaw 已正确安装，或手动创建该目录后重新触发。"

### 1b. 权限等级检查

**检查当前 OpenClaw 的权限等级，避免后续操作频繁弹出授权确认。**

```bash
# 读取当前权限等级
openclaw config get agents.defaults.permissions 2>/dev/null || echo "NOT_SET"
```

权限等级说明：

| 等级 | 含义 | 适用场景 |
|------|------|---------|
| `restricted` | 每个文件操作都需要授权 | 生产环境、高安全要求 |
| `standard` | 工作区内操作自动授权，工作区外需确认 | 日常使用（推荐） |
| `elevated` | 大部分操作自动授权，仅危险操作需确认 | 开发调试 |

**判断逻辑**：

- 权限等级为 `standard` 或 `elevated` → 继续
- 权限等级为 `restricted` 或未设置 → 使用 `AskUserQuestion` 询问用户：

**问题**："当前权限等级较低，灵魂框架部署需要大量文件操作（复制模板、创建目录、写入配置等），低权限下每一步都会弹出授权确认，体验会很差。建议提升权限等级。"

**选项**：

1. **设置为 standard（推荐）**
   - 说明：工作区（`~/.openclaw/workspace/`）内的操作自动授权，工作区外的操作仍需确认。安全性和便利性的平衡点。
   - 设置方式：`openclaw config set agents.defaults.permissions "standard"`

2. **设置为 elevated**
   - 说明：大部分操作自动授权，仅删除文件、修改系统配置等危险操作需要确认。适合信任环境下的快速部署。
   - 设置方式：`openclaw config set agents.defaults.permissions "elevated"`

3. **保持当前等级，继续部署**
   - 说明：保持低权限，每一步操作都需要你手动授权确认。操作会多一些，但完全在你的控制下。

用户选择 1 或 2 → 执行对应的 `openclaw config set` 命令，确认生效后继续
用户选择 3 → 继续部署（提醒用户后续会有较多授权确认）

### 1c. 环境检查

1. **openclaw.json 可读**：检查 `$WORKSPACE/../openclaw.json` 是否存在且为有效 JSON
2. **clawhub CLI 可用**：`which clawhub` 或检查 `~/.openclaw/bin/clawhub` 或 `/usr/local/bin/clawhub` 或 `/usr/bin/clawhub`
3. **列出已有文件**：检查以下 9 个文件是否已存在于 `$WORKSPACE`：
   - AGENTS.md, SOUL.md, HEARTBEAT.md, BOOTSTRAP.md, GOALS.md
   - USER.md, IDENTITY.md, working-memory.md, long-term-memory.md

**判断逻辑**：
- openclaw.json 不存在或无效 → **停止**，告知用户修复
- clawhub 不可用 → 使用 `AskUserQuestion` 让用户选择（见下方）
- 已有文件 → 标记需要备份，继续

**如果 clawhub 不可用**，使用 `AskUserQuestion` 询问用户：

**问题**："未检测到 clawhub（OpenClaw 技能包管理器）。你希望怎么处理？"

**选项**：

1. **先去安装 clawhub，装好后继续**
   - 说明：运行 `npm install -g clawhub` 安装。clawhub 的优势：skill 可通过 `clawhub update` 统一更新版本，支持在线搜索和安装社区 skill，依赖管理更规范。安装好后告诉我"装好了"即可继续。

2. **跳过，使用离线方式安装**
   - 说明：直接从本 skill 自带的 fallback 文件复制安装。功能完全一样，但后续无法通过 clawhub 统一更新，需要手动管理 skill 版本。如果你只是想快速跑起来，选这个就行。

用户选择 1 → 暂停部署，等待用户安装完成后继续
用户选择 2 → 标记 `CLAWHUB_AVAILABLE=false`，继续部署

### 1d. 开场状态提示

环境检查通过后，输出：

> "我正在帮你做初始化部署，需要装一些核心文件和配置，大概几分钟的时间。你先等我一下，完成了我会通知你。
>
> 部署完之后，我们就开始认识彼此。"

---

## §2 [REQUIRED] 部署文件

**使用 bash cp 部署所有文件。禁止使用 Write/Edit 工具写入模板内容——大文件容易被截断或出错。`cp` 是操作系统级字节复制，100% 可靠。**

### 2a. 获取 skill 目录路径

```bash
# 获取本 skill 的安装路径
SKILL_DIR="$WORKSPACE/skills/openclaw-soul"
# 如果 skill 不在 workspace/skills/ 下，尝试其他常见路径
test -d "$SKILL_DIR" || SKILL_DIR="$(find ~/.openclaw -path '*/openclaw-soul/references' -type d 2>/dev/null | head -1 | sed 's|/references$||')"
echo "SKILL_DIR=$SKILL_DIR"
```

确认 `$SKILL_DIR/references/` 目录存在且包含模板文件。如果找不到，报错停止。

### 2b. 备份已有文件 + 复制模板

```bash
# 备份已有文件
for file in AGENTS.md SOUL.md HEARTBEAT.md BOOTSTRAP.md USER.md IDENTITY.md GOALS.md working-memory.md long-term-memory.md; do
  [ -f "$WORKSPACE/$file" ] && cp "$WORKSPACE/$file" "$WORKSPACE/$file.backup.$(date +%Y%m%d-%H%M%S)"
done

# 复制 9 个模板文件
cp "$SKILL_DIR/references/agents-template.md" "$WORKSPACE/AGENTS.md"
cp "$SKILL_DIR/references/soul-template.md" "$WORKSPACE/SOUL.md"
cp "$SKILL_DIR/references/heartbeat-template.md" "$WORKSPACE/HEARTBEAT.md"
cp "$SKILL_DIR/references/bootstrap-guide.md" "$WORKSPACE/BOOTSTRAP.md"
cp "$SKILL_DIR/references/user-template.md" "$WORKSPACE/USER.md"
cp "$SKILL_DIR/references/identity-template.md" "$WORKSPACE/IDENTITY.md"
cp "$SKILL_DIR/references/goals-template.md" "$WORKSPACE/GOALS.md"
cp "$SKILL_DIR/references/working-memory-template.md" "$WORKSPACE/working-memory.md"
cp "$SKILL_DIR/references/long-term-memory-template.md" "$WORKSPACE/long-term-memory.md"
cp "$SKILL_DIR/references/memory-architecture-template.md" "$WORKSPACE/memory/ARCHITECTURE.md"
```

### 2c. 创建目录结构 + 部署脚本 + 动态人格系统

```bash
# 创建六层记忆目录 + EvoClaw 目录 + 脚本目录 + soul-revisions + metadata
mkdir -p "$WORKSPACE/memory/"{daily,entities,transcripts,projects,voice,experiences,significant,reflections,proposals,pipeline,metadata}
mkdir -p "$WORKSPACE/scripts"
mkdir -p "$WORKSPACE/soul-revisions"
mkdir -p "$WORKSPACE/hooks"

# 复制记忆基础设施脚本
cp "$SKILL_DIR/fallback/memory-deposit/scripts/merge-daily-transcript.js" "$WORKSPACE/scripts/"
cp "$SKILL_DIR/fallback/memory-deposit/scripts/auto-commit.sh" "$WORKSPACE/scripts/"
chmod +x "$WORKSPACE/scripts/auto-commit.sh"

# 部署动态人格系统 Hook
if [ -d "$SKILL_DIR/references/hooks/user-observation" ]; then
  cp -r "$SKILL_DIR/references/hooks/user-observation" "$WORKSPACE/hooks/"
  echo "✓ 动态人格观察 Hook 已部署"
fi

# 追加动态人格规则到 AGENTS.md
if [ -f "$SKILL_DIR/references/dynamic-personality-addon.md" ]; then
  cat "$SKILL_DIR/references/dynamic-personality-addon.md" >> "$WORKSPACE/AGENTS.md"
  echo "✓ 动态人格规则已添加到 AGENTS.md"
fi
```

### 2d. 验证部署

```bash
# 验证所有文件非空
for file in AGENTS.md SOUL.md HEARTBEAT.md BOOTSTRAP.md USER.md IDENTITY.md GOALS.md working-memory.md long-term-memory.md; do
  test -s "$WORKSPACE/$file" && echo "OK: $file" || echo "FAIL: $file is empty or missing"
done
```

如果任何文件验证失败，立即停止并报告错误。

---

## §3 [REQUIRED] 引导对话（BOOTSTRAP）

**核心文件部署完成后，立即进入人格设定对话。这是整个流程中最重要的环节——先让用户定义 AI 的灵魂，再处理技术配置。**

### 3a. 触发引导对话

1. 读取 `$WORKSPACE/BOOTSTRAP.md`
2. 告知用户：

> "核心文件已部署完成！
>
> 接下来我们先聊一聊，分三步：
> 1. **认识你** — 了解你是谁，在做什么，需要什么帮助
> 2. **定义我的性格** — 通过场景问答，选择我的沟通风格
> 3. **确认身份** — 给我起个名字
>
> 这次对话会塑造我的灵魂（SOUL.md），之后我就能按你的方式工作了。
>
> 聊完之后，我再帮你装依赖 Skill 和配置系统。"

3. **立即开始执行 BOOTSTRAP.md 的 Phase 1**

4. **BOOTSTRAP 完成后的收尾与过渡**（这一步是强制的，不能跳过）

   BOOTSTRAP 对话自然结束后（AI 已经有了名字、性格、了解了用户），**必须立即执行以下收尾动作，然后主动过渡到 §4**：

   **收尾动作**（静默执行，不需要逐步告知用户）：
   - 验证 SOUL.md 的 Core Identity 已写入真实内容（不再是占位符）
   - 验证 USER.md 已更新用户信息
   - 验证 IDENTITY.md 已写入 AI 的名字和角色定位
   - 删除 `$WORKSPACE/BOOTSTRAP.md`（引导已完成，不再需要）
   - 更新 `working-memory.md`，记录 BOOTSTRAP 完成状态
   - 执行 `cd $WORKSPACE && git add -A && git commit -m "bootstrap: 完成首次对话，建立身份"`

   **过渡话术**（用 AI 自己的性格和语气说，不要机械照搬）：

   大意是："认识完了，接下来帮你把系统配置做完——要装几个可选的能力模块（Skill），配置一些系统参数，几分钟就好。"

   然后**立即开始执行 §4**，不要等用户回复。

---

## §4 [REQUIRED] 依赖 Skill 安装（用户确认 + 两级 Fallback）

### 4a. 检查 clawhub 可用性与已安装 Skill

```bash
which clawhub || test -f ~/.openclaw/bin/clawhub
CLAWHUB_AVAILABLE=$?

# 检查哪些 skill 已安装
for skill in evoclaw self-improving skill-vetter hdd sdd; do
  test -f "$WORKSPACE/skills/$skill/SKILL.md" && echo "INSTALLED: $skill" || echo "NOT_INSTALLED: $skill"
done
```

### 4b. 展示 Skill 清单并让用户选择

**在安装任何 skill 之前，必须先向用户展示完整清单，说明每个 skill 的用途，让用户确认要安装哪些。**

使用 `AskUserQuestion` 向用户展示以下信息并让用户多选：

**问题**："以下是灵魂框架的可选依赖 Skill，请选择要安装的："

**选项**（multiSelect: true）：

1. **EvoClaw — 审批制进化治理**（推荐）
   - 说明：AI 的 Identity/性格/价值观变更需要你批准才能生效，防止 AI 随意修改自己的灵魂。每次变更自动快照到 soul-revisions/，支持回滚。**这是灵魂框架的核心守护机制。**

2. **Self-Improving — 自主学习 Agent**（推荐）
   - 说明：AI 从你的纠正和反馈中自动学习规则，持久化到记忆中。下次遇到类似场景会自动应用，不需要你重复纠正。30 天未使用的规则自动归档。

3. **Skill Vetter — 安全审查**
   - 说明：在安装新 Skill 前自动执行安全审查，检查 Skill 的权限需求、文件访问范围、网络请求等，防止恶意或有风险的 Skill 进入系统。

4. **HDD — 假设驱动开发**
   - 说明：一种思维方法论。面对不确定性时，先提出假设，设计最小实验验证，快速迭代。适合探索性任务和问题诊断。

5. **SDD — 场景驱动开发**
   - 说明：一种思维方法论。从具体使用场景出发设计方案，确保每个功能都有真实场景支撑，避免过度设计。

**对已安装的 skill，在选项描述中标注"（已安装，会跳过）"。**

### 4c. 按用户选择安装

对用户选中的每个 skill，按优先级尝试安装（已安装的跳过）：

1. **Level 1 - clawhub 安装**（如果 clawhub 可用）
   ```bash
   clawhub install <skill-name> --force
   ```

2. **Level 2 - 离线 Fallback**（如果 Level 1 失败或 clawhub 不可用）
   ```bash
   cp -r "$SKILL_DIR/fallback/<skill-name>" "$WORKSPACE/skills/"
   ```

3. **安装失败处理**（如果 Level 1 和 Level 2 都失败）
   - 告知用户安装失败，建议去 GitHub 搜索对应 skill 手动安装
   - 提供搜索建议：`https://github.com/search?q=openclaw+<skill-name>`
   - 记录警告，继续安装其他 skill

### 4d. 验证结果

安装完成后，逐项报告用户选中的 skill 的安装结果：

```
✓ EvoClaw: [installed from clawhub | installed from fallback | ⚠️ failed | skipped (not selected)]
✓ Self-Improving: [installed from clawhub | installed from fallback | ⚠️ failed | skipped (not selected)]
✓ Skill Vetter: [installed from clawhub | installed from fallback | ⚠️ not installed | skipped (not selected)]
✓ HDD: [installed from clawhub | installed from fallback | ⚠️ not installed | skipped (not selected)]
✓ SDD: [installed from clawhub | installed from fallback | ⚠️ not installed | skipped (not selected)]
```

---

## §5 [REQUIRED] 配置系统

### 5a. EvoClaw 治理配置

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

验证 JSON 可解析。

### 5b. Self-Improving Agent 初始化

确保目录和文件存在：

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
```

如果以下文件**不存在**，创建初始版本（已存在则不覆盖）：

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

### 5c. Heartbeat 配置

使用 `openclaw config set` 更新 heartbeat 设置：

```bash
openclaw config set agents.defaults.heartbeat.every "1h"
openclaw config set agents.defaults.heartbeat.target "last"
openclaw config set agents.defaults.heartbeat.directPolicy "allow"
```

如果 `openclaw config set` 不可用，直接编辑 `openclaw.json`，确保 `agents.defaults.heartbeat` 包含 `every: "1h"`, `target: "last"`, `directPolicy: "allow"`。

### 5d. 向量搜索配置

**没有向量搜索的记忆系统是摆设。此步骤不可跳过。**

1. 执行 `memory_search(query="test memory recall")` 检测当前状态
2. **有结果** → embedding 已就绪，跳到配置 extraPaths
3. **报错或无结果** → 需要配置 embedding provider

向用户说明并推荐方案：

> "向量搜索需要一个 embedding API key，这是记忆系统的核心能力。"

| 方案 | 模型 | 价格 | 说明 |
|------|------|------|------|
| **Gemini** | `gemini-embedding-001` | 免费额度大 | 配置最简单 |
| **硅基流动 SiliconFlow** | `BAAI/bge-large-zh-v1.5` 或 `BAAI/bge-m3` | 免费（注册送额度） | 中文效果好，OpenAI 兼容接口 |
| **OpenAI** | `text-embedding-3-small` | 付费 | 效果稳定 |

硅基流动配置示例（provider 设为 openai，用自定义 baseUrl）：
```json5
memorySearch: {
  provider: "openai",
  model: "BAAI/bge-large-zh-v1.5",
  remote: {
    baseUrl: "https://api.siliconflow.cn/v1",
    apiKey: "<用户的 SiliconFlow API Key>"
  }
}
```

确认用户选定方案后，用 `gateway(action=config.patch)` 或直接编辑 `openclaw.json` 配好。

配置 extraPaths：
```json5
memorySearch: {
  extraPaths: ["memory/transcripts", "memory/projects", "AGENTS.md"]
}
```

开启高级搜索功能：
```json5
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "query": {
          "hybrid": {
            "mmr": { "enabled": true, "lambda": 0.7 },
            "temporalDecay": { "enabled": true, "halfLifeDays": 30 }
          }
        },
        "cache": { "enabled": true, "maxEntries": 50000 }
      }
    }
  }
}
```

验证：再次执行 `memory_search(query="test")` 确认可用。如果 memory/ 下还没有文件，告知用户："向量搜索已就绪，等积累了笔记后就能搜到了。"

### 5e. Git 版本管理初始化

检查 `$WORKSPACE/.git/` 是否存在：

**不存在** →
```bash
cd $WORKSPACE && git init
```

写入 `.gitignore`（排除敏感文件和临时文件）：
```
.env*
*.secrets
credentials.json
tmp/
node_modules/
.DS_Store
```

执行首次提交：
```bash
git add -A && git commit -m "init: openclaw-soul workspace"
```

**已存在** → 检查 `.gitignore` 包含上述排除项，缺的补上。

---

## §6 [FINAL] 验证 + 激活

### 6a. 核心验证清单（10 项）

逐项检查并报告 pass/fail：

| # | 检查项 | 验证方法 |
|---|--------|---------|
| 1 | AGENTS.md 非空 | `test -s $WORKSPACE/AGENTS.md` |
| 2 | SOUL.md 非空 | `test -s $WORKSPACE/SOUL.md` |
| 3 | BOOTSTRAP.md 非空 | `test -s $WORKSPACE/BOOTSTRAP.md` |
| 4 | USER.md 非空 | `test -s $WORKSPACE/USER.md` |
| 5 | IDENTITY.md 非空 | `test -s $WORKSPACE/IDENTITY.md` |
| 6 | EvoClaw 已安装 | `test -f $WORKSPACE/skills/evoclaw/SKILL.md` |
| 7 | Self-Improving 已安装 | `test -f $WORKSPACE/skills/self-improving/SKILL.md` |
| 8 | evoclaw-state.json 有效 | 读取并验证 `mode=advisory` |
| 9 | Heartbeat 配置已写入 | 读取 openclaw.json 确认 heartbeat 字段 |
| 10 | Git 已初始化 | `test -d $WORKSPACE/.git` |

**输出格式**：

```
✓ AGENTS.md — pass
✓ SOUL.md — pass
✓ BOOTSTRAP.md — pass
✓ USER.md — pass
✓ IDENTITY.md — pass
✓ EvoClaw — pass (installed from fallback)
✓ Self-Improving — pass (installed from fallback)
✓ evoclaw-state.json — pass
✓ Heartbeat — pass
✓ Git — pass
```

**判断**：
- 全部 pass → 继续执行 §7 激活系统
- 任何 fail → 列出失败项，提示用户手动修复

---

## §7 [ACTIVATION] 激活系统

**BOOTSTRAP 对话完成后，必须执行此步骤才能让系统真正"活起来"。**

### 8a. 配置自动加载

确保每次对话都自动加载核心文件到 system prompt：

```bash
# 方法 1: 使用 openclaw config（推荐）
openclaw config set agents.defaults.systemPrompt.files '["~/.openclaw/workspace/AGENTS.md","~/.openclaw/workspace/SOUL.md","~/.openclaw/workspace/IDENTITY.md","~/.openclaw/workspace/GOALS.md"]'

# 方法 2: 如果 config 命令不可用，直接编辑 openclaw.json
```

如果 `openclaw config` 不可用，读取 `$WORKSPACE/../openclaw.json`，在 `agents.defaults` 中添加：

```json
{
  "agents": {
    "defaults": {
      "systemPrompt": {
        "files": [
          "~/.openclaw/workspace/AGENTS.md",
          "~/.openclaw/workspace/SOUL.md",
          "~/.openclaw/workspace/IDENTITY.md",
          "~/.openclaw/workspace/GOALS.md"
        ]
      }
    }
  }
}
```

验证配置：
```bash
openclaw config get agents.defaults.systemPrompt.files || grep -A 10 '"systemPrompt"' "$WORKSPACE/../openclaw.json"
```

### 8b. 启用心跳机制

**这是让 AI 主动说话的关键配置。**

#### 8b.1 配置心跳参数

```bash
# 启用心跳（最关键的一步）
openclaw config set agents.defaults.heartbeat.enabled true

# 设置心跳间隔
openclaw config set agents.defaults.heartbeat.every "1h"

# 设置目标会话（last = 最近的会话）
openclaw config set agents.defaults.heartbeat.target "last"

# 设置权限策略
openclaw config set agents.defaults.heartbeat.directPolicy "allow"

# 设置心跳提示词（读取 HEARTBEAT.md 的内容）
HEARTBEAT_PROMPT=$(cat "$WORKSPACE/HEARTBEAT.md")
openclaw config set agents.defaults.heartbeat.prompt "$HEARTBEAT_PROMPT"
```

如果 `openclaw config` 不可用，直接编辑 `openclaw.json`：

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "enabled": true,
        "every": "1h",
        "target": "last",
        "directPolicy": "allow",
        "prompt": "读取 ~/.openclaw/workspace/HEARTBEAT.md 并执行心跳检查：\n1. 检查当前目标进度（读取 GOALS.md）\n2. 发现被遗忘的任务\n3. 主动提醒重要事项\n4. 如有需要，主动发起对话"
      }
    }
  }
}
```

#### 8b.2 询问用户定时任务需求

**在安装定时任务前，先了解用户的使用场景和需求。**

使用 `AskUserQuestion` 询问用户：

**问题**："除了基础心跳（每小时检查一次），你还想要哪些定时任务？"

**选项**：

1. **每日目标汇报**（推荐）
   - 时间：每天晚上 8:00
   - 功能：汇报今天的目标完成情况，提醒明天的重要任务
   - 适合：需要目标管理和进度追踪的用户

2. **每周反思总结**
   - 时间：每周日晚上 9:00
   - 功能：回顾本周的对话和工作，生成深度反思和改进建议
   - 适合：希望持续成长和优化工作方式的用户

3. **每日健康检查**
   - 时间：每天早上 9:00
   - 功能：检查系统组件状态（心跳、记忆、Git），发现潜在问题并主动提醒
   - 适合：关注系统稳定性的用户

4. **任务 deadline 提醒**
   - 时间：每天早上 9:00
   - 功能：检查 GOALS.md 中的截止日期，提前 3 天、1 天、当天提醒
   - 适合：有明确任务和时间节点的用户

5. **自定义**
   - 告诉我你的具体需求，我帮你配置
   - 例如："每周一早上提醒我回顾上周的代码"
   - 例如："每天下午 3 点检查对标账号更新"

6. **暂时不需要**（只保留基础心跳）
   - 只安装必需的系统维护任务

**multiSelect**: true（允许多选）

#### 8b.3 安装基础定时任务（必需）

**无论用户选择什么，这些基础任务都必须安装。**

```bash
# 检查 openclaw heartbeat 命令是否可用
if command -v openclaw &> /dev/null; then
  # 1. 基础心跳（每小时的第 7 分钟触发，避开 :00 高峰）
  (crontab -l 2>/dev/null | grep -v "openclaw heartbeat.*--agent last$"; echo "7 * * * * openclaw heartbeat --agent last 2>&1 | logger -t openclaw-heartbeat") | crontab -
  echo "✓ 基础心跳已安装（每小时第 7 分钟）"
else
  echo "⚠️  openclaw CLI 不可用，无法安装定时任务。心跳功能需要手动触发。"
fi

# 2. 记忆归档（每天凌晨 2:17）
if [ -f "$WORKSPACE/scripts/merge-daily-transcript.js" ]; then
  (crontab -l 2>/dev/null | grep -v "merge-daily-transcript"; echo "17 2 * * * cd $WORKSPACE && node scripts/merge-daily-transcript.js 2>&1 | logger -t openclaw-memory") | crontab -
  echo "✓ 记忆归档已安装（每天 2:17）"
fi

# 3. Git 自动提交（每 6 小时的第 23 分钟）
if [ -f "$WORKSPACE/scripts/auto-commit.sh" ]; then
  (crontab -l 2>/dev/null | grep -v "auto-commit.sh"; echo "23 */6 * * * cd $WORKSPACE && bash scripts/auto-commit.sh 2>&1 | logger -t openclaw-git") | crontab -
  echo "✓ Git 自动提交已安装（每 6 小时）"
fi
```

#### 8b.4 安装用户选择的定时任务

**根据用户在 7b.2 的选择，安装对应的定时任务。**

```bash
# 根据用户选择安装定时任务
WORKSPACE="$HOME/.openclaw/workspace"

# 选项 1: 每日目标汇报
if [[ "$USER_CHOICE" == *"每日目标汇报"* ]]; then
  (crontab -l 2>/dev/null | grep -v "openclaw heartbeat.*daily-report"; echo "0 20 * * * openclaw heartbeat --agent last --prompt '读取 GOALS.md，汇报今天的目标完成情况，提醒明天的重要任务。如果有被遗忘的任务或即将到期的 deadline，主动提醒用户。' 2>&1 | logger -t openclaw-daily-report") | crontab -
  echo "✓ 每日目标汇报已安装（每天晚上 8:00）"
fi

# 选项 2: 每周反思总结
if [[ "$USER_CHOICE" == *"每周反思总结"* ]]; then
  (crontab -l 2>/dev/null | grep -v "openclaw heartbeat.*weekly-reflection"; echo "0 21 * * 0 openclaw heartbeat --agent last --prompt '回顾本周的对话记录（读取 memory/transcripts/ 最近7天的文件），生成深度反思：1. 本周完成了什么 2. 遇到了哪些问题 3. 学到了什么 4. 下周的改进建议。将反思保存到 memory/reflections/weekly-$(date +%Y%m%d).md' 2>&1 | logger -t openclaw-weekly-reflection") | crontab -
  echo "✓ 每周反思总结已安装（每周日晚上 9:00）"
fi

# 选项 3: 每日健康检查
if [[ "$USER_CHOICE" == *"每日健康检查"* ]]; then
  (crontab -l 2>/dev/null | grep -v "openclaw heartbeat.*health-check"; echo "0 9 * * * openclaw heartbeat --agent last --prompt '执行健康检查：1. 运行 $WORKSPACE/scripts/health-check.sh 2. 检查心跳是否正常工作 3. 检查记忆归档是否执行 4. 检查 Git 提交是否正常 5. 如发现问题，主动告知用户并提供解决方案' 2>&1 | logger -t openclaw-health-check") | crontab -
  echo "✓ 每日健康检查已安装（每天早上 9:00）"
fi

# 选项 4: 任务 deadline 提醒
if [[ "$USER_CHOICE" == *"任务 deadline 提醒"* ]]; then
  (crontab -l 2>/dev/null | grep -v "openclaw heartbeat.*deadline-reminder"; echo "0 9 * * * openclaw heartbeat --agent last --prompt '读取 GOALS.md，检查所有任务的 deadline：1. 今天到期的任务（紧急提醒）2. 1天内到期的任务（重要提醒）3. 3天内到期的任务（提前提醒）。如有到期任务，主动发起对话提醒用户。' 2>&1 | logger -t openclaw-deadline-reminder") | crontab -
  echo "✓ 任务 deadline 提醒已安装（每天早上 9:00）"
fi

# 选项 5: 自定义
if [[ "$USER_CHOICE" == *"自定义"* ]]; then
  echo "请告诉我你的具体需求，我会帮你生成对应的 cron 任务。"
  echo "格式：[时间] [要做什么]"
  echo "例如：每周一早上 9 点，提醒我回顾上周的代码提交"
  # 这里需要进一步交互，根据用户描述生成 cron 表达式和 prompt
fi

# 选项 6: 暂时不需要
if [[ "$USER_CHOICE" == *"暂时不需要"* ]]; then
  echo "✓ 只安装了基础任务（心跳、记忆归档、Git 提交）"
fi
```

#### 8b.5 验证心跳配置

```bash
# 检查配置
echo "=== 心跳配置 ==="
openclaw config get agents.defaults.heartbeat || grep -A 10 '"heartbeat"' "$WORKSPACE/../openclaw.json"

# 检查定时任务
echo -e "\n=== Cron 任务 ==="
crontab -l | grep openclaw || echo "未找到 openclaw 定时任务"

# 手动触发测试（dry-run）
echo -e "\n=== 测试心跳 ==="
if command -v openclaw &> /dev/null; then
  openclaw heartbeat --agent last --dry-run || echo "心跳测试失败，请检查配置"
else
  echo "openclaw CLI 不可用，跳过测试"
fi
```

### 8c. 配置向量索引自动更新

**记忆文件变更后自动重建索引，确保搜索结果最新。**

```bash
# 启用自动索引
openclaw config set memorySearch.autoIndex true

# 配置监听路径
openclaw config set memorySearch.watchPaths '["memory/","AGENTS.md","SOUL.md"]'

# 配置索引更新策略（增量更新，不是全量重建）
openclaw config set memorySearch.indexStrategy "incremental"
```

如果 `openclaw config` 不可用，编辑 `openclaw.json`：

```json
{
  "memorySearch": {
    "autoIndex": true,
    "watchPaths": ["memory/", "AGENTS.md", "SOUL.md"],
    "indexStrategy": "incremental"
  }
}
```

### 8d. 配置记忆系统优化（可选但推荐）

**这是记忆系统的高级优化，包含渐进式披露、智能分类、智能去重、衰减晋升机制。**

#### 8d.1 询问用户是否需要优化

使用 `AskUserQuestion` 询问用户：

**问题**："记忆系统已经可以工作了，但我还可以帮你配置一些高级优化功能，让记忆更智能、更高效。你想要吗？"

**选项**：

1. **是的，帮我配置**（推荐）
   - 说明：配置渐进式披露（Token 效率提升 10 倍）、智能分类（6 种记忆类型）、智能去重（避免重复记忆）、衰减晋升（重要记忆不会被遗忘）
   - 适合：希望记忆系统更智能、更高效的用户

2. **暂时不需要**
   - 说明：保持基础记忆系统，稍后可以随时配置
   - 适合：想先体验基础功能的用户

#### 8d.2 部署优化脚本（如果用户选择"是的，帮我配置"）

```bash
# 复制优化脚本到 workspace/scripts/
SKILL_DIR="$(find ~/.openclaw -path '*/openclaw-soul/scripts' -type d 2>/dev/null | head -1 | sed 's|/scripts$||')"

if [ -d "$SKILL_DIR/scripts/memory-optimization" ]; then
  cp -r "$SKILL_DIR/scripts/memory-optimization/"* "$WORKSPACE/scripts/"
  chmod +x "$WORKSPACE/scripts/"*.js
  echo "✓ 记忆优化脚本已部署"
else
  echo "⚠️  未找到优化脚本，跳过"
fi
```

#### 8d.3 更新 AGENTS.md（添加记忆管理规则）

```bash
# 检查 AGENTS.md 是否已包含记忆管理规则
if ! grep -q "§2 记忆管理规则" "$WORKSPACE/AGENTS.md"; then
  # 追加记忆管理规则到 AGENTS.md
  cat "$SKILL_DIR/references/memory-rules-addon.md" >> "$WORKSPACE/AGENTS.md"
  echo "✓ AGENTS.md 已更新（添加记忆管理规则）"
fi
```

#### 8d.4 配置定时任务

```bash
# 1. 每天凌晨 3:00 更新记忆衰减状态
(crontab -l 2>/dev/null | grep -v "memory-decay.js"; echo "0 3 * * * cd $WORKSPACE && node scripts/memory-decay.js update 2>&1 | logger -t openclaw-memory-decay") | crontab -
echo "✓ 记忆衰减更新任务已安装（每天 3:00）"

# 2. 更新 merge-daily-transcript.js 为优化版
if [ -f "$WORKSPACE/scripts/merge-daily-transcript.js" ]; then
  # 备份原版本
  cp "$WORKSPACE/scripts/merge-daily-transcript.js" "$WORKSPACE/scripts/merge-daily-transcript.js.backup"

  # 替换为优化版（整合了分类、去重、衰减、索引构建）
  cp "$SKILL_DIR/scripts/memory-optimization/merge-daily-transcript.js" "$WORKSPACE/scripts/"
  echo "✓ 记忆归档脚本已升级为优化版"
fi
```

#### 8d.5 配置自动加载 L0 索引

```bash
# 更新 systemPrompt.files，添加 L0 索引
openclaw config set agents.defaults.systemPrompt.files '["~/.openclaw/workspace/AGENTS.md","~/.openclaw/workspace/SOUL.md","~/.openclaw/workspace/IDENTITY.md","~/.openclaw/workspace/GOALS.md","~/.openclaw/workspace/memory/metadata/L0-index.md"]'

echo "✓ 已配置自动加载 L0 记忆索引"
```

#### 8d.6 初始化记忆索引

```bash
# 构建初始索引
if [ -f "$WORKSPACE/scripts/memory-index-builder.js" ]; then
  node "$WORKSPACE/scripts/memory-index-builder.js" build
  echo "✓ 记忆索引已构建（L0/L1/L2）"
fi
```

#### 8d.7 告知用户优化效果

> "记忆系统优化已完成！
>
> **新增功能**：
> - ✓ 渐进式披露：三层索引（L0/L1/L2），Token 使用量降低 10 倍
> - ✓ 智能分类：6 种记忆类型（profiles/preferences/entities/events/cases/patterns）
> - ✓ 智能去重：向量相似度 + LLM 语义决策，避免重复记忆
> - ✓ 衰减晋升：Weibull 模型，重要记忆半衰期 90 天，频繁访问的记忆自动晋升
>
> **新增定时任务**：
> - 每天凌晨 3:00：更新记忆衰减状态
>
> **如何使用**：
> - 正常和我聊天，系统会自动分类、去重、强化记忆
> - 明天运行健康检查：`node ~/.openclaw/workspace/scripts/memory-health-check.js`
> - 查看记忆索引：`cat ~/.openclaw/workspace/memory/metadata/L0-index.md`"

### 8e. 验证激活状态

**逐项检查所有激活配置是否生效。**

```bash
echo "=== 激活状态检查 ==="

# 1. 自动加载
echo -e "\n[1/6] 自动加载配置"
if openclaw config get agents.defaults.systemPrompt.files | grep -q "SOUL.md"; then
  echo "✓ 自动加载已配置"
  # 检查是否包含 L0 索引
  if openclaw config get agents.defaults.systemPrompt.files | grep -q "L0-index.md"; then
    echo "✓ L0 记忆索引已配置自动加载"
  fi
else
  echo "❌ 自动加载未配置"
fi

# 2. 心跳
echo -e "\n[2/6] 心跳机制"
if openclaw config get agents.defaults.heartbeat.enabled | grep -q "true"; then
  echo "✓ 心跳已启用"
  crontab -l | grep "openclaw heartbeat" && echo "✓ 心跳定时任务已安装" || echo "⚠️  心跳定时任务未安装"
else
  echo "❌ 心跳未启用"
fi

# 3. 记忆归档
echo -e "\n[3/6] 记忆归档"
crontab -l | grep "merge-daily-transcript" && echo "✓ 记忆归档任务已安装" || echo "⚠️  记忆归档任务未安装"

# 4. 记忆衰减（如果配置了优化）
echo -e "\n[4/6] 记忆衰减更新"
crontab -l | grep "memory-decay" && echo "✓ 记忆衰减任务已安装" || echo "⚠️  记忆衰减任务未安装（未配置优化）"

# 5. Git 自动提交
echo -e "\n[5/6] Git 自动提交"
crontab -l | grep "auto-commit" && echo "✓ Git 自动提交任务已安装" || echo "⚠️  Git 自动提交任务未安装"

# 6. 向量索引
echo -e "\n[6/6] 向量索引自动更新"
if openclaw config get memorySearch.autoIndex | grep -q "true"; then
  echo "✓ 向量索引自动更新已启用"
else
  echo "⚠️  向量索引自动更新未启用"
fi

echo -e "\n=== 所有定时任务 ==="
crontab -l | grep openclaw || echo "未找到 openclaw 相关定时任务"

# 检查记忆优化脚本
echo -e "\n=== 记忆优化脚本 ==="
if [ -f "$WORKSPACE/scripts/memory-classifier.js" ]; then
  echo "✓ 记忆优化脚本已安装"
  ls -1 "$WORKSPACE/scripts/memory-"*.js 2>/dev/null | wc -l | xargs echo "  脚本数量:"
else
  echo "⚠️  记忆优化脚本未安装（未配置优化）"
fi
```

### 8f. 首次使用指南

**激活完成后，告知用户如何验证系统是否正常工作。**

根据用户在 7b.2 选择的定时任务，动态生成提示信息：

**基础提示**（所有用户）：

> "系统已激活！接下来：
>
> **立即生效**：
> - ✓ 下次对话会自动加载你的 SOUL、AGENTS 宪法、IDENTITY 和 GOALS
> - ✓ 记忆系统已就绪，所有对话自动归档到 memory/daily/
> - ✓ 向量搜索已配置，可以召回历史记忆
>
> **基础定时任务**（已安装）：
> - 每小时第 7 分钟：基础心跳检查
> - 每天凌晨 2:17：自动合并对话记录到 memory/transcripts/
> - 每 6 小时：自动提交记忆变更到 Git

**如果用户选择了"每日目标汇报"**，追加：

> **每天晚上 8:00**：
> - 我会主动找你，汇报今天的目标完成情况
> - 提醒明天的重要任务
> - 如果有被遗忘的任务或即将到期的 deadline，会主动提醒

**如果用户选择了"每周反思总结"**，追加：

> **每周日晚上 9:00**：
> - 我会回顾本周的对话和工作
> - 生成深度反思：完成了什么、遇到了哪些问题、学到了什么、下周的改进建议
> - 反思会保存到 memory/reflections/ 目录

**如果用户选择了"每日健康检查"**，追加：

> **每天早上 9:00**：
> - 我会执行系统健康检查
> - 检查心跳、记忆归档、Git 提交是否正常
> - 如发现问题，会主动告知并提供解决方案

**如果用户选择了"任务 deadline 提醒"**，追加：

> **每天早上 9:00**：
> - 我会检查 GOALS.md 中的所有任务截止日期
> - 提前 3 天、1 天、当天提醒
> - 如有到期任务，会主动发起对话提醒

**通用验证指南**（所有用户）：

> **试试这些命令验证系统**：
> 1. `现在的目标是什么？` — 查看当前目标（读取 GOALS.md）
> 2. `我是谁？` — 查看你的身份档案（读取 IDENTITY.md）
> 3. `你的性格是什么？` — 查看我的灵魂（读取 SOUL.md）
> 4. `回忆一下我们刚才讨论的内容` — 测试记忆召回
>
> **如果心跳没有按预期工作**：
> 1. 运行 `crontab -l | grep openclaw` 检查定时任务是否安装
> 2. 运行 `openclaw config get agents.defaults.heartbeat.enabled` 检查心跳是否启用
> 3. 手动触发测试：`openclaw heartbeat --agent last`
> 4. 查看日志：`tail -f /var/log/system.log | grep openclaw`（macOS）或 `journalctl -f | grep openclaw`（Linux）
> 5. 运行健康检查脚本：`bash ~/.openclaw/workspace/scripts/health-check.sh`
>
> 如果遇到问题，参考下面的 §7 故障排查。"

---

## §8 [TROUBLESHOOTING] 故障排查

### 8a. 心跳不工作

**症状**：1 小时后 AI 没有主动发起对话。

**诊断步骤**：

```bash
# 1. 检查心跳是否启用
openclaw config get agents.defaults.heartbeat.enabled
# 期望输出：true

# 2. 检查定时任务是否安装
crontab -l | grep "openclaw heartbeat"
# 期望输出：7 * * * * openclaw heartbeat --agent last ...

# 3. 检查 openclaw CLI 是否可用
which openclaw
# 期望输出：/usr/local/bin/openclaw 或类似路径

# 4. 手动触发心跳测试
openclaw heartbeat --agent last
# 观察是否有错误输出

# 5. 查看心跳日志（macOS）
log show --predicate 'eventMessage contains "openclaw-heartbeat"' --last 1h

# 6. 查看心跳日志（Linux）
journalctl -t openclaw-heartbeat --since "1 hour ago"
```

**常见问题与解决方案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `enabled: false` | 心跳未启用 | `openclaw config set agents.defaults.heartbeat.enabled true` |
| cron 任务不存在 | 定时任务未安装 | 重新执行 §7b.2 |
| `openclaw: command not found` | CLI 未安装或不在 PATH | 安装 openclaw CLI 或配置 PATH |
| 心跳触发但无响应 | `prompt` 未配置 | 重新执行 §7b.1，确保 `prompt` 字段包含 HEARTBEAT.md 内容 |
| 权限被拒绝 | `directPolicy` 未设置 | `openclaw config set agents.defaults.heartbeat.directPolicy "allow"` |

### 8b. 记忆召回失败

**症状**：问"回忆一下 XX"时，AI 说找不到相关记忆。

**诊断步骤**：

```bash
# 1. 检查向量搜索配置
openclaw config get memorySearch
# 确认 provider、model、apiKey 已配置

# 2. 测试向量搜索
openclaw memory search "test"
# 如果报错，说明 embedding 配置有问题

# 3. 检查记忆文件是否存在
ls -lh "$WORKSPACE/memory/daily/"
ls -lh "$WORKSPACE/memory/transcripts/"
# 确认有对话记录文件

# 4. 检查索引是否存在
ls -lh "$WORKSPACE/.openclaw/memory-index/"
# 确认有索引文件

# 5. 手动重建索引
openclaw memory reindex
```

**常见问题与解决方案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `embedding provider not configured` | 未配置 embedding API | 重新执行 §5d，配置 Gemini/SiliconFlow/OpenAI |
| `API key invalid` | API key 错误或过期 | 更新 `openclaw.json` 中的 `memorySearch.remote.apiKey` |
| 搜索返回空结果 | 索引未建立或过期 | `openclaw memory reindex` |
| memory/ 目录为空 | 还没有对话记录 | 正常现象，多对话几次后会积累 |
| `extraPaths` 未配置 | 搜索范围不包含记忆目录 | 重新执行 §5d，配置 `extraPaths` |

### 8c. SOUL 没有加载

**症状**：AI 的行为不符合 SOUL.md 中定义的性格。

**诊断步骤**：

```bash
# 1. 检查自动加载配置
openclaw config get agents.defaults.systemPrompt.files
# 期望输出：包含 SOUL.md、AGENTS.md 等文件路径

# 2. 检查文件是否存在
test -f "$WORKSPACE/SOUL.md" && echo "SOUL.md 存在" || echo "SOUL.md 不存在"

# 3. 手动测试加载
# 在对话中说："读取 ~/.openclaw/workspace/SOUL.md 并总结我的性格"
# 观察 AI 是否能正确读取和理解

# 4. 检查文件权限
ls -l "$WORKSPACE/SOUL.md"
# 确认文件可读（-rw-r--r--）
```

**常见问题与解决方案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| `systemPrompt.files` 为空 | 自动加载未配置 | 重新执行 §7a |
| SOUL.md 不存在 | 部署失败或文件被删除 | 重新执行 §2 部署文件 |
| 文件权限错误 | 文件不可读 | `chmod 644 "$WORKSPACE/SOUL.md"` |
| 配置了但不生效 | OpenClaw 版本不支持 | 检查 OpenClaw 版本，升级到最新版 |

### 8d. 记忆归档不执行

**症状**：memory/daily/ 下的文件一直不合并到 transcripts/。

**诊断步骤**：

```bash
# 1. 检查定时任务
crontab -l | grep "merge-daily-transcript"
# 期望输出：17 2 * * * cd ... && node scripts/merge-daily-transcript.js

# 2. 检查脚本是否存在
test -f "$WORKSPACE/scripts/merge-daily-transcript.js" && echo "脚本存在" || echo "脚本不存在"

# 3. 手动执行脚本测试
cd "$WORKSPACE" && node scripts/merge-daily-transcript.js
# 观察是否有错误输出

# 4. 查看日志
log show --predicate 'eventMessage contains "openclaw-memory"' --last 24h  # macOS
journalctl -t openclaw-memory --since "24 hours ago"  # Linux
```

**常见问题与解决方案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| cron 任务不存在 | 定时任务未安装 | 重新执行 §7c |
| 脚本不存在 | 部署失败 | 重新执行 §2c |
| `node: command not found` | Node.js 未安装 | 安装 Node.js：`brew install node`（macOS）或 `apt install nodejs`（Linux） |
| 脚本执行报错 | 脚本逻辑问题 | 查看错误信息，检查 memory/daily/ 目录权限 |

### 8e. Git 自动提交不工作

**症状**：memory/ 下的文件变更没有自动提交到 Git。

**诊断步骤**：

```bash
# 1. 检查定时任务
crontab -l | grep "auto-commit"
# 期望输出：23 */6 * * * cd ... && bash scripts/auto-commit.sh

# 2. 检查脚本是否存在且可执行
test -x "$WORKSPACE/scripts/auto-commit.sh" && echo "脚本可执行" || echo "脚本不可执行"

# 3. 手动执行脚本测试
cd "$WORKSPACE" && bash scripts/auto-commit.sh
# 观察是否有错误输出

# 4. 检查 Git 状态
cd "$WORKSPACE" && git status
# 查看是否有未提交的变更

# 5. 查看 Git 提交历史
cd "$WORKSPACE" && git log --oneline --since="1 day ago"
# 确认是否有自动提交记录
```

**常见问题与解决方案**：

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| cron 任务不存在 | 定时任务未安装 | 重新执行 §7b.3 |
| 脚本不可执行 | 权限问题 | `chmod +x "$WORKSPACE/scripts/auto-commit.sh"` |
| Git 未初始化 | §5e 未执行 | 重新执行 §5e |
| `git: command not found` | Git 未安装 | 安装 Git：`brew install git`（macOS）或 `apt install git`（Linux） |

### 8f. 完整健康检查脚本

**一键检查所有组件状态。**

将以下脚本保存为 `$WORKSPACE/scripts/health-check.sh`：

```bash
#!/bin/bash
WORKSPACE="$HOME/.openclaw/workspace"

echo "=== OpenClaw Soul 健康检查 ==="
echo ""

# 1. 核心文件
echo "[1/7] 核心文件"
for file in AGENTS.md SOUL.md HEARTBEAT.md BOOTSTRAP.md USER.md IDENTITY.md GOALS.md; do
  test -s "$WORKSPACE/$file" && echo "  ✓ $file" || echo "  ❌ $file 缺失或为空"
done

# 2. 自动加载
echo -e "\n[2/7] 自动加载"
if openclaw config get agents.defaults.systemPrompt.files 2>/dev/null | grep -q "SOUL.md"; then
  echo "  ✓ 已配置"
else
  echo "  ❌ 未配置"
fi

# 3. 心跳
echo -e "\n[3/7] 心跳机制"
if openclaw config get agents.defaults.heartbeat.enabled 2>/dev/null | grep -q "true"; then
  echo "  ✓ 已启用"
  crontab -l 2>/dev/null | grep -q "openclaw heartbeat" && echo "  ✓ 定时任务已安装" || echo "  ⚠️  定时任务未安装"
else
  echo "  ❌ 未启用"
fi

# 4. 记忆归档
echo -e "\n[4/7] 记忆归档"
crontab -l 2>/dev/null | grep -q "merge-daily-transcript" && echo "  ✓ 定时任务已安装" || echo "  ⚠️  定时任务未安装"

# 5. Git 自动提交
echo -e "\n[5/7] Git 自动提交"
crontab -l 2>/dev/null | grep -q "auto-commit" && echo "  ✓ 定时任务已安装" || echo "  ⚠️  定时任务未安装"
test -d "$WORKSPACE/.git" && echo "  ✓ Git 已初始化" || echo "  ❌ Git 未初始化"

# 6. 向量搜索
echo -e "\n[6/7] 向量搜索"
if openclaw config get memorySearch.provider 2>/dev/null | grep -q -E "gemini|openai"; then
  echo "  ✓ Embedding 已配置"
else
  echo "  ❌ Embedding 未配置"
fi

# 7. 依赖 Skills
echo -e "\n[7/7] 依赖 Skills"
for skill in evoclaw self-improving skill-vetter hdd sdd; do
  test -f "$WORKSPACE/skills/$skill/SKILL.md" && echo "  ✓ $skill" || echo "  ⚠️  $skill 未安装"
done

echo -e "\n=== 检查完成 ==="
```

使用方法：
```bash
chmod +x "$WORKSPACE/scripts/health-check.sh"
bash "$WORKSPACE/scripts/health-check.sh"
```

---

_openclaw-soul v3.0.0 — Lightweight, growable soul. Slimmed AGENTS.md (-79%), reordered flow (BOOTSTRAP first), user-controlled skill install, permission check, two-level fallback._
