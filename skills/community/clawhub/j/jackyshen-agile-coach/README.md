# Jacky Shen's Agile Coach Prompt Toolkit

EN | [中文](README.zh-cn.md)

> **Skill ID**: `jackyshen-agile-coach`  
> **Author**: Jacky Shen — Chief Agile Coach, Scrum Alliance Certified CST  
> **Organization**: UPerform Enterprise Management Co., Ltd. (Shanghai)  


A battle-tested prompt toolkit for Scrum practitioners — 11 ready-to-use AI prompt templates covering the highest-impact scenarios for **Scrum Masters** and **Product Owners**.

---

## Why This Toolkit?

Most AI prompts for agile teams are too generic to be useful. This toolkit addresses that by giving every prompt:

- **A specific expert persona** with 15 years of experience in that domain
- **Three named capabilities** so the AI knows exactly what expertise to draw on
- **"You Never" guardrails** — explicit anti-patterns that prevent vague advice, individual blame, and unverifiable action items
- **Structured output formats** tied to real Scrum ceremonies and artifacts

The result: prompts that behave like a specialist colleague, not a generic assistant.

---
## Installation

`npx skills add mebusw/jackyshen-agile-coach`

---

## The GRACE Prompt Framework

All 11 prompts follow the same five-layer structure:

```
### GOAL ###      What you want to achieve and why it matters
### ROLE ###      Expert identity + 3 capabilities + "You Never" guardrails
### ACTION ###    Specific tasks with explicit Do / Don't boundaries
### CONTEXT ###   Business scenario, team details, and input data
### EXPRESSION ###    Output structure, tables, length, and examples
```

The **"You Never" guardrails** in the ROLE section are the key differentiator. Each prompt's guardrails are tailored to the most common failure modes of that specific scenario — not generic boilerplate.

---

## Scenario Coverage

### 🔵 Agile General (Roles: SM + PO)

| # | Scenario | Best Used At |
|---|----------|-------------|
| 1 | **Definition of Ready (DoR) Check** | Before Sprint Planning |
| 2 | **Backlog Prioritization & Ordering** | Sprint Planning / Release Planning |
| 3 | **Risk Identification & Analysis** | Sprint Planning / Quarterly Review |

### 🟢 Product Owner

| # | Scenario | Best Used At |
|---|----------|-------------|
| 4 | **Data Analysis & Insight Extraction** | Product iteration planning |
| 5 | **Backlog Refinement & Estimation** | Refinement sessions |
| 6 | **User Persona Creation** | Product inception / Feature kickoff |
| 7 | **Customer Churn Prediction & Analysis** | Quarterly health review |
| 8 | **Product Requirements Definition** | Feature kickoff / PRD drafting |
| 9 | **Decision Support & Option Comparison** | Strategic decision points |

### 🟠 Scrum Master

| # | Scenario | Best Used At |
|---|----------|-------------|
| 10a | **Retrospective Agenda Design** | Before the retro |
| 10b | **Retrospective Pattern Analysis** | After the retro |
| 11 | **Scenario Modeling & Hypothesis Testing** | Org design / Process experiments |

---

## How to Use

### Step 1 — Describe your situation
Tell the AI what you're working on. Examples:
- *"I need to check if these user stories are ready for Sprint Planning"*
- *"Help me analyze our app store reviews for product insights"*
- *"We just finished a retro — help me find the patterns in this feedback"*

### Step 2 — The skill selects the scenario
The skill matches your description to the most relevant prompt template from the library.

### Step 3 — Fill in the placeholders
The prompt output will include `[placeholders]` for anything the skill needs from you — team size, Sprint goal, raw data, etc. Fill these in and run the completed prompt.

### Step 4 — Copy and use
Paste the filled prompt into any AI chat (Claude, GPT-4, etc.) or use it directly here.

---

## Prompt Design Principles

### 1. Expert Personas, Not Generic Roles
Every prompt assigns the AI a specific expert identity with named competencies:

```
You are a senior Product Owner with 15 years of experience in agile
product development and Backlog Refinement facilitation.

Your expertise:
- Acceptance Criteria Writing (Given/When/Then, INVEST criteria)
- Dependency Mapping and Technical Risk Detection
- Story Point Estimation (Fibonacci scale, team velocity calibration)
```

### 2. "You Never" Guardrails
Each scenario has three tailored anti-patterns. Examples:

| Scenario | "You Never" Rules |
|----------|------------------|
| DoR Check | Accept vague language like "user-friendly" without challenging it |
| Risk Analysis | Surface one-time incidents as systemic risks |
| Retro Analysis | Offer advice like "communicate better" / attribute problems to individuals |
| Churn Analysis | Recommend retention tactics that can't be tested within one Sprint |
| Requirements | Accept requirements written as solutions ("we need a button that...") |

### 3. Verifiable, Sprint-Scoped Actions
All action items and recommendations produced by these prompts are constrained to be:
- **Completable** within one Sprint
- **Measurable** with a defined success criterion
- **Systemic** — never attributed to individual people

---

## File Structure

```
jackyshen-agile-coach/
├── SKILL.md                      # Skill definition and quick reference table
├── README.md                     # This file (English)
├── README.zh-cn.md               # Chinese version
└── references/
    └── prompt-library.md         # All 11 complete prompt templates
```

---

## About the Author

**Jacky Shen** is a Chief Agile Coach and Scrum Alliance Certified Scrum Trainer (CST) , also the 1st Certified Team Coach in the world. As a CST, he is authorized to issue **CSM** (Certified ScrumMaster) , **CSPO** (Certified Scrum Product Owner) and **CAL** (Certified Agile Leadership) certifications.

He is the global partner of UPerform AI & Agile Consulting and a practitioner at the intersection of agile methodology and AI-assisted workflows.

---

## License & Attribution

This prompt library references templates from Scrum Alliance's official Prompt Engineering resources and their *AI for SM* / *AI for PO* micro-certification courses.

© Jacky Shen / UPerform Enterprise Management Co., Ltd.  
For learning, team use, and internal training. Please credit the author if sharing externally.
