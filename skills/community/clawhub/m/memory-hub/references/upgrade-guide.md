# 升级指南：从 Markdown 到向量检索

## 何时升级

单个文件超过 200 行，或加载缓存时 token 消耗明显增大时考虑升级。

## 升级路径

### 阶段二：SQLite FTS5（无额外依赖）

适合：记忆条数 200-2000 条，仍希望零依赖。

```bash
# 将 Markdown 导入 SQLite
python3 scripts/migrate_to_sqlite.py ~/.openclaw/shared-memory/

# 检索
python3 scripts/search_sqlite.py "关键词"
```

SQLite 文件可以直接加入 git 仓库同步，单文件，跨平台。

### 阶段三：Qdrant + 本地 Ollama（完全离线向量检索）

适合：记忆条数 2000+，需要语义检索（"喜欢简洁"能搜到"不喜欢废话"）。

**部署 Qdrant（Docker）：**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**部署 Ollama embedding 模型：**
```bash
ollama pull nomic-embed-text
```

**迁移数据：**
```bash
python3 scripts/migrate_to_qdrant.py ~/.openclaw/shared-memory/
```

**检索：**
```bash
python3 scripts/search_qdrant.py "关键词或语义描述"
```

## 数据格式保障

当前 Markdown 格式（每条独立段落）可直接用于 embedding，无需重新整理。
迁移脚本按 `## ` 标题分割段落，每段作为一个向量单元。

## 重要原则

**数据始终在你手里**：无论哪个阶段，原始 Markdown 文件保留在 git 仓库，向量/SQLite 是索引层，随时可以重建，不依赖任何外部服务。
