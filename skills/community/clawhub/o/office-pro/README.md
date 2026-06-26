# OpenClaw Office Pro

**企业级文档自动化套件 - 专为AI Agent设计**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 安装

```bash
pip install python-docx openpyxl
```

## 快速开始

### 生成合同

```python
from office_pro import generate_contract

# 车位租赁合同
generate_contract('parking_lease',
    party_a='张三', party_b='李四',
    location='XX小区地下停车场',
    space_number='A-123',
    monthly_rent=500,
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# 其他合同类型
generate_contract('house_lease', ...)    # 房屋租赁
generate_contract('labor', ...)          # 劳动合同
generate_contract('sales', ...)          # 销售合同
generate_contract('service', ...)        # 服务合同
generate_contract('purchase', ...)       # 采购合同
generate_contract('nda', ...)            # 保密协议
generate_contract('cooperation', ...)    # 合作协议
generate_contract('loan', ...)           # 借款合同
generate_contract('commission', ...)     # 委托合同
```

### 生成Excel

```python
from office_pro import generate_excel

generate_excel('financial_report', company_name='XX公司')  # 财务报表
generate_excel('project_schedule', ...)   # 项目进度表
generate_excel('employee_roster', ...)    # 员工花名册
generate_excel('asset_inventory', ...)    # 资产清单
generate_excel('expense_report', ...)     # 费用报销单
generate_excel('invoice', ...)            # 发票管理表
```

### 生成报告

```python
from office_pro import generate_report

generate_report('meeting_minutes', meeting_title='Q1规划会议', ...)
generate_report('work_report', reporter='张三', ...)
```

## 可用模板

### 合同模板 (10种)

| ID | 名称 | ID | 名称 |
|---|------|---|------|
| `parking_lease` | 车位租赁 | `sales` | 销售合同 |
| `house_lease` | 房屋租赁 | `service` | 服务合同 |
| `labor` | 劳动合同 | `purchase` | 采购合同 |
| `nda` | 保密协议 | `cooperation` | 合作协议 |
| `loan` | 借款合同 | `commission` | 委托合同 |

### Excel模板 (6种)

| ID | 名称 | ID | 名称 |
|---|------|---|------|
| `financial_report` | 财务报表 | `project_schedule` | 项目进度表 |
| `employee_roster` | 员工花名册 | `asset_inventory` | 资产清单 |
| `expense_report` | 费用报销单 | `invoice` | 发票管理表 |

### 报告模板 (2种)

| ID | 名称 |
|---|------|
| `meeting_minutes` | 会议纪要 |
| `work_report` | 工作报告 |

## 高级功能（可选）

### Excel图表

```python
from office_pro import create_chart

create_chart('report.xlsx') \
    .add_bar_chart('Sheet1', 'A1:B10', '销售数据') \
    .add_pie_chart('Sheet1', 'C1:D5', '占比分析') \
    .save()
```

### Word高级样式

```python
from office_pro import create_styled_document

create_styled_document() \
    .add_styled_heading('报告', color='1F4E79') \
    .add_table_with_style([['项目', '金额'], ['收入', '100万']]) \
    .add_picture('chart.png', width=6) \
    .save('report.docx')
```

## 工具函数

```python
from office_pro import list_templates, num_to_chinese

# 列出所有模板
list_templates()
# {'contracts': [...], 'reports': [...], 'excel': [...]}

# 数字转中文大写
num_to_chinese(15000)  # 壹万伍仟
```

## 许可证

MIT License

---

**Made for OpenClaw Community**
