---
name: investment-post-management-report-updater
description: 自动更新投后管理报告；当用户需要根据新财务报表和访谈纪要更新季度投后管理报告、生成财务数据分析、更新公司经营情况和行业分析时使用
dependency:
  python:
    - openpyxl==3.1.2
    - python-docx==1.1.0
---

# 投后管理报告自动更新技能

## 任务目标
- 本 Skill 用于：基于新季度财务报表、访谈纪要和上季度投后管理报告，自动生成新季度的投后管理报告
- 能力包含：财务数据提取、财务数据分析、经营情况更新、行业分析更新、Word 报告生成
- 触发条件：用户提供财务报表文件、访谈纪要文件和上季度投后管理报告文件，要求生成新季度报告

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包及版本
  ```
  openpyxl==3.1.2
  python-docx==1.1.0
  ```

## 操作步骤

### 标准流程

1. **接收和验证输入文件**
   - 确认用户提供三个文件：
     - 新季度财务报表（XLS/XLSX 格式）
     - 访谈纪要（DOCX 格式）
     - 上季度投后管理报告（DOCX 格式）
   - 检查文件格式和完整性

2. **解析财务报表数据**
   - 调用 `scripts/parse_financial_data.py` 提取财务数据：
     ```bash
     python3 /workspace/projects/investment-post-management-report-updater/scripts/parse_financial_data.py --file <财务报表路径>
     ```
   - 提取内容包括：资产负债表、利润表、现金流量表的关键指标

3. **解析访谈纪要和上季度报告**
   - 调用 `scripts/parse_docx.py` 提取文本内容：
     ```bash
     python3 /workspace/projects/investment-post-management-report-updater/scripts/parse_docx.py --file <访谈纪要路径>
     python3 /workspace/projects/investment-post-management-report-updater/scripts/parse_docx.py --file <上季度报告路径>
     ```
   - 保留上季度报告的结构和格式

4. **财务数据分析（智能体处理）**
   - 对比新旧财务数据，识别关键变化
   - 参考 [references/financial-analysis-guide.md](references/financial-analysis-guide.md) 中的分析方法
   - 分析要点包括：
     - 收入增长率和趋势
     - 利润率变化
     - 现金流状况
     - 资产负债结构变化
   - 生成财务分析段落

5. **公司经营情况更新（智能体处理）**
   - 从访谈纪要中提取关键经营信息
   - 参考 [references/content-update-template.md](references/content-update-template.md) 中的模板
   - 更新内容包括：
     - 业务进展
     - 产品/服务更新
     - 团队变化
     - 重大事件
   - 生成经营情况描述段落

6. **行业情况更新（智能体处理）**
   - 从访谈纪要中提取行业相关信息
   - 结合外部知识进行行业分析
   - 更新内容包括：
     - 行业发展趋势
     - 竞争格局变化
     - 政策影响
   - 生成行业分析段落

7. **生成新季度投后管理报告**
   - 调用 `scripts/generate_report.py` 生成报告：
     ```bash
     python3 /workspace/projects/investment-post-management-report-updater/scripts/generate_report.py \
       --template <上季度报告路径> \
       --financial-data <财务数据JSON> \
       --financial-analysis <财务分析文本> \
       --business-update <经营情况文本> \
       --industry-update <行业分析文本> \
       --output <输出报告路径>
     ```
   - 保持原有报告格式、样式和结构
   - 更新相关章节内容

8. **输出和验证**
   - 提供生成的报告文件路径
   - 简要说明主要更新内容
   - 建议用户检查报告准确性

### 可选分支
- 当财务报表格式特殊时：手动提取关键数据，智能体进行分析
- 当需要保留特定格式时：在 generate_report.py 中自定义样式映射
- 当需要生成多个版本时：多次调用生成脚本，输出不同文件

## 资源索引
- 必要脚本：
  - [scripts/parse_financial_data.py](scripts/parse_financial_data.py)（用途：解析 Excel 财务报表，提取关键财务指标）
  - [scripts/parse_docx.py](scripts/parse_docx.py)（用途：解析 DOCX 文件，提取文本内容和结构）
  - [scripts/generate_report.py](scripts/generate_report.py)（用途：基于模板和分析内容，生成新季度报告）
- 领域参考：
  - [references/report-structure.md](references/report-structure.md)（何时读取：了解投后管理报告的标准结构和章节要求）
  - [references/financial-analysis-guide.md](references/financial-analysis-guide.md)（何时读取：执行财务数据分析时，参考分析框架和要点）
  - [references/content-update-template.md](references/content-update-template.md)（何时读取：生成各部分更新内容时，参考写作模板）

## 注意事项
- 仅在需要时读取参考文档，保持上下文简洁
- 智能体负责内容分析和生成，脚本负责文件格式处理
- 生成报告后建议用户检查数据准确性和内容完整性
- 保持上季度报告的格式风格，确保报告一致性
- 对于复杂的财务分析，可以多次调用脚本进行验证

## 使用示例

### 示例1：标准季度报告更新
- 功能说明：基于标准输入文件生成新季度报告
- 执行方式：脚本+智能体混合
- 关键参数：三个输入文件路径
- 示例流程：
  1. 用户上传：2025Q4财务报表.xlsx、访谈纪要.docx、2025Q3报告.docx
  2. 智能体调用脚本解析所有文件
  3. 智能体分析数据并生成更新内容
  4. 智能体调用脚本生成2025Q4报告.docx

### 示例2：自定义分析重点
- 功能说明：在标准更新基础上，强调特定分析维度
- 执行方式：智能体主导
- 关键要点：根据投资方关注点调整分析重点
- 示例调整：增加现金流分析、债务风险评估等专项分析

### 示例3：多季度对比分析
- 功能说明：在报告中增加多季度趋势对比
- 执行方式：智能体主导
- 关键要点：提取历史数据，生成对比图表或表格
- 示例内容：近四个季度的收入趋势、利润率变化对比
