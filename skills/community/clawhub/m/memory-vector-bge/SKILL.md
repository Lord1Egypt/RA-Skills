# memory-vector 技能 v2.1

> 分布式记忆系统，支持知识库 + 向量检索 + 自动蒸馏 + 多层同步

## 🎯 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                      三层记忆架构 (v2.1)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  知识库层 (长期记忆)                                       │  │
│  │  ├── MEMORY.md        - 核心准则/精选记忆                 │  │
│  │  ├── SOUL.md          - 人设定义/性格                     │  │
│  │  ├── USER.md          - 用户信息/习惯/偏好                │  │
│  │  ├── IDENTITY.md      - 身份定义                          │  │
│  │  ├── AGENTS.md        - 智能体配置/行为规则               │  │
│  │  └── TOOLS.md         - 工具配置/API/环境变量              │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↑                                   │
│                      LLM 智能蒸馏同步                            │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  日志层 (中期记忆)                                        │  │
│  │  └── memory/YYYY-MM-DD.md - 每日对话日志                 │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↑                                   │
│                      BGE-M3 向量化                                │
│                              │                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  向量层 (快速检索)                                        │  │
│  │  └── memory/vector/memories.json                        │  │
│  │       - 1024维向量 (BGE-M3)                               │  │
│  │       - 标签 + 重要性权重                                │  │
│  │       - 语义搜索支持                                      │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 📦 功能特性

### v2.1 完整功能

| 功能 | 说明 |
|------|------|
| **三层存储** | 知识库 + 日志 + 向量，各司其职 |
| **多层同步** | LLM 判断写入哪个知识库文件 |
| **自动蒸馏** | 每日/每周自动提取关键信息 |
| **向量搜索** | BGE-M3 语义匹配，支持按标签/重要性筛选 |
| **智能评分** | 综合评分 = 语义×0.7 + 重要性×0.3 |

## 📋 知识库文件说明

| 文件 | 内容 | 蒸馏来源 |
|------|------|----------|
| MEMORY.md | 核心准则、长期记忆 | 重要规则、决策 |
| SOUL.md | 我的人设、性格、说话方式 | 人设调整 |
| USER.md | 您的习惯、偏好、作息 | 用户偏好 |
| IDENTITY.md | 我的身份定义 | 身份信息 |
| AGENTS.md | 智能体配置、行为规则 | 技能配置 |
| TOOLS.md | 工具配置、API、环境变量 | 工具使用习惯 |

## 🔧 环境变量配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `EMBEDDING_URL` | Embedding 服务 | http://localhost:11434/v1/embeddings |
| `EMBEDDING_MODEL` | Embedding 模型 | bge-m3 |
| `EMBEDDING_API_KEY` | API 密钥 | (空) |
| `LLM_URL` | LLM 服务 | http://localhost:11434/v1/chat/completions |
| `LLM_MODEL` | LLM 模型 | qwen2.5:7b |
| `DISTILL_DAYS` | 蒸馏天数 | 7 |

## 📁 文件结构

```
skills/memory-vector/
├── SKILL.md                    # 本文件
├── dist/
│   ├── memory-distill.js       # 蒸馏脚本
│   └── memory-search.js        # 搜索脚本
└── references/
    └── config.json             # 配置文件
```

## 🚀 使用方法

### 1. 蒸馏记忆

```bash
# 蒸馏最近7天
node skills/memory-vector/dist/memory-distill.js

# 蒸馏最近30天
node skills/memory-vector/dist/memory-distill.js 30
```

**蒸馏流程：**
1. 读取 `memory/*.md` 日志文件
2. LLM 分析内容，提取：
   - 关键信息 + 重要性
   - 内容类型（判断写入哪个知识库）
   - 标签
3. 使用 BGE-M3 生成向量
4. 存入 `memory/vector/memories.json`
5. 根据内容类型同步到对应知识库文件

### 2. 搜索记忆

```bash
# 基本搜索
node memory-search.js "搜索内容"

# 按标签筛选
node memory-search.js "内容" --tag 家庭

# 按重要性筛选 (0-1)
node memory-search.js "内容" --min-importance 0.7

# 查看所有标签
node memory-search.js --tags

# 列出所有记忆
node memory-search.js --list
```

### 3. 自动蒸馏 (Heartbeat)

在 `HEARTBEAT.md` 中配置：

```markdown
### 🧠 记忆维护（每3天执行一次）
1. 运行记忆蒸馏：
   - 命令: `node skills/memory-vector/dist/memory-distill.js 7`
   - 功能:
     - 读取近期7天日志
     - LLM 智能分析内容类型
     - BGE-M3 向量化
     - 存入向量数据库
     - 同步到对应知识库文件
```

## 💡 v2.1 核心改进

### 智能判断写入目标

```javascript
// LLM 输出格式 (v2.1)
{
  "targetFile": "USER.md",        // 判断写入哪个文件
  "importance": 0.8,              // 重要性 0-1
  "keyInfo": ["关键信息"],
  "tags": ["家庭", "偏好"],
  "summary": "一句话摘要",
  "action": "append"              // append / overwrite
}
```

### 判断逻辑

| 内容类型 | 目标文件 | 关键词 |
|----------|----------|--------|
| 工具/环境变量 | TOOLS.md | API、工具、配置 |
| 智能体配置 | AGENTS.md | 技能、行为、规则 |
| 我的人设 | SOUL.md | 性格、风格、说话方式 |
| 您的习惯 | USER.md | 偏好、习惯、作息 |
| 身份定义 | IDENTITY.md | 名字、角色、身份 |
| 核心准则 | MEMORY.md | 重要规则、长期记忆 |

## 📊 存储格式

### memories.json (v2.1)

```json
{
  "version": "2.1",
  "updated": "2026-03-23T12:00:00Z",
  "memories": [
    {
      "id": "2026-03-23-xxx",
      "content": "记忆内容...",
      "summary": "一句话摘要",
      "targetFile": "USER.md",       // v2.1 新增
      "tags": ["家庭", "偏好"],
      "importance": 0.8,
      "keyInfo": ["关键点1"],
      "embedding": [0.1, -0.2, ...],
      "source": "2026-03-23.md",
      "created": "2026-03-23T..."
    }
  ],
  "index": {
    "byTag": { "家庭": ["id1"] },
    "byImportance": [{ "id": "id1", "importance": 0.8 }],
    "byTargetFile": { "USER.md": ["id1"], "MEMORY.md": ["id2"] }
  }
}
```

## 🔐 安全机制

- 蒸馏时自动过滤敏感信息（API keys, tokens）
- 不保存完整凭据到知识库
- 知识库文件只保存脱敏后的内容
- 写入前先备份

## ⚠️ 注意事项

1. Ollama 必须保持运行
2. 首次运行需要足够日志才能生成向量
3. 建议每周运行一次蒸馏
4. 写入知识库前会自动备份原文件

## 📈 性能

- 向量维度: 1024 (BGE-M3)
- 搜索速度: <100ms
- 支持标签: 无限
- 知识库文件: 6个

---

*让 AI 真正记住你 - 分布式多层记忆系统 v2.1*