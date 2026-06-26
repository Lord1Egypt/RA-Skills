# Phase 0 — 项目初始化

> OpenClaw Skill "novel-free" 生命周期 Phase 0 详细流程文档

## 触发条件

用户说 **"新建小说"**（或等价指令）时触发 Phase 0。
本阶段负责所有前置准备工作，完成后方可进入 Phase 1（前期架构）。

---

## Step 0-1：收集核心设定

Coordinator 主动询问或确认以下信息（用户已提供的字段可跳过）：

| 字段 | 说明 | 示例 |
|------|------|------|
| 标题 | 可暂定，后续可修改 | 《星渊纪》 |
| 类型/题材 | 魔幻 / 现代 / 古言 / 悬疑 / 科幻 / 仙侠等 | 东方玄幻 |
| 目标字数 / 预计章节数 | 总体篇幅规划 | 50 章 / 20 万字 |
| 基调 | 治愈 / 爽文 / 正剧 / BE / HE | 正剧偏燃，HE |
| 主角 / 主要角色粗略描述 | 外貌 + 性格 + 核心诉求 | 冷面少年，渴望自由 |
| 特殊元素 / 雷点 / 偏好 | R18 / 魂穿 / 重生 / 禁忌话题等 | 重生、不接受后宫 |

**交互策略：**
- 若用户一次性给出所有信息，直接进入下一步。
- 若信息不完整，逐项追问，每次追问不超过 3 个字段。
- 将收集到的信息临时存放于内存，待 Step 0-5 写入元数据文件。

---

## Step 0-2：创建项目目录树

运行初始化脚本，在 `projects/<项目名>/` 下创建完整目录结构。

推荐入口：

```bash
scripts/init-project.sh "<项目名>"
```

> 说明：`init-project.sh` 是唯一提供的初始化脚本。Windows 环境建议通过 Git Bash、WSL，或宿主提供的等价 shell 能力执行同一脚本。若宿主不直接允许执行脚本，只要具备创建目录、复制模板与写入文件的等价能力，也可按本节目录结构完成初始化。

生成的目录结构：

```
projects/<项目名>/
├── meta/
│   ├── project.md              # 项目元数据
│   ├── metadata.json           # 统一元数据（进度/版本/自动推进状态）
│   ├── workflow-state.json     # 机器可读工作流状态（phase / gate / 恢复状态）
│   ├── config.md               # 模型分工 + 关键章节配置 + 自动推进参数
│   ├── style-anchor.md         # 风格锚定文档（v0.1→v1.0）
│   ├── selected-style-sample.md # 用户选定的文风样本（Phase 1-6.5 产出）
│   └── agent-registry.json     # Agent 注册表
├── worldbuilding/
│   └── world.md                # 世界观文档
├── characters/
│   ├── protagonist.md          # 主角详细档案
│   └── characters.md           # 其他角色卡集合
├── outline/
│   ├── outline.md              # 全书大纲
│   └── chapter-outline.md      # 章节细纲
├── chapters/
│   ├── ch001.md ~ ch999.md     # 章节正文（3位数编号）
│   ├── chapter_name.md         # 章节中文名称映射表
│   └── history/                # 历史版本
├── archive/
│   ├── archive.md              # 项目日志
│   ├── phase1-review.md        # Phase 1 终审报告
│   ├── phase1-revision-log.md  # Phase 1 修改日志
│   └── reader-feedback/        # 读者反馈存档
└── references/
    ├── state-tracker.md        # 状态追踪表
    ├── relationship-tracker.md # 关系追踪表
    ├── plot-tracker.md         # 剧情追踪表
    ├── rolling-summary.md      # 滚动摘要
    └── fixed-context.md        # 固定层摘要
```

---

## Step 0-3：检测可用模型（新增步骤）

Coordinator 读取 `openclaw.json`，解析所有可用 AI 模型（`provider/model-id` 格式），并向用户展示模型列表。

> 下文出现的 `read()`、`displayModelList()` 等代码块均为**示意性伪代码**，只用于说明 Phase 0 的调度与展示逻辑，不代表宿主环境必须提供同名 API。

### 文件路径

按以下顺序依次尝试读取，找到即止：

```
1. ~/.openclaw/openclaw.json        （用户级配置，优先）
2. ./openclaw.json                  （当前工作目录）
3. /etc/openclaw/openclaw.json      （系统级配置）
```

### JSON 结构说明

`openclaw.json` 的 `providers` 数组包含所有已配置的模型提供商，每个 model 的 `id` 字段与 `provider.name` 组合后即为 `sessions_spawn` 的 `model` 参数值：

```json
{
  "providers": [
    {
      "name": "anthropic",
      "models": [
        {
          "id": "claude-opus-4-6",
          "displayName": "Claude Opus 4.6",
          "contextWindow": 200000,
          "capabilities": ["reasoning", "literary", "long-context"]
        }
      ]
    },
    {
      "name": "openai",
      "models": [
        {
          "id": "gpt-4o",
          "displayName": "GPT-4o",
          "contextWindow": 128000,
          "capabilities": ["reasoning", "general"]
        }
      ]
    }
  ]
}
```

> `capabilities` 常见标签：`reasoning`（推理）、`literary`（文学）、`long-context`（长上下文）、`general`（通用）

### 读取伪代码

```javascript
// Coordinator 伪代码
const config = JSON.parse(read("~/.openclaw/openclaw.json"));
const availableModels = [];

for (const provider of config.providers) {
  for (const model of provider.models) {
    availableModels.push({
      id: `${provider.name}/${model.id}`,        // ← 调用 sessions_spawn 时的 model 值
      displayName: model.displayName,
      contextWindow: model.contextWindow,
      capabilities: model.capabilities
    });
  }
}

// 向用户展示
displayModelList(availableModels);
```

### 失败降级处理

若文件不存在或读取/解析失败，**不阻断流程**，改为手动模式：

```
⚠️ 无法读取 openclaw.json（文件不存在或格式错误）。
请手动输入各 Agent 使用的模型，格式为 provider/model-id。
示例：anthropic/claude-opus-4-6、openai/gpt-4o、google/gemini-2.5-pro
（如不确定 ID，输入模型名称，系统将在调用时尝试匹配）
```

**展示格式示例：**

```
可用模型列表：
1. anthropic/claude-opus-4-6   — 高推理 / 文学表达，200K 上下文  [reasoning, literary]
2. anthropic/claude-sonnet-4-6 — 平衡 / 长上下文，200K 上下文    [reasoning, long-context]
3. openai/gpt-4o               — 通用模型，128K 上下文           [general]
4. google/gemini-2.5-pro       — 长上下文模型，1M 上下文         [long-context]
5. deepseek/deepseek-r1        — 推理模型，64K 上下文            [reasoning]
...
```

---

## Step 0-4：模型-Agent 映射

展示 `12Agent` 体系的角色清单，并为 **11 个可调度子 Agent** 选择具体模型。Coordinator 是当前主会话，不参与子 Agent 模型分配。映射结果写入 `meta/config.md`。

### 默认推荐映射

| Agent | 职责简述 | 推荐模型类型 |
|-------|---------|-------------|
| Worldbuilder | 世界观构建 | 高推理模型 |
| CharacterDesigner | 角色设计 | 高推理模型 |
| OutlinePlanner | 全书大纲 | 高推理模型 |
| ChapterOutliner | 章节细纲 | 长上下文模型 |
| MainWriter | 正文写作 | 长上下文 + 文学表达更强模型 |
| OOCGuardian | 一致性检查 | 长上下文模型 |
| BattleAgent | 战斗/动作场景 | 通用模型 |
| FinalReviewer | 终审一致性 | 高推理模型 |
| ReaderSimulator | 读者视角反馈 | 通用模型 |
| StyleAnchorGenerator | 风格锚定生成 | 高推理模型 |
| RollingSummarizer | 滚动摘要 | 长上下文模型 |

> **注意：** 表中未列出 Coordinator，因为 Coordinator 即当前运行的主 Agent，不需要额外分配模型。

### 交互方式

- 展示上表后，用户可逐个指定，也可输入"使用推荐"接受默认。
- 若用户只指定部分 Agent 的模型，其余沿用推荐。
- 最终映射结果写入 `meta/config.md` 的 `model_assignment` 段，并同步写入 `meta/agent-registry.json`。

> **格式强制要求：** 写入 `meta/config.md` 和 `meta/agent-registry.json` 的模型值必须使用 `provider/model-id` 格式（与子 Agent 调度时使用的模型参数一致）。
>
> 正确示例：
> - ✅ `anthropic/claude-opus-4-6`
> - ✅ `openai/gpt-4o`
> - ✅ `google/gemini-2.5-pro`
> - ❌ `Claude Opus`（自然语言名称，无法直接用于配置）
>
> 如用户输入自然语言名称（如"Claude Opus"），Coordinator 须结合 Step 0-3 解析的可用模型列表，将其转换为 `provider/model-id` 格式后再写入。

---

## Step 0-5：初始化元数据文件

从 `assets/` 复制模板并填充用户设定：

### meta/project.md — 项目元数据

```markdown
# 项目元数据

| 字段 | 内容 |
|------|------|
| 标题 | {{project_title}} |
| 类型 | {{genre}} |
| 风格标签 | {{style_tags}} |
| 目标篇幅 | {{target_scope}} |
| 基调 | {{tone}} |
| 章节字数目标 | 4000字 |
| 字数允许浮动 | 3000-6000字 |
| 版本 | v0.1 |
| 创建日期 | {{created_at}} |
| 最后更新 | {{updated_at}} |

## 用户授权边界

- R18：{{r18}}
- 露骨色情：{{explicit}}
- BE结局：{{be_ending}}
- 特定元素：{{special_elements}}

## 项目简介

{{project_summary}}
```

### meta/metadata.json — 统一元数据

```json
{
  "project": {
    "title": "{{project_title}}",
    "version": "v0.1",
    "phase": 0,
    "lastUpdated": "{{updated_at}}"
  },
  "writingProgress": {
    "currentChapter": 0,
    "lastCompletedChapter": 0,
    "autoAdvance": {
      "enabled": false,
      "remaining": 0,
      "totalRequested": 0,
      "currentChapter": 0,
      "intervalSeconds": 6,
      "autoConfirm": false,
      "status": "idle"
    }
  },
  "chapters": {}
}
```

### meta/workflow-state.json — 工作流状态机

```json
{
  "phaseState": {
    "currentPhase": 0,
    "status": "initialized",
    "lastTransitionAt": "{{updated_at}}",
    "architectureFinalized": false
  },
  "chapterWorkflow": {
    "currentChapter": 0,
    "lastClosedChapter": 0,
    "lastOocCheckChapter": 0,
    "lastRollingSummaryChapter": 0,
    "lastReaderFeedbackChapter": 0,
    "resumeRequired": true,
    "currentTrack": "none",
    "chapterEntryChecklistComplete": false,
    "currentChapterArtifacts": {
      "plan": false,
      "draft": false,
      "polish": false,
      "battlePass": false,
      "oocCheck": false,
      "finalReview": false,
      "archiveSync": false,
      "userReport": false
    }
  },
  "milestoneAudit": {
    "lastMilestoneAuditChapter": 0,
    "lastAuditResult": "green",
    "pendingWarnings": [],
    "nextAuditChapter": 20
  },
  "phase3Maintenance": {
    "lastModifiedChapter": 0,
    "cascadeAffectedChapters": [],
    "pendingRewrites": [],
    "lastMaintenanceAt": ""
  }
}
```

### meta/config.md — 模型分工 + 配置

```markdown
# 模型分工与项目配置

> ⚠️ **格式要求：** 模型值必须使用 `provider/model-id` 格式（如 `anthropic/claude-opus-4-6`）。自然语言名称不能直接写入配置文件。

## 模型分配

| 角色 | 模型 | 职责 |
|------|------|------|
| 主控/协调 | （当前会话模型，无需填写） | 整体调度、存档管理、用户汇报 |
| 主笔/初稿 | {{mainWriter_model}} | 完成章节初稿 |
| 润色/氛围 | {{mainWriter_model}} | 优化语言、氛围、感官细节 |
| OOC守护 | {{oocGuardian_model}} | 一致性检查 |
| 战斗/动作 | {{battleAgent_model}} | 仅高强度/复杂战斗 |
| 终稿三审 | {{finalReviewer_model}} | 逻辑/情感/节奏/语言终审 |
| 读者模拟 | {{readerSimulator_model}} | 读者视角反馈 |
| 风格锚定 | {{styleAnchorGenerator_model}} | 风格锚定生成 |
| 章节细纲 | {{chapterOutliner_model}} | 章节细纲规划 |
| 世界观 | {{worldbuilder_model}} | 世界观构建 |
| 滚动摘要 | {{rollingSummarizer_model}} | 滚动摘要压缩 |

## 关键章节配置（动态生成）

| 字段 | 内容 |
|------|------|
| key_chapters | （Phase 1 完成后填充） |
| act_boundaries | （Phase 1 完成后填充） |
| total_chapters | {{total_chapters}} |
| batch_mode | false |

## 自动推进配置（默认）

| 字段 | 默认值 | 说明 |
|------|--------|------|
| auto_advance_chapters | 4 | 一次自动写4章 |
| write_interval_seconds | 6 | API缓冲 + 阅读思考时间 |
| auto_confirm | false | 保留手动安全感 |

## 战斗Agent调用条件

满足以下任一条件时调用战斗Agent：
- 细纲/本章规划标注"高强度/复杂/多方战斗"
- 需要专业动作/物理/兵器描写
- 大规模战役场景

不满足上述条件时，战斗描写由主笔完成。
```

### meta/style-anchor.md — 风格锚定 v0.1

（见 Step 0-6 详细说明）

> `meta/config.md` 是**项目全生命周期配置文件**：Phase 0 初始化基础模型分工与默认参数，Phase 1 回填关键章节配置，Phase 2 持续读取并消费这些配置。

### meta/agent-registry.json — Agent 注册表

> `"model"` 字段值必须为 `provider/model-id` 格式（如 `anthropic/claude-opus-4-6`），从 Step 0-3 解析的模型列表中取值。

```json
{
  "projectId": "{{project_id}}",
  "projectTitle": "{{project_title}}",
  "registeredAgents": {
    "worldbuilder": {
      "id": "worldbuilder",
      "name": "世界观构建",
      "model": "{{worldbuilder_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "characterDesigner": {
      "id": "characterDesigner",
      "name": "角色设计",
      "model": "{{characterDesigner_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "outlinePlanner": {
      "id": "outlinePlanner",
      "name": "大纲规划",
      "model": "{{outlinePlanner_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "chapterOutliner": {
      "id": "chapterOutliner",
      "name": "章节细纲",
      "model": "{{chapterOutliner_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "mainWriter": {
      "id": "mainWriter",
      "name": "主笔",
      "model": "{{mainWriter_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "oocGuardian": {
      "id": "oocGuardian",
      "name": "OOC守护",
      "model": "{{oocGuardian_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "battleAgent": {
      "id": "battleAgent",
      "name": "战斗写作",
      "model": "{{battleAgent_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "finalReviewer": {
      "id": "finalReviewer",
      "name": "终稿审核",
      "model": "{{finalReviewer_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "readerSimulator": {
      "id": "readerSimulator",
      "name": "读者模拟",
      "model": "{{readerSimulator_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "styleAnchorGenerator": {
      "id": "styleAnchorGenerator",
      "name": "风格锚定生成",
      "model": "{{styleAnchorGenerator_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    },
    "rollingSummarizer": {
      "id": "rollingSummarizer",
      "name": "滚动摘要",
      "model": "{{rollingSummarizer_model}}",
      "status": "available",
      "registeredAt": "{{created_at}}",
      "lastUsed": "",
      "taskCount": 0
    }
  },
  "version": "v1.0",
  "createdAt": "{{created_at}}"
}
```

> **注意：** 表中未列出 Coordinator，因为 Coordinator 即当前运行的主 Agent（OpenClaw 会话本身），不需要额外注册。

---

## Step 0-6：初始化风格锚定 v0.1

创建 `meta/style-anchor.md` 基础版本：

```markdown
# 风格锚定文档

> ⚠️ Phase 0 初始化时仅填写基础偏好，风格示范文本在 Phase 1 Step 1-7 由 StyleAnchorGenerator 生成后升级为 v1.0

## 基本信息

| 字段 | 内容 |
|------|------|
| 项目 | {{project_title}} |
| 版本 | v0.1 |
| 最后更新 | {{updated_at}} |

---

## 叙事视角

### 当前视角
{{narrative_pov}}  （如：第三人称限知视角 / 第一人称 / 全知视角）

### 视角说明
（详细描述视角选择的原因和使用规范）

---

## 语言风格关键词

{{style_keywords}}  （3-5个核心风格词汇，如：典雅、凝练、含蓄、流畅等）

---

## 禁用词表

（可先留空，Phase 1 后补充）

---

## 对话风格基础偏好

{{dialogue_style}}  （对话的整体风格倾向）

---

## 感官描写优先级

1. {{sense_1}}  （最优先调动的感官）
2. {{sense_2}}
3. {{sense_3}}
4. {{sense_4}}

---

## 风格示范文本

> 以下内容在 Phase 1 由 StyleAnchorGenerator 生成 v1.0 定稿后填充

### 示范文本1
（200-500字）

### 示范文本2
（200-500字）

### 示范文本3
（200-500字）

---

## 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v0.1 | {{created_at}} | 初始化 |
| v1.0 | | 定稿，含示范文本 |
```

**重要说明：**
- Phase 0 仅初始化基础偏好，所有 `{{}}` 占位符根据用户输入填充。
- 风格示范文本（示例段落、标杆片段）在 Phase 1 Step 1-7 由 StyleAnchorGenerator 生成。
- 版本从 v0.1 升至 v1.0 后，所有写作 Agent 的 prompt 必须严格附带风格锚定全文。

---

## Step 0-7：输出确认

### 展示内容

在输出确认前，Coordinator 还必须同步：
- `meta/metadata.json.project.phase = 0`
- `meta/workflow-state.json.phaseState.currentPhase = 0`
- `meta/workflow-state.json.phaseState.status = "phase0_ready"`

Coordinator 向用户展示以下信息：

1. **项目目录树**（完整目录结构）
2. **项目元数据摘要**（标题、类型、篇幅、基调）
3. **模型分配表**（每个 Agent 对应的模型）
4. **风格锚定 v0.1 摘要**（叙事视角、语言风格、对话风格）
5. **下一步预告**（Phase 1 将依次调用 Worldbuilder → CharacterDesigner → OutlinePlanner → ChapterOutliner → FinalReviewer → 预选文风（Step 1-6.5）→ StyleAnchorGenerator）

### 确认交互

```
✅ 项目初始化完成！

📁 项目目录：projects/{{project_title}}/
📝 类型：{{genre}} | 基调：{{tone}} | 目标：{{total_chapters}}
🤖 模型分配：已配置 11 个子 Agent

是否确认以上设定，进入 Phase 1（前期架构）？
- 输入「确认」→ 进入 Phase 1
- 输入「修改 + 字段名」→ 修改对应设定
```

等待用户确认后，必须同时更新：
- `meta/metadata.json.project.phase = 1`
- `meta/workflow-state.json.phaseState.currentPhase = 1`
- `meta/workflow-state.json.phaseState.status = "phase1_ready"`

完成后才算正式进入 Phase 1。

---

## Phase 0 完整流程图

```
用户："新建小说"
    │
    ▼
Step 0-1：收集核心设定（交互式问答）
    │
    ▼
Step 0-2：创建项目目录树（scripts/init-project.sh）
    │
    ▼
Step 0-3：检测可用模型（读取 openclaw.json）
    │
    ▼
Step 0-4：模型-Agent 映射（用户选择/接受推荐）
    │
    ▼
Step 0-5：初始化元数据文件（从 assets/ 复制模板并填充）
    │
    ▼
Step 0-6：初始化风格锚定 v0.1（基础偏好）
    │
    ▼
Step 0-7：输出确认（展示 + 等待用户确认）
    │
    ▼
→ 进入 Phase 1
```
