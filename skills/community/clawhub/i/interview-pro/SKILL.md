---
name: interview-pro
description: 面试助手。支持模拟面试、面试问题预测、简历优化、面试复盘。覆盖所有行业。Use when user needs interview preparation, mock interviews, resume optimization, or interview feedback. 面试准备、模拟面试、简历优化、面试技巧、求职。
version: 1.2.0
license: MIT-0
metadata: {"openclaw": {"emoji": "🎯", "requires": {"bins": [], "env": []}, "always": false}}
---

# 面试助手 Interview Pro

AI-powered interview preparation assistant with full industry coverage.

## Trigger / 触发条件

- "帮我准备面试" / "Help me prepare for interview"
- "模拟面试" / "Mock interview"
- "面试会问什么问题" / "Interview questions"
- "优化简历" / "Optimize my resume"
- "面试复盘" / "Interview feedback"

---

## 行业覆盖 Industry Coverage

| Industry | Roles | Focus |
|----------|-------|-------|
| Tech/Internet | Dev, Architect, QA, DevOps, PM | Technical depth, system design |
| Finance/Banking | IB, Fund, Risk, Audit, Finance | Domain knowledge, case analysis |
| Marketing | Brand, Digital, PR | Creativity, case studies |
| Sales | Rep, Key Account, Channel | Sales skills, achievements |
| HR | HRBP, Recruiting, Training, Comp | Communication, cases |
| Design | UI/UX, Graphic, Interaction | Portfolio, design philosophy |
| Education | Teacher, Trainer, Curriculum | Teaching ability, communication |
| Healthcare | Doctor, Nurse, Pharma Rep | Domain knowledge, empathy |
| Legal | Lawyer, In-house, Compliance | Legal knowledge, logic |
| Consulting | Mgmt/Strategy/IT Consulting | Problem-solving, case interview |
| Manufacturing | Production, QA, Supply Chain | Process mgmt, cost control |
| Service | Hotel, F&B, Account Mgmt | Service mindset, adaptability |

---

## 核心功能 Core Features

### 1. 岗位分析 Job Analysis

Analyze job requirements based on AI knowledge:
- Core skills and qualifications
- Salary range estimation
- Market demand and trends
- Key differentiators

### 2. 面试问题预测 Question Prediction

**Finance/Banking:**
- Explain duration and convexity
- How to assess credit risk
- Describe VaR calculation
- Financial statement analysis case

**Marketing:**
- How to develop product launch strategy
- Explain AARRR model
- Design social media campaign
- User growth methods

**Sales:**
- Sell me this pen
- Customer says "too expensive" — how to respond?
- How to uncover customer needs
- Describe your biggest deal

**HR:**
- Describe recruiting process
- How to design performance system
- High department turnover — how to solve?
- Employee-supervisor conflict — how to mediate?

**Design:**
- Describe your design process
- Introduce your best project
- Balance aesthetics vs usability
- Design tools proficiency

**Education:**
- Describe teaching philosophy
- Explain a concept in 5 minutes
- Student grades declining — how to help?
- Handle classroom emergencies

**Legal:**
- Analyze a legal case
- How to conduct contract review
- Explain complex legal issues to clients
- Describe a successful case

**Consulting (Case Interview):**
- Estimate market size
- Analyze company profit decline
- Design growth strategy
- Evaluate M&A feasibility

---

### 3. 模拟面试 Mock Interview

| Interviewer | Style | Difficulty |
|-------------|-------|------------|
| Technical | Professional, deep | ⭐⭐⭐⭐ |
| HR | Friendly, comprehensive | ⭐⭐⭐ |
| Stress | High-pressure, challenging | ⭐⭐⭐⭐⭐ |
| Hiring Manager | Practical, experience-based | ⭐⭐⭐⭐ |

---

### 4. 简历优化 Resume Optimization

**Keyword optimization:**
- Extract key skills from job description
- Identify must-have vs nice-to-have keywords
- Suggest resume keywords to add

**Project experience:**
- STAR method (Situation, Task, Action, Result)
- Quantify achievements
- Highlight relevant experience

**Skills presentation:**
- Tier 1: Core skills (must show)
- Tier 2: Supporting skills (good to have)
- Tier 3: Bonus skills (differentiators)

**Integration with resume skills:**
- resume-studio: Word/PDF resume generation
- resume-html: HTML resume creation

---

### 5. 面试分析报告 Interview Analysis Report

```
Interview Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━
Position: {role} | Company: {company} | Date: {date}
━━━━━━━━━━━━━━━━━━━━━━━━

Overall Score: {X}/100 | Rating: {Excellent/Good/Acceptable/Needs Work}

Dimension Scores:
┌─────────────────┬────────┬────────┐
│ Dimension       │ Score  │ Rating │
├─────────────────┼────────┼────────┤
│ Professional    │ {X}/10 │ ⭐⭐⭐⭐⭐ │
│ Communication   │ {X}/10 │ ⭐⭐⭐⭐⭐ │
│ Logical Thinking│ {X}/10 │ ⭐⭐⭐⭐⭐ │
│ Problem Solving │ {X}/10 │ ⭐⭐⭐⭐⭐ │
│ Teamwork        │ {X}/10 │ ⭐⭐⭐⭐⭐ │
│ Role Fit        │ {X}/10 │ ⭐⭐⭐⭐⭐ │
└─────────────────┴────────┴────────┘

Strengths:
1. {strength} - {evidence} - Suggestion: {suggestion}

Weaknesses:
1. {weakness} (Impact: High/Medium/Low)
   Issue: {description}
   Improvement: {plan}
   Timeline: {estimate}

Learning Resources:
📚 Book: {title} - {reason}
🎥 Course: {name} - {platform}
💻 Resource: {name} - {description}

Improvement Plan:
- Short-term (1 week): {actions}
- Medium-term (1 month): {actions}
- Long-term (3 months): {actions}

Next Interview Tips:
- Questions: {suggestions}
- Non-verbal: {suggestions}
- Preparation: {suggestions}

Performance Trend:
| Session | Total | Prof | Comm | Trend |
|---------|-------|------|------|-------|
| 1st     | {X}   | {X}  | {X}  | -     |
| 2nd     | {X}   | {X}  | {X}  | ↑/↓   |

Hiring Likelihood: {X}%
```

---

## 与其他 Skills 集成 Integrations

| Skill | Purpose | Install |
|-------|---------|---------|
| resume-studio | Word/PDF resume | `npx clawhub@latest install resume-studio` |
| resume-html | HTML resume | `npx clawhub@latest install resume-html` |
| research-orchestrator | Industry research | `npx clawhub@latest install research-orchestrator` |
| word-studio | Word report | `npx clawhub@latest install word-studio` |
| pdf-studio | PDF report | `npx clawhub@latest install pdf-studio` |

**Integration workflows:**
1. **Interview + Resume** — interview-pro analyzes job → resume-studio generates resume
2. **Interview + Research** — interview-pro prepares questions → research-orchestrator provides industry data
3. **Interview + Report** — interview-pro evaluates → word-studio/pdf-studio generates report

---

## 完整示例 Full Example

**User:** "Help me prepare for ByteDance Python developer interview"

**AI Execution:**
```
Interview Preparation Start
━━━━━━━━━━━━━━━━━━━━━━━━━
Position: Python Developer
Company: ByteDance
━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Job Analysis:
- Core requirements: Python, Django, Microservices, High concurrency
- Salary: 25-45K
- Bonus: AI/ML experience

📝 Question Prediction:
1. Technical: Python GIL, Django lifecycle, High concurrency design
2. Behavioral: Project experience, Teamwork, Problem solving

🎭 Mock Interview...
[Conduct mock interview]

📊 Analysis Report:
[Generate detailed report]

📝 Resume Optimization:
- Keywords: Python, Django, Microservices
- Projects: Highlight performance optimization experience
```

---

## 版本历史 Version History

- v1.2.0 (2026-04-19): Removed external dependencies, optimized for security
- v1.1.0 (2026-04-16): Full industry coverage, detailed analysis, resume integration
- v1.0.0 (2026-04-16): Initial version