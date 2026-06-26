# MedPilot Self-Use

Manage a single-patient medication and health-tracking workflow — ingest doctor orders, log intakes, record vitals, and generate follow-up summaries.

## What it does
- Ingests doctor prescription text and structures it into active medications with dosage and frequency
- Records medication intake, skip, or missed states with timestamps and next-dose confirmations
- Logs home metrics like blood pressure and glucose, with abnormal alerts
- Generates structured weekly follow-up reports with compliance trends and a follow-up plan

## Example scenarios

**1. Record a new doctor prescription**
> 👤 "I just got a new prescription from my doctor, please record it"
> 🤖 The skill ingests the doctor order text, structures it into active medications with dosage and frequency, and asks for confirmation before setting reminders.

**2. Generate a weekly health report**
> 👤 "Generate my weekly health report"
> 🤖 Structured weekly summary including medication intake compliance, blood pressure/glucose trends, abnormal alerts, and a follow-up plan.

**3. 体检报告看不懂**
> 👤 "今年公司体检报告出来了，有个'甲状腺结节TI-RADS 3类'，还有个'低密度脂蛋白偏高'，严不严重？"
> 🤖 解读体检指标：TI-RADS 3类恶性风险较低（良性概率>95%），建议6-12个月复查。低密度脂蛋白偏高需生活方式干预：减少红肉和油炸食品、增加蔬菜纤维、每周至少150分钟有氧运动。建议去三甲医院内分泌科进一步咨询。同时说明该解读不能替代医生诊断。
