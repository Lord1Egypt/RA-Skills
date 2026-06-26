---
name: method-repository
description: 将论文分析中提取的流行病学研究设计和统计方法存入本地知识库数据库，支持去重。当用户说"存入数据库"、"保存到知识库"、"记一下这个方法"时激活。
version: 1.1.0
user-invocable: true
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/openclaw/clawhub"}}
---

# Method Repository

将论文分析中提取的流行病学研究设计和统计方法存入本地 SQLite 数据库，实现自动去重。

## 触发条件

当用户说以下话语时激活：
- "存入数据库"
- "保存到知识库"
- "记一下这个方法"
- "把分析结果存到数据库"
- "记录这些方法"

## 数据库结构

数据库路径：`D:\autoclaw\结果\医学研究方法库\methods.db`

### 表1：study_designs（流行病学研究设计）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| design_name | TEXT UNIQUE | 研究设计名称（中文） |
| design_name_en | TEXT | 英文名称 |
| cohort_name | TEXT | 队列名称（如：UK Biobank、Framingham Heart Study、NHANES等著名队列的具体队列名称） |
| data_source | TEXT | 数据来源（如：UK Biobank、NHANES、SEER等公开数据库，或研究发起单位的医院/社区） |
| cohort_features | TEXT | 队列特征（样本量、年龄范围、随访周期、地理/人口特征） |
| description | TEXT | 研究设计描述 |
| key_features | TEXT | 核心特征 |
| suitable_scenarios | TEXT | 适用场景（什么研究问题适合用此设计） |
| advantages | TEXT | 优点 |
| limitations | TEXT | 局限性 |
| paper_source | TEXT | 来源论文标题 |
| added_date | TEXT | 录入日期 |

### 表2：statistical_methods（统计方法）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| method_name | TEXT UNIQUE | 方法名称（中文） |
| method_name_en | TEXT | 英文名称 |
| category | TEXT | 方法类别（如：生存分析、降维方法、缺失数据处理、因果推断） |
| purpose | TEXT | 用途/解决的问题 |
| key_assumptions | TEXT | 核心假设前提（如：Cox的比例风险假设、MICE的随机缺失假设） |
| data_requirements | TEXT | 数据要求（如：需要随访时间、需要分类变量、样本量要求） |
| suitable_scenarios | TEXT | 适用场景（在什么情况下选择此方法） |
| interpretation | TEXT | 结果解读方式（HR/OR/RR/PD等指标的含义） |
| advantages | TEXT | 优点 |
| limitations | TEXT | 局限性 |
| paper_source | TEXT | 来源论文标题 |
| added_date | TEXT | 录入日期 |

### 表3：concepts（流行病学概念/指标）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| concept_name | TEXT UNIQUE | 概念名称 |
| concept_name_en | TEXT | 英文名称 |
| definition | TEXT | 定义（权威来源的定义，非自行推断） |
| measurement | TEXT | 测量方式（如何操作化定义） |
| suitable_contexts | TEXT | 适用情境（在哪些研究场景中使用） |
| related_methods | TEXT | 相关联的方法（如：竞争风险相关方法列表） |
| data_source | TEXT | 典型数据来源（如：哪个公开数据库收录此变量） |
| paper_source | TEXT | 来源论文标题 |
| added_date | TEXT | 录入日期 |

### 表4：table_layouts（论文图表布局规范）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| table_name | TEXT UNIQUE | 表格名称（如 Table 1、Table 2） |
| table_name_en | TEXT | 英文名称 |
| purpose | TEXT | 用途/展示目的 |
| row_structure | TEXT | 行结构（变量如何排列、嵌套逻辑） |
| column_structure | TEXT | 列结构（分组如何排列、模型如何布局） |
| variable_order | TEXT | 变量排列顺序（连续→分类→代谢/疾病指标） |
| formatting_rules | TEXT | 格式规范（连续变量格式、分类变量格式、HR/CI格式） |
| statistical_tests | TEXT | 统计方法（用什么检验、用什么模型） |
| notes | TEXT | 注意事项（如脚注内容、参照组标注方式） |
| paper_source | TEXT | 来源论文标题 |
| added_date | TEXT | 录入日期 |

## 执行步骤

### Step 1：解析当前会话上下文

从最近的分析对话中提取：
- 研究设计名称、数据来源、队列特征
- 统计方法的假设前提、数据要求、适用场景
- 概念的权威定义、测量方式、典型应用

如果当前会话中没有足够信息，先询问用户补充。

### Step 2：自动去重检查

```sql
SELECT * FROM statistical_methods WHERE method_name = '?'
SELECT * FROM study_designs WHERE design_name = '?'
SELECT * FROM concepts WHERE concept_name = '?'
SELECT * FROM table_layouts WHERE table_name = '?'
```
- 已存在 → 跳过
- 不存在 → 准备插入

### Step 3：写入数据库

```python
conn.execute('INSERT OR IGNORE INTO study_designs
    (design_name, design_name_en, cohort_name, data_source, cohort_features,
     description, key_features, suitable_scenarios, advantages, limitations, paper_source)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (design_name, en_name, cohort_name, data_source, cohort_features,
     desc, key_features, scenarios, advantages, limitations, paper_source))

conn.execute('INSERT OR IGNORE INTO statistical_methods
    (method_name, method_name_en, category, purpose, key_assumptions, data_requirements,
     suitable_scenarios, interpretation, advantages, limitations, paper_source)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (name, en_name, category, purpose, assumptions, data_req,
     scenarios, interpretation, advantages, limitations, paper_source))

conn.execute('INSERT OR IGNORE INTO table_layouts
    (table_name, table_name_en, purpose, row_structure, column_structure,
     variable_order, formatting_rules, statistical_tests, notes, paper_source)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (table_name, en_name, purpose, row_structure, column_structure,
     variable_order, formatting_rules, statistical_tests, notes, paper_source))
```

### Step 4：汇总报告

```
【数据库存入完成】

## 新增记录（X条）
| 类型 | 名称 | 数据来源/类别 | 来源 |
|------|------|-------------|------|

## 跳过（已存在，X条）
| 类型 | 名称 |

## 当前数据库统计
- 研究设计：N 条
- 统计方法：N 条
- 流行病学概念：N 条
- 论文图表布局：N 条
```

## 注意事项

- 使用 INSERT OR IGNORE 保证 UNIQUE 约束自动去重，不报错
- 每个字段都尽量填写完整，不要留空；无法确定的字段标注"待补充"
- paper_source 记录来源论文，方便追溯
- 数据来源尽量写具体数据库名称（如 UK Biobank、SEER、CHNS），而非泛泛写"公开数据库"
- 数据库文件不存在时会自动创建
