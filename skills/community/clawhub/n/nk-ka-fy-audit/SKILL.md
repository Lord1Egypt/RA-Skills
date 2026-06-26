---
name: 内控-集团客户部FY审计
description: 集团客户部FY审计工具。当用户要求"审计返佣"、"核查KA返佣"、"核对返佣数据"、"检查返佣表"、"返佣对账"或类似场景时使用。本技能自动识别各月KA返佣工作表结构，从原始数据独立重算返佣金额并与汇总表比对，发现数据差异和规则执行问题，输出结构化审计报告。支持增量追加新月份数据到SQLite数据库，不修改历史数据。
---

# 内控-集团客户部FY审计

> 核心原则：**"表格公式对了，不等于算出来的结果对了。必须用原始数据独立重算，才能发现数据入口错误。"**

## 触发条件

用户提到以下关键词时使用此 skill：
- "审计返佣" / "核查KA返佣" / "核对返佣数据"
- "检查返佣表" / "返佣对账" / "出审计报告"
- "审计2026XX" 或 "审计YYYYMM"（新月份入库）
- "重新审计" / "增量审计"

## 标准工作流（两阶段法）

### 阶段A：新月份数据入库
1. 打开 xlsx 文件，探测所有 Sheet 结构
2. 与已知 4 种结构变体（A/B/C/D，见 `references/01-structure-variants.md`）匹配
3. 若有从未见过的 Sheet 名，先打印前5行询问分类和公式
4. 按匹配的变体解析全部 Sheet → INSERT 到 `raw_records` 表
5. ⚠️ **仅在此时读取 Excel 计算表**，其他情况不读

### 阶段B：快速全量重算（默认模式）
1. 从 `raw_records` 表读取所有月份的原始字段
2. 从 Excel 汇总表读取汇总金额（只需 "汇总" Sheet）
3. 按 `calc_method` 分类型使用对应公式独立重算（见 `references/02-recalculation-methodology.md`）
4. 与汇总表逐月比对 → 输出审计报告

## 报告交付物

每次审计完成后**同时交付**以下两个报告：

### Word版报告（面向管理层）
- 命名：`集团客户部FY审计报告（YYYYMM~YYYYMM）.docx`
- 6章框架：审计结论 → 数据分析（趋势图+TOP10图表）→ 重点核实事项 → 审计结果明细说明 → 方法论
- 结论开头标准表述："经审计集团客户部{年}年{月}月至{年}年{月}月返佣计算表，发现疑似多支付返佣{金额}元"
- 差异标准：|差额|≤1元→通过，|差额|>1元→差异

### Excel版报告（面向被审计方）
- 命名：`集团客户部FY审计结果明细（YYYYMM~YYYYMM）.xlsx`
- Sheet：审计摘要 → 月度趋势 → 审计结果-多发&历史调差明细 → 品牌增长预警
- 基于模版填充，数据从SQLite计算

### 存储规则
- 所有文件只保存到用户**个人云文档（飞书云盘）**，不写入知识库
- 仅保存最新版，旧版先删除再上传新文件

## 关键约束

| 规则 | 说明 |
|------|------|
| **不改历史** | 除非用户明确要求，不修改任何历史月份的记录 |
| **增量追加** | 新月份数据只INSERT，不UPDATE/DELETE |
| **结构探测** | 未知Sheet先问用户 |
| **中快Like匹配** | `LIKE '中快%'` 而非精确匹配 |
| **志华不重复** | 只通过calc_method计入 |
| **SQL表排除** | 202602的sql表不计入汇总 |
| **异常表排除** | 默认排除，仅 `audit_note=历史差额调整` 的补充 |
| **重算粒度** | 逐行 ROUND(txn×rate,2) 再按品牌SUM |

## 重算公式速查

| calc_method | 公式 |
|-------------|------|
| regular | ROUND(txn×rate,2) 每通道，∑ |
| zhongkuai | 直接用 total_rebate |
| expansion_307 | ROUND(txn×(fee-mer_rate-cost)×ch_ratio,2)，**必须读Excel** |
| expansion_308 | ROUND(txn×yield×ch_ratio,2)，**读Excel或用total_rebate** |
| sql_recalc | total_rebate（202602跳过） |
| abnormal | 不计入重算（见 `references/03-abnormal-rules.md`） |

## Skill目录脚本

`scripts/` 目录下包含12个脚本，按用途分类：

- **核心流程**：`parse_one_month.py`（Excel→DB入库）、`generate_comprehensive_report.py`（生成Word+Excel报告）
- **批量处理**：`batch_process.py` / `batch_reparse.py` / `batch_reparse_all.py` / `batch_summaries.py`
- **数据库**：`rebuild_db.py` / `restore_db.py` / `restore_raw_records.py`
- **返佣信息表**：`parse_fanyong_table.py` / `analyze_fanyong.py`

所有脚本位置：`/workspace/skills/内控-集团客户部FY审计/scripts/`

## 参考文档

| 文件 | 内容 |
|------|------|
| `references/01-structure-variants.md` | 4种结构变体（A/B/C/D）+ 特殊表格 + 英文列名映射 |
| `references/02-recalculation-methodology.md` | 完整重算公式 + 比对逻辑 |
| `references/03-abnormal-rules.md` | 异常表备注规则 + 区块标题继承机制 |
| `references/04-database-schema.md` | 数据库表结构 + 增量入库流程 |
| `references/05-historical-errors.md` | 14个历史错误复盘 |
| `references/06-operating-norms.md` | 操作规范 + 检查清单 |