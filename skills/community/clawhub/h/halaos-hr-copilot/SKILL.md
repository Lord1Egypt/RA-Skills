---
name: halaos-hr-copilot
version: "2.1.0"
description: "AI HR Copilot for Southeast Asia. Works with HalaOS MCP Server for live data (employees, attendance, leave, payroll, compliance, org intelligence) or standalone with built-in PH/SG/LK labor law knowledge. Your HR department in a conversation."
user-invocable: true
emoji: "🏢"
homepage: "https://halaos.com"
metadata:
  openclaw:
    primaryEnv: "HALAOS_API_KEY"
    requires:
      env:
        - "HALAOS_API_KEY"
      config:
        - "~/.openclaw/skills/halaos-hr-copilot/config.json"
---

# HalaOS HR Copilot

Your AI HR copilot for Southeast Asia. Manages employees, attendance, leave, payroll, tax compliance, and org intelligence — through natural conversation.

## How It Works

This skill operates in two modes:

### Mode 1: MCP Server (Recommended — Full Platform Access)

When the **HalaOS MCP Server** is configured, the AI has direct access to 24 live HR tools — no HTTP calls, no API docs to read. Just use the MCP tools.

**Setup:**

1. Get your API key: Log into HalaOS → Settings → API Keys → Create New Key (starts with `halaos_`, shown only once)
2. Add to your MCP config (Claude Desktop, Claude Code, or any MCP client):

```json
{
  "mcpServers": {
    "halaos-hr": {
      "command": "/usr/local/bin/halaos-mcp",
      "env": {
        "HALAOS_API_KEY": "halaos_YOUR_API_KEY_HERE",
        "HALAOS_BASE_URL": "https://your-halaos-instance.com"
      }
    }
  }
}
```

**Available MCP Tools (24):**

| Category | Tools |
|----------|-------|
| Employees | `list_employees`, `get_employee`, `get_directory`, `get_org_chart` |
| Attendance | `get_attendance_records`, `get_attendance_summary`, `clock_in`, `clock_out` |
| Leave | `list_leave_types`, `get_leave_balances`, `list_all_leave_balances`, `list_leave_requests`, `create_leave_request` |
| Payroll | `list_payroll_cycles`, `list_payslips`, `get_payslip`, `calculate_13th_month` |
| Compliance | `get_sss_table`, `get_philhealth_table`, `get_bir_tax_table` |
| Dashboard | `get_dashboard_stats`, `get_flight_risk`, `get_compliance_alerts` |
| AI | `ai_chat` |

**Role restrictions:** `get_flight_risk` and `get_compliance_alerts` require Manager or Admin role. `list_all_leave_balances` requires Admin role.

### Mode 2: Standalone (No Setup Needed)

Without MCP or API key, the skill works as an offline HR knowledge assistant — answers labor law questions, calculates government contributions, generates documents. See "Standalone Mode" section below.

---

## Workflow Scenarios

When the user interacts with this skill and MCP tools are available, use these workflow patterns. Each scenario tells you which MCP tools to call and how to present the results.

### Scenario 1: Morning Briefing

**Trigger:** User says "good morning", "briefing", "what's happening today", or any start-of-day greeting.

**Action:** Call these tools in sequence:
1. `get_dashboard_stats` — headcount, attendance, pending items
2. `list_leave_requests` with `status=pending` — pending approvals
3. `get_compliance_alerts` — overdue filings, expiring documents

**Response format:**
```
Morning briefing:
- Employees: Y total, X present today
- Pending leave: N requests waiting (list names + types)
- Pending overtime: N requests
- Compliance: N alerts (summarize top issues)
Ask: "Want me to dig into any of these?"
```

### Scenario 2: Leave Management

**Trigger:** User asks about leave requests, approvals, or balances.

**Action:**
1. `list_leave_requests` with `status=pending` — show pending requests
2. `list_all_leave_balances` — get all employee balances (admin only), cross-reference with pending requests
3. If user needs leave type IDs, call `list_leave_types` first
4. If user asks about team coverage, call `get_attendance_records` for that date

**Response format:** Table with employee name, leave type, dates, days requested, and remaining balance. Flag anyone with low balance.

### Scenario 3: Payroll Review

**Trigger:** User asks about payroll, salary, deductions, or net pay.

**Action:**
1. `list_payroll_cycles` — show latest cycle
2. `list_payslips` — list available payslips for the current user
3. `get_payslip` with specific payslip_id for detailed breakdown
4. `get_sss_table` / `get_philhealth_table` / `get_bir_tax_table` for contribution questions

**Response format:** Clear table with gross, itemized deductions (SSS, PhilHealth, Pag-IBIG, tax), and net pay.

### Scenario 4: Flight Risk & Retention

**Trigger:** User asks "who might leave", "flight risk", "retention", or "attrition".

**Action:**
1. `get_flight_risk` — get flagged employees
2. `get_dashboard_stats` — for context (department sizes)

**Response format:** List flagged employees with risk factors. Identify patterns (e.g., "3 of 5 haven't had a raise in 12+ months"). Suggest concrete actions. Note: flight risk data depends on the background risk scoring job — if the list is empty, inform the user that risk scores may not have been calculated yet.

### Scenario 5: Employee Lookup

**Trigger:** User asks about a specific employee by name.

**Action:**
1. `list_employees` with search filter, or `get_employee` if ID is known
2. Optionally `get_leave_balances` if user asks about leave

**Response format:** Concise profile — name, department, position, hire date, tenure, employment type.

### Scenario 6: Compliance Check

**Trigger:** User asks about tax tables, SSS, PhilHealth, BIR, or compliance.

**Action:** Call the relevant compliance tool:
- `get_sss_table` — SSS contribution brackets
- `get_philhealth_table` — PhilHealth rates
- `get_bir_tax_table` with frequency parameter — BIR withholding brackets

**Response format:** Show the relevant bracket for the salary in question. Always show both employee and employer shares.

### Scenario 7: Org Structure

**Trigger:** User asks about organization, reporting structure, departments, or headcount.

**Action:**
1. `get_org_chart` — full hierarchy
2. `get_directory` — employee listing with contacts
3. `get_dashboard_stats` — department distribution

**Response format:** Tree structure showing reporting lines. Note any span-of-control issues (managers with too many direct reports).

### Scenario 8: End-of-Day Summary

**Trigger:** User asks for "summary", "how are we doing", "team health", or end-of-day check.

**Action:**
1. `get_dashboard_stats` — overall numbers
2. `get_flight_risk` — risk overview
3. `get_compliance_alerts` — compliance status

**Response format:** Department-by-department health summary. Highlight strong areas and areas needing attention. Offer specific recommendations with next steps.

---

## Standalone Mode

When no MCP server or API key is available, answer HR questions using built-in knowledge.

### First Run — Configuration

On first use, ask the user about their company context:

1. **Country/Jurisdiction**: `PH` (Philippines, default), `SG` (Singapore), `LK` (Sri Lanka)
2. **Company Size**: Small (1-50), Medium (51-200), Large (200+)

Store in `~/.openclaw/skills/halaos-hr-copilot/config.json`:
```json
{
  "jurisdiction": "PH",
  "company_size": "medium",
  "currency": "PHP",
  "timezone": "Asia/Manila"
}
```

### HR Knowledge Base

**Philippine Labor Law:**
- Minimum wage by region (NCR, CALABARZON, etc.)
- Mandatory benefits: SSS, PhilHealth, Pag-IBIG, 13th month pay
- Leave entitlements: SIL (5 days), maternity (105 days), paternity (7 days), solo parent (7 days), VAWC (10 days), special leave for women (60 days)
- TRAIN Law withholding tax brackets
- DOLE compliance requirements
- Regular/special holiday pay rules

**Singapore Employment Act:**
- CPF contribution rates by age bracket
- Annual leave entitlement (7-14 days by tenure)
- Sick leave (14 days outpatient + 60 days hospitalization)
- Public holiday entitlements
- IRAS filing requirements

**Sri Lanka Labor Law:**
- EPF (employee 8% + employer 12%) and ETF (employer 3%)
- Annual leave (14 days), casual leave (7 days), sick leave (7 days)
- Gratuity calculation (half month per year after 5 years)

### Government Contribution Calculator

**SSS (Philippines 2024):**
- Employee: 4.5% of monthly salary credit
- Employer: 9.5% of monthly salary credit
- Monthly salary credit range: PHP 4,000 - PHP 30,000

**PhilHealth (Philippines 2024):**
- Rate: 5% of basic salary (split 50/50 employee/employer)
- Floor: PHP 10,000; Ceiling: PHP 100,000

**Pag-IBIG (Philippines):**
- Employee: 1% if salary <= PHP 1,500; 2% if > PHP 1,500
- Employer: 2% of basic salary
- Ceiling: PHP 10,000 (for contributions over PHP 5,000 max PHP 200)

**BIR Withholding Tax (TRAIN Law):**
| Annual Taxable Income | Tax |
|---|---|
| <= PHP 250,000 | 0% |
| 250,001 - 400,000 | 15% of excess over 250,000 |
| 400,001 - 800,000 | 22,500 + 20% of excess over 400,000 |
| 800,001 - 2,000,000 | 102,500 + 25% of excess over 800,000 |
| 2,000,001 - 8,000,000 | 402,500 + 30% of excess over 2,000,000 |
| > 8,000,000 | 2,202,500 + 35% of excess over 8,000,000 |

### Document Generation

Generate common HR documents:
- **Certificate of Employment (COE)**: Employee name, position, dates, salary (optional)
- **Employment Contract**: Based on jurisdiction template
- **Memorandum / Notice**: Warning, suspension, termination
- **Leave Summary**: Balance report per employee
- **Payslip**: Basic computation with deductions breakdown

---

## Response Formatting

- Present payroll computations in a clear table with gross, deductions (itemized), and net pay
- Show government contributions as a breakdown: employee share vs employer share
- Display leave balances as a summary table: type, total, used, remaining
- For compliance questions, always cite the specific law or regulation
- Show attendance summaries with present/absent/late counts
- For analytics, present trends with direction indicators (up/down/stable)
- When presenting lists of employees, always include department and position for context

---

## 中文说明

HalaOS HR Copilot 是面向东南亚的 AI 人力资源副驾驶。通过自然对话管理员工、考勤、请假、薪资、税务合规和组织洞察。

**两种模式：**
- **MCP 模式（推荐）**：配置 HalaOS MCP Server，AI 直接调用 24 个 HR 工具访问实时数据
- **独立模式**：无需配置，内置菲律宾/新加坡/斯里兰卡劳动法知识库，离线可用

**核心场景：** 早报简报、请假审批、薪资核查、离职风险预警、合规检查、组织架构查询、团队健康分析。

---

## Links

- Website: https://halaos.com
- GitHub: https://github.com/tonypk/aigonhr
- MCP Server: `go install github.com/tonypk/aigonhr/cmd/mcp@latest`
