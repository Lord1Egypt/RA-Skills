---
name: mu-excel-toolbox
version: 1.1
description: "Excel全能工具箱：读写、预览、合并、拆分、关联、去重、清洗、校验、模板填充、样式、条件格式、公式、图表、透视表、数据分析、差异对比、图片插入、密码保护。典型场景：月度业务报表合并汇总、HR花名册/考勤表关联清洗、运营数据透视分析、绩效数据校验去重、批量生成offer/通知模板、薪酬表加密保护、业务周报图表生成。触发词：Excel、表格、xlsx、csv、电子表格、合并Excel、拆分Excel、Excel图表、数据透视表、Excel公式、条件格式、数据清洗、Excel模板、Excel对比、Excel加密、VLOOKUP、去重、数据校验、统计分析、格式转换、业务报表、花名册、考勤表、绩效数据、运营数据、excel toolbox、spreadsheet、merge excel、split excel、excel chart、pivot table。即使用户没有明说'用Excel工具箱'，只要涉及Excel/表格/xlsx/csv文件的操作都应触发。不适用：在线协作编辑(用Google Sheets等在线工具)、纯代码开发、Skill管理。"
tags: Excel,表格,xlsx,csv,数据处理,图表,透视表,数据分析,工具箱
visibility: public
compatibility: "需要 Python 3.9+；首次使用自动安装依赖(openpyxl/pandas/xlsxwriter/xlrd/msoffcrypto-tool)"

---

**IRON LAW：①操作前必须先 peek 了解文件结构（WHY：盲操作=猜列名猜Sheet名，错误率极高）；②写入/修改操作必须保留原文件备份（WHY：Excel 操作不可逆，无备份=数据丢失风险）；③大文件（>10万行）必须用流式模式（WHY：全量加载会撑爆内存导致进程被 kill）；④输出文件路径必须用绝对路径并确认目录存在（WHY：相对路径在不同 cwd 下行为不一致）。**

## 功能路由表

> 根据用户意图匹配对应脚本。所有脚本位于 `scripts/` 目录下

| # | 功能 | 脚本 | 场景举例 |
|---|------|------|---------|
| 1 | 📋 智能预览 | `peek.py` | "帮我看看这个Excel有几个Sheet、每个Sheet有什么列" |
| 2 | 📖 读取Excel | `read_excel.py` | "读取sales.xlsx的Sheet2，取A~D列前100行" |
| 3 | ✏️ 写入/创建 | `write_excel.py` | "把这份数据生成一个Excel文件" |
| 4 | 🔄 格式互转 | `convert.py` | "把这个csv转成xlsx"、"把Excel导出为JSON" |
| 5 | 📎 合并文件 | `merge.py` | "把这5个月度报表合并成一个年度汇总表" |
| 6 | ✂️ 拆分文件 | `split.py` | "把大表按Sheet拆成独立文件" |
| 7 | ✂️ 按列值拆分 | `split.py --mode by-column` | "按'部门'列拆分，每个部门一个独立Excel" |
| 8 | 🔗 VLOOKUP/关联 | `vlookup.py` | "用工号把花名册和考勤表关联起来" |
| 9 | 🧹 去重 | `dedup.py` | "按姓名+手机号去重，保留最新的那条" |
| 10 | 🧽 数据清洗 | `clean.py` | "把空行删掉，手机号统一11位，日期统一YYYY-MM-DD" |
| 11 | 📄 模板填充 | `template_fill.py` | "用员工数据批量生成offer letter" |
| 12 | ✅ 数据校验 | `validate.py` | "检查哪些行邮箱格式不对、哪些工号重复了" |
| 13 | 🎨 条件格式 | `style.py --mode conditional` | "绩效低于60标红，高于90标绿" |
| 14 | 💅 样式排版 | `style.py` | "给表头加粗加背景色，列宽自适应，加边框" |
| 15 | 📐 函数公式 | `formula.py` | "在E列加SUM公式汇总B~D列" |
| 16 | 📊 图表生成 | `chart.py` | "用销售数据生成柱状图+折线图组合" |
| 17 | 📈 数据透视表 | `pivot.py` | "按部门和月份交叉汇总销售额" |
| 18 | 🔬 数据分析 | `analyze.py` | "给我这份数据的统计摘要：均值、中位数、分布" |
| 19 | 🔍 差异对比 | `diff.py` | "对比两版花名册，哪些人新增/离职/信息变更" |
| 20 | 🖼️ 图片插入 | `image.py` | "在每个员工对应行插入照片" |
| 21 | 🔒 密码保护 | `protect.py` | "给薪酬表加密码保护"、"解密这个加密的Excel" |
| 22 | ⚡ 大文件处理 | 自动触发 | 超10万行自动切换流式模式，坏行跳过并汇报 |

## 快速开始

### 环境准备（全自动，无需手动操作）

首次调用任何脚本时，`utils.py` 会自动检测并安装缺失依赖（版本锁定，120s 超时兆底）。安装完成后自动验证导入成功才继续执行。

手动安装（仅当自动安装失败时）：
```bash
cd scripts/
pip install -r requirements.txt
```

### 典型工作流
```bash
# 1. 先看文件结构
python3 peek.py input.xlsx

# 2. 根据需要操作
python3 read_excel.py input.xlsx --sheet Sheet1 --format json
python3 merge.py file1.xlsx file2.xlsx --output merged.xlsx
python3 chart.py data.xlsx --type bar --x-column 月份 --y-columns 销售额 --output report.xlsx
```

## 核心设计原则

1. **Peek First**：任何操作前先预览文件结构，避免盲操作
2. **安全写入**：修改操作自动备份原文件（`原文件名_backup_时间戳.xlsx`）
3. **流式处理**：>10 万行自动切换 `read_only`/`write_only` 模式，防止内存溢出
4. **错误容错**：遇到坏行/坏单元格跳过继续，最后汇总错误报告（ErrorCollector）
5. **统一输出**：所有脚本支持 `--format`（json/csv/markdown/table）
6. **管道友好**：支持 stdin/stdout，可与其他工具组合
7. **依赖自愈**：首次运行自动安装缺失依赖（版本锁定），安装后验证导入成功才继续
8. **编码自适应**：CSV 自动尝试 UTF-8/GBK/GB2312/Latin-1，无需用户指定

## 技术栈

| 库 | 用途 |
|------|------|
| openpyxl | 核心读写 + 样式 + 公式 |
| pandas | 数据分析 + 透视 + 清洗 |
| xlsxwriter | 高性能写入 + 图表渲染 |
| xlrd | .xls 旧格式只读兼容 |
| msoffcrypto-tool | 文件级加密/解密 |
| numpy | 数值计算（分析/清洗） |

## Gotchas

- **chart.py 用 xlsxwriter 不能修改已有文件**：它会新建文件写入数据+图表。如需在已有文件加图表，先用 openpyxl 读数据，再用 xlsxwriter 生成新文件
- **openpyxl 的 data_only=True 会丢失公式**：读取计算结果时用 `data_only=True`，但保存后公式消失。需要公式时不加此参数
- **条件格式的颜色值不带 #**：openpyxl 颜色用 6 位十六进制（如 `FF0000`），不要加 `#` 前缀
- **csv 编码**：Windows Excel 生成的 csv 常为 GBK/GB2312，用 `--encoding gbk` 参数处理
- **合并时列名对齐**：不同文件列名不完全一致时，用 concat 模式会自动对齐（缺失列填 NaN）
- **模板填充占位符**：使用 `{{字段名}}` 语法，字段名必须与数据源列名完全一致（含大小写）

## 子Agent最小执行规范

必读文件：`SKILL.md`

不可跳过的硬 Gate：
- 操作前必须 `peek.py` 了解文件结构
- 写入操作确认输出路径存在
- 大文件自动走流式模式

禁止行为：
- 禁止不 peek 直接操作（盲猜列名）
- 禁止覆盖原文件不备份
- 禁止全量加载 >10 万行的文件

## Anti-Pattern 清单

| # | 反模式 | 正确做法 |
|---|--------|---------|
| 1 | 不看文件结构直接操作 | 先 `peek.py` 确认 Sheet/列名/行数 |
| 2 | 猜测列名填参数 | 从 peek 结果中复制精确列名 |
| 3 | 大文件全量加载 | utils.py 自动检测并切换流式模式 |
| 4 | 覆盖原文件 | 输出到新路径或让 safe_write 自动备份 |
| 5 | 硬编码文件路径 | 用用户提供的路径，不假设固定位置 |
| 6 | 忽略错误继续 | 用 ErrorCollector 收集所有错误最后汇报 |

## Pre-Delivery Checklist

- [ ] 操作前已 peek 确认文件结构
- [ ] 输出路径已确认存在且可写
- [ ] 写入操作有原文件备份
- [ ] 大文件已走流式模式
- [ ] 错误已汇总报告给用户
- [ ] 输出格式符合用户要求

## references/ 索引

| 文件 | 说明 |
|------|------|
| [references/api-reference.md](references/api-reference.md) | 各脚本完整参数说明 + 代码示例 |
| [references/examples.md](references/examples.md) | 22 个功能的场景举例合集 |
