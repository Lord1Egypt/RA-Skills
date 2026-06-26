# Hita-Mind & Knowledge

> AI Agent 记忆与知识管理系统，让 AI 拥有"记忆"和"知识"

## Introduction

**Hita-Mind & Knowledge** is an AI Agent skill kit developed by hita, containing two complementary modules:

| Module | Purpose | Stores |
|--------|---------|--------|
| **Mind Module** | AI's Memory | Preferences, decisions, lessons, habits |
| **Knowledge Manager** | AI's Knowledge | Tips, methods, rules, experiences |

## Structure

```
Hita-Mind & Knowledge/
├── README.md
├── LICENSE
├── package.json
├── hita-mind-module/          # Mind Module (8 categories)
│   ├── SKILL.md
│   ├── index.js
│   ├── memory-store.json
│   └── README.md
└── hita-knowledge-manager/   # Knowledge Manager (3-tier system)
    ├── SKILL.md
    ├── index.js
    ├── knowledge-manager.js
    ├── knowledge-store.json
    └── README.md
```

## Quick Start

### Installation

```bash
# Mind Module
cd hita-mind-module && npm install

# Knowledge Manager
cd hita-knowledge-manager && npm install
```

### Usage Examples

**Mind Module**
```bash
cd hita-mind-module
node index.js add preferences "叫用户" "叫老板"
node index.js search 工作习惯
node index.js context patterns 5
```

**Knowledge Manager**
```bash
cd hita-knowledge-manager
node index.js add "冰箱除异味" "放一杯小苏打在冰箱里" "生活技巧"
node index.js search 冰箱
node index.js context 10
```

## Module Details

### Mind Module

AI memory system based on 8 categories.

**8 Categories:**
- decisions — Technical choices, important decisions
- preferences — Communication style, work habits
- patterns — Work templates, analysis processes
- causality — Problem root causes, lessons learned
- contacts — Names, contacts
- feedback — User corrections, feedback
- projects — Specific tasks, project data
- daily — Daily work logs

### Knowledge Manager

3-tier knowledge base system (L1/L2/L3) with smart tiering.

**3-Tier Architecture:**
- L1 (Hot): Full content, 50 items max, demoted after 30 days unused
- L2 (Warm): Summary + tags, 200 items max, demoted after 90 days unused
- L3 (Cold): Metadata index only, unlimited

## Use Cases / 使用场景

### Mind Module Use Cases

**【场景1】新任务接手 / New Task Handover**
```
用户交代新任务 → AI 先查 memory/daily 和 memory/projects → 了解背景再开始
User assigns a new task → AI checks memory/daily and memory/projects → Understand context before starting
```

**【场景2】用户偏好记住 / Remembering User Preferences**
```
用户说"以后开会纪要这样写" → AI 自动存到 preferences
User says "Write meeting notes this way from now on" → AI saves to preferences automatically
```

**【场景3】踩坑后记教训 / Learn from Mistakes**
```
任务出错被纠正 → 自动记到 causality，下次不再犯
Task fails and gets corrected → Automatically saved to causality, won't repeat
```

**【场景4】项目经验积累 / Project Experience Accumulation**
```
完成一个项目 → 存到 projects，下次遇到类似直接调用
Complete a project → Save to projects, invoke directly for similar tasks next time
```

### Knowledge Manager Use Cases

**【场景1】工具使用技巧 / Tool Usage Tips**
```
学会了一个 Vim 骚操作 → 存到 L1 热数据，随时能查
Learn a cool Vim trick → Save to L1 hot data, available anytime
```

**【场景2】故障排除记录 / Troubleshooting Records**
```
修了一个 bug → 存到知识库，下次遇到同类问题 5 分钟解决
Fix a bug → Save to knowledge base, solve similar issues in 5 minutes next time
```

**【场景3】团队规范沉淀 / Team Norms Documentation**
```
团队定了一个流程 → 存到 L2，新人来了也能看懂
Team sets a process → Save to L2, even newcomers can understand
```

**【场景4】冷知识归档 / Cold Knowledge Archiving**
```
不常用的配置命令 → L3 冷数据，只留索引，需要时再翻出来
Rarely used config commands → L3 cold data, index only, retrieve when needed
```

## Technical Details

- **Language**: JavaScript (Node.js >= 14)
- **Dependencies**: None, pure native implementation
- **Storage**: JSON files, no database required
- **Deployment**: Plug and play, modify `*-store.json` to customize

## Applicable Frameworks

- OpenClaw
- Other Node.js AI Agent frameworks

## License

MIT License - Developed by **hita**
