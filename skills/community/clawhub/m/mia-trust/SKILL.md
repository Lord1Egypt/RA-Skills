---
name: mia-trust
description: MIA-Trust Pipeline - Memory-Intelligent Assistant 信任守门+记忆进化 pipeline
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires":
          { "bins": ["node"], "env": [] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mia-trust",
              "bins": ["mia-trust"],
              "label": "Install mia-trust",
            },
          ],
      },
  }
---

# MIA-Trust Pipeline

Memory-Intelligent Assistant 信任守门 + 记忆进化 Pipeline

```
用户问题 → guard_blocked → Planner → evaluate_plan → 执行 → 双记忆存储
```

## 安装

```bash
cd skills/mia-trust
npm install
```

## 配置环境变量

```bash
export MIA_PLANNER_MODE=api
export MIA_PLANNER_API_KEY=your-api-key
export MIA_PLANNER_URL=https://your-api-endpoint/v1/chat/completions
export MIA_PLANNER_MODEL=your-model
```

## 使用

### 完整 Pipeline

```bash
# 一键执行
./run.mjs "你的问题"
```

### 分步执行

```bash
# Step 1: 问题预检
node trust/mia-trust.mjs guard_blocked '{"query":"你的问题"}'

# Step 2: 生成计划
node planner/mia-planner.mjs "你的问题"

# Step 3: 计划审查
node trust/mia-trust.mjs evaluate_plan '{"query":"问题","plan_draft":"计划","memories":[]}'
```

### 记忆与反馈

```bash
# 搜索记忆
node memory/mia-memory.mjs search "之前是怎么做的"

# 存储经验
node memory/mia-memory.mjs store '{"question":"...","plan":"...","execution":[]}'

# 列出记忆
node memory/mia-memory.mjs list 10

# 反馈
node feedback/mia-feedback.mjs store "问题" "答案" "good"
node feedback/mia-feedback.mjs list 10
```

## 目录结构

```
mia-trust/
├── run.mjs              # 一键执行入口
├── SKILL.md             # 本文档
├── package.json         # npm 配置（若存在根目录旧 trust_experience.json，postinstall 会同步到 trust/）
├── memory/              # 记忆模块
│   ├── mia-memory.mjs
│   └── memory.jsonl
├── planner/
│   └── mia-planner.mjs
├── feedback/
│   ├── mia-feedback.mjs
│   └── feedback.jsonl
└── trust/               # Trust 守门模块
    ├── mia-trust.mjs
    └── trust_experience.json
```

## 核心流程

| Step | 模块 | 功能 |
|------|------|------|
| 1 | guard_blocked | 问题安全预检 (6维度) |
| 2 | Planner | 生成执行计划 |
| 3 | evaluate_plan | 计划安全审查 (3轮) |
| 4 | 执行 | 按计划执行 |
| 5 | 双记忆 | memory + trust_experience |

## License

ISC