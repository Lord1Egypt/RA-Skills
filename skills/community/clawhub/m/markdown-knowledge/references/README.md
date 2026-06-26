# Markdown Knowledge Base for OpenClaw

将您的本地 Markdown 知识库与 OpenClaw 无缝集成，让 AI 助手能够基于您的专业知识回答问题。

---

## 功能特性

- **🔍 智能检索**：基于关键词和语义的混合搜索
- **📦 即装即用**：一键安装，自动配置
- **🔄 实时同步**：支持定时自动更新索引
- **💡 上下文注入**：自动将相关知识注入 AI 对话
- **🏃 轻量高效**：专为资源受限环境优化（树莓派友好）
- **🌐 跨平台**：支持树莓派、Linux、macOS、Windows

---

## 安装

```bash
# 使用 ClawHub 安装（推荐）
clawhub install markdown-knowledge

# 或手动安装
git clone https://github.com/your-repo/markdown-knowledge.git
cd markdown-knowledge
cp -r . ~/.openclaw/workspace/skills/markdown-knowledge
```

---

## 快速开始

### 1. 配置知识库路径

编辑 `~/.openclaw/workspace/skills/markdown-knowledge/config.json`：

```json
{
    "knowledge_path": "~/Knowledge",
    "index_path": "~/.openclaw/workspace/skills/markdown-knowledge/index.json",
    "search_top_k": 3,
    "auto_refresh": true
}
```

### 2. 将 Markdown 文件放入 `~/Knowledge`

目录结构示例：
```
~/Knowledge/
├── 编程技术/
│   ├── Python/
│   │   └── 基础语法.md
│   └── JavaScript/
├── 业务知识/
│   └── 产品设计.md
└── 个人成长/
    └── 学习笔记.md
```

### 3. 构建索引

```bash
python3 knowledge_base.py build
```

---

## 使用方法

### 命令行工具

```bash
# 构建或更新索引
python3 knowledge_base.py build

# 搜索知识库
python3 knowledge_base.py search "你的问题"

# 查看统计信息
python3 knowledge_base.py stats
```

### OpenClaw 对话触发

用户可以直接说以下命令：

| 命令 | 触发动作 |
|------|----------|
| "刷新知识库索引" | rebuild |
| "更新知识库" | rebuild |
| "知识库统计" | stats |

---

## AI 使用指南

当用户提问时，AI 应：

1. **立即搜索**：收到问题后调用 search 动作检索知识库
2. **搜到结果**：将相关文档片段注入上下文，告诉用户"根据知识库..."
3. **搜不到**：明确告知"知识库中没有找到相关信息"

### 文档格式建议

为获得最佳检索效果，文档建议包含以下头部：

```markdown
---
title: 文档标题
keywords: 关键词1, 关键词2
tags: [标签1, 标签2]
created: 2024-01-15
---

# 文档标题

正文内容...
```

---

## 工作原理

```
用户提问 → OpenClaw → 知识检索 → 上下文注入 → AI 回答
```

1. 文档解析：扫描 Markdown 文件，提取元数据和内容块
2. 索引构建：生成 JSON 索引文件
3. 语义匹配：根据查询词计算文档相关性分数
4. 上下文注入：将相关文档片段注入 AI 对话

---

## 系统要求

- Python 3.8+
- OpenClaw 1.0+
- 本地 Markdown 文档目录

---

## 支持平台

- ✅ 树莓派
- ✅ Linux
- ✅ macOS
- ✅ Windows

---

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `knowledge_path` | string | `~/Knowledge` | Markdown 文档目录 |
| `index_path` | string | `~/.openclaw/workspace/skills/markdown-knowledge/index.json` | 索引文件路径 |
| `search_top_k` | number | `3` | 返回结果数量 |
| `auto_refresh` | boolean | `true` | 自动刷新索引 |

---

## 常见问题

**Q: 安装后没有自动初始化？**

```bash
python3 knowledge_base.py build
```

**Q: 索引构建失败？**

检查知识库路径配置是否正确，确保目录存在且包含 Markdown 文件。

**Q: 树莓派上运行内存不足？**

减少 `search_top_k` 值，或使用增量更新。

---

## 许可证

MIT License
