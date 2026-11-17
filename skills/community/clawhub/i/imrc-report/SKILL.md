---
name: imrc-report
description: "Generate monthly/annual operations reports from IMRC system data across 10 pages"
tags: [analysis, data, visual, file-based, template-based]
version: 1.0.0
triggers:
  - 运营报告
  - 月度汇�?  - 年度总结
  - IMRC数据
  - 装备所运营
  - 运营情况
---

# IMRC 运营报告生成技�?
## 概述

�?IMRC 运营管理系统提取装备所运营数据，结合美信消息，生成结构化运营报告�?
报告采用**总分结构**�?- **第一�?*：整体介绍（10分钟汇报用）
- **后续分项**：项目运�?预算/合同/投资/风险等详细分�?
## 数据�?
### IMRC 系统 10 个页�?
| ID | 页面名称 | URL | 单位 |
|----|---------|-----|------|
| 1 | 项目运营情况 | /analysis/projectOverviewOperations | - |
| 2 | 项目立项占用分析 | /holdAnalysis | 万元 |
| 3 | 项目超预算分�?| /overBudgetAnalysis | 万元 |
| 4 | 合同分析 | /contractAnalysis | 万元 |
| 5 | 重点项目看板 | /topProjectDashboard | - |
| 6 | 预付款逾期分析 | /advanceOverdueAnalysis | 万元 |
| 7 | 合同执行分析 | /contractExecute | �?|
| 8 | 投资分析 | /investAnalysis | 万元 |
| 9 | 投资异常合同 | /abnormalInvestmentContract | - |
| 10 | 项目执行情况 | /projectManage | - |

### 美信消息

搜索装备所相关美信消息，提取团队协作、技术分享、人员变动等信息�?
## 工作流程

### 1. 数据提取

```python
# �?IMRC 系统提取数据
python scripts/extractor.py --month 2026-07
```

### 2. 美信消息收集

```python
# 收集装备所相关美信消息
python scripts/meixin_collector.py --days 30
```

### 3. 报告生成

```python
# 生成完整报告
python scripts/report_generator.py --month 2026-07 --output report.md
```

## 报告结构

### 第一页：整体介绍�?0分钟汇报�?
```markdown
# 智能装备研究所 {YYYY}年{M}月运营报�?## 汇报人：尹德�?| 日期：{YYYY-MM-DD}

### 一、核心指标速览
| 指标 | 本月 | 上月 | 环比 | 年度目标 | 完成�?|
|------|------|------|------|---------|--------|
| 在研项目�?| | | | | |
| 本月交付项目 | | | | | |
| 合同金额（万元） | | | | | |
| 营收（万元） | | | | | |
| 投资执行�?| | | | | |
| 超预算项目数 | | | | | |

### 二、三大研究室概况
| 研究�?| 项目�?| 交付�?| 营收(�? | 投资(�? | 关键进展 |
|--------|--------|--------|---------|---------|---------|
| 机电系统 | | | | | |
| 工业视觉 | | | | | |
| 物流自动�?| | | | | |

### 三、风险预警（Top 3�?1. [风险1]
2. [风险2]
3. [风险3]

### 四、下月重�?1. [重点1]
2. [重点2]
3. [重点3]
```

### 后续分项报告

1. **项目运营情况详细分析**
2. **预算执行与超预算分析**
3. **合同签约与执行分�?*
4. **重点项目进展**
5. **预付款逾期分析**
6. **投资分析**
7. **异常合同说明**
8. **美信消息摘要**

## 配置

- **页面配置**: `config/pages.json`
- **报告模板**: `config/report_template.md`
- **数据目录**: `memory/imrc_data/`
- **筛选条�?*: `装备所|智能装备研究所|智能装备`

## 输出

- Markdown 格式报告
- 可选：导出�?PPT（调�?pptx skill�?
## 测试

```bash
python scripts/test_imrc_report.py
```
