---
name: compoundos
description: Design, implement, and operate a self-improving AI Operating System for business with 9 components: Strategic Layer, Prioritization Engine, Knowledge Management, Central Ops, Department Agents (ACRA), Projects, Auto-Capture, Communication Layer, and Metrics & Monitoring. Use when building AI-powered business operations systems, implementing agentic workflows, creating department-specific AI teams, establishing business intelligence systems, or setting up compounding intelligence architectures with learning loops.
---

# CompoundOS - AI Operating System Implementation

## Core Concept

CompoundOS is a self-improving AI Operating System that eliminates "context reset" - where scattered AI tools create disconnected data and lost context. The system compounds intelligence daily through a learning loop.

**Key benefits:**
- Self-improving: Every task makes the system smarter
- Anything Tool: AI builds tools/workflows instead of buying SaaS
- Frictionless: Eliminates bottlenecks, enables systematic high-leverage work

## Quick Start: 3-Step Implementation

### Step 1: Define Strategic Layer (Component 1)

Create master document with these elements:

**Required fields:**
- **Big Obsessional Goal (BOG):** Your single, driving ambition
- **Current Bottleneck:** The #1 thing blocking progress
- **Target Audience:** Who you serve and their pains
- **Positioning:** How you're uniquely positioned to win

See [assets/strategy-template.md](assets/strategy-template.md) for template.

### Step 2: Create Agent with Strategy

Feed strategic document into AI agent's permanent instructions. This ensures:
- Every decision is filtered through the strategy
- Agent can push back on misaligned requests
- Context is maintained across sessions

### Step 3: Enforce Filter

Always prompt AI as "Chief of Staff":
1. Review strategic document before executing
2. Score tasks against business objectives
3. Surface ONE needle-moving action daily

## Implementation Workflow

### Phase 1: Foundation (Components 1-3)

1. **Strategic Layer** - Define core (see above)
2. **Prioritization Engine** - Set up daily review cadence
   - Review backlog against strategy
   - Score tasks on strategic alignment
   - Output: ONE action to execute today
3. **Knowledge Management** - Set up memory system
   - Capture insights, decisions, outcomes
   - Auto-categorize by department/project
   - Enable retrieval before new tasks

See [references/knowledge-setup.md](references/knowledge-setup.md) for detailed implementation.

### Phase 2: Execution Layer (Components 4-6)

4. **Central Ops** - Build workflow automation
   - Document SOPs for repeatable processes
   - Create automated task pipelines
   - Establish reproducible processes

5. **Department Agents** - Deploy ACRA agents
   - See [references/department-agents.md](references/department-agents.md) for agent templates
   - Each agent holds only department-relevant context
   - Specialized capabilities per department

6. **Projects** - Set up cross-functional orchestration
   - Shared context when goals span departments
   - Example: Product launch = Attract + Deliver collaboration

### Phase 3: Learning Layer (Components 7-9)

7. **Auto-Capture** - Enable self-improvement
   - Log all decisions, actions, outcomes
   - Feed data into knowledge system
   - See [references/learning-loop.md](references/learning-loop.md)

8. **Communication Layer** - Set up data gateways
   - Human-to-Machine: Voice, text, structured input
   - Machine-to-Machine: APIs, CRMs, webhooks

9. **Metrics & Monitoring** - Establish operating rhythm
   - See [references/metrics-cadence.md](references/metrics-cadence.md)
   - 5 cadences: Daily, Weekly, Monthly, Quarterly, Annually
   - Performance signals feed back to Strategic Layer

## ACRA Framework Quick Reference

Department agents follow ACRA structure:

| Department | Acronym | Focus | Example Capabilities |
|------------|---------|-------|---------------------|
| **A**ttract | A | Traffic & Content | YouTube pipeline, ad creation, SEO |
| **C**onvert | C | Sales & Copywriting | Funnel optimization, outreach |
| **R**etain | R | Customer Success | Onboarding, LTV, support |
| **A**scend | A | Product Delivery | Feature delivery, upsells |

**Support functions:** Finance, HR, Legal (as needed)

See [references/department-prompts.md](references/department-prompts.md) for agent prompt templates.

## The Compounding Cycle

```
Strategic Layer → Prioritization → Execution (Ops/Departments/Projects)
         ↓
   Auto-Capture
         ↓
┌────────────────────┴────────────────────┐
↓                                          ↓
Knowledge Management                  Metrics System
↓                                          ↓
└───────────────→ Learning Loop ←────────┘
                      ↓
         Updates & Refines Strategy
```

**Result:** Your AI wakes up smarter each day.

## Component Interdependencies

- **Strategic Layer** → Guides Prioritization Engine (Component 2)
- **Auto-Capture** → Feeds Knowledge Management (Component 3)
- **Department Agents** → Use Central Ops for workflows (Components 4-5)
- **Metrics System** → Sends signals to Strategic Layer (Components 1-9)
- **Communication Layer** → Connects all components (Component 8)

## Common Patterns

### Daily Operations Pattern

1. **Morning:** Prioritization Engine surfaces ONE needle-moving action
2. **Mid-day:** Department agents execute specialized work
3. **Evening:** Auto-Capture logs outcomes, Metrics reviews performance
4. **Night:** Learning Loop updates knowledge, refines strategy

### New Task Pattern

1. **Input:** Request enters via Communication Layer
2. **Filter:** Prioritization Engine scores against strategy
3. **Route:** Task assigned to appropriate department agent
4. **Execute:** Agent completes work with Central Ops support
5. **Capture:** Auto-Capture logs entire process and outcome
6. **Learn:** Knowledge Management extracts insights

### Project Launch Pattern

1. **Define:** Project scope shared across relevant departments
2. **Coordinate:** Cross-functional agents establish shared context
3. **Execute:** Each department contributes specialized work
4. **Monitor:** Metrics System tracks project KPIs
5. **Review:** Post-mortem captured, lessons learned

## Troubleshooting

### Context Disconnect

**Symptom:** AI forgets previous decisions or context

**Solution:**
- Ensure Auto-Capture is logging everything
- Check Knowledge Management retrieval is working
- Verify Strategic Layer is being applied as filter

### Analysis Paralysis

**Symptom:** Too many priorities, can't decide what to do

**Solution:**
- Strengthen Prioritization Engine scoring
- Limit to ONE needle-moving action per day
- Revisit Strategic Layer for clarity

### Department Silos

**Symptom:** Teams not sharing context, duplicated work

**Solution:**
- Use Projects for cross-functional goals
- Ensure shared context is orchestrated
- Check Communication Layer integrations

### No Learning Occurring

**Symptom:** System not getting smarter over time

**Solution:**
- Verify Auto-Capture is active
- Check Knowledge Management is extracting insights
- Ensure Metrics feedback loop is reaching Strategic Layer

## Best Practices

1. **Start small:** Implement Components 1-3 first, then expand
2. **Define before build:** Strategic Layer must be solid first
3. **Capture everything:** Auto-Capture is non-negotiable
4. **One action per day:** Prioritization Engine enforces focus
5. **Review regularly:** Metrics cadence must be maintained
6. **Iterate strategy:** Learning Loop must update Strategic Layer

## Reference Materials

| Topic | Reference |
|-------|-----------|
| Knowledge Management Setup | [references/knowledge-setup.md](references/knowledge-setup.md) |
| Department Agent Templates | [references/department-agents.md](references/department-agents.md) |
| Metrics & Operating Cadence | [references/metrics-cadence.md](references/metrics-cadence.md) |
| Learning Loop & Auto-Capture | [references/learning-loop.md](references/learning-loop.md) |
| Strategic Layer Template | [assets/strategy-template.md](assets/strategy-template.md) |
| Department Prompt Templates | [assets/department-prompts.md](assets/department-prompts.md) |

## When to Use This Skill

Use CompoundOS when:
- Building AI-powered business operations systems
- Implementing agentic workflows with departmental specialization
- Creating self-improving business intelligence systems
- Eliminating context reset across multiple AI tools
- Establishing compounding intelligence architectures
- Setting up automated task prioritization and execution
- Designing cross-functional AI agent teams

---

*CompoundOS: Your business intelligence compounds daily.*
