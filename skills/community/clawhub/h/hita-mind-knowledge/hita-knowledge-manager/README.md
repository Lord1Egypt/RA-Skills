# hita Knowledge Manager

三层知识库系统，是 **Hita-Mind & Knowledge** 的一部分。

## 功能 / Features

- **三层分层**：L1热数据 / L2温数据 / L3冷数据
- **自动压缩**：按访问时间自动降级，冷数据只保留索引
- **CLI 工具**：add / search / list / delete / stats / context / compress
- **上下文构建**：为 LLM 生成格式化的知识上下文

## 快速开始 / Quick Start

```bash
cd hita-knowledge-manager

# 添加知识 / Add knowledge
node index.js add "冰箱除异味" "放一杯小苏打在冰箱里，第二天味道就没了" "生活技巧"

# 搜索 / Search
node index.js search 冰箱

# 列出所有 / List all
node index.js list

# 构建上下文 / Build context
node index.js context 10
```

## 三层架构 / 3-Tier Architecture

| 层级 | 容量 | 内容 | 降级条件 |
|------|------|------|---------|
| L1 | 50条 | 完整内容 | 30天未访问 |
| L2 | 200条 | 摘要+标签 | 90天未访问 |
| L3 | 无限制 | 元数据索引 | - |

## 使用场景 / Use Cases

**【场景1】工具使用技巧 / Tool Usage Tips**
```
学会了一个骚操作 → 存到 L1 热数据，随时能查
Learn a cool trick → Save to L1 hot data, available anytime
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

## 配合使用 / Combined Usage

本模块负责"知识"（技巧、方法、规则），
配合 [hita-mind-module](../hita-mind-module/) 负责"记忆"（偏好、决策、教训），
构成 AI 的完整知识体系。

## 依赖 / Dependencies

- Node.js >= 14
- 无其他外部依赖 / No external dependencies

## 关于 / About

由 **hita** 开发，作为 **Hita-Mind & Knowledge** 的一部分。
