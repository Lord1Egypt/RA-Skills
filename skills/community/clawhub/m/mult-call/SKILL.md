---
name: multi_call
slug: multi_call
version: 1.0.2
description: 多路召回skill ,用于将意图识别skill中的指标和维度信息进行分析，通过向量知识库召回QA问答对，通过图数据库召回表的定义结构。
metadata: {"clawdbot":{"emoji":"🐬"}}
---

# Skill: multi_call

- Description: 多路召回 skill，将意图识别结果分析后，通过向量知识库召回 QA 问答对，通过图数据库召回表的 DDL 结构。
- Inputs: [intent_output]（从 `skills/.workflow/intent_output.json` 读取）
- Outputs: [table_scheme, Q_A_pairs]（写入 `skills/.workflow/multicall_output.json`）
- ID: multi_call
- Role: 知识召回引擎
- 功能描述：基于实体标签，从元数据中心检索表结构（Schema）、指标计算口径、枚举值及业务知识。
- 输入参数：
    - final_query (string): 来自 intent_output.json
    - indicator_metric (list): 指标 + 维度信息

- 输出结果：
    - table_scheme (string): CREATE TABLE DDL 字符串（来自 Neo4j）。
    - Q_A_pairs (list): 相似问题 + SQL 示例（来自 Milvus）。
    - 召回权重：表结构 (0.5) + 指标定义 (0.3) + 知识库 (0.2)。

## 注入服务（通过 `.env` 配置）

| 服务类 | 作用 | .env 关键配置 |
|--------|------|---------------|
| `_RealNeo4jService` | 查询表结构 DDL | `NEO4J_URI` / `NEO4J_USER` / `NEO4J_PASSWORD` |
| `_RealMilvusQAService` | 召回相似 QA 对 | `MILVUS_*`, `EMBEDDING_*`, `MILVUS_QA_COLLECTION`（默认 `dev_vanna_sql`） |

> 两个服务均可独立失败降级：Neo4j 失败时返回空 DDL，Milvus 失败时返回空 QA 对。

## 独立运行说明

```bash
# 前置：先运行前两步
python ../rewrite-question/rewrite_question.py --query "今天汉河店的成交额"
python ../recognize-intent/recognize_intent.py

# 运行多路召回（从 .workflow/intent_output.json 自动读取）
python multi_call.py

# 带清理（清除本步及后续输出）
python multi_call.py --clean
```

### 下一步
```bash
python ../sql-generator/sql_generator.py
```
