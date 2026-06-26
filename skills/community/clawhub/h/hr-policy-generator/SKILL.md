---
name: hr-policy-generator
version: 1.0.0
description: "Comprehensive HR policy development covering attendance, time-off, overtime, remote work, and compliance. Generates structured policy documents, legal checklists, exception handling frameworks, and employee communication plans tailored to company size, work arrangement, and jurisdiction."
author: "hr-policy"
tags:
  - hr
  - policy
  - attendance
  - leave
  - overtime
  - compliance
  - remote-work
invocable: true
---

# HR Policy Generator

## Description
Comprehensive HR policy development covering attendance, time-off, overtime, remote work, and compliance. Generates structured policy documents, legal checklists, exception handling frameworks, and employee communication plans tailored to company size, work arrangement, and jurisdiction.

## Input

| Name | Type | Required | Description |
|------|------|----------|-------------|
| company_size | text | Yes | Number of employees and locations |
| work_arrangement | text | Yes | On-site, remote, hybrid structure |
| jurisdiction | text | Yes | Applicable labor laws and regulations |
| current_policy | text | No | Existing attendance policies |
| employee_feedback | text | No | Known concerns or requests |
| industry_standards | text | No | Industry benchmark practices |

## Output

| Name | Type | Description |
|------|------|-------------|
| attendance_policy | text | Comprehensive policy document |
| work_hours_framework | text | Core hours and flexibility guidelines |
| leave_categories | text | PTO, sick, parental, other leave types |
| overtime_policy | text | Overtime rules and compensation |
| exception_procedures | text | Handling exceptions and accommodations |
| compliance_checklist | text | Legal compliance verification |
| communication_plan | text | Employee rollout and training |

## Example

### Input
```json
{
  "company_size": "150 employees, 2 offices",
  "work_arrangement": "Hybrid - 3 days office, 2 days remote",
  "jurisdiction": "California, USA",
  "current_policy": "Informal flexible schedule, unlimited PTO"
}