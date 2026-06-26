---
name: graphify
description: "✏️ 小龙的 Graphify 知识图谱管理工具。使用本地 Llama.cpp (Qwen3.5-9B) 作为推理后端，完全免费，MIT-0 许可。"
owner: 小龙
version: "1.0.0"
homepage: https://clawhub.ai/fantox/graphify
metadata:
  license: MIT-0
  cost: Free
  requires_api_key: false
  llm_provider: "llama.cpp"
  local_model: "qwen3.5-9b-q4_k_m"
  llm_endpoint: "http://127.0.0.1:8080/v1"
---

# 🧠 Graphify - 知识图谱管理工具

## ✏️ 小龙的定制版本 - 本地 Llama.cpp 支持

这是一个将代码库、文档、图片和视频转换为**可查询的知识图谱**的工具，使用本地 Llama.cpp 服务作为推理后端。

### 🌟 核心功能

- **代码库理解** - 将复杂代码库转换为结构化知识图谱
- **架构追踪** - 追踪设计意图和组件关系
- **自然语言查询** - 用自然语言查询代码结构
- **增量更新** - 仅处理变更文件，节省资源
- **交互式可视化** - 生成交互式 HTML 浏览器

### 🖥️ 本地 Llama.cpp 支持

**服务地址**: `http://127.0.0.1:8080/v1`  
**模型**: `Qwen3.5-9B-Q4_K_M`  
**API Key**: `llama-localhost`  
**状态**: ✅ 完全本地运行，无需外部 API

### 🆓 完全免费

- License：MIT-0
- 无版本限制
- 无使用次数限制
- 本地运行，数据安全
- 使用本地 Llama.cpp 模型，无需付费 API

### 🆓 完全免费

- License：MIT-0
- 无版本限制
- 无使用次数限制
- 本地运行，数据安全

### 🚀 小龙的定制版本 - 已安装

**安装位置**: `~/.workbuddy/skills/graphify.py`  
**状态**: ✅ 已安装并配置  
**调用方式**: 直接在 AI 助手中使用 `/graphify` 命令

### 💡 使用方法

#### 首次运行 - 构建知识图谱

```bash
# 解析项目代码库
graphify .
```

执行三步处理管道：

1. **AST 提取** - 使用 tree-sitter 解析代码文件（无需 API key）
2. **转录** - 本地 Whisper 处理视频/音频
3. **语义提取** - 使用配置的 API key 分析文档和代码

#### 增量更新 - 保持图谱最新

```bash
# 仅处理变更文件（推荐）
graphify . --update
```

#### 监听模式 - 文件变化自动同步

```bash
# 文件变化时自动更新图谱
graphify . --watch
```

#### 深度模式 - 增加推断边

```bash
# 深度分析，增加推断的边
graphify . --mode deep
```

### 🔍 查询知识图谱

```bash
# 自然语言语义搜索
graphify query "where is authentication handled?"

# 追踪特定路径（DFS 遍历）
graphify query "how does the request reach the database?" --dfs

# 两个节点间最短路径
graphify path "AuthMiddleware" "PostgresAdapter"

# 解释节点功能
graphify explain "UserSessionManager"
```

### 📊 输出产物

所有产物位于 `graphify-out/` 目录：

| 文件 | 用途 |
|------|------|
| **GRAPH_REPORT.md** | 核心节点、社区结构、意外连接（首先阅读） |
| **graph.html** | 交互式浏览器可视化 |
| **graph.json** | 原始图数据，用于程序化查询 |
| **cache/** | SHA-256 增量缓存 |

### 🌐 支持的格式

**编程语言：** Python, JavaScript, TypeScript, Go, Rust, Java, C++, C#, Kotlin, PHP, Swift, Ruby, R, Julia, Scala, Elixir, Dart, Vue, Svelte, PowerShell

**文档/媒体：** Markdown, HTML, 纯文本，PDF, 图片 (PNG/JPG/WebP/GIF), 视频 (MP4/MOV/MKV), 音频 (MP3/WAV)

### 💰 成本优化

- 使用 `GRAPH_REPORT.md` 比读取原始代码便宜 **71.5 倍**
- SHA-256 缓存机制，`--update` 非常便宜

### 🔐 安全说明

- 代码 AST 提取和语音转写完全本地运行
- 语义提取使用自己的 API key
- 通过 VirusTotal、ClawScan 和静态分析扫描，安全

### ⚠️ 注意事项

- 需要 API key：`ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY` 用于语义提取
- 首次运行需要完整的 API key 配置

### 🛠️ 推荐配置

```bash
# 设置 API key（如果需要使用 LLM）
export ANTHROPIC_API_KEY="your-key"
export OPENAI_API_KEY="your-key"

# 或使用环境变量文件
export GRAPHIFY_API_KEY="your-key"
```

### 📝 小龙的技能使用方式

**在 AI 助手中使用**:
```
/graphify build .           # 构建当前目录的知识图谱
/graphify query "what..."   # 查询知识图谱
```

**直接运行**:
```bash
cd <项目目录>
python ~/.workbuddy/skills/graphify.py build .
python ~/.workbuddy/skills/graphify.py query "what is the structure?"
```

### 📚 相关资源

- [完整官方文档](https://clawhub.ai/fantox/graphify)
- [Graphify 项目](~/.workbuddy/projects/knowledge-graph/)

---

**版本**: 1.0.0  
**所有者**: 小龙  
**状态**: ✅ 已安装为技能，Python 实现位于 `~/.workbuddy/skills/graphify.py`  
**更新时间**: 2026-05-06
