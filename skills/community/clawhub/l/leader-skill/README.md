# create-leader - 领导.skill 创建器 | Leader Skill Creator

Create a Leader AI Skill with Leadership Simulation, Upward Management, and Replacement Path Planning. 一个用于创建领导AI技能的OpenClaw skill，支持领导力模拟、向上管理、取代路径规划，帮助你理解领导、搞定老板、规划职业发展。

## 语言 / Language

本 Skill 支持中英文。根据用户第一条消息的语言，全程使用同一语言回复。

This skill supports both English and Chinese. Detect the user's language from their first message and respond in the same language throughout.

---

## 核心功能 (Chinese)

### Track 1：领导力模拟
- "如果是这位领导，他会怎么决策？"
- "这位领导在这个场景下会说什么？"

### Track 2：向上管理辅助
- "我该怎么向这位领导汇报？"
- "这个方案怎么说服这位领导？"

### Track 3：取代路径规划（核心差异化）
- "我该怎么取代这个领导？"
- "这位领导的软肋是什么？"
- "我需要具备什么能力才能坐上这个位置？"

---

## Core Features (English)

### Track 1: Leadership Simulation
- "If this leader were here, how would he decide?"
- "What would this leader say in this scenario?"

### Track 2: Upward Management Assistance
- "How should I report to this leader?"
- "How to convince this leader of this proposal?"

### Track 3: Replacement Path Planning (Core Differentiator)
- "How can I replace this leader?"
- "What are this leader's weaknesses?"
- "What capabilities do I need to take this position?"

---

## 目录结构 (Directory Structure)

```
create-leader/
├── SKILL.md (主文件 / Main file)
├── README.md (本文件 / This file)
├── _meta.json (Skill元数据 / Skill metadata)
├── examples/
│   └── EXAMPLE.md (使用示例 / Usage examples)
├── prompts/
│   ├── intake.md (基础信息录入 / Basic info collection)
│   ├── leadership_analyzer.md (领导力模拟分析 / Leadership simulation analysis)
│   ├── upward_analyzer.md (向上管理分析 / Upward management analysis)
│   ├── replacement_analyzer.md (取代路径规划分析 / Replacement path planning analysis)
│   ├── feishu_private_chat.md (飞书私聊采集 / Feishu private chat collection)
│   ├── merger.md (增量内容合并 / Incremental content merging)
│   ├── correction_handler.md (对话纠正处理 / Conversation correction handling)
│   ├── work_builder.md (领导能力生成 / Leadership content builder)
│   └── persona_builder.md (人物性格生成 / Persona content builder)
└── tools/
    ├── skill_writer.py (Skill文件写入 / Skill file writer)
    ├── version_manager.py (版本管理 / Version manager)
    └── feishu_auto_collector.py (飞书自动采集 / Feishu auto collector)
```

---

## 使用方式 (Usage)

1. `/create-leader` - 创建新的领导skill / Create a new leader skill
2. `/list-leaders` - 列出所有已生成的领导 / List all generated leaders
3. `/{slug}` - 使用完整的领导skill（包含三个模块）/ Use full leader skill (all three modules)
4. `/{slug}-leadership` - 仅使用领导力模拟 / Leadership simulation only
5. `/{slug}-upward` - 仅使用向上管理 / Upward management only
6. `/{slug}-replacement` - 仅使用取代路径规划 / Replacement path planning only

---

## 设计亮点 (Design Highlights)

- **三轨结构**：Leadership（领导力）+ Upward（向上管理）+ Replacement（取代路径）
- **核心差异化**："取代路径规划"是这个skill的爆款功能
- **数据采集**：支持飞书/钉钉自动采集
- **持续进化**：支持追加文件 + 对话纠正 + 版本管理
- **中英文双语**：根据用户语言自动切换
- **伦理提醒**：明确提示仅用于个人成长参考

- **Three-track structure**: Leadership + Upward Management + Replacement Path Planning
- **Core differentiator**: "Replacement Path Planning" is this skill's standout feature
- **Data collection**: Supports Feishu/DingTalk auto-collection
- **Continuous evolution**: Supports file appending + conversation correction + version management
- **Bilingual support**: Auto-switches based on user language
- **Ethical reminder**: Clear guidance for personal growth only

---

## 待完善 (To-Do)

- `tools/` 目录下的Python脚本（数据采集、版本管理等）
- `prompts/` 目录下的其他文件（merger.md、correction_handler.md等）
- `assets/` 目录下的模板文件

- Python scripts in `tools/` directory (data collection, version management, etc.)
- Other files in `prompts/` directory (merger.md, correction_handler.md, etc.)
- Template files in `assets/` directory
