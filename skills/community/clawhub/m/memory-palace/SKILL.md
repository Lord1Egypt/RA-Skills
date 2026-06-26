---
name: memory-palace
description: |
  持久化记忆管理。Use when: 用户告诉你个人信息/偏好/习惯、需要记住项目状态/技术决策、完成任务后有可复用经验、用户说"记住""别忘了""下次注意"、需要回忆之前的对话内容。支持语义搜索和时间推理。
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["node"]
    install:
      - id: "node-memory-palace"
        kind: "node"
        package: "memory-palace"
        bins: ["memory-palace"]
        label: "Install Memory Palace CLI (npm)"
---

# Memory Palace

Agent 的持久化记忆系统。让 AI Agent 能够**记住**用户偏好、对话上下文、项目状态、经验教训，并在需要时**主动检索**。

## 可选：语义搜索增强

语义搜索需要 Python 环境和向量模型（~100MB，首次使用自动下载）：

```bash
# 检查 Python 环境
python3 --version  # 需要 3.8+

# 安装依赖
pip install sentence-transformers

# 首次搜索时自动下载模型到 ~/.openclaw/models/embedding/
# 模型：BAAI/bge-small-zh-v1.5
```

> **无 Python 环境时**：系统自动降级为文本搜索，功能正常使用。

## 何时使用

✅ **Use when**:
- 用户告诉你个人信息、偏好、习惯
- 需要记录项目状态、技术决策
- 完成任务后积累了可复用经验
- 需要回忆之前的对话内容
- 用户提到"记住""别忘了""下次注意"

❌ **Do NOT use**:
- 临时性的单次查询（直接回答即可）
- 不需要持久化的即时计算
- 已经有明确文档记录的信息

---

## 快速开始

```json
// 记住用户信息
memory_palace_write: { "content": "用户叫盘古，喜欢简洁回复", "tags": ["用户", "偏好"], "importance": 0.9 }

// 搜索记忆
memory_palace_search: { "query": "用户名字" }

// 记录经验
memory_palace_record_experience: { "content": "API 用名词命名端点", "category": "development", "applicability": "设计新 API", "source": "task-001" }
```

---

## 核心工具

### 基础操作

| 工具 | 功能 | 必填参数 |
|------|------|---------|
| `memory_palace_write` | 写入记忆 | `content` |
| `memory_palace_search` | 搜索记忆 | `query` |
| `memory_palace_get` | 获取记忆 | `id` |
| `memory_palace_update` | 更新记忆 | `id` |
| `memory_palace_delete` | 删除记忆 | `id` |
| `memory_palace_list` | 列出记忆 | — |
| `memory_palace_stats` | 统计信息 | — |

### 经验管理

| 工具 | 功能 | 必填参数 |
|------|------|---------|
| `memory_palace_record_experience` | 记录经验 | `content`, `applicability`, `source` |
| `memory_palace_get_experiences` | 查询经验 | — |
| `memory_palace_verify_experience` | 验证经验 | `id`, `effective` |
| `memory_palace_get_relevant_experiences` | 相关经验 | `context` |

### LLM 增强

| 工具 | 功能 | 必填参数 |
|------|------|---------|
| `memory_palace_summarize` | 智能总结 | `id` |
| `memory_palace_parse_time` | 解析时间 | `expression` |
| `memory_palace_expand_concepts` | 扩展概念 | `query` |

---

## 参数速查

### write 参数

```json
{
  "content": "记忆内容",       // 必填
  "tags": ["标签"],           // 可选，分类检索
  "importance": 0.7,          // 可选，0-1，重要记忆建议 0.7+
  "location": "default",      // 可选，存储位置
  "type": "fact"              // 可选：fact/experience/lesson/preference/decision
}
```

### search 参数

```json
{
  "query": "搜索词",          // 必填，支持自然语言
  "tags": ["标签"],           // 可选，过滤标签
  "topK": 10                  // 可选，返回数量
}
```

### record_experience 参数

```json
{
  "content": "经验内容",       // 必填
  "applicability": "适用场景", // 必填
  "source": "来源标识",        // 必填
  "category": "development"   // 可选：development/operations/product/communication/general
}
```

---

## 经验有效性机制

经验按 `effectivenessScore`（0-1）排序：

| 操作 | 分数变化 |
|------|---------|
| 新建经验 | 初始 0.1 |
| 查询使用 | +0.1 |
| 验证有效 | +0.3 |
| 验证无效 | -0.1 |

**验证规则**：需 2+ 次验证才标记为"已验证"

---

## 详细文档

- [完整参数说明](references/api-reference.md)
- [使用场景示例](references/usage-examples.md)
- [工作原理与架构](references/architecture.md)