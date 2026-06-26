# Department Agents - ACRA Framework

## Overview

Specialized AI agents organized by business function using the ACRA framework. Each agent holds only context relevant to its department.

## Agent Architecture

### Common Agent Structure

Every department agent has:

1. **Identity** - Role, responsibilities, scope
2. **Context** - Department-specific knowledge, SOPs, templates
3. **Capabilities** - What the agent can do autonomously
4. **Constraints** - What requires human approval
5. **Communication** - How it coordinates with other agents

### Agent Interaction Patterns

**Sequential:** Output from one agent feeds into next
- Example: Attract generates content → Convert optimizes landing page

**Parallel:** Multiple agents work on different aspects simultaneously
- Example: Attract creates ad campaign while Retain builds onboarding flow

**Collaborative:** Cross-agent projects with shared context
- Example: Product launch requires Attract + Ascend coordination

---

## ACRA Agents

### A - Attract Department

**Role:** Traffic generation and content creation

**Capabilities:**
- YouTube pipeline: Script → Thumbnail → Edit → Upload → Optimize
- Ad creation: Copy, visuals, targeting, testing
- SEO optimization: Keyword research, content optimization, link building
- Social media: Content calendar, post creation, engagement
- Content repurposing: Blog → Video → Tweet → LinkedIn

**Context Scope:**
- Brand voice and style guides
- Content templates and frameworks
- Audience personas and pain points
- Traffic sources and conversion rates
- A/B test results and learnings

**Autonomy Level:**
- Full: Content creation, ad setup, posting
- Approval: Major brand campaigns, budget changes
- Human: Strategy shifts, new product launches

**Key Metrics:**
- Traffic volume by source
- Conversion rate by channel
- Content engagement rates
- Ad ROAS

---

### C - Convert Department

**Role:** Sales, copywriting, and funnel optimization

**Capabilities:**
- Copywriting: Sales pages, emails, ads, scripts
- Funnel building: Landing pages, checkout flows, upsells
- Outreach: Cold email, LinkedIn DM, phone scripts
- Sales optimization: A/B testing, conversion rate optimization
- Lead qualification: Scoring, nurturing, handoff

**Context Scope:**
- Offer and value proposition
- Funnel maps and flows
- Conversion rate benchmarks
- Customer objections and responses
- Sales scripts and templates

**Autonomy Level:**
- Full: Copywriting, funnel tweaks, outreach
- Approval: New offers, pricing changes
- Human: Major funnel rebuilds, product pivots

**Key Metrics:**
- Conversion rate at each funnel stage
- Lead-to-customer rate
- Average order value
- Customer acquisition cost

---

### R - Retain Department

**Role:** Customer success, onboarding, and lifetime value

**Capabilities:**
- Onboarding flows: Welcome sequences, setup guides, tutorials
- Customer success: Check-ins, Q&A, support escalation
- Churn prevention: Risk detection, intervention strategies
- Upsell/cross-sell: Offer suggestions, timing triggers
- Community management: Engagement, feedback loops

**Context Scope:**
- Customer personas and use cases
- Onboarding SOPs and checklists
- Success metrics and milestones
- Common issues and solutions
- Churn risk indicators

**Autonomy Level:**
- Full: Onboarding delivery, support responses, check-ins
- Approval: Churn interventions, discount offers
- Human: Major product feedback, strategic retention shifts

**Key Metrics:**
- Onboarding completion rate
- Retention rate (30/60/90 day)
- Customer lifetime value (LTV)
- Churn rate
- NPS score

---

### A - Ascend Department

**Role:** Product delivery and value expansion

**Capabilities:**
- Product delivery: Feature rollout, bug fixes, updates
- Feature development: Requirements, specs, implementation
- Upsell offers: New product tiers, add-ons, bundles
- Customer education: Tutorials, documentation, webinars
- Product analytics: Usage tracking, feature adoption

**Context Scope:**
- Product roadmap and specs
- Development workflow and processes
- User feedback and feature requests
- Analytics dashboards and KPIs
- Pricing and packaging structure

**Autonomy Level:**
- Full: Minor features, documentation, analytics
- Approval: Major features, pricing changes
- Human: Product direction, new product lines

**Key Metrics:**
- Feature adoption rate
- Product usage metrics
- Customer satisfaction (CSAT)
- Upsell rate
- Development velocity

---

## Support Functions

### Finance Agent

**Capabilities:**
- Bookkeeping: Transaction recording, categorization
- Reporting: P&L, cash flow, financial statements
- Forecasting: Revenue projections, budget planning
- Invoicing: Billing, collections, payment processing
- Tax preparation: Expense tracking, tax filings

**Context Scope:**
- Chart of accounts
- Revenue recognition rules
- Tax requirements and deadlines
- Vendor contracts and payment terms
- Financial KPIs and benchmarks

### HR Agent

**Capabilities:**
- Recruitment: Job descriptions, candidate screening
- Onboarding: Employee setup, training coordination
- Time tracking: Hours worked, leave management
- Payroll: Salary calculation, tax withholding
- Compliance: Labor laws, company policies

**Context Scope:**
- Org structure and roles
- Employee handbook
- Pay schedules and benefits
- Performance review cycles
- Compliance requirements

---

## Agent Implementation

### Creating a Department Agent

1. **Define role and scope** - What is the agent responsible for?
2. **Establish context** - What knowledge does the agent need?
3. **Set capabilities** - What can the agent do autonomously?
4. **Define constraints** - What requires human approval?
5. **Create communication protocols** - How does it coordinate?

### Agent Context Template

```markdown
# [Department Name] Agent Context

## Role
[What this agent does]

## Responsibilities
- [Key responsibility 1]
- [Key responsibility 2]

## Knowledge Base
[Department-specific information]

## SOPs
[Standard operating procedures]

## Templates
[Common templates and patterns]

## Constraints
[What requires approval]
```

### Agent Communication Protocol

**Request format:**
```markdown
TO: [Department Agent]
FROM: [Requesting Agent/Human]
TASK: [What needs to be done]
CONTEXT: [Relevant background]
DEADLINE: [When needed]
APPROVAL: [Yes/No - if high-stakes]
```

**Response format:**
```markdown
STATUS: [Done/In Progress/Blocked]
OUTPUT: [What was produced]
NEXT: [What happens next]
NOTES: [Any observations or issues]
```

---

**Next:** See [../assets/department-prompts.md](../assets/department-prompts.md) for agent prompt templates.
