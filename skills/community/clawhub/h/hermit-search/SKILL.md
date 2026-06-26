---
name: hermit-search
description: 'Local semantic search over knowledge base collections powered by Hermit. Use when: searching knowledge base, semantic search, querying documents, managing collections, adding knowledge base, indexing files.'
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - hermit
        - uv
    os:
      - macos
    homepage: https://github.com/xxxgqcoder/hermit
---

# Skill: hermit-search

Hermit 本地语义搜索服务的使用指南。Hermit 提供基于向量的混合检索（Dense + Sparse）和 Cross-Encoder 精排，支持多知识库管理。

## 平台支持

- **macOS**：已测试通过
- **Linux**：即将支持（短期内增加测试）

## 前置条件

### 安装

```sh
uv tool install git+https://github.com/xxxgqcoder/hermit.git
# 部署 Skill 到 ~/.agents/skills/hermit-search/（可选，使 Agent 自动发现）
hermit install-skills
```

### 模型下载

首次使用前需下载模型（约 1GB）：

```sh
hermit download
```

## 使用流程

### 1. 启动服务

```sh
hermit start
```

输出示例：`{"status": "started", "pid": 12345, "port": 8000}`

### 2. 添加知识库

将一个文件夹注册为知识库 collection：

```sh
hermit kb add <name> <directory> [--ignore <glob>]... [--ignore-ext <ext>]...
```

- `name`：collection 别名（字母数字 + 下划线/连字符，以字母或数字开头）
- `directory`：文件夹路径，Hermit 会递归扫描并索引其中的文本文件
- `--ignore`：glob 模式，匹配的**相对路径**将被忽略（可重复指定多个）
- `--ignore-ext`：文件后缀名，匹配的文件将被忽略（大小写不敏感，可重复指定多个）

示例：

```sh
# 基本用法
hermit kb add my-notes ~/Documents/notes

# 忽略特定路径和后缀
hermit kb add my-project ~/code/project \
  --ignore "build/**" \
  --ignore "*.tmp" \
  --ignore "node_modules/*" \
  --ignore-ext .pdf \
  --ignore-ext .png
```

### 3. 更新知识库忽略规则

修改已有知识库的忽略配置（替换模式，非追加）：

```sh
hermit kb update <name> [--ignore <glob>]... [--ignore-ext <ext>]... [--clear-ignore] [--clear-ignore-ext]
```

- `--ignore`：设置新的路径忽略 glob 模式（替换已有配置）
- `--ignore-ext`：设置新的后缀忽略规则（替换已有配置）
- `--clear-ignore`：清除所有路径忽略模式
- `--clear-ignore-ext`：清除所有后缀忽略规则

示例：

```sh
# 更新忽略模式
hermit kb update my-project --ignore "dist/**" --ignore "*.log"

# 清除所有忽略规则
hermit kb update my-project --clear-ignore --clear-ignore-ext
```

### 4. 语义搜索

```sh
hermit search <collection> "<query>"
```

参数：

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `collection` | str | — | Collection 名称 |
| `query` | str | — | 搜索查询 |
| `--top-k` | int | 5 | 返回结果数 |
| `--rerank-candidates` | int | 50 | 精排候选池大小 |

示例：

```sh
hermit search my-notes "如何实现二分查找"
```

### 5. 其他管理命令

```sh
# 查看所有知识库
hermit kb list

# 删除知识库
hermit kb remove <name>

# 触发同步（需要服务运行中）
hermit collection sync <name>

# 查看索引状态
hermit collection status <name>

# 查看索引任务队列
hermit collection tasks <name>
```

### 6. 服务生命周期

```sh
hermit status    # 查看服务状态
hermit stop      # 停止服务
hermit logs      # 查看日志（流式输出）
```

## 输出格式

所有命令输出 JSON。添加 `--pretty` 获取格式化输出：

```sh
hermit --pretty search my-notes "query"
```

错误输出格式：`{"error": "message"}`

## 忽略规则说明

- 路径模式（`--ignore`）使用 glob 语法（与 `.gitignore` 类似），匹配相对于知识库根目录的路径
  - `*.log` — 忽略根目录下所有 `.log` 文件
  - `build/**` — 忽略 `build/` 目录下所有文件
  - `**/temp/*` — 忽略任意层级下的 `temp/` 目录内容
- 后缀模式（`--ignore-ext`）大小写不敏感：`.PDF` 和 `.pdf` 等价
- 隐藏文件（以 `.` 开头的目录或文件）始终被忽略，无需额外配置
- `hermit kb list` 可查看每个知识库当前的忽略配置

## 技术细节

- **Embedding 模型**：jinaai/jina-embeddings-v2-base-zh（768 维）
- **Sparse 模型**：Qdrant/bm25
- **Reranker**：jinaai/jina-reranker-v2-base-multilingual
- **向量数据库**：Qdrant（嵌入式模式）
- **推理后端**：fastembed（ONNX Runtime，纯 CPU）
- **数据目录**：`~/.hermit/`（可通过 `HERMIT_HOME` 环境变量覆盖）
