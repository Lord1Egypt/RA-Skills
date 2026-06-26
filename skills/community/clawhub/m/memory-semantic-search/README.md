# memory-semantic-search

对 workspace 中的 Markdown 文件进行语义搜索的独立 Skill。基于 OpenAI 兼容的 Embedding API + SQLite 向量存储，纯 Python stdlib 实现，无额外依赖。

## 工作原理

```
.md 文件 → 切 chunk → Embedding API → 向量存入 SQLite
                                            ↓
用户查询 → Embedding API → 查询向量 → 余弦相似度 → Top-K 结果
```

## 快速开始

### 1. 配置环境变量

```bash
export EMBEDDING_API_KEY="your-api-key"
export EMBEDDING_API_BASE="https://api.openai.com/v1"   # 任何 OpenAI 兼容端点
export EMBEDDING_MODEL="text-embedding-3-small"          # 可选，这是默认值
```

### 2. 建索引

```bash
python3 scripts/index.py /path/to/workspace
```

### 3. 搜索

```bash
python3 scripts/search.py "你的查询"
```

## 命令详情

### index.py — 索引

扫描目录下所有 `.md` 文件，按 ~400 token 切 chunk，调用 Embedding API 获取向量，存入 SQLite。

```bash
python3 scripts/index.py /path/to/workspace [选项]
```

| 选项 | 说明 |
|------|------|
| `--db PATH` | SQLite 数据库路径（默认：skill 目录下 `memory_search.sqlite`） |
| `--api-base URL` | Embedding API 地址 |
| `--api-key KEY` | API Key |
| `--model NAME` | Embedding 模型名 |
| `--force` | 清空已有索引，全量重建 |

支持增量更新：只 embed 新增/修改的 chunk，自动清理已删除文件的索引。

### search.py — 搜索

将查询文本转为向量，与 SQLite 中已存的 chunk 向量计算余弦相似度，返回最相关的结果。

```bash
python3 scripts/search.py "查询内容" [选项]
```

| 选项 | 说明 |
|------|------|
| `--db PATH` | SQLite 数据库路径 |
| `--api-base URL` | Embedding API 地址 |
| `--api-key KEY` | API Key |
| `--model NAME` | Embedding 模型名 |
| `--top-k N` | 返回结果数（默认：5） |
| `--min-score F` | 最低相似度阈值（默认：0.3） |
| `--json` | 以 JSON 格式输出 |

## 环境变量

所有参数均可通过环境变量设置，命令行参数优先级更高：

| 环境变量 | 说明 |
|----------|------|
| `EMBEDDING_API_KEY` | API Key（必填） |
| `EMBEDDING_API_BASE` | API 地址（默认：`https://api.openai.com/v1`） |
| `EMBEDDING_MODEL` | 模型名（默认：`text-embedding-3-small`） |
| `MSS_DB` | SQLite 数据库路径 |
| `MSS_TOP_K` | 搜索返回数量 |
| `MSS_MIN_SCORE` | 最低相似度阈值 |

## 技术细节

- chunk 策略：按行切分，目标 ~400 token/chunk，80 token 重叠
- 向量存储：SQLite + 二进制 blob（`struct.pack` 打包 float 数组）
- 相似度计算：余弦相似度（cosine similarity）
- 增量索引：基于内容 MD5 哈希判断 chunk 是否变更
- 批量 embedding：每批 10 条，避免 API 超时

## 兼容的 Embedding API

任何兼容 OpenAI `/v1/embeddings` 接口的服务均可使用，包括但不限于：

- OpenAI（text-embedding-3-small / text-embedding-3-large）
- 讯飞星火（xop3qwen8bembedding）
- Gemini Embedding
- Ollama
- 各类 OpenAI 兼容代理

## License

MIT
