# nova-memory — Nova 工作空间自研记忆技能

## 元信息

- **name**: nova-memory
- **description**: Nova 工作空间自研记忆技能，提供本地语义记忆存储、检索、实体管理、自动反思能力。纯 Python 实现，无外部 API 依赖，安全可靠。
- **trigger words**: 记忆、remember、recall、实体、entity、反思、reflect、图谱、graph、搜索、search、标签、tag

---

## 功能说明

### 核心能力

| 功能 | 说明 |
|------|------|
| `remember(content, tags, entity)` | 记忆一条信息，自动生成 ID，存储到本地 JSON |
| `recall(query, top_k)` | 语义检索，基于 TF-IDF + Cosine Similarity 返回最相关记忆 |
| `remember_entity(name, facts)` | 记住一个实体的多个属性 |
| `get_entity(name)` | 获取实体完整信息 |
| `search_by_tag(tag)` | 按标签精确搜索记忆 |
| `get_memory_graph()` | 返回记忆图谱（实体关系可视化结构） |
| `auto_reflect()` | 自动反思：基于近期记忆生成洞察摘要 |
| `save()` / `load()` | 持久化保存与加载 |

### 技术方案

- **向量相似度**：TF-IDF + Cosine Similarity（sklearn，纯本地）
- **存储格式**：JSON 文件，每条记忆独立一个 `.json` 文件
- **索引结构**：
  - 倒排索引：`tag → memory_id[]`
  - 向量索引：`memory_id → TF-IDF vector`
- **实体图**：简单 JSON 图结构（`entity_name → {facts}`）
- **存储路径**：`/workspace/memory/nova-memory/`

### 目录结构

```
/workspace/skills/nova-memory/
├── SKILL.md                  # 本文件
├── src/
│   ├── __init__.py          # 模块入口
│   └── memory_core.py       # 核心引擎
└── scripts/
    └── memory_cli.py        # 命令行工具
```

---

## 使用示例

### Python API

```python
from nova_memory import NovaMemory

# 初始化
mem = NovaMemory(storage_dir="/workspace/memory/nova-memory/")

# 记忆一条信息
mid = mem.remember(
    content="Eric 喜欢在周末去重庆大学城附近骑行",
    tags=["eric", "偏好", "运动"],
    entity="Eric"
)

# 语义检索
results = mem.recall("周末运动习惯", top_k=3)
for r in results:
    print(r["content"], "→ 相似度:", round(r["score"], 3))

# 记住实体
mem.remember_entity("Eric", {
    "职业": "投资者",
    "时区": "UTC+8",
    "地点": "重庆"
})

# 获取实体
info = mem.get_entity("Eric")
print(info)

# 按标签搜索
results = mem.search_by_tag("偏好")

# 记忆图谱
graph = mem.get_memory_graph()
print(graph)

# 自动反思
insight = mem.auto_reflect()
print(insight)

# 持久化
mem.save()
```

### CLI 工具

```bash
# 记忆一条信息
python -m nova_memory.scripts.memory_cli remember "Eric 今天讨论了投资组合优化" --tags 投资,组合

# 语义检索
python -m nova_memory.scripts.memory_cli recall "投资策略"

# 实体操作
python -m nova_memory.scripts.memory_cli entity add "Eric" --facts 职业=投资者,地点=重庆
python -m nova_memory.scripts.memory_cli entity get "Eric"

# 标签搜索
python -m nova_memory.scripts.memory_cli tags search "投资"

# 记忆图谱
python -m nova_memory.scripts.memory_cli graph

# 自动反思
python -m nova_memory.scripts.memory_cli reflect
```

---

## OLAP 分析模块（memory_olap.py）

集成 SQLite 本地 OLAP 引擎，支持记忆数据的深度分析：

```python
from nova_memory.memory_olap import MemoryOLAP

olap = MemoryOLAP()

# 生成完整分析报告
print(olap.full_report())

# 每日趋势
print(olap.trend_analysis(30))

# 标签热度
print(olap.tag_analysis(10))

# 实体统计
print(olap.entity_stats())

# 内容熵（多样性评分）
print(olap.content_entropy())
```

---

## 与 Nova 记忆体系的整合

本技能与 Nova 四层记忆体系互补：

| Nova 层级 | 文件 | 本技能可补充 |
|-----------|------|------------|
| 长期 | MEMORY.md | 结构化实体记忆 |
| 项目 | memory/projects.md | 语义搜索相似项目 |
| 日志 | memory/YYYY-MM-DD.md | 语义检索历史事件 |
| 教训 | memory/lessons.md | 按标签回溯教训 |

> `auto_reflect()` 的输出可写入 `MEMORY.md` 或 `memory/lessons.md`，形成闭环。

---

## 安全与限制

- ✅ 纯本地运行，无外部 API 调用，无数据泄露风险
- ✅ 无 `eval()` / `exec()`，无代码注入风险
- ✅ 所有文件存储在 `/workspace/` 目录下
- ⚠️ 大量记忆（>10,000 条）建议定期清理旧记忆文件
