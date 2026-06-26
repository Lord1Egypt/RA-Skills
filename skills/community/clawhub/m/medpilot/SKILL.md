---
name: medpilot-self-use
description: "Manage a single-patient medication and health-tracking workflow with MedPilot. Use when the user wants to ingest doctor orders, confirm active medications, record intakes or skipped doses, log blood pressure or glucose, generate follow-up summaries, or operate the MedPilot self-use edition through its CLI or local API. NOT for: multi-patient clinic workflows, diagnosis, treatment decisions, or replacing physician judgment."
version: v1.0.0
tags: medication-management, health-tracking, patient-assistant
---

# MedPilot Self-Use

## Usage Scenarios

### Scenario 1: Ingest a New Doctor Prescription
**User input:** "I just got a new prescription from my doctor, please record it"
**Expected output:** The skill ingests the doctor order text, structures it into active medications with dosage and frequency, and asks for confirmation before setting reminders.

### Scenario 2: Log a Medication Intake
**User input:** "I took my morning blood pressure medication"
**Expected output:** The skill records the intake timestamp, updates the medication log, and confirms the next scheduled dose time.

### Scenario 3: Generate a Weekly Follow-Up Summary
**User input:** "Generate my weekly health report"
**Expected output:** The skill produces a structured weekly summary including medication intake compliance, blood pressure/glucose trends, abnormal alerts, and a follow-up plan.
### Scenario 4: 体检报告看不懂
**User input:** "今年公司体检报告出来了，有个'甲状腺结节TI-RADS 3类'，还有个'低密度脂蛋白偏高'，严不严重？"
**Expected output:** 解读体检指标：TI-RADS 3类表示甲状腺结节恶性风险较低（良性概率>95%），建议6-12个月复查观察大小变化即可。低密度脂蛋白偏高（LDL-C >3.4mmol/L）提示需要生活方式干预：减少红肉和油炸食品、增加蔬菜纤维摄入、每周至少150分钟有氧运动。建议去三甲医院内分泌科进一步咨询，如果是首次发现可以3个月后复查血脂四项。同时说明该解读不能替代医生诊断。

## Input to ask for
- patient identity for this local instance
- doctor order text
- medication intake updates
- home metrics such as blood pressure or glucose
- report date range when the user wants a summary

## Output
- structured order ingestion
- active medication/reminder state
- intake or skip logs
- abnormal metric alerts
- follow-up summary / weekly report

## Workflow
1. Register or identify the local patient profile.
2. Ingest the doctor order text.
3. Confirm the order before treating reminders as active.
4. Record intake, skip, or missed states.
5. Record home metrics and review generated alerts.
6. Build a follow-up report when needed.

## Boundaries
- Keep the scope to one patient in one local deployment.
- Treat MedPilot as a health-management and record-keeping tool, not a diagnosis system.
- Never present medication changes as autonomous medical advice.

## References
- Read `references/quickstart.md` for CLI and API examples when you need exact commands.
