---
name: pans-excel
description: |
  全功能智能 Excel 处理专家。功能：数据分析 | 图表可视化(7种) | 数据处理 | 报表模板(7种) | AI智能 | CSV/JSON导入导出 | 数据验证 | PDF导出 | 数据清洗。
  触发词：Excel处理, 表格分析, 数据可视化, 图表制作, 公式生成, 报表生成, 销售看板, 财务分析, 对账清单, CSV导入, JSON导出, PDF导出, 数据清洗
---

# PansExcel Pro Max

## 命令速查

| 命令 | 功能 |
|------|------|
| `create` | 从数据创建 Excel |
| `report` | 生成专业报表（7种模板） |
| `analyze` | AI 智能分析数据 |
| `formula` | 自然语言生成公式 |
| `chart` | 添加图表（7种） |
| `format` | 一键美化 |
| `cond` | 条件格式（7种） |
| `dv` | 数据验证（下拉/数字/日期/文本长度） |
| `clean` | 数据清洗管道 |
| `split` | 分列（按分隔符） |
| `import` | CSV/JSON → XLSX |
| `export` | XLSX → CSV/JSON/PDF |
| `pdf` | 直接导出 PDF |
| `merge` | 合并多个 Excel |
| `insights` | AI 数据洞察 |

---

## create - 创建 Excel

```bash
python3 scripts/excel.py create -d '{"部门":["华东","华南"],"销售额":[125,98],"利润":[31,20]}' -o out.xlsx
```

## report - 报表模板（7种）

```bash
# 销售看板 - KPI卡片+柱状图+饼图
python3 scripts/excel.py report -d '{"部门":["华东","华南"],"销售额":[100,200],"利润":[30,50]}' -t sales -o 看板.xlsx

# 财务报表
python3 scripts/excel.py report -d '{"项目":["收入","成本","利润"],"Q1":[100,60,40],"Q2":[120,70,50]}' -t financial -o 财务.xlsx

# 项目甘特图（颜色随进度变化）
python3 scripts/excel.py report -d '{"项目":["A项目","B项目"],"进度":[80,50],"负责人":["张三","李四"]}' -t gantt -o 项目.xlsx

# 对账清单（正负自动标色）
python3 scripts/excel.py report -d '{"合同":["甲","乙"],"预算":[100,200],"实际":[110,190],"差异":[10,-10]}' -t recon -o 对账.xlsx

# 日报（状态自动标色）
python3 scripts/excel.py report -d '{"事项":["需求","开发"],"负责人":["张三"],"状态":["完成","进行中"]}' -t daily -o 日报.xlsx

# 周报
python3 scripts/excel.py report -d '{"日期":["周一","周二"],"完成任务":[3,5],"进行中":[2,1]}' -t weekly -o 周报.xlsx
```

## chart - 图表（7种）

```bash
python3 scripts/excel.py chart -f data.xlsx -t bar -T "销售对比" -p F2   # 柱状图
python3 scripts/excel.py chart -f data.xlsx -t line -T "趋势" -p F2       # 折线图
python3 scripts/excel.py chart -f data.xlsx -t pie -T "占比"                # 饼图
python3 scripts/excel.py chart -f data.xlsx -t area -T "堆积"                # 面积图
python3 scripts/excel.py chart -f data.xlsx -t radar -T "能力图"            # 雷达图
python3 scripts/excel.py chart -f data.xlsx -t combo -T "组合"              # 组合图
python3 scripts/excel.py chart -f data.xlsx -t scatter -T "分布"            # 散点图
```

## cond - 条件格式（7种）

```bash
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t scale  # 三色热力图
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t bar      # 数据条
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t icon    # 图标集
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t top     # Top N 高亮
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t avg     # 高于平均
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t gt -v 0  # 大于0标绿
python3 scripts/excel.py cond -f data.xlsx -r B2:B100 -t lt -v 0 # 小于0标红
```

## dv - 数据验证

```bash
# 下拉菜单
python3 scripts/excel.py dv -f data.xlsx -c 3 -t list -o "优,良,差"

# 数字范围（0-100）
python3 scripts/excel.py dv -f data.xlsx -c 4 -t number --min 0 --max 100

# 日期验证
python3 scripts/excel.py dv -f data.xlsx -c 5 -t date

# 文本长度限制
python3 scripts/excel.py dv -f data.xlsx -c 2 -t length --min-len 1 --max-len 50
```

## clean - 数据清洗

```bash
# 清洗管道：去重 → 填空 → 去首尾空格
python3 scripts/excel.py clean -f data.xlsx -s "dedup,blanks,trim"

# 转换为小写
python3 scripts/excel.py clean -f data.xlsx -s "lower"

# 数字清洗（文本→数字）
python3 scripts/excel.py clean -f data.xlsx -s "number"
```

## split - 分列

```bash
# 按逗号分列
python3 scripts/excel.py split -f data.xlsx -c 1 -d "," -o split.xlsx

# 按空格分列
python3 scripts/excel.py split -f data.xlsx -c 2 -d " " -o split.xlsx
```

## import / export - 格式转换

```bash
# CSV → Excel
python3 scripts/excel.py import -f data.csv -t xlsx -o out.xlsx

# JSON → Excel
python3 scripts/excel.py import -f data.json -t xlsx -o out.xlsx

# Excel → CSV
python3 scripts/excel.py export -f data.xlsx -t csv -o out.csv

# Excel → JSON
python3 scripts/excel.py export -f data.xlsx -t json -o out.json

# Excel → PDF（需安装 LibreOffice）
python3 scripts/excel.py pdf -f data.xlsx -o out.pdf
```

## merge - 合并文件

```bash
python3 scripts/excel.py merge -f a.xlsx b.xlsx c.xlsx -o merged.xlsx -k 1
```

## analyze / insights - AI 分析

```bash
# 完整分析
python3 scripts/excel.py analyze -f data.xlsx

# 仅洞察
python3 scripts/excel.py insights -f data.xlsx
```

## formula - 公式生成

```bash
python3 scripts/excel.py formula --描述 "计算毛利率" -c "利润,销售额"
python3 scripts/excel.py formula --描述 "统计大于1000的数量"
python3 scripts/excel.py formula --描述 "同比增长率"
python3 scripts/excel.py formula --描述 "IF条件"
```

## 视觉设计

| 元素 | 设计 |
|------|------|
| 主色调 | 现代蓝 #2E5BFF |
| 配色系 | 蓝/绿/橙/红/紫 5色循环 |
| 交替行 | 浅灰 #F8FAFC / 白色 |
| 图表 | 渐变配色 + 精细边框 |
| 字体 | 微软雅黑 |

## 数据格式

| 类型 | Excel 格式 |
|------|-----------|
| 金额 | ¥#,##0.00 |
| 百分比 | 0.00% |
| 数字 | #,##0 |
| 日期 | YYYY-MM-DD |
