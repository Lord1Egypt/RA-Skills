# 工作原理与架构

## 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                    MemoryPalaceManager                       │
│                    (src/manager.ts)                          │
└─────────────────────────────────────────────────────────────┘
         │
         ├──────► FileStorage (src/storage.ts)
         │        - Markdown + YAML frontmatter 格式
         │        - 支持软删除、回收站
         │
         ├──────► VectorSearch (src/background/vector-search.ts)
         │        - 可选：BGE-small-zh-v1.5 向量模型
         │        - 降级：文本关键词匹配
         │
         ├──────► TimeReasoning (src/background/time-reasoning.ts)
         │        - 规则引擎解析时间表达
         │
         ├──────► ConceptExpansion (src/background/concept-expansion.ts)
         │        - 概念映射 + 向量扩展
         │
         └──────► ExperienceManager (src/experience-manager.ts)
                  - 经验记录、验证、检索
```

---

## 存储格式

记忆存储为 Markdown 文件，位于 `{workspaceDir}/memory/palace/`：

```markdown
---
id: "uuid"
tags: ["tag1", "tag2"]
importance: 0.8
status: "active"
createdAt: "2026-03-18T10:00:00Z"
updatedAt: "2026-03-18T10:00:00Z"
source: "conversation"
location: "projects"
type: "fact"
---

记忆内容...

## Summary
可选摘要
```

---

## 遗忘机制（艾宾浩斯曲线）

模拟人类记忆的自然衰减：

**核心参数：**
- `decayScore`：0-1，1=新鲜，0=遗忘
- 初始值：1.0
- 每次访问：`decayScore = min(1, decayScore × 0.9 + 0.2)`
- 归档阈值：`decayScore < 0.1`

**环境变量：**
| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MEMORY_DECAY_ENABLED` | true | 启用衰减 |
| `MEMORY_DECAY_ARCHIVE_THRESHOLD` | 0.1 | 归档阈值 |
| `MEMORY_DECAY_RECOVERY_FACTOR` | 0.2 | 恢复因子 |

---

## 搜索流程

```
1. 用户查询 query
       │
       ▼
2. TimeReasoning 解析时间表达
       │
       ▼
3. ConceptExpansion 扩展概念
       │
       ▼
4. VectorSearch 向量匹配（如果可用）
       │
       ├── 可用 ──► 语义相似度匹配
       │
       └── 不可用 ──► 文本关键词匹配（降级）
              │
              ▼
5. 结合 importance + decayScore 排序
       │
       ▼
6. 返回 topK 结果
```

---

## 经验有效性评分

经验按 `effectivenessScore` 排序：

**计算方式：**
```
effectivenessScore = min(1, verifiedCount × 0.3 + usageCount × 0.1)
```

**验证规则：**
- 需要 2+ 次验证才标记为"已验证"
- 每次验证有效：+0.3
- 每次验证无效：-0.1
- 每次被查询：+0.1

---

## 向量搜索（可选）

**依赖：**
- Python 3.8+
- sentence-transformers
- numpy

**启动方式：**
```bash
pip install sentence-transformers numpy
python scripts/vector-service.py
```

**模型：** BGE-small-zh-v1.5（~100MB，自动下载）

**降级策略：** 向量服务不可用时自动降级到文本搜索

---

## 与 OpenClaw 集成

Memory Palace 通过 `VectorSearchProvider` 接口与 OpenClaw MemoryIndexManager 集成：

```typescript
import { MemoryPalaceManager } from '@openclaw/memory-palace';
import { MemoryIndexManager } from 'openclaw/memory';

// 包装为 VectorSearchProvider
const vectorSearchProvider = {
  search: (query, topK, filter) => memoryManager.search(query, { maxResults: topK }),
  index: (id, content, metadata) => { /* OpenClaw 自动索引 */ },
  remove: (id) => { /* 删除文件即可 */ }
};

const palace = new MemoryPalaceManager({
  workspaceDir: '/workspace',
  vectorSearch: vectorSearchProvider
});
```