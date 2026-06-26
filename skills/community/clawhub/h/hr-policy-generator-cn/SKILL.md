---
name: hr-policy-generator-cn
version: 1.0.0
description: "综合性 HR 政策设计工具，覆盖考勤、休假、加班、远程办公及合规要求。根据公司规模、办公模式、适用法律等输入，生成完整的政策文档、法律合规清单、例外处理机制及员工沟通方案。"
author: "hr-policy"
tags:
  - hr
  - 人力资源
  - 考勤
  - 休假
  - 加班
  - 合规
  - 远程办公
invocable: true
---

# 人力资源政策生成器（中文版）

## 描述
综合性 HR 政策设计工具，覆盖考勤、休假、加班、远程办公及合规要求。根据公司规模、办公模式、适用法律等输入，生成完整的政策文档、法律合规清单、例外处理机制及员工沟通方案。

## 输入

| 名称 | 类型 | 必填 | 说明 |
|------|------|------|------|
| company_size | text | 是 | 员工人数及办公地点分布 |
| work_arrangement | text | 是 | 办公模式：现场办公、远程办公、混合办公 |
| jurisdiction | text | 是 | 适用的劳动法律法规（如中国上海、美国加州） |
| current_policy | text | 否 | 现有考勤与休假政策 |
| employee_feedback | text | 否 | 已知的员工意见或诉求 |
| industry_standards | text | 否 | 行业标杆实践 |

## 输出

| 名称 | 类型 | 说明 |
|------|------|------|
| attendance_policy | text | 完整的考勤与休假政策文档 |
| work_hours_framework | text | 核心工作时间与弹性安排框架 |
| leave_categories | text | 年假、病假、育儿假、婚丧假等各类假别 |
| overtime_policy | text | 加班认定规则及补偿方式 |
| exception_procedures | text | 例外情形处理流程（紧急、医疗、特殊需求等） |
| compliance_checklist | text | 劳动法合规性检查清单 |
| communication_plan | text | 政策发布与员工培训沟通方案 |

## 示例

### 输入
```json
{
  "company_size": "150 人，2 个办公室",
  "work_arrangement": "混合办公 - 每周 3 天办公室，2 天远程",
  "jurisdiction": "中国上海",
  "current_policy": "弹性工时，无限年假（无具体指引）",
  "employee_feedback": "年假申请审批慢；远程办公期间考勤不清晰",
  "industry_standards": "互联网行业普遍采用电子考勤和明确休假指引"
}
