# /novel init - 初始化新小说项目

## 触发方式

```
/novel init [项目名]
/novel init [项目名] [目录路径]   # 指定目录
```

或对话式：
```
初始化新小说项目
创建新项目
```

---

## 功能

创建标准小说项目结构。

---

## 执行步骤

### 1. 确定项目路径

**规则**：
- 用户提供了目录 → 使用用户目录
- 用户没提供 → 使用 agent 工作目录 + `novel/<项目名>/`

**Agent 工作目录**：由 OpenClaw 运行时决定（通常是 `~/.openclaw/workspace-coding/`）

**示例**：
```
用户: /novel init 我的小说
     → 项目路径: <Agent工作目录>/novel/我的小说/

用户: /novel init 我的小说 /custom/path/
     → 项目路径: /custom/path/我的小说/
```

### 2. 创建标准结构

```
<项目名>/
├── memory/
│   └── README.md
├── stories/
│   └── <项目名>/
│       ├── specification.md
│       ├── creative-plan.md
│       ├── tasks.md
│       └── content/
│           ├── volume1/
│           ├── volume2/
│           └── volume3/
├── spec/
│   ├── knowledge/
│   │   └── README.md
│   └── tracking/
│       ├── character-state.json
│       ├── relationships.json
│       ├── plot-tracker.json
│       └── validation-rules.json
└── .claude/
    ├── settings.json
    └── knowledge-base/
        ├── genres/
        ├── styles/
        └── requirements/
```

### 3. 复制知识库

从 skill 目录复制：
- `knowledge-base/genres/` - 5种类型知识
- `knowledge-base/styles/` - 写作风格
- `knowledge-base/requirements/` - 写作规范

### 4. 初始化追踪文件（空壳 + progress.json）

自动创建追踪系统所需的基础文件：

**spec/tracking/character-state.json**
```json
{
  "version": "1.0",
  "characters": {},
  "last_updated": "ISO日期"
}
```

**spec/tracking/relationships.json**
```json
{
  "version": "1.0",
  "relationships": [],
  "last_updated": "ISO日期"
}
```

**spec/tracking/plot-tracker.json**
```json
{
  "version": "1.0",
  "plotlines": [],
  "foreshadowing": [],
  "milestones": [],
  "last_updated": "ISO日期"
}
```

**spec/tracking/validation-rules.json**
```json
{
  "version": "1.0",
  "word_count": {
    "min": 2000,
    "max": 4000,
    "strict": false
  },
  "must_include": [],
  "forbidden": [],
  "last_updated": "ISO日期"
}
```

**spec/tracking/progress.json**
```json
{
  "version": "1.0",
  "current_chapter": 0,
  "completed_chapters": [],
  "total_planned": 0,
  "last_updated": "ISO日期"
}
```

---

## 输出

```
✅ 项目初始化完成

📁 项目路径：<根据上述规则确定>

📋 项目结构：
├── memory/                    # 创作记忆
├── stories/<项目名>/         # 故事文件
│   ├── specification.md      # 故事规格
│   ├── creative-plan.md      # 创作计划
│   ├── tasks.md              # 任务清单
│   └── content/              # 正文内容
├── spec/
│   ├── knowledge/            # 项目知识库
│   └── tracking/             # 状态追踪
└── .claude/
    └── knowledge-base/       # 写作知识库

🎯 下一步：
/novel constitution - 创建创作宪法
```
