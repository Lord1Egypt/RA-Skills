# OpenClaw 记忆架构详解

## 一、双源记忆系统

OpenClaw 采用双源记忆架构，分为动态记忆和静态记忆：

| 类型 | 文件 | 用途 | 特点 |
|------|------|------|------|
| **动态记忆** | `memory/YYYY-MM-DD.md` | 每日日志 | 自动写入，会话细节 |
| **静态记忆** | `MEMORY.md` | 长期知识 | 手动精炼，规则决策 |

### 存储实现

- **Source of Truth**: Markdown 文件
- **索引**: SQLite 全文索引
- **检索**: 向量 + BM25 混合搜索
- **分块**: 400 token 分块，按需检索

---

## 二、记忆生命周期

```
┌─────────────────────────────────────────────────────┐
│  1. 会话开始                                         │
│     └─ 加载 MEMORY.md + today/yesterday logs        │
│                                                      │
│  2. 会话过程                                         │
│     └─ 追加到 daily log (memory/YYYY-MM-DD.md)      │
│                                                      │
│  3. 上下文接近上限                                   │
│     └─ 触发 Pre-Compaction Memory Flush             │
│     └─ Agent 筛选 durable memories 写入文件         │
│                                                      │
│  4. Compaction 压缩                                  │
│     └─ LLM 生成摘要替换旧对话                       │
│                                                      │
│  5. 周期性精炼                                       │
│     └─ 从 daily logs 提取规则到 MEMORY.md           │
└─────────────────────────────────────────────────────┘
```

---

## 三、Memory Flush 详解

### 触发条件

- 上下文接近 `reserveTokensFloor` 阈值
- 距离阈值还有 `softThresholdTokens` 时触发

### 执行过程

```
System Prompt: "Pre-compaction memory flush turn.
The session is near auto-compaction;
capture durable memories to disk."

User Message: "Pre-compaction memory flush.
Store durable memories now (use memory/YYYY-MM-DD.md)"
```

### 配置参数

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "systemPrompt": "...",
          "prompt": "..."
        }
      }
    }
  }
}
```

---

## 四、Compaction 压缩机制

### 问题

模型有上下文窗口限制（Claude 200K tokens），超出时需要压缩。

### 处理方式

1. 用 LLM 对历史对话生成摘要
2. 用摘要替换旧对话
3. **风险**：关键约束可能在压缩中丢失

### 截断策略

超限时按 **70/20/10** 分割：
- 70% 头部保留
- 20% 尾部保留
- 10% 截断标记

> ⚠️ **重要**：MEMORY.md 的**开头和结尾最重要**，中间部分最容易被丢弃！

---

## 五、"失忆"四层含义

| 层级 | 问题 | 解决方案 |
|------|------|---------|
| **Layer 1** | 历史没带进上下文 | 检查 session history 配置 |
| **Layer 2** | Compaction 压缩丢了关键约束 | 启用 memoryFlush |
| **Layer 3** | 关键内容没进入 durable memory | 优化记忆写入策略 |
| **Layer 4** | Tool result 太大挤爆 prompt | 限制工具输出大小 |

---

## 六、Token 消耗优化

### 问题根源

- 默认全量加载：today + yesterday + 长期记忆
- Token 消耗滚雪球式增长
- 无关信息占用大量上下文

### 优化策略

1. **精简 MEMORY.md**：保持在 500 行以内
2. **关键信息前置**：放在文件开头和结尾
3. **定期清理**：归档 30 天以上的 daily logs
4. **按需检索**：安装 qmd 插件增强搜索
5. **降低预留**：适当调整 reserveTokensFloor

---

## 七、记忆检索机制

### 原生搜索

- SQLite FTS5 全文索引
- 关键词匹配，无语义理解
- 对长文本检索效果有限

### 增强搜索（qmd）

三重检索机制：
1. **BM25**: 关键词精确匹配
2. **向量检索**: 语义相似度搜索
3. **重排序**: Cross-encoder 精排

---

## 八、最佳实践总结

### MEMORY.md 维护

- **行数**：控制在 500 行以内
- **结构**：开头放最关键信息
- **更新**：每周精炼一次
- **安全**：永不存储敏感信息

### Daily Logs 维护

- **自动追加**：会话过程自动写入
- **定期精炼**：提取规则到 MEMORY.md
- **归档策略**：30 天以上归档

### 配置优化

```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "reserveTokensFloor": 40000,
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```