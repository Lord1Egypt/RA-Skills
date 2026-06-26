---
name: memory-system
description: 完整的记忆系统 - 文件系统记忆 + 支持搜索 + 自动加载 + 内存刷新
---

# Memory System 🧠

> 完整的记忆系统 - 文件系统记忆 + 支持搜索 + 自动加载 + 内存刷新

## 特性

- 📁 **文件系统存储** - 基于 Markdown 文件，无数据库依赖，可读、可手动编辑、易备份
- 🔍 **支持搜索** - 支持语义搜索（需配置 Ollama）；未配置时自动降级为关键词匹配
- ⚡ **自动加载** - 会话启动时自动加载相关记忆，无需手动触发
- 🏠 **群组隔离** - 支持多群组独立记忆，群组之间数据互不干扰
- 💾 **Memory Flush** - 上下文接近阈值时自动持久化，防止信息丢失
- 🔒 **安全防护** - 路径验证防止目录遍历攻击，确保文件操作仅限于 memoryDir

---

## 安全说明

- 所有文件读写操作都经过路径验证
- 禁止 `../` 目录遍历
- 禁止访问 memoryDir 外的任何文件
- 绝对路径和符号链接都会被解析并验证

---

## 安装

```bash
clawhub install memory-system
```

---

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
| `flushMode` | string | `safeguard` | Flush 触发模式，见下方说明 |
| `softThresholdTokens` | number | `300000` | 触发自动 Flush 的 token 软阈值 |
| `vectorEnabled` | boolean | `false` | 是否启用语义搜索 |
| `embeddingModel` | string | `nomic-embed-text` | Ollama 使用的嵌入模型 |

### flushMode 说明

| 值 | 行为 |
|----|------|
| `safeguard` | 上下文 token 超过 `softThresholdTokens` 时，自动将当前会话记忆持久化到文件，防止丢失（推荐） |
| `manual` | 仅在显式调用 `memory_flush` 时触发持久化 |
| `off` | 禁用 Flush，记忆仅存在于当前会话 |

---

## 工具

### memory_search

语义搜索记忆文件，返回最相关的记忆片段。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | ✅ | 搜索关键词或自然语言描述 |
| `group` | string | ❌ | 限定搜索的群组，不传则搜索全局 |
| `topK` | number | ❌ | 返回结果数量，默认 `5` |

**示例**

```json
{
  "query": "用户上次提到的项目需求",
  "group": "project-a",
  "topK": 3
}
```

> 若 `vectorEnabled` 为 `false` 或 Ollama 不可用，自动降级为关键词全文匹配。

---

### memory_get

读取指定记忆文件的完整内容。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | string | ✅ | 记忆文件路径（相对于 `memoryDir`） |
| `group` | string | ❌ | 群组名称，用于定位文件 |

**示例**

```json
{
  "file": "user-preferences.md",
  "group": "project-a"
}
```

---

### memory_write

写入或追加内容到记忆文件。文件不存在时自动创建。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | string | ✅ | 目标文件路径（相对于 `memoryDir`） |
| `content` | string | ✅ | 写入的 Markdown 内容 |
| `group` | string | ❌ | 群组名称 |
| `mode` | string | ❌ | `overwrite`（覆盖）或 `append`（追加），默认 `append` |

**示例**

```json
{
  "file": "user-preferences.md",
  "content": "## 偏好设置\n- 语言：中文\n- 风格：简洁",
  "group": "project-a",
  "mode": "append"
}
```

---

### memory_flush

手动触发记忆持久化，将当前会话中的记忆写入文件系统。

**参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `group` | string | ❌ | 仅持久化指定群组，不传则持久化全部 |

**示例**

```json
{
  "group": "project-a"
}
```

> 建议在长会话结束前手动调用一次，确保数据不丢失。

---

## 搜索配置（可选）

语义搜索依赖本地 [Ollama](https://ollama.com) 服务，需提前安装并拉取嵌入模型：

```bash
# 安装 Ollama（参考官网）
ollama pull nomic-embed-text
```

确认 Ollama 服务正在运行后，将 `vectorEnabled` 设置为 `true` 即可启用。

**未配置 Ollama 时**：系统自动降级为关键词全文匹配，不影响基本功能使用。

---

## 注意事项

- 同一群组内并发写入时，以最后一次写入为准（last-write-wins），建议避免并发写入同一文件
- `memoryDir` 目录需要有读写权限，首次使用时会自动创建
- 记忆文件为标准 Markdown 格式，可用任意编辑器手动查看和修改

---

**作者**：团宝 (openclaw)  
**版本**：1.0.2
