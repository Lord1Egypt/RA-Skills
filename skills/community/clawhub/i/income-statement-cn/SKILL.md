# 财务报表生成技能

## 技能概述
根据明细表数据自动生成规范化利润表，支持动态行数扩展。

## 核心规则

### 数据提取规则

**收入类：**
- 来源：明细表中 分类 1 = "收入" 或 "实收"
- 取值优先级：
  1. 优先取"发生金额"列（列 8）
  2. 其次取"收入金额"列（列 6）
- 分组：按 分类 2 和 分类 3 两级分组汇总

**支出类：**
- 来源：明细表中 分类 1 = "支出"
- 取值优先级：
  1. 优先取"发生金额"列（列 8）
  2. 其次取"支出金额"列（列 7）
- 分组：按 分类 2 和 分类 3 两级分组汇总

### 利润表格式规范

**列结构：**
| 列 | 内容 | 宽度 |
|----|------|------|
| B | 标题（收入/支出/经营利润） | 15 |
| C | 分类 2（工作坊/个案/导师费等） | 12 |
| D | 分类 3（具体项目名称） | 40 |
| E | 金额 | 15 |
| F | 空白 | 40 |

**行结构：**
1. **标题行**：合并 B1:F1，"利润表 YYYYMM"居中，粗体
2. **收入区块**：
   - 行 3：B3="收入"（粗体），E3=合计公式（粗体）
   - 行 4+：分类 2 标题（如"工作坊"），E 列=小计
   - 后续行：D 列=分类 3 明细，E 列=金额（动态行数）
3. **支出区块**：
   - 标题行：B 列="支出"（粗体），E 列=合计（粗体）
   - 分类 2 标题行（导师费/场地费等），E 列=小计
   - 明细行：D 列=分类 3，E 列=金额（动态行数）
4. **经营利润行**：B 列="经营利润"（粗体），E 列=公式（粗体）

**格式要求：**
- 无边框
- "收入"、"支出"、"经营利润"文字粗体
- 三者对应金额粗体
- F 列留空，宽度与 D 列相同（40）

## 代码模板

```python
#!/usr/bin/env python3
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, Alignment
import glob

def create_income_statement(source_file, output_file):
    """
    根据明细表生成利润表
    
    Args:
        source_file: 源 Excel 文件路径（含明细表）
        output_file: 输出利润表路径
    """
    wb_source = load_workbook(source_file)
    ws_detail = wb_source['明细']
    
    # 数据提取
    income_by_cat2_cat3 = {}
    expense_by_cat2_cat3 = {}
    
    for row in range(2, ws_detail.max_row + 1):
        cat1 = ws_detail.cell(row=row, column=3).value
        cat2 = ws_detail.cell(row=row, column=4).value
        cat3 = ws_detail.cell(row=row, column=5).value
        income_amt = ws_detail.cell(row=row, column=6).value
        expense_amt = ws_detail.cell(row=row, column=7).value
        amount = ws_detail.cell(row=row, column=8).value
        
        # 收入：优先发生金额
        if cat1 in ['收入', '实收']:
            amt = amount if amount else (income_amt if income_amt else 0)
            if amt and amt > 0:
                if cat2 not in income_by_cat2_cat3:
                    income_by_cat2_cat3[cat2] = {}
                if cat3 not in income_by_cat2_cat3[cat2]:
                    income_by_cat2_cat3[cat2][cat3] = 0
                income_by_cat2_cat3[cat2][cat3] += amt
        
        # 支出：优先发生金额
        if cat1 == '支出':
            amt = amount if amount else (expense_amt if expense_amt else 0)
            if amt and amt > 0:
                if cat2 not in expense_by_cat2_cat3:
                    expense_by_cat2_cat3[cat2] = {}
                if cat3 not in expense_by_cat2_cat3[cat2]:
                    expense_by_cat2_cat3[cat2][cat3] = 0
                expense_by_cat2_cat3[cat2][cat3] += amt
    
    # 创建工作簿
    wb = Workbook()
    ws = wb.active
    ws.title = '利润表'
    
    # 样式
    title_font = Font(name='微软雅黑', size=12, bold=True)
    bold_font = Font(name='微软雅黑', size=10, bold=True)
    
    # === 填写数据 ===
    # 标题行
    ws.merge_cells('B1:F1')
    ws['B1'] = '利润表 YYYYMM'  # 替换实际月份
    ws['B1'].font = title_font
    ws['B1'].alignment = Alignment(horizontal='center', vertical='center')
    
    # 收入部分
    ws['B3'] = '收入'
    ws['B3'].font = bold_font
    
    # 动态填充收入明细...
    # （按分类 2 标题 + 分类 3 明细的顺序）
    
    # 支出部分
    # （按分类 2 标题 + 分类 3 明细的顺序）
    
    # 经营利润
    # E 列 = E3 - 支出合计行
    
    # F 列留空
    for r in range(2, max_data_row + 1):
        ws.cell(row=r, column=6, value='')
    
    # 列宽
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 40
    ws.column_dimensions['E'].width = 15
    ws.column_dimensions['F'].width = 40
    
    wb.save(output_file)
```

## 使用示例

```python
# 生成 202601 利润表
create_income_statement(
    source_file='/Users/zhengyong/.openclaw/qqbot/downloads/财务报表 202601-claw_1774271697631.xlsx',
    output_file='/Users/zhengyong/.openclaw/workspace/利润表 202601_明细生成.xlsx'
)
```

## 关键要点

1. **动态行数**：有多少明细项目就占多少行，不固定
2. **金额优先级**：发生金额 > 收入/支出金额
3. **分类层级**：分类 2 是标题，分类 3 是明细
4. **格式统一**：收入/支出/经营利润粗体 + 金额粗体
5. **F 列预留**：宽度 40，留空备用

## 文件位置

- **输入**：`/Users/zhengyong/.openclaw/qqbot/downloads/财务报表 YYYYMM*.xlsx`
- **输出**：`/Users/zhengyong/.openclaw/workspace/利润表 YYYYMM_明细生成.xlsx`
- **脚本**：`/Users/zhengyong/.openclaw/workspace/create_income_YYYYMM_simple.py`

---
*创建时间：2026-03-23*
*最后更新：2026-03-23*
