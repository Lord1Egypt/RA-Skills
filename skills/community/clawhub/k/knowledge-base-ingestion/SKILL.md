---
name: knowledge-base-ingestion
slug: knowledge-base-ingestion
displayName: 知识库灌入
description: 将外部知识库（文档/笔记/共享文件等）提取内容并灌入向量数据库的标准流程。支持 ChromaDB、Pinecone、Weaviate 等多种向量库后端。包括预扫描目录、识别并排除无效文件、执行分批灌入、验证索引质量、失败恢复。
priority: medium
source: auto-evolved
workers: [tech, ops]
created: 2026-04-23
updated: 2026-07-06
version: 3.0.1
category: data-pipeline
tags: [knowledge-base, vector-search, ingestion, vector-database]
---

> ⚠️ **外部依赖声明**：本 Skill 的核心脚本 `scripts/knowledge-ingest.py` 不包含在本目录中。
> 它是一个独立的 Python 工具，需从项目仓库单独获取或根据本 Skill 描述的接口自行实现。
> 默认向量库后端为 ChromaDB，如需 Pinecone/Weaviate 等，设置环境变量 `VECTOR_DB`。


# 知识库提取与向量索引灌入

> 通用知识库灌入流程，支持多种向量数据库后端

## 何时使用

将外部知识库（文档/笔记/共享文件等）的内容灌入向量数据库。

**触发场景：**
- 用户要求"把新文档灌入向量库"或"同步知识库"
- Cron 定时任务触发
- 新增知识库目录后首次灌入
- 灌入后检索质量下降，需要重建索引

**不使用的场景：**
- 仅需查询已有知识 → 使用对应的搜索工具
- 少量文件手动添加 → 使用针对单客户的灌入命令

## 快速流程图

```
预扫描 → 统计文件分布 → ⚠️ 识别无效文件 → 更新排除规则
  ↓
Checkpoint #1：向用户确认灌入范围
  ↓
执行灌入（分批处理，每批 ≤500 文件）
  ↓
Checkpoint #2：验证索引 → 检查数量和维度
  ↓
测试语义检索 → 抽查 3 条典型查询
  ↓
记录结果到当日 memory
```

## 支持的向量数据库后端

| 后端 | 适用场景 | 配置方式 |
|------|----------|----------|
| ChromaDB | 本地部署、小规模（<100K docs） | `VECTOR_DB=chroma` |
| Pinecone | 云端、大规模、生产环境 | `VECTOR_DB=pinecone` + API Key |
| Weaviate | 云端/本地、中等规模 | `VECTOR_DB=weaviate` + endpoint |
| Qdrant | 本地/云端、高性能 | `VECTOR_DB=qdrant` + endpoint |
| Milvus | 大规模、分布式 | `VECTOR_DB=milvus` + endpoint |

默认使用 ChromaDB（本地免费），可通过环境变量切换。

## 核心资源

| 资源 | 说明 |
|------|------|
| 灌入脚本 | `scripts/knowledge-ingest.py` — 主灌入脚本，支持分批/指定客户/状态恢复 |
| 知识库源目录 | 通过 `KB_DIR` 环境变量指定 |
| 向量库存储 | 根据 `VECTOR_DB` 配置自动选择 |
| 灌入状态文件 | 记录进度、错误、统计 |

## 执行步骤

### Step 1: 预扫描目录

**目标：** 了解文件分布，识别并排除无效文件。

```bash
# 1. 统计文件数量和类型分布
find $KB_DIR -type f | wc -l
find $KB_DIR -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# 2. 检查是否有超大文件（>1MB，可能灌入失败）
find $KB_DIR -type f -size +1M -name "*.md"

# 3. 查看目录结构
ls -la $KB_DIR
```

**无效文件识别规则（自动排除）：**

| 文件类型 | 排除规则 | 原因 |
|----------|----------|------|
| 代码文件 | `.js, .ts, .py, .java, .go, .css, .html` | 无语义价值，污染检索结果 |
| 二进制文件 | `.pdf, .docx, .xlsx, .png, .zip` | 无法直接读取文本 |
| 系统文件 | `.DS_Store, .git, .svn, Thumbs.db` | 系统垃圾 |
| 构建产物 | `node_modules/, dist/, build/, __pycache__/` | 自动生成，无需灌入 |
| 空/过短文件 | 文本 < 100 字符 | 内容不足，无索引价值 |

### Step 2: 更新排除规则

根据预扫描结果，如发现新的无效目录，更新脚本的排除规则。

### Checkpoint #1: 用户确认灌入范围 ⚠️

**在执行灌入前，向用户报告并确认：**

```
📊 预扫描结果：
- 总文件数：X 个
- 有效文件：Y 个（.md 文本）
- 排除文件：Z 个（代码/二进制/系统）
- 向量库当前索引：M chunks
- 向量库后端：{VECTOR_DB}

请确认：是否开始灌入有效文件？(y/n)
```

- 用户确认后才执行 Step 3
- 如果文件量异常（>5000 新增），先分批确认

### Step 3: 执行灌入（分批处理）

**目标：** 将有效文件分批灌入向量数据库，每批 ≤500 文件。

```bash
# 方式 A：自动下一批（推荐，从断点续跑）
python3 scripts/knowledge-ingest.py

# 方式 B：指定单个客户（调试或重跑）
python3 scripts/knowledge-ingest.py --client <客户名>

# 方式 C：查看当前状态
python3 scripts/knowledge-ingest.py --status

# 方式 D：重置进度（从头重跑，慎用！）
python3 scripts/knowledge-ingest.py --reset
```

**灌入脚本行为说明：**
- 自动从状态文件恢复进度，断点续跑
- 大文件（>4000 字符）自动按段落分割为 chunks，每 chunk ≤8000 字符
- 去重：基于文件路径 MD5 前 16 位，已存在的文件自动跳过
- 每批处理完自动保存状态

### Step 4: 验证索引质量

**目标：** 确保灌入结果正确，索引数量和数据完整。

```bash
# 1. 查看灌入状态和向量库统计
python3 scripts/knowledge-ingest.py --status
```

**验证检查清单：**

| 检查项 | 通过标准 | 失败处理 |
|--------|----------|----------|
| 索引数量 | chunks > 0 | → 见「失败恢复流程」 |
| 向量维度 | 每个 chunk 有 embedding | → 见「失败恢复流程」 |
| 错误率 | errors 数组长度 < 总文件数的 5% | 超过阈值 → 检查具体错误，修复后重跑 |
| 客户覆盖 | 所有客户目录都有对应集合 | 缺少 → 手动指定客户重跑 |

### Step 5: 测试语义检索准确性

**目标：** 端到端验证检索质量。

```bash
# 使用搜索脚本做语义检索测试（选取 3 条典型查询）
python3 scripts/kg_search.py "你的测试查询1" --top 5
python3 scripts/kg_search.py "你的测试查询2" --top 5
python3 scripts/kg_search.py "你的测试查询3" --top 5
```

**检索质量评估标准：**

| 等级 | 标准 |
|------|------|
| ✅ 优秀 | Top-3 结果与查询高度相关 |
| ⚠️ 可接受 | Top-5 中有 2-3 条相关 |
| ❌ 不合格 | Top-5 无明显相关结果 → 需排查 |

**不合格排查步骤：**
1. 检查向量库集合是否真的有数据：`--status`
2. 检查嵌入模型是否正常
3. 检查源文件内容质量：文件是否过短或乱码
4. 尝试精确关键词搜索 vs 语义搜索，判断是索引问题还是查询问题

### Checkpoint #2: 灌入结果确认 ⚠️

**完成后向用户报告：**

```
✅ 灌入完成报告：
- 新增灌入：X 个文件，Y 个 chunks
- 跳过（已存在）：Z 个
- 错误：E 个（如有）
- 向量库总计：M chunks
- 检索测试：3/3 通过
- 状态文件：已更新
```

### Step 6: 记录到当日 memory

将灌入结果追加到 `memory/daily/YYYY-MM-DD.md`。

## 失败恢复流程

### 场景 1：向量库连接失败

**症状：** 脚本报错，提示无法连接或创建集合。

**恢复步骤：**
```bash
# 0. 检查磁盘空间（本地向量库持续增长可能写满磁盘）
df -h

# 1. 检查向量库存储目录/连接是否正常

# 2. 如果目录损坏，备份后重建

# 3. 重置灌入状态（从头重跑）
python3 scripts/knowledge-ingest.py --reset

# 4. 重新执行灌入
python3 scripts/knowledge-ingest.py
```

### 场景 2：灌入中途中断

**症状：** 脚本因内存不足/超时/网络断开中断。

**恢复步骤：**
```bash
# 1. 查看当前状态（脚本自动保存进度）
python3 scripts/knowledge-ingest.py --status

# 2. 直接重新运行（自动从断点续跑）
python3 scripts/knowledge-ingest.py

# 3. 如果卡在某个客户，跳过该客户
python3 scripts/knowledge-ingest.py --client <下一个客户>
```

### 场景 3：灌入后检索质量差

**症状：** 检索返回不相关结果。

**恢复步骤：**
1. 确认数据量
2. 检查具体集合的数据
3. 如果是特定客户数据有问题，重置该客户状态后重跑

### 场景 4：嵌入模型异常

**症状：** chunks 写入成功但检索不到结果（可能 embedding 未正确生成）。

**恢复步骤：**
1. 确认嵌入模型已安装
2. 如果模型缺失，安装后重跑

## 注意事项

- **执行前确认当前系统状态**，避免在已有操作进行中执行
- **配置类操作必须先备份再修改**（脚本、状态文件、向量库目录）
- **如遇到未预料的问题**，先记录到当日 memory 文件，再排查
- **大批量灌入**（>5000 文件）建议分天完成，避免单次耗时过长
- **客户目录命名规范**：目录名用于生成集合名，避免特殊字符
- **KB_DIR 环境变量**：可通过设置 `KB_DIR` 指向不同的源目录
- **VECTOR_DB 环境变量**：可通过设置 `VECTOR_DB` 切换向量库后端

## 版本历史

| 日期 | 版本 | 变更说明 |
|------|------|----------|
| 2026-04-23 | 1.0 | 初始版本，基础流程 |
| 2026-06-01 | 2.0 | Phase 2 优化：补充具体命令、失败恢复流程、用户确认检查点、检索质量评估标准 |
| 2026-07-04 | 3.0 | 通用化改造：去除 ChromaDB 硬依赖，支持多种向量数据库后端 |
