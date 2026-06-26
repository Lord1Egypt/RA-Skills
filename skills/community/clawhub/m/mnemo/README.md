# Memory System 🧠

> 完整记忆系统 - 文件系统记忆 + 向量搜索 + 自动加载 + Memory Flush

## 特性

- 📁 **文件系统存储** - 基于 Markdown 文件，无数据库依赖
- 🔍 **向量搜索** - 支持语义搜索（需配置 Ollama）
- ⚡ **自动加载** - 会话启动时自动加载相关记忆
- 🏠 **群组隔离** - 支持多群组独立记忆
- 💾 **Memory Flush** - 上下文满了自动持久化

## 安装

```bash
# 1. 克隆或下载此 Skill
# 2. 放入你的 skills 目录
cp -r memory-system-skill ~/.openclaw/workspace/skills/

# 3. 重启 Gateway
openclaw gateway restart
```

## 配置

在 `openclaw.json` 中配置：

```json
{
  "skills": {
    "memory-system": {
      "memoryDir": "~/.openclaw/workspace/memory",
      "flushMode": "safeguard",
      "softThresholdTokens": 300000,
      "vectorEnabled": true,
      "embeddingModel": "nomic-embed-text"
    }
  }
}
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `memoryDir` | string | `~/.openclaw/workspace/memory` | 记忆文件存储目录 |
| `flushMode` | string | `safeguard` | flush 模式：`safeguard` / `manual` / `disabled` |
| `softThresholdTokens` | number | 300000 | 触发 flush 的 token 阈值 |
| `vectorEnabled` | boolean | true | 是否启用向量搜索 |
| `embeddingModel` | string | `nomic-embed-text` | 向量嵌入模型 |

### 可选：安装 Ollama（向量搜索）

```bash
# macOS
brew install ollama

# 启动 Ollama
ollama serve

# 拉取嵌入模型
ollama pull nomic-embed-text
```

## 文件结构

```
memory/
├── MEMORY.md              # 长期记忆（核心知识）
├── memory/
│   ├── 2026-03-17.md     # 每日对话记录
│   ├── 2026-03-16.md     # 历史记录
│   └── groups/           # 群组记忆
│       ├── {group-id}/
│       │   └── MEMORY.md
│       └── ...
└── vectors/              # 向量索引（可选）
```

## 工具

### memory_search

语义搜索记忆。

```json
{
  "query": "用户 偏好 模型",
  "topK": 5,
  "group": "optional-group-id"
}
```

### memory_get

读取记忆文件。

```json
{
  "path": "MEMORY.md",
  "from": 1,
  "lines": 20
}
```

### memory_write

写入记忆文件。

```json
{
  "path": "memory/2026-03-17.md",
  "content": "今天用户提到...",
  "mode": "append"
}
```

### memory_flush

手动触发 flush。

```json
{
  "force": true
}
```

## 自动加载规则

| 会话类型 | 自动加载 |
|----------|----------|
| 直接对话 | `MEMORY.md` + 当天日记 + 昨天日记 |
| 群组对话 | `MEMORY.md` + 当天日记 + 群组记忆 |

## Flush 机制

- **safeguard**（默认）：当 token 达到阈值时自动 flush
- **manual**：仅手动触发
- **disabled**：禁用 flush

## 使用示例

### 搜索记忆

```
用户: 查一下我上次说什么模型？
AI: memory_search("模型 偏好")
→ 返回相关记忆片段
```

### 记录新信息

```
用户: 我喜欢 Claude 模型
AI: memory_write("MEMORY.md", "## 用户偏好\n- 喜欢: Claude 模型", "append")
→ 已记录
```

### 手动保存

```
AI: 上下文快满了
→ memory_flush({force: true})
→ 内存已保存到文件
```

## 依赖

- Node.js 18+
- Ollama 0.3.0+（可选，向量搜索需要）

---

**作者**: 团宝 (openclaw)  
**版本**: 1.0.0  
**许可**: MIT
