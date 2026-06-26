---
name: halaos-hr
version: "1.1.0"
description: "AI-powered HR Operating System for Southeast Asia. Full payroll with PH/SG/LK compliance, 9 AI agents (payroll specialist, compliance officer, leave advisor...), attendance with GPS geofencing, leave/OT/expense workflows, org intelligence with flight risk & burnout detection. Zero-setup via OpenClaw."
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
        - "~/.openclaw/skills/halaos-hr/config.json"
---

# HalaOS — AI-Powered HR Operating System

Enterprise HR system built for Southeast Asia. Handles employees, attendance, leave, payroll, tax compliance, benefits, loans, training, performance reviews, and more — with 9 specialized AI agents that understand local labor law.

**Zero setup for basic use.** Install and start asking HR questions immediately. Connect your HalaOS account for full platform access.

## How It Works

This skill operates in two modes:

### Mode 1: OpenClaw Native (Default — No Registration Needed)

AI HR assistant powered by your OpenClaw channels. Answers HR questions, calculates PH/SG/LK government contributions, generates compliance documents, and manages team data locally.

**Just install and start:**
```
/halaos-hr
> Calculate SSS contribution for salary 25,000 PHP
> How many vacation leave days does Philippine labor law require?
> Generate a Certificate of Employment for John Santos
> What are the BIR filing deadlines this quarter?
> Calculate 13th month pay for employee with 180,000 annual salary
```

### Mode 2: Cloud Platform (Full Features — Requires Registration)

Connect to your HalaOS account for the complete HR platform: payroll processing, attendance tracking, leave management, AI-powered org intelligence, and automated compliance.

Set `HALAOS_API_KEY` to enable. See "Cloud Platform Setup" section below.

---

## What It Does

### Core HR
- **Employee Management**: Profiles, 201 files, document tracking, salary assignment, org chart, directory
- **Attendance & Time**: Clock in/out, GPS geofencing, shift scheduling, DTR reports, correction workflows
- **Leave Management**: Balances, requests, approvals, calendar, carryover, encashment
- **Overtime**: Request submission, approval workflow, rate calculation
- **Payroll**: Multi-frequency cycles, automated computation, payslips, 13th month pay, final pay, bonus structures
- **Benefits**: Plan enrollment, dependent management, claims workflow
- **Loans**: Application, approval, amortization, salary deduction integration

### Compliance & Tax (Southeast Asia)
- **Philippines**: SSS, PhilHealth, Pag-IBIG, BIR withholding tax (TRAIN Law), BIR 2316/2550M/2550Q/1601C/1701/1702/0619E/SAWT
- **Sri Lanka**: EPF/ETF filings
- **Singapore**: IRAS compliance
- **Reports**: DTR, DOLE register, CSV/bank file export

### Workforce Operations
- **Onboarding/Offboarding**: Templates, checklists, clearance workflows, final pay
- **Training & Certification**: Programs, enrollment, expiry tracking, compliance training
- **Performance**: Review cycles, self/manager reviews, KPI & goal tracking
- **Disciplinary**: Incident logging, actions, appeals, resolution
- **Grievance**: Filing, investigation, resolution, withdrawal
- **Policies**: Creation, versioning, employee acknowledgment tracking
- **Expenses**: Claims, approvals, reimbursement tracking

### AI & Intelligence
- **9 Specialized AI Agents** with tool access to live company data
- **Org Intelligence**: Flight risk detection, burnout risk, team health metrics, blind spot analysis
- **Dashboard AI**: Briefings, form auto-fill, compliance alerts, manager suggestions
- **Workflow Automation**: Rules engine, SLA tracking, autonomous decision agent

---

## 中文说明

HalaOS 是一款面向东南亚的 AI 驱动人力资源操作系统。支持员工管理、考勤、请假、薪资、税务合规、福利、贷款、培训、绩效等全模块 HR 功能，内置 9 个专业 AI 代理，精通当地劳动法。

**两种模式：**
- **原生模式（默认）**：直接通过 OpenClaw 提问 HR 问题、计算政府缴费、生成合规文件，零注册即用
- **云平台模式（完整功能）**：连接 HalaOS 账号，使用完整薪资处理、考勤追踪、AI 组织洞察等功能

**核心功能：**
- 全自动薪资计算（含菲律宾 SSS/PhilHealth/Pag-IBIG/BIR 税表）
- GPS 地理围栏考勤、弹性排班、DTR 报表
- 假期管理（余额、审批、结转、兑现）
- 9 个 AI 代理（薪资专家、合规官、考勤经理、请假顾问等）
- 组织智能（离职风险、倦怠风险、团队健康、盲点分析）
- 201 档案管理、培训认证、绩效 KPI、纪律处分、申诉流程

---

## OpenClaw Native Mode

### First Run — Configuration

On first use, ask the user about their company context:

1. **Country/Jurisdiction**: Which country's labor law to apply?
   - `PH` (Philippines) — default, most comprehensive
   - `SG` (Singapore)
   - `LK` (Sri Lanka)

2. **Company Size**: Affects compliance requirements
   - Small (1-50), Medium (51-200), Large (200+)

3. **Storage**: Where to save HR data locally
   - Notion, Google Sheets, Obsidian, Local files

Store in `~/.openclaw/skills/halaos-hr/config.json`:
```json
{
  "jurisdiction": "PH",
  "company_size": "medium",
  "storage": "notion",
  "currency": "PHP",
  "timezone": "Asia/Manila"
}
```

### HR Knowledge Base

In native mode, answer HR questions using built-in knowledge of Southeast Asian labor law:

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

When asked to calculate contributions, use these formulas:

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

Generate common HR documents in native mode:

- **Certificate of Employment (COE)**: Employee name, position, dates, salary (optional)
- **Employment Contract**: Based on jurisdiction template
- **Memorandum / Notice**: Warning, suspension, termination
- **Leave Summary**: Balance report per employee
- **Payslip**: Basic computation with deductions breakdown

### Employee Data Management

When the user manages employees locally:

```
> Add employee Maria Santos, position: Accountant, department: Finance, salary: 35000 PHP
> List all employees
> Show Maria's leave balance
> Calculate Maria's net pay for January
> Generate DTR report for Finance department, March 2026
```

Employee record format:
```json
{
  "name": "Maria Santos",
  "position": "Accountant",
  "department": "Finance",
  "salary": 35000,
  "currency": "PHP",
  "hire_date": "2024-06-15",
  "status": "active",
  "jurisdiction": "PH"
}
```

---

## AI Agents Reference

When connected to the cloud platform, 9 specialized AI agents are available. Each has tools that access live company data.

| ID | Agent | Specialty | Tools |
|----|-------|-----------|-------|
| 1 | General HR Assistant | All-purpose HR questions | 9 tools (employee, leave, attendance, payroll, policy, compliance, knowledge base) |
| 2 | Payroll Specialist | Payroll, tax, deductions, 13th month, final pay | Payroll analysis, salary simulation, contribution tables |
| 3 | Attendance Manager | Clock in/out, DTR, schedules, geofencing | Attendance records, patterns, schedule data |
| 4 | Compliance Officer | Labor law, DOLE, BIR, government filings | Compliance checking, policy lookup, filing deadlines |
| 5 | Leave Advisor | Balances, entitlements, carryover, encashment | Leave balances, request history, calendar |
| 6 | Onboarding Guide | New hire setup, 201 file, policies | Onboarding tasks, document requirements |
| 7 | Performance Reviewer | KPIs, goals, review cycles | Performance data, goal tracking |
| 8 | Training Advisor | Skills gaps, certifications, compliance training | Training records, certification expiry |
| 9 | Workflow Decision Agent | Autonomous approval recommendations | Approval context, workflow rules, confidence scoring |

### Using Agents in Native Mode

In native mode (no API key), the skill itself acts as a general HR assistant using built-in knowledge. Agent-specific expertise is simulated:

```
> Ask the compliance officer: what BIR forms do I need to file this month?
> Ask the payroll specialist: calculate overtime pay for 8 hours on a regular holiday
> Ask the leave advisor: can an employee carry over unused SIL to next year?
```

### Using Agents in Cloud Mode

With `HALAOS_API_KEY` set, queries are routed to specialized agents with access to your actual company data:

```
> How many employees are at risk of burnout?
> Generate this month's payroll for all employees
> Who has expiring certifications in the next 30 days?
> What's the leave utilization rate by department?
```

---

## Cloud Platform Setup

For the full HR platform with payroll processing, attendance, AI agents, and compliance automation:

1. Visit your HalaOS instance (provided by your admin)
2. Log in or register with magic link
3. Go to Settings > API Keys > Create New Key
4. Set `HALAOS_API_KEY` in your OpenClaw config

### Cloud API Endpoints

All API calls require: `Authorization: Bearer <HALAOS_API_KEY>`

Base URL: `HALAOS_URL` env var, or your HalaOS instance URL.

**Dashboard & Intelligence:**
```
GET  {baseUrl}/api/v1/dashboard/stats              — Company overview stats
GET  {baseUrl}/api/v1/dashboard/action-items        — Pending approvals & tasks
GET  {baseUrl}/api/v1/dashboard/flight-risk          — Employee attrition risk
GET  {baseUrl}/api/v1/dashboard/burnout-risk         — Burnout detection
GET  {baseUrl}/api/v1/dashboard/team-health          — Team health metrics
GET  {baseUrl}/api/v1/dashboard/compliance-alerts    — Compliance warnings
GET  {baseUrl}/api/v1/ai/briefing                    — AI-generated daily briefing
```

**Employees:**
```
GET  {baseUrl}/api/v1/employees                     — List employees
GET  {baseUrl}/api/v1/employees/:id                 — Get employee details
GET  {baseUrl}/api/v1/directory                     — Employee directory
GET  {baseUrl}/api/v1/directory/org-chart            — Organization chart
```

**Attendance:**
```
POST {baseUrl}/api/v1/attendance/clock-in           — Clock in
POST {baseUrl}/api/v1/attendance/clock-out           — Clock out
GET  {baseUrl}/api/v1/attendance/records             — Attendance records
GET  {baseUrl}/api/v1/attendance/summary             — Attendance summary
GET  {baseUrl}/api/v1/attendance/report              — DTR report
```

**Leave:**
```
GET  {baseUrl}/api/v1/leaves/balances               — My leave balances
POST {baseUrl}/api/v1/leaves/requests               — Submit leave request
GET  {baseUrl}/api/v1/leaves/requests               — List leave requests
GET  {baseUrl}/api/v1/leaves/calendar               — Leave calendar
```

**Payroll:**
```
GET  {baseUrl}/api/v1/payroll/cycles                — List payroll cycles
POST {baseUrl}/api/v1/payroll/runs                  — Run payroll
GET  {baseUrl}/api/v1/payroll/payslips              — List payslips
GET  {baseUrl}/api/v1/payroll/payslips/:id/pdf      — Download payslip PDF
POST {baseUrl}/api/v1/payroll/13th-month/calculate  — Calculate 13th month pay
```

**Compliance:**
```
GET  {baseUrl}/api/v1/compliance/sss-table          — SSS contribution table
GET  {baseUrl}/api/v1/compliance/philhealth-table   — PhilHealth table
GET  {baseUrl}/api/v1/compliance/pagibig-table      — Pag-IBIG table
GET  {baseUrl}/api/v1/compliance/bir-tax-table      — BIR tax table
POST {baseUrl}/api/v1/compliance/government-forms/generate — Generate BIR forms
GET  {baseUrl}/api/v1/tax-filings/upcoming          — Upcoming filing deadlines
```

**Approvals:**
```
GET  {baseUrl}/api/v1/approvals/pending             — Pending approvals
POST {baseUrl}/api/v1/approvals/:id/approve         — Approve request
POST {baseUrl}/api/v1/approvals/:id/reject          — Reject request
```

**Analytics:**
```
GET  {baseUrl}/api/v1/analytics/summary             — HR analytics summary
GET  {baseUrl}/api/v1/analytics/headcount-trend     — Headcount over time
GET  {baseUrl}/api/v1/analytics/turnover            — Turnover statistics
GET  {baseUrl}/api/v1/analytics/department-costs    — Department cost analysis
GET  {baseUrl}/api/v1/analytics/attendance-patterns — Attendance patterns
GET  {baseUrl}/api/v1/analytics/leave-utilization   — Leave utilization
GET  {baseUrl}/api/v1/analytics/blind-spots         — Manager blind spots
```

**AI Chat:**
```
POST {baseUrl}/api/v1/ai/chat                       — Chat with AI agent
GET  {baseUrl}/api/v1/ai/agents                     — List available agents
GET  {baseUrl}/api/v1/ai/sessions                   — List chat sessions
```

When `HALAOS_API_KEY` is set, prefer using cloud API endpoints for all queries. When not set, use built-in knowledge and local data.

## Response Formatting

- Present payroll computations in a clear table with gross, deductions (itemized), and net pay
- Show government contributions as a breakdown: employee share vs employer share
- Display leave balances as a summary table: type, total, used, remaining
- For compliance questions, always cite the specific law or regulation
- Show attendance summaries with present/absent/late counts
- For analytics, present trends with direction indicators (up/down/stable)

## Links

- Website: https://halaos.com
- GitHub: https://github.com/tonypk/aigonhr
