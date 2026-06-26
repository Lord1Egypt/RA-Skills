---
name: Office Pro
slug: office-pro
version: 1.2.0
description: "Enterprise document automation suite for AI Agents. Generate professional Word contracts and Excel reports with one function call. Built-in 10 contract templates, 6 Excel templates, and report templates. No external template files required."
changelog: "v1.2.0 - Simplified API for AI Agents, built-in templates, removed external dependencies."
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["python3"],"pip":["python-docx","openpyxl"]},"os":["linux","darwin","win32"]}}
---

# Office Pro - 企业级文档自动化套件

专为 AI Agent 设计的文档生成工具，一键生成专业合同和报表。

## 核心功能

- **一键生成**：无需外部模板文件，内置完整条款
- **合同模板**：10种专业合同（车位租赁、房屋租赁、劳动合同等）
- **Excel模板**：6种报表模板（财务报表、项目进度、员工花名册等）
- **报告模板**：会议纪要、工作报告
- **高级功能**：Excel图表、Word高级样式（可选）

## API Schema

### generate_contract
生成合同文档

```json
{
  "input": {
    "type": "object",
    "required": ["contract_type"],
    "properties": {
      "contract_type": {
        "type": "string",
        "enum": ["parking_lease", "house_lease", "labor", "sales", "service", "purchase", "nda", "cooperation", "loan", "commission"],
        "description": "Contract type ID"
      },
      "party_a": {"type": "string", "description": "Party A name"},
      "party_b": {"type": "string", "description": "Party B name"},
      "location": {"type": "string", "description": "Location/address"},
      "monthly_rent": {"type": "number", "description": "Monthly rent (yuan)"},
      "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
      "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"},
      "output": {"type": "string", "description": "Output filename (optional)"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "success": {"type": "boolean"},
      "output_path": {"type": "string"},
      "message": {"type": "string"}
    }
  }
}
```

### generate_excel
生成Excel报表

```json
{
  "input": {
    "type": "object",
    "required": ["excel_type"],
    "properties": {
      "excel_type": {
        "type": "string",
        "enum": ["financial_report", "project_schedule", "employee_roster", "asset_inventory", "expense_report", "invoice"],
        "description": "Excel template type ID"
      },
      "company_name": {"type": "string", "description": "Company name"},
      "output": {"type": "string", "description": "Output filename (optional)"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "success": {"type": "boolean"},
      "output_path": {"type": "string"},
      "message": {"type": "string"}
    }
  }
}
```

### generate_report
生成报告文档

```json
{
  "input": {
    "type": "object",
    "required": ["report_type"],
    "properties": {
      "report_type": {
        "type": "string",
        "enum": ["meeting_minutes", "work_report"],
        "description": "Report type ID"
      },
      "meeting_title": {"type": "string", "description": "Meeting title (for meeting_minutes)"},
      "meeting_date": {"type": "string", "description": "Meeting date"},
      "reporter": {"type": "string", "description": "Reporter name (for work_report)"},
      "output": {"type": "string", "description": "Output filename (optional)"}
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "success": {"type": "boolean"},
      "output_path": {"type": "string"},
      "message": {"type": "string"}
    }
  }
}
```

### list_templates
列出可用模板

```json
{
  "input": {
    "type": "object",
    "properties": {
      "category": {
        "type": "string",
        "enum": ["contract", "excel", "report", null],
        "default": null,
        "description": "Template category (null for all)"
      }
    }
  },
  "output": {
    "type": "object",
    "properties": {
      "contracts": {"type": "array", "items": {"type": "string"}},
      "excel": {"type": "array", "items": {"type": "string"}},
      "reports": {"type": "array", "items": {"type": "string"}}
    }
  }
}
```

## 可用模板

### 合同模板 (10种)

| ID | 名称 | ID | 名称 |
|---|------|---|------|
| `parking_lease` | 车位租赁合同 | `sales` | 销售合同 |
| `house_lease` | 房屋租赁合同 | `service` | 服务合同 |
| `labor` | 劳动合同 | `purchase` | 采购合同 |
| `nda` | 保密协议 | `cooperation` | 合作协议 |
| `loan` | 借款合同 | `commission` | 委托合同 |

### Excel模板 (6种)

| ID | 名称 |
|---|------|
| `financial_report` | 财务报表 |
| `project_schedule` | 项目进度表 |
| `employee_roster` | 员工花名册 |
| `asset_inventory` | 资产清单 |
| `expense_report` | 费用报销单 |
| `invoice` | 发票管理表 |

### 报告模板 (2种)

| ID | 名称 |
|---|------|
| `meeting_minutes` | 会议纪要 |
| `work_report` | 工作报告 |

## 使用示例

### Python API

```python
from office_pro import generate_contract, generate_excel, generate_report

# 生成车位租赁合同
generate_contract('parking_lease',
    party_a='张三', party_b='李四',
    location='XX小区地下停车场',
    space_number='A-123',
    monthly_rent=500,
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# 生成财务报表
generate_excel('financial_report', company_name='XX公司')

# 生成会议纪要
generate_report('meeting_minutes',
    meeting_title='Q1规划会议',
    meeting_date='2024-03-15'
)
```

### 高级功能（可选）

```python
from office_pro import create_chart, create_styled_document

# Excel图表
create_chart('report.xlsx') \
    .add_bar_chart('Sheet1', 'A1:B10', '销售数据') \
    .save()

# Word高级样式
create_styled_document() \
    .add_styled_heading('报告', color='1F4E79') \
    .add_table_with_style([['项目', '金额'], ['收入', '100万']]) \
    .save('report.docx')
```

## 安装依赖

```bash
pip install python-docx openpyxl
```

## 许可协议

MIT License
