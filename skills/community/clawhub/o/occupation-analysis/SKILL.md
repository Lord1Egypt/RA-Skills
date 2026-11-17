---
name: occupation-analysis
version: 1.1.0
description: 职业教育专业建设辅助工具，生成职业分析报告（工作过程系统化方法，七部分结构）。支持教育层次：中职、高职、职教本科。**MUST USE场景**：(1) 用户提供专业名称/代码，要求生成职业分析报告；(2) 用户明确要求"职业分析"、"工作任务分析"、"典型工作任务提取"；(3) 用户要求"行动领域划分"、"学习领域转换"、"学习情境设计"。**触发关键词**：职业分析、专业建设、典型工作任务、行动领域、学习领域、职业面向、教育层次、专业代码、课程开发、西餐烹饪、汽车维修。**输出物**：Markdown报告 + Word文档
dependency:
  python:
    - requests==2.31.0
    - python-dotenv==1.0.0
    - pypdf==3.17.0
    - python-docx==1.2.0
  system:
    - sudo apt-get update && sudo apt-get install -y pandoc
---

# 职业教育职业分析 Skill

## 概述

本skill用于职业教育专业建设中的职业分析环节，按照工作过程系统化课程开发方法(工作任务分析-典型工作任务分析-行动领域划分-职业能力归纳-学习领域转换-学习情境设计)，自动生成规范的职业分析文档。

**适用范围**：
- 中等职业教育（中职）
- 高等职业教育（高职/专科）
- 职业教育本科（职教本科）

---

## 分析前思维框架

在开始职业分析前，必须理解以下关键决策点：

### 1. 层次适配原则

**核心问题**：这个教育层次的职业面向和能力深度是什么？

| 层次 | 职业面向 | 能力要求 | 课程特征 |
|------|----------|----------|----------|
| 中职 | 操作岗位 | 技能操作为主 | 操作技能、规范执行 |
| 高职 | 技术岗位 | 技术应用能力 | 技术应用、问题诊断 |
| 职教本科 | 管理/技术岗 | 技术创新与管理 | 综合应用、系统优化 |

**判断方法**：查看专业教学标准中的"培养目标"关键词：
- "技能人才" → 中职深度
- "高素质技术技能人才" → 高职深度
- "高层次技术技能人才" → 职教本科深度

### 2. 数据源选择决策树

```
需要职业数据（本地文档）？
├─ 职业教育专业和职业岗位信息 → 专业-职业对照表.xlsx
├─ 职业定义和主要任务 → 必须用中国职业大典
├─ 技能和能力补充、工具和工作环境、职业素养 → 推荐 ESCO/O*NET（本地文档）和 O*NET Tools & Technology

```

**数据源必要性判断**：

| 场景 | 中国职业大典 | ESCO | O*NET |
|------|-------------|------|-------|
| 专业与职业岗位对照 | 必须 | 补充 | 补充 |
| 职业定义提取 | 必须 | 补充 | 补充 |
| 工作任务分析 | 必须 | 补充 | 补充 |
| 技能要求分析 | 参考 | 推荐 | 推荐 |
| 工作情境分析 | 参考 | 推荐 | 推荐 |
| 工具技术分析 | 不需要 | 推荐 | 推荐 |

### 3. 职业大典分段加载策略

```

**分块策略**：
├─ 按职业代码第一位选择大类文件
├─ 第5大类- 农林牧渔业生产及辅助人员
├─ 第6大类- 生产制造类及有关人员
├─ 第2大类- 专业技术人员
├─ 第4大类- 社会生产服务和生活服务人员
└─ 其他大类

**关键判断**：
- 如果目标职业代码以 `6-` 开头 → 加载第6大类
- 如果需要多个职业 → 检查是否属于同一大类，合并加载

```
### 4. 课程转换逻辑

**行动领域 → 学习领域 的转换依据**：

1. **工作对象相似性**：处理相同或相关对象的任务归为一类，适配职业岗位工作内容范畴
2. **任务难度梯度**：从简单到复杂，符合学习认知规律
3. **工作逻辑顺序**：按实际工作流程排列
4. **学时合理性**：每个学习领域参考学时 48-144 学时为宜,累计学时：中职一般不少于1200学时，高职专科和本科一般不少于1600学时
5. **学习领域数量**: 一般为10个左右

---

## NEVER Do

### Token 和性能


- **NEVER** 在同一会话中重复加载同一大类文件
  - 原因：浪费 tokens，`OccupationDictionaryLoader` 已实现缓存
  - 正确做法：复用已加载的内容

### 数据处理

- **NEVER** 使用简单字符串匹配来对应中国职业代码与ESCO、ISCO和O*NET代码
  - 原因：不同分类体系命名差异大（如"汽车维修工" vs "Motor Vehicle Mechanic"）
  - 正确做法：进行语义理解和推断

- **NEVER** 忽略教育层次差异，为所有层次生成相同深度的内容
  - 原因：中职侧重操作和陈述性知识，本科侧重创新、组织管理和策略性知识，工作任务分析和学习领域描述等内容深度必须匹配
  - 正确做法：参考"层次适配原则"调整能力描述深度

- **NEVER** 在用户确认职业信息前就开始数据检索
  - 原因：可能检索错误的专业或层次
  - 正确做法：先展示确认面板，用户确认后再执行

- **NEVER** 接受用户提出的非职业大典中的职业
  - 原因：非职业大典职业无法获取标准定义和任务
  - 正确做法：要求用户重新提出职业大典中存在的职业

### 流程

- **NEVER** 跳过步骤0预检验证
  - 原因：数据文件缺失会导致后续所有步骤失败
  - 正确做法：每次执行前运行预检脚本

- **NEVER** 跳过用户确认环节
  - 原因：职业信息可能有误或不完整，用户可能需要修改、删除或新增职业
  - 正确做法：步骤4必须使用 `question` 工具展示确认面板，**等待用户回复**后才能继续步骤5
  - ⚠️ 即使执行"全流程测试"也必须等待用户确认

- **NEVER** 忽略本地文档缺失警告
  - 原因：缺失文档会影响分析完整性
  - 正确做法：展示缺失列表，用户确认后继续

- **NEVER** 使用非职业大典中的职业
  - 原因：无法获取标准职业定义和任务
  - 正确做法：要求用户提供职业大典中存在的职业

---

## 边缘场景处理

> **详细场景处理方法**: 详见 [references/troubleshooting.md](references/troubleshooting.md)

---

## 工作流程

### 架构概览

本Skill采用**分层架构**，明确区分Python脚本层和大模型处理层：

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Python脚本层（数据获取与格式化）                            │
│                                                                                 │
│  职责：精确匹配、文件读写、API调用、格式转换                                       │
│  特点：不调用大模型API，执行确定性逻辑                                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼ JSON数据
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        agent大模型处理层（语义分析与生成）                              │
│                                                                                 │
│  职责：文本检索、语义理解、创造性生成、质量校验                                             │
│  特点：由执行本Skill的Agent（当前大模型）完成                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 完整工作流程

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 阶段一：数据获取（Python脚本 + 大模型）                                            │
├──────────────────────────────────────────────────────────────────────────────────┤
│  步骤1: 检索专业教学标准及职业编码对照（Python脚本）                              │
│         - search_major.py 检索专业教学标准                                        │
│         - 查询专业-职业对照表.xlsx，获取职业编码和名称                              │
│         → major_info.json（含职业编码列表）                                        │
│                                                                                  │
│  步骤2: 获取职业详细信息（大模型处理）                                            │
│         ⚠️ MANDATORY: 必须使用 OccupationDictionaryLoader 加载职业大典              │
│         - 根据职业代码首位加载对应的职业大典文档（class_*.md）                         │
│         - 使用完整职业代码在文件中检索职业定义和主要工作任务                           │
│         - 语义解析职业面向字段补充岗位信息                                             │
│         → occupation_info.json                                                   │
│                                                                                  │
│  步骤3: ESCO/O*NET映射推断（大模型世界知识）                                   │
│         - 输入：occupation_dict_data.json                                           │
│         - Agent构造提示词，调用自身大模型的世界知识推断                              │
│         - 输出ESCO编码（4位数字）+名称、O*NET编码（XX-XXXX.XX）+名称               │
│         - 后处理验证编码格式                                                      │
│         → occupation_mapping_info.json                                            │
│                                                                                  │
│  步骤4: 用户确认环节（⚠️ 强制性暂停点）                                    │
│         - 展示提取的职业信息（批量展示）                                           │
│         - 确认面板同时展示中国职业信息和国际映射结果                                 │
│         - 使用 question 工具展示确认选项                                          │
│         - ⚠️ 必须等待用户回复（确认/修改/删除）                                     │
│         - 若用户提出新职业不在职业大典 → 要求重新提出                              │
│         → 确认后的occupation_info.json                                            │
│                                                                                  │
│  步骤5: 整合全部数据（Python脚本）                                               │
 │         - 读取 major_info.json、occupation_dict_data.json、mapping_info.json       │
 │         - 按映射代码读取 assets/esco_details_md/ 和 onet_details_md/ 原始文档      │
 │         - 零提取、零转换，合并输出 Markdown                                         │
 │         → combined_data.md（4个数据源）                                            │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 阶段二：语义分析与生成（大模型）                                                │
├──────────────────────────────────────────────────────────────────────────────────┤
│  步骤6: 职业面向语义解析                                                          │
│         - 从职业面向、职业岗位、职业工种等内容提取职业名称、岗位名称、工作任务    │
│         - 生成分岗位的工作任务列表                                                │
│                                                                                   │
│  步骤7: 工作任务分析                                                              │
│         - 参考：report_template.md 表1字段定义                                    │
│         - 为每个职业的每个工作任务生成完整分析                                    │
│         - 输出：job_tasks[]（表1数据源）                                          │
│                                                                                   │
│  步骤8: 典型工作任务确定                                                          │
│         - 参考：report_template.md 表2+表3字段定义                                │
│         - 参考：work_process_method.md 典型工作任务特征                           │
│         - 从job_tasks中筛选提炼典型工作任务                                       │
│         - 输出：typical_tasks[]（表2+表3数据源）                                  │
│                                                                                   │
│  步骤9: 行动领域划分                                                             │
│         - 按工作对象相似性、任务难度梯度、工作逻辑顺序等原则聚类                  │
│         - 生成行动领域表和聚类原则                                                │
│         - 设定能力等级递进（初级→中级→高级）                                      │
│                                                                                   │
│  步骤10: 职业能力分析                                                             │
│         - 推导专业能力、方法能力、社会能力                                        │
│         - 生成表6（汇总表）、表7（一览表）、表8（解构表）                         │
│         - 确保表7与表8能力编号和名称一致                                          │
│                                                                                   │
│  步骤11: 学习领域转换                                                             │
│         - 行动领域转换为学习领域                                                  │
│         - 设定参考学时                                                            │
│         - 生成学习目标和学习内容                                                  │
│                                                                                   │
│  步骤12: 学习情境设计                                                             │
│         - 为每个学习领域设计3-6个学习情境                                         │
│         - 生成学时、教学方式、评价方式                                            │
│                                                                                   │
│  步骤13: 输出结构化分析数据 → analysis_data.json                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 阶段三：格式化输出（Python脚本）                                                   │
├──────────────────────────────────────────────────────────────────────────────────┤
│  步骤14: 生成Markdown报告   → generate_report.py    → report.md                  │
│           - 将analysis_data.json转换为Markdown格式                                │
│           - 按七部分结构组织表格                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│ 阶段四：自我校正（大模型自身）                                                      │
├──────────────────────────────────────────────────────────────────────────────────┤
│  步骤15: 质量校验                                                                │
│          - 验证表1岗位与表2对应岗位一致                                           │
│          - 验证表4覆盖表2所有典型任务                                             │
│          - 验证表格编号连续（表1→表11）                                           │
│          - 验证表7与表8能力编号一致                                               │
│          - 验证总学时符合教育层次要求                                             │
│          - 验证学习情境数量合理（每领域3-6个）                                     │
│                                                                                  │
│  步骤16: 问题修复（如有）                                                         │
│          - 修复发现的问题                                                         │
│          - 重新生成analysis_data.json                                            │
│          - 最多3次修复循环                                                        │
└──────────────────────────────────────────────────────────────────────────────────┘
```

### 职责划分速查表

| 步骤 | 执行者 | 任务类型 | 输出 |
|------|--------|----------|------|
| 1 | Python脚本 | 数据获取+精确匹配 | major_info.json（含职业编码） |
| **2** | **大模型** | 文档解析、职业信息提取 | occupation_info.json |
| **3** | **大模型** | ESCO/O*NET映射推断 | occupation_mapping_info.json |
| **4** | **大模型+用户** | 用户确认 | 确认后的occupation_info.json |
| 5 | Python脚本 | 整合全部数据（读取4个数据源+本地原始MD） | combined_data.md |
| 6-13 | **大模型自身** | 语义分析与生成 | analysis_data.json |
| 14 | Python脚本 | 格式化输出 | report.md |
| 15-16 | **大模型自身** | 质量校验与修复 | 最终报告 |

###  重要原则

1. **Python脚本不做语义分析**：脚本只负责精确匹配和格式转换
2. **大模型不调用外部API**：所有语义分析由执行Skill的Agent完成
3. **数据驱动**：每个阶段的输出是下一阶段的输入
4. **结构化传递**：使用JSON格式传递数据，确保数据完整性
5. **用户确认必需**：步骤4和步骤5均需用户确认

### 步骤0：预检验证（必须执行）

> **MANDATORY - READ REFERENCE FILE**: 在开始工作流程前，建议阅读
> [`references/precheck_guide.md`](references/precheck_guide.md)
> 获取完整的环境检查清单和预检脚本。

**快速检查命令**：
```bash
# 检查核心数据文件
python -c "from pathlib import Path; files=['assets/moe_pdfs_final.json', 'assets/esco_details_md', 'assets/onet_details_md']; [print('[OK]' if Path(f).exists() else '[X]', f) for f in files]"
```

**核心检查项**：Python 3.8+、依赖安装、数据文件（职业大典、ESCO、O*NET本地文档）。

## 数据源配置（摘要）

> **详细数据源说明**：[`references/workflow_details.md`](references/workflow_details.md)

### 本地数据文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 专业教学标准 | `assets/moe_pdfs_final.json` | 教育部发布的专业教学标准索引 |
| 专业-职业对照表 | `assets/专业-职业对照表.xlsx` | 专业对应职业和岗位的对照表 |
| 职业大典 | `assets/occupation_dictionary_split/` | 中国职业分类大典（2022版，按大类拆分） |
| ESCO文档 | `assets/esco_detail_md/` | ESCO职业详细文档（约3000+个MD文件） |
| O*NET文档 | `assets/onet_details_md/` | O*NET职业详细文档（894个MD文件） |

### 职业大典分段加载

> **关键判断**：根据职业代码首位数字加载对应大类文件（完整代码→大类映射表见 [`workflow_details.md`](references/workflow_details.md) 步骤2）
>
> **使用方法**：`OccupationDictionaryLoader.load_by_occupation_code('6-22-02')`

### ESCO/O*NET查询

- ESCO文件命名：`{ISCO代码}.{序号}.md`（如 `7231.1.md`）
- O*NET文件命名：`{O*NET代码}.md`（如 `49-3023.00.md`）

## 实施步骤概览

> **详细执行命令和输出格式**：各步骤的详细内容详见 [`references/workflow_details.md`](references/workflow_details.md)

---

## 阶段一：数据获取

### 步骤1：检索专业教学标准（Python脚本）

> **MANDATORY - READ**: [`references/workflow_details.md`](references/workflow_details.md) 步骤1

**执行命令**：`python scripts/search_major.py --major "专业名称" --level "教育层次" --output temp/major_info.json`

**输出**：`major_info.json`

### 步骤2：获取职业信息（大模型处理）

> **MANDATORY - READ**: [`references/workflow_details.md`](references/workflow_details.md) 步骤2
>
> ⚠️ **CRITICAL - 必须使用 OccupationDictionaryLoader**
>
> 本步骤必须调用 `scripts/occupation_dict_loader.py` 加载职业大典数据。
> 禁止直接读取职业信息而不查询职业大典，会导致职业定义缺失。

**核心任务**：检索专业-职业对照表、加载职业大典、提取职业详细信息

**输出**：`occupation_info.json`

### 步骤3：ESCO/O*NET映射推断（大模型世界知识）

> **MANDATORY - READ**: [`references/workflow_details.md`](references/workflow_details.md) 步骤3

**核心任务**：利用大模型世界知识推断ESCO和O*NET职业编码

**输出**：`occupation_mapping_info.json`

### 步骤4：用户确认环节（⚠️ 强制性暂停点）

> **MANDATORY - READ**: [`references/workflow_details.md`](references/workflow_details.md) 步骤4
> 
> ⚠️ **必须等待用户回复**：确认面板展示中国职业+国际映射 → question工具确认 → 等待回复 → 继续步骤5

**重要约束**：用户新增职业必须在职业大典中存在。

### 步骤5：整合全部数据（Python脚本）

> **MANDATORY - READ**: [`references/workflow_details.md`](references/workflow_details.md) 步骤5

**执行命令**：
```bash
python scripts/integrate_data.py \
    --major temp/major_info.json \
    --occupation temp/occupation_dict_data.json \
    --mapping temp/occupation_mapping_info.json \
    --output temp/combined_data.md
```

**整合内容**（4个数据源）：
1. 专业教学标准（major_info.json → `# 专业教学标准`）
2. 中国职业信息（occupation_dict_data.json → `# 职业信息`）
3. 国际职业代码映射（mapping_info.json → `# 国际职业代码映射` 表格）
4. ESCO/O*NET原始MD文档（按映射代码直接从assets/读取 → 按职业分节）

**输出**：`combined_data.md`（零提取、零转换，原始内容供大模型参考）

---

## 阶段二：语义分析与生成

> Agent/大模型基于阶段一获取的数据，进行语义理解、分析推理、创造性生成。
> 
> **核心参考资料**：[`references/work_process_method.md`](references/work_process_method.md)

**输入文件**：`temp/combined_data.md`

### 步骤6：职业面向语义解析

**任务**：从职业面向字段提取职业名称、岗位名称、工作任务列表

**输出**：`occupations[].tasks`（职业面向解析的原始任务列表，供步骤7分析使用）

### 步骤7：工作任务分析

> **MANDATORY - READ**: [`references/report_template.md`](references/report_template.md) 表1字段定义（第31-39行）

**任务**：为每个职业的每个工作任务生成完整的五个维度分析

**输出数据结构**：`job_tasks[]`（表1数据源）

**关键约束**：
- 每个职业的所有任务必须完整分析（无遗漏）
- occupation_code/occupation_name字段必须追溯职业来源
- 表格属性：纵向表格，每个任务单独一个表格

**教育层次适配**：
| 层次 | 能力动词 | 禁止动词 |
|------|----------|----------|
| 中职 | 操作、执行、完成、使用、识别、检测、制作、编制 | 设计、优化、创新、管理、分析 |
| 高职 | 检测、诊断、分析、维护、维修、优化 | 研发、创新、管理 |
| 职教本科 | 设计、优化、管理、创新 | - |

### 步骤8：典型工作任务确定

> **MANDATORY - READ**: [`references/report_template.md`](references/report_template.md) 表2字段（第61-64行）+ 表3字段（第74-83行）<br>
> **MANDATORY - READ**: [`references/work_process_method.md`](references/work_process_method.md) 第3.2节（典型工作任务特征，第82-89行）

**任务**：从job_tasks中筛选提炼典型工作任务

**输出数据结构**：`typical_tasks[]`（表2+表3数据源）

**关键约束**：
- related_tasks字段必须引用job_tasks中的任务ID
- typical_tasks数量通常为job_tasks的40%-60%
- 工作要求字段（work_requirements）必须填写具体内容，不可空白

### 步骤9：行动领域划分

> **MANDATORY - READ**: [`references/work_process_method.md`](references/work_process_method.md) 第3.3节（行动领域）+ 第2.1节（模板）+ 第四节步骤3（一致性检查）

**聚类原则**：工作对象相似性、任务难度梯度、工作逻辑顺序

### 步骤10：职业能力分析

**能力编号规则**：Z=专业能力、F=方法能力、S=社会能力

**关键约束**：表7与表8能力编号必须一一对应

### 步骤11：学习领域转换

> **MANDATORY - READ**: [`references/work_process_method.md`](references/work_process_method.md) **第五节**（推导算法：数量计算、命名规则、拆分判断、学时估算）+ 第2.2节（模板）

**转换原则**：
- 每个行动领域对应1-2个学习领域
- 参考学时：每领域48-144学时
- 总学时：中职≥1200，高职≥1600

### 步骤12：学习情境设计

> **MANDATORY - READ**: [`references/work_process_method.md`](references/work_process_method.md) **第六节**（情境设计：数量计算、命名规则、学时分配）+ 第2.3节（模板）

**任务**：为每个学习领域设计3-8个情境，分配学时（16-32学时/情境）

### 步骤13：输出结构化分析数据

> **MANDATORY - READ**: [`references/analysis_data_template.json`](references/analysis_data_template.json) 完整格式规范 + [`references/analysis_data_template.json`](references/analysis_data_template.json) appendix.table_data_mapping（数据结构对应关系）

**必需字段**：major_info、occupations、jobs、job_tasks、typical_tasks、action_domains、abilities、learning_domains、learning_situations、metadata

**关键约束**：
- job_tasks包含每个职业的所有工作任务（表1数据源）
- typical_tasks引用job_tasks任务ID（表2+表3数据源）
- action_domains[i]必须包含tasks和abilities
- learning_domains[i]必须包含methods和assessment

---

## 阶段三：格式化输出（Python脚本执行）

### 步骤14：生成Markdown报告

```bash
python scripts/generate_report.py \
  --data temp/analysis_data.json \
  --output temp/report.md
```

脚本将 `analysis_data.json` 转换为七部分结构的Markdown报告。

**转换为Word**：
```bash
pandoc temp/report.md --reference-doc=references/reference.docx -o output/report.docx
```

---

## 阶段四：自我校正

### 步骤15：质量校验

Agent读取生成的报告，检查以下项：

| 检查项 | 严重程度 | 验证方法 |
|--------|----------|----------|
| job_tasks包含每个职业的所有任务 | 高 | 无遗漏 |
| typical_tasks引用job_tasks任务ID正确 | 高 | related_tasks字段ID匹配 |
| 表1岗位与表2对应岗位一致 | 高 | 不得统称为单一岗位 |
| 表4覆盖表2所有典型任务 | 高 | 无遗漏任务 |
| 表7与表8能力编号一致 | 高 | 一一对应 |
| 能力动词符合教育层次要求 | 高 | 中职禁用"设计/优化/创新" |
| 能力等级有递进 | 中 | 不得全为同一等级 |
| 表格编号连续（表1→表11） | 中 | 无跳跃 |

### 步骤16：问题修复

如发现问题：
1. 修改 `analysis_data.json` 中对应字段
2. 重新执行步骤14生成报告
3. 重复步骤14验证
4. 最多3次修复循环

**修复后输出**：最终版 `report.md` 和 `report.docx`

---

## 执行检查清单

Agent执行本Skill时，按以下清单逐项确认：

### 阶段一检查
- [ ] 步骤1（Python脚本）：`major_info.json` 已生成，包含 `career_orientation`
- [ ] 步骤2（大模型）：已加载职业大典文档，输出职业信息
- [ ] 步骤3（大模型）：ESCO/O*NET映射已完成
- [ ] 步骤4（大模型+用户）：确认面板已展示中国职业+国际映射参考，**用户已回复确认**，`occupation_info.json` 已更新
- [ ] 步骤5（Python脚本）：`combined_data.md` 已整合（4个数据源）

### 阶段二检查（大模型自身）
- [ ] 步骤6：职业面向已解析
- [ ] 步骤7：每个职业的每个工作任务已生成完整分析（job_tasks已生成）
- [ ] 步骤8：典型工作任务已确定（typical_tasks已生成，related_tasks引用正确）
- [ ] 步骤9：行动领域已划分，能力等级已设定
- [ ] 步骤10：能力分析完成，表7/表8一致
- [ ] 步骤11：学习领域已转换
- [ ] 步骤12：学习情境已设计
- [ ] 步骤13：`analysis_data.json` 已生成，包含job_tasks和typical_tasks

### 阶段三检查（Python脚本）
- [ ] 步骤14：`report.md` 已生成


### 阶段四检查（大模型自身）
- [ ] 步骤15：质量校验通过
- [ ] 步骤16：如有问题已修复

---

## 脚本工具

| 脚本 | 功能 | 核心命令 |
|------|------|----------|
| `scripts/search_major.py` | 专业教学标准检索（支持PDF解析） | `python scripts/search_major.py --major "专业名称" --level "层次"` |
| `scripts/pdf_parser.py` | PDF下载与解析 | `python scripts/pdf_parser.py --url "PDF_URL" --code "专业代码"` |
| `scripts/major_catalog_mapper.py` | 专业目录映射（xlsx→大类→MD文件） | `python scripts/major_catalog_mapper.py` |
| `scripts/integrate_data.py` | 多源数据整合 | `python scripts/integrate_data.py --major major.json --occupation occupation.json --mapping mapping.json --output combined.md` |
| `scripts/generate_report.py` | Markdown 报告生成（表7/表8一致） | `python scripts/generate_report.py --data analysis.json --output report.md` |
| `scripts/validate_report.py` | 报告验证与审校 | `python scripts/validate_report.py --report report.md --data analysis.json` |
| `scripts/occupation_dict_loader.py` | 职业大典分块加载 | `get_occupation_dictionary('6-22-02')` |

**关键参数**：
- `--output`: 输出文件路径
- `--no-pdf`: 跳过PDF解析（仅返回基本信息）
- `--cache-dir`: PDF缓存目录
- `--mapping`: 映射信息JSON文件（用于本地文档查询）

## 配置要求

### Python依赖

```bash
pip install requests python-dotenv pypandoc pypdf pdfplumber
```

**系统依赖**：pandoc（Word 转换必需）

### 本地数据文件

确保以下目录和文件存在：
- `assets/moe_pdfs_final.json` - 专业教学标准
- `assets/occupation_dictionary_split/` - 职业大典（按大类拆分）
- `assets/esco_detail_md/` - ESCO职业文档
- `assets/onet_details_md/` - O*NET职业文档

## 注意事项

| 类别 | 关键点 |
|------|--------|
| 数据完整性 | 专业教学标准用最新官方版、职业大典用2022 markdown版、ESCO/O*NET用本地文档 |
| 职业匹配 | 中国代码与国际标准需大模型语义推断、不同体系名称差异大、由大模型进行语义理解 |
| 本地化 | ESCO/O*NET数据为英文需翻译、注意专业术语准确性、可保留双语版本 |
| 层次适配 | 中职→操作技能、高职→技术应用、职教本科→管理优化 |
| 用户确认 | 步骤4必须让用户确认职业信息（同时展示国际映射参考） |

## 故障排除

> **CONDITIONAL - READ IF NEEDED**: 如需详细的故障排除指南，请阅读
> [`references/troubleshooting.md`](references/troubleshooting.md)
> 获取常见问题、调试方法、数据完整性检查指南。
>
> **Do NOT load** `troubleshooting.md` during 阶段一（步骤1-5）or 阶段二（步骤6-13）unless 遇到脚本报错或验证失败。该文件仅在异常时提供价值，提前加载会浪费上下文。

### 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 找不到专业教学标准 | 名称/代码错误 | 用代码检索、检查官方名称 |
| 本地文档缺失 | 文件名不匹配 | 检查ESCO英文名/O*NET代码、支持模糊匹配 |
| 表格格式错误 | 缺少分隔行 | 检查纵向表格格式 |
| 用户提出非职业大典职业 | 无法获取标准定义 | 要求用户重新提出职业大典中存在的职业 |

## 参考资料

| 文件 | 用途 | 加载时机 |
|------|------|----------|
| `references/precheck_guide.md` | 预检验证详细指南 | 步骤0 **按需** 加载 |
| `references/workflow_details.md` | 步骤1-5详细执行命令和输出格式 | 阶段一 **按需** 参考 |
| `references/work_process_method.md` | 行动领域/学习领域/学习情境描述模板 | 步骤9/11/12 **必须** 加载对应章节 |
| `references/analysis_data_template.json` | analysis_data.json 完整格式规范 | 步骤13 **必须** 参考 |
| `references/occupation_mapping_template.json` | 映射输出格式规范 | 步骤3 参考 |
| `references/report_template.md` | Markdown 报告模板（七部分结构） | 步骤14 **必须** 加载 |
| `references/troubleshooting.md` | 故障排除详细指南 | 遇到问题时 **按需** 加载 |
| `references/reference.docx` | Word 样式模板（自定义格式） | 步骤14 **可选** |

