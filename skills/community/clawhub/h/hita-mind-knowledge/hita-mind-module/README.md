# hita Mind Module

AI 个人记忆系统，是 **Hita-Mind & Knowledge** 的一部分。

## 功能 / Features

- **8大分类**：decisions / preferences / patterns / causality / contacts / feedback / projects / daily
- **JSON 存储**：结构化数据，便于备份和迁移
- **CLI 工具**：list / search / stats / context / add / delete / update
- **上下文构建**：适合塞进 LLM context 的格式

## 快速开始 / Quick Start

```bash
cd hita-mind-module

# 列出所有分类 / List all categories
node index.js list

# 搜索记忆 / Search memory
node index.js search 开会

# 添加记忆 / Add memory
node index.js add preferences "叫用户" "叫老板，说话轻松一点"

# 构建上下文 / Build context
node index.js context patterns 5
```

## 使用场景 / Use Cases

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

## 配合使用 / Combined Usage

本模块负责"记忆"（偏好、决策、教训），
配合 [hita-knowledge-manager](../hita-knowledge-manager/) 负责"知识"（技巧、方法、规则），
构成 AI 的完整知识体系。

## 依赖 / Dependencies

- Node.js >= 14
- 无其他外部依赖 / No external dependencies

## 关于 / About

由 **hita** 开发，作为 **Hita-Mind & Knowledge** 的一部分。
