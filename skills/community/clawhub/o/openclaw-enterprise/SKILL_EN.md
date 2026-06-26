---
name: openclaw-enterprise
description: >-
  Enterprise AI Agent Orchestration Platform - Multi-agent collaboration for complex business workflows. Use when multi-agent collaboration, enterprise workflow automation, Agent orchestration. For mid-to-large enterprises, e-commerce platforms, operations teams. Trigger on AI employees, multi-agent, enterprise automation, workflow orchestration.
homepage: https://openclaw.ai
license: MIT-0
version: 2.0.2
progressive:
  layers:
    - name: metadata
      tokens: 200
      loaded: startup
      description: "Skill configuration, Agent list, pricing"
    - name: instructions
      tokens: 5000
      loaded: trigger
      description: "System positioning, team architecture, technical implementation"
    - name: resources
      tokens: variable
      loaded: on-demand
      description: "Keyword routing tables, workflow templates, configuration guides"
  resource_paths:
    - scripts/*.py
    - templates/*.md
    - references/routing_tables/
metadata:
  openclaw:
    homepage: https://openclaw.ai
    primaryEnv: OPENAI_API_KEY
    requires:
      env:
        - OPENAI_API_KEY
      bins:
        - python3
        - pip
        - curl
    third_party:
      - name: GitHub
        domain: github.com
        purpose: "Open source community collaboration"
        verify_url: https://github.com/openclaw
    apis:
      - name: OpenAI API
        domain: api.openai.com
        purpose: "LLM for Agent reasoning and content generation"
        auth:
          type: Bearer Token
          env_var: OPENAI_API_KEY
      - name: Anthropic API
        domain: api.anthropic.com
        purpose: "Claude for advanced reasoning"
        auth:
          type: Bearer Token
          env_var: ANTHROPIC_API_KEY
          optional: true
          note: "Optional - enables enhanced Claude reasoning"
    emoji: "🏢"
    version: "2.0.0"
    author: "OpenClaw AI Team"
    category: "enterprise-ai"
    tags: ["multi-agent", "enterprise", "collaboration", "workflow", "planning", "automation", "AI team"]
pricing:
  basic:
    price: 999
    currency: CNY
    period: month
    features: ["1 ChiefOfStaff + 5 Agents", "Basic workflows", "10 concurrent users"]
  professional:
    price: 3999
    currency: CNY
    period: month
    features: ["1 ChiefOfStaff + 20 Agents", "Full coverage", "Process coordination", "50 concurrent users", "SLA 99.5%"]
  enterprise:
    price: 29999
    currency: CNY
    period: month
    features: ["Private deployment", "Industry customization", "Source code", "Unlimited concurrent", "Dedicated consultant"]
triggers:
  - "AI employee"
  - "multi-agent collaboration"
  - "enterprise automation"
  - "workflow orchestration"
  - "digital employee"
  - "agent scheduling"
  - "enterprise AI transformation"
  - "intelligent agent orchestration"
  - "operations automation"
  - "enterprise AI team"
  - "chief of staff"
  - "AI workflow"
---

> 🏢 **Your AI Middle Management Team** — 1 ChiefOfStaff + 20 specialized Agents, 10x your enterprise operations efficiency

## ⚡ Quick Start (5 Minutes)

### 1. Install the Skill
```bash
openclaw skills install openclaw-enterprise
```

### 2. Configure Environment
```bash
export OPENAI_API_KEY="your-api-key-here"
# Optional: Enhanced Claude reasoning
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### 3. Run Your First Task
Describe your needs in natural language:
- *"We have an urgent order, how should we handle it?"*
- *"Generate last month's business analysis report"*
- *"A new customer wants Net-60 terms, assess the risk"*

---

## 🎯 Core Features

### 🧠 Intelligent ChiefOfStaff
**Description**: AI Chief Operating Officer that understands requests, distributes tasks, and integrates results

**Example 1**:
> "3 urgent orders next week, how should we schedule them?"
- ChiefOfStaff parses task → distributes to Production/Logistics/Quality Agents
- 3 Agents execute in parallel → ChiefOfStaff integrates results
- Output: Optimal scheduling plan + Gantt chart

**Example 2**:
> "Help me evaluate if we can take on this new customer"
- ChiefOfStaff initiates review → Customer/Risk/Compliance Agents collaborate
- Output: Comprehensive assessment report + risk recommendations

---

### 📊 Full-Chain Operations Coverage
**Description**: 20 specialized Agents covering procurement/production/sales/finance/HR/compliance

**Example 1**: Emergency Procurement Response
> "Customer added 5 tons, delivery needed in 3 days"
- Procurement Agent checks inventory → Logistics Agent evaluates capacity → Quote Agent generates emergency quote
- Output: Optimal plan comparison table

**Example 2**: Monthly Business Analysis
> "Generate last month's business analysis report"
- Data Analysis Agent extracts data → Cost Agent analyzes margins → Report Agent drafts
- Output: Complete monthly report

---

### 🔄 Multi-Agent Collaborative Workflows
**Description**: Multiple AI Agents working in parallel/series to complete complex tasks

**Example 1**: Annual Supplier Assessment
> "Do the annual supplier performance review"
1. ChiefOfStaff defines assessment criteria
2. Procurement Agent tallies delivery performance
3. Quality Agent tallies defect rates
4. Cost Agent tallies cost variances
5. Supplier Agent summarizes scores
- Output: Annual supplier assessment report

**Example 2**: Customer Credit Approval
> "A new customer wants Net-60 terms"
1. Customer Agent investigates background
2. Risk Agent assesses creditworthiness
3. Compliance Agent checks qualifications
- Output: Risk assessment report + credit recommendations

---

## 📖 Details

### 20 Specialized Agents

| Category | Agent | Function |
|----------|-------|----------|
| Procurement | Material Procurement Agent | Market quotes, price comparison, purchasing plans |
| Procurement | Warehouse Agent | Inventory planning, safety stock, slotting |
| Procurement | Logistics Agent | Route optimization, freight calculation |
| Procurement | Supplier Agent | Rating, KPI, contract management |
| Production | Production Scheduling Agent | Scheduling, work orders, delivery planning |
| Production | Formulation Agent | New materials, substitutes, cost optimization |
| Production | Quality Inspection Agent | Incoming, in-process, finished goods testing |
| Production | Equipment Maintenance Agent | Predictive maintenance, downtime reduction |
| Sales | Quote Agent | Quick response, cost-plus pricing |
| Sales | Order Fulfillment Agent | Order tracking, exception handling |
| Sales | Customer Agent | Segmentation, follow-up, repurchase strategy |
| Sales | Competitor Agent | Market analysis, pricing strategy |
| Finance | Cost Accounting Agent | Actual cost, standard cost, margin analysis |
| Finance | Compliance Agent | Environmental, safety, tax compliance |
| Finance | Risk Alert Agent | Credit assessment, bad debt warning |
| Finance | Policy Agent | Industry policies, subsidy applications |
| Operations | Data Analysis Agent | Daily/monthly business reports |
| Operations | Report Generation Agent | Meeting minutes, presentation materials |
| Operations | Project Management Agent | Milestones, risks, progress tracking |
| Operations | Customer Service Agent | After-sales, complaints, FAQ |

### Deployment Options

| Option | Features |
|--------|----------|
| SaaS | Ready to use, monthly subscription, scalable |
| Private Deployment | Deploy on your servers, industry customization |
| API Access | RESTful API + Webhook, multi-language SDK support |

---

## 🔒 Security

✅ **Data Isolation**: All operations execute locally, API calls sent directly to OpenAI/Anthropic servers  
✅ **Credential Protection**: No third-party API keys stored, credentials only exist in user environment variables  
✅ **User Authorization**: All write/delete operations require explicit confirmation  
✅ **Minimal Permissions**: Only requests necessary environment variables (OPENAI_API_KEY, ANTHROPIC_API_KEY)

### Data Collection Scope
- **Data Collected**: Task descriptions and context provided by users
- **Data Sent**: Task content sent to OpenAI/Anthropic API for processing
- **Data NOT Collected**: API keys, enterprise internal data, user behavior logs

### This Skill Will NOT
❌ Execute any operation without user knowledge  
❌ Modify system files or configurations  
❌ Collect user behavior data  
❌ Use user data for model training

---

## ⭐ Support Us

If this skill helps you, please give us a **5-star rating** on ClawHub and XiaPing! 🌟🌟🌟🌟🌟

Your reviews motivate us to keep improving and help more users discover this skill!

- **ClawHub**: https://clawhub.ai/skills/openclaw-enterprise
- **XiaPing**: Visit https://xiaping.coze.site and search for the skill

Thanks for your support! 🙏
