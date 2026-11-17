---
name: ontology-knowledge-graph-mgmt
slug: ontology-knowledge-graph-mgmt
displayName: 知识图谱管理
description: 知识图谱的补录、同步、修复、搜索全流程。包括graph.jsonl格式校验→SQLite同步→向量搜索集成→可选向量库接入。
priority: medium
source: auto-evolved-worker
workers: [tech, ops]
created: 2026-04-23
updated: 2026-07-06
version: 2.0.1
category: knowledge-management
tags: [knowledge-graph, ontology, sqlite, vector-search]
---

> ⚠️ **外部依赖声明**：本 Skill 引用的 `scripts/graph_sync.py`、`scripts/graph_vectorize.py`、`scripts/graph_search.py` 不包含在本目录中。
> 它们是与知识图谱绑定的独立 Python 工具集，需从项目仓库单独获取，或根据本 Skill 描述的接口自行实现。


# 知识图谱管理与补录

> 知识图谱全生命周期管理：补录、同步、修复、搜索

## 何时使用

知识图谱的补录、同步、修复、搜索全流程。

**触发场景：**
- 需要补录新的实体/关系/文档
- 图谱数据需要同步到 SQLite
- 需要集成向量搜索能力
- 图谱数据异常需要修复

## 执行步骤

### Step 1: 读取原始图谱数据

```bash
# 读取 graph.jsonl
cat graph.jsonl | head -20
```

### Step 2: 校验格式

```bash
# 检查 JSON 格式是否正确
python3 -c "
import json
with open('graph.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f'Line {i}: {e}')
"
```

**常见问题：**
- Line N: 双 JSON 粘连 → 拆分为两行
- Line N: JSON 格式错误 → 修复引号/括号

### Step 3: 补录实体/关系/文档

**实体补录格式：**
```json
{"type": "entity", "id": "task_001", "name": "任务名称", "attributes": {"status": "active"}}
```

**关系补录格式：**
```json
{"type": "relation", "source": "agent_001", "target": "task_001", "relation": "assigned_to"}
```

**文档补录格式：**
```json
{"type": "document", "id": "doc_001", "content": "文档内容", "metadata": {"source": "manual"}}
```

### Step 4: 同步到 SQLite

```bash
# 同步图谱数据到 SQLite
python3 scripts/graph_sync.py --sync
```

**同步检查项：**
- 实体数量是否一致
- 关系数量是否一致
- 无孤立节点（可选）

### Step 5: 集成向量搜索

```bash
# 为图谱内容生成向量索引
python3 scripts/graph_vectorize.py --index
```

**向量搜索测试：**
```bash
python3 scripts/graph_search.py "查询内容" --top 5
```

### Step 6: 可选向量库接入

如需持久化向量索引，可接入向量数据库：

| 后端 | 适用场景 | 配置方式 |
|------|----------|----------|
| ChromaDB | 本地部署、小规模 | `VECTOR_DB=chroma` |
| Pinecone | 云端、大规模 | `VECTOR_DB=pinecone` |
| Weaviate | 云端/本地 | `VECTOR_DB=weaviate` |

默认使用 SQLite + 内存向量，无需额外配置。

### Step 7: 定时更新索引

```bash
# 添加 cron 定时任务（可选）
# 每天凌晨 2:00 更新向量索引
0 2 * * * cd /path/to/project && python3 scripts/graph_vectorize.py --update
```

## 注意事项

- 执行前确认当前系统状态，避免在已有操作进行中执行
- 如遇到未预料的问题，先记录到当日 memory 文件
- 配置类操作必须先备份再修改
- 完成后验证端到端功能是否正常

## 版本历史

| 日期 | 版本 | 变更说明 |
|------|------|----------|
| 2026-04-23 | 1.0 | 初始版本 |
| 2026-07-04 | 2.0 | 通用化改造：去除 ChromaDB 硬依赖，支持可选向量库后端 |
