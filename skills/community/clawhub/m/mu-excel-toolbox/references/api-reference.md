# API Reference — mu-excel-toolbox

> 所有脚本位于 `scripts/` 目录下
> 通用参数：大部分脚本支持 `--format`（json/csv/markdown/table）控制输出格式

---

## 1. peek.py — 智能预览

```bash
python3 peek.py <input_file> [--rows N] [--format FORMAT]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | Excel/CSV 文件路径 | 必填 |
| --rows | 预览行数 | 5 |
| --format | 输出格式(json/markdown/table) | table |

**示例：**
```bash
python3 peek.py sales.xlsx --rows 3
```

---

## 2. read_excel.py — 读取 Excel

```bash
python3 read_excel.py <input_file> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 文件路径 | 必填 |
| --sheet | Sheet 名或索引 | 第一个 |
| --range | 范围如 A1:D100 | 全部 |
| --columns | 列名列表(逗号分隔) | 全部 |
| --rows | 行范围如 1-100 | 全部 |
| --filter | 筛选条件 "列名 op 值" | 无 |
| --header-row | 表头行号 | 1 |
| --format | 输出格式 | table |

**示例：**
```bash
python3 read_excel.py data.xlsx --sheet Sheet2 --columns "姓名,部门,工号" --format json
python3 read_excel.py data.xlsx --filter "年龄 > 30" --format markdown
```

---

## 3. write_excel.py — 写入/创建

```bash
python3 write_excel.py --output <path> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --output | 输出路径 | 必填 |
| --sheet | Sheet 名 | Sheet1 |
| --data | JSON 数据或文件路径 | stdin |
| --headers | 列头列表(逗号分隔) | 从数据推断 |
| --append | 追加到已有文件 | false |
| --col-width | 列宽（数字或 'auto'，默认自动） | auto |
| --no-freeze | 不冻结首行（默认冻结） | false |

**示例：**
```bash
python3 write_excel.py --output report.xlsx --data '[{"name":"张三","age":28}]'
echo '[{"a":1},{"a":2}]' | python3 write_excel.py --output out.xlsx
```

---

## 4. convert.py — 格式互转

```bash
python3 convert.py <input_file> --to <FORMAT> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 源文件 | 必填 |
| --to | 目标格式(xlsx/csv/json/markdown/tsv) | 从 --output 推断 |
| --output | 输出路径 | 自动命名 |
| --sheet | 指定 Sheet | 第一个 |
| --encoding | 编码 | utf-8 |
| --delimiter | CSV 分隔符 | , |

**示例：**
```bash
python3 convert.py data.xlsx --to csv --output data.csv
python3 convert.py report.csv --to xlsx --encoding gbk
```

---

## 5. merge.py — 合并文件

```bash
python3 merge.py <file1> <file2> [...] --output <path> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_files | 多个文件路径 | 必填 |
| --output | 输出路径 | 必填 |
| --mode | concat/horizontal/by-sheet | concat |
| --sheet | 指定 Sheet | 全部 |
| --ignore-headers | 第2个文件起跳过表头 | false |

**示例：**
```bash
python3 merge.py jan.xlsx feb.xlsx mar.xlsx --output q1.xlsx --ignore-headers
python3 merge.py data1.xlsx data2.xlsx --output combined.xlsx --mode horizontal
```

---

## 6. split.py — 拆分文件

```bash
python3 split.py <input_file> --output-dir <dir> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 源文件 | 必填 |
| --output-dir | 输出目录 | ./split_output |
| --mode | by-sheet / by-column | by-sheet |
| --column | 按列拆分时的列名 | 无 |
| --naming | 命名规则 | 列值/Sheet名 |

**示例：**
```bash
python3 split.py all_data.xlsx --output-dir ./by_dept --mode by-column --column 部门
python3 split.py workbook.xlsx --output-dir ./sheets --mode by-sheet
```

---

## 7. vlookup.py — 多表关联

```bash
python3 vlookup.py --main <file> --lookup <file> --key <col> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --main | 主表文件 | 必填 |
| --lookup | 查找表文件 | 必填 |
| --key | 关联列名 | 必填 |
| --columns | 要匹配的列(逗号分隔) | 全部 |
| --output | 输出路径 | 必填 |
| --how | left/inner/outer | left |
| --main-sheet | 主表 Sheet | 第一个 |
| --lookup-sheet | 查找表 Sheet | 第一个 |

**示例：**
```bash
python3 vlookup.py --main roster.xlsx --lookup attendance.xlsx --key 工号 --columns "出勤天数,迟到次数" --output result.xlsx
```

---

## 8. dedup.py — 去重

```bash
python3 dedup.py <input_file> --columns <cols> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| input_file | 源文件 | 必填 |
| --columns | 去重依据列(逗号分隔) | 全部列 |
| --keep | first/last/none | first |
| --output | 输出路径 | 覆盖原文件 |
| --report | 去重报告路径 | 无 |

**示例：**
```bash
python3 dedup.py contacts.xlsx --columns "姓名,手机号" --keep last --output clean.xlsx --report dup_report.xlsx
```

---

## 9. clean.py — 数据清洗

```bash
python3 clean.py <input_file> --output <path> [--rules RULES_JSON]
```

| 规则类型 | 说明 | 参数 |
|---------|------|------|
| remove_empty_rows | 删除空行 | — |
| trim_spaces | 去除前后空格 | columns(可选) |
| normalize_phone | 手机号统一11位 | column |
| normalize_date | 日期统一格式 | column, format(如%Y-%m-%d) |
| normalize_case | 大小写统一 | column, case(upper/lower/title) |
| fill_empty | 填充空值 | column, method(value/ffill/bfill), value |
| remove_duplicates | 简单去重 | columns |
| type_convert | 类型转换 | column, dtype(int/float/str/date) |

**示例：**
```bash
python3 clean.py raw.xlsx --output clean.xlsx --rules '[{"type":"remove_empty_rows"},{"type":"normalize_phone","column":"手机"},{"type":"normalize_date","column":"入职日期","format":"%Y-%m-%d"}]'
```

---

## 10. template_fill.py — 模板填充

```bash
python3 template_fill.py --template <file> --data <file> --output-dir <dir> [OPTIONS]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --template | 模板文件(含{{占位符}}) | 必填 |
| --data | 数据文件(JSON/CSV/Excel) | 必填 |
| --output-dir | 输出目录 | ./filled |
| --naming | 命名规则如 {{姓名}}_offer.xlsx | row_N.xlsx |
| --single | 所有数据填入同一文件不同Sheet | false |

**占位符语法：** `{{字段名}}`，字段名与数据列名完全一致

**示例：**
```bash
python3 template_fill.py --template offer_template.xlsx --data employees.csv --output-dir ./offers --naming "{{姓名}}_offer.xlsx"
```

---

## 11. validate.py — 数据校验

```bash
python3 validate.py <input_file> --rules <RULES> [OPTIONS]
```

| 规则类型 | 说明 | 参数 |
|---------|------|------|
| required | 必填 | column |
| unique | 唯一性 | column |
| type | 类型检查 | column, dtype(number/date/email/phone/idcard) |
| range | 范围 | column, min, max |
| pattern | 正则 | column, regex |
| enum | 枚举 | column, values[] |
| length | 长度 | column, min_len, max_len |
| cross_field | 跨字段逻辑 | expression(如 "开始日期 < 结束日期") |

**示例：**
```bash
python3 validate.py staff.xlsx --rules '[{"type":"required","column":"工号"},{"type":"type","column":"邮箱","dtype":"email"},{"type":"unique","column":"工号"}]' --output report.json
```

---

## 12. style.py — 样式排版 + 条件格式

```bash
# 样式模式
python3 style.py <input_file> --output <path> [STYLE_OPTIONS]
# 条件格式模式
python3 style.py <input_file> --output <path> --mode conditional [COND_OPTIONS]
```

**样式参数：** `--header-bold` `--header-bg COLOR` `--border all/outer/none` `--auto-width` `--freeze-row N` `--font NAME` `--font-size N`

**条件格式参数：** `--column COL` `--rule gt/lt/eq/between/contains/top_n/bottom_n` `--value VAL` `--color COLOR` `--font-color COLOR`

**示例：**
```bash
python3 style.py data.xlsx --output styled.xlsx --header-bold --header-bg 4472C4 --auto-width --border all
python3 style.py scores.xlsx --output highlighted.xlsx --mode conditional --column 绩效分 --rule lt --value 60 --color FF0000
```

---

## 13. formula.py — 函数公式

```bash
python3 formula.py <input_file> --output <path> [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --column | 目标列(如 E) |
| --formula | 公式模板(用{row}占位) |
| --range | 应用范围(如 2:100) |
| --auto-sum | 末尾加SUM |
| --auto-average | 末尾加AVERAGE |
| --sum-columns | 指定列求和 |
| --average-columns | 指定列求平均 |

**示例：**
```bash
python3 formula.py data.xlsx --output result.xlsx --column E --sum-columns "B,C,D"
python3 formula.py data.xlsx --output result.xlsx --column F --formula "=B{row}*C{row}" --range "2:50"
```

---

## 14. chart.py — 图表生成

```bash
python3 chart.py <input_file> --output <path> --type TYPE [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --type | bar/line/pie/scatter/area/combo/doughnut/radar |
| --title | 图表标题 |
| --x-column | X轴数据列 |
| --y-columns | Y轴数据列(逗号分隔，支持多列) |
| --position | 图表位置(如 E2) |
| --size | 宽,高(如 720,480) |
| --combo | 组合图表配置 |

**示例：**
```bash
python3 chart.py sales.xlsx --output report.xlsx --type bar --x-column 月份 --y-columns "销售额,目标" --title "月度销售对比"
python3 chart.py data.xlsx --output report.xlsx --type combo --x-column 月份 --y-columns "收入,利润率" --combo "收入:bar,利润率:line"
```

---

## 15. pivot.py — 数据透视表

```bash
python3 pivot.py <input_file> --output <path> --rows ROWS --values VALUES [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --rows | 行字段(逗号分隔) |
| --columns | 列字段(逗号分隔) |
| --values | 值字段(逗号分隔) |
| --aggfunc | 聚合函数(sum/mean/count/max/min) |
| --margins | 加汇总行列 |
| --fill-value | 空值填充 |
| --sort-by | 排序依据 |
| --format | 输出格式 |

**示例：**
```bash
python3 pivot.py sales.xlsx --output pivot.xlsx --rows 部门 --columns 月份 --values 销售额 --aggfunc sum --margins
```

---

## 16. analyze.py — 数据分析

```bash
python3 analyze.py <input_file> [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --columns | 分析指定列 |
| --output | 报告输出路径 |
| --format | 输出格式 |
| --detail | brief/full |

**输出包含：** 基础统计 + 数值列统计(均值/中位数/标准差/分位数) + 文本列统计(唯一值/TOP5) + 相关性矩阵 + 异常值检测

**示例：**
```bash
python3 analyze.py employee_data.xlsx --detail full --format markdown
```

---

## 17. diff.py — 差异对比

```bash
python3 diff.py --old <file> --new <file> --key <col> [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --old | 旧文件 |
| --new | 新文件 |
| --key | 主键列 |
| --output | 报告路径 |
| --highlight | 生成高亮Excel |
| --ignore-columns | 忽略列 |
| --format | 报告格式 |

**示例：**
```bash
python3 diff.py --old roster_v1.xlsx --new roster_v2.xlsx --key 工号 --highlight --output diff_report.xlsx
```

---

## 18. image.py — 图片插入

```bash
python3 image.py <input_file> --output <path> --column COL [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --column | 图片放置列 |
| --images | 图片路径列表或目录 |
| --match-by | 按哪列匹配文件名 |
| --size | 图片尺寸(width,height) |
| --start-row | 起始行 |

**示例：**
```bash
python3 image.py staff.xlsx --output with_photos.xlsx --column F --images ./photos/ --match-by 工号 --size 80,100
```

---

## 19. protect.py — 密码保护

```bash
python3 protect.py <input_file> --output <path> --mode MODE --password PWD [OPTIONS]
```

| 参数 | 说明 |
|------|------|
| --mode | encrypt/decrypt/sheet-protect |
| --password | 密码 |
| --sheet-protect | 保护指定Sheet |
| --allow | 允许操作(select_cells/sort/filter) |

**示例：**
```bash
python3 protect.py salary.xlsx --output salary_locked.xlsx --mode encrypt --password "s3cret"
python3 protect.py locked.xlsx --output unlocked.xlsx --mode decrypt --password "s3cret"
```
