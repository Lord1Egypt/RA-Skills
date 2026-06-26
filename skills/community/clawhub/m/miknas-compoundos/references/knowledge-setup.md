# Knowledge Management Setup

## Purpose

Create your business's long-term memory that auto-categorizes, retrieves, and prevents redoing work.

## Core Components

### 1. Memory Structure

**Daily Memory Files:** `memory/YYYY-MM-DD.md`
- Raw logs of what happened
- Decisions made
- Tasks completed
- Issues encountered
- Lessons learned

**Long-term Memory:** `MEMORY.md`
- Curated, distilled knowledge
- Key insights worth keeping
- Process improvements
- Strategic decisions with rationale
- Contact/vendor info

**Department Memory:** `memory/departments/[department].md`
- Attract/Convert/Retain/Ascend specific knowledge
- SOPs and best practices per department
- Templates and patterns

**Project Memory:** `memory/projects/[project].md`
- Project-specific context, decisions, outcomes
- Cross-department collaboration notes

### 2. Auto-Categorization Rules

Use consistent tagging patterns:

```markdown
## Category: [category-name]

### [subcategory]

- [Insight/decision/outcome]
  - Context: ...
  - Outcome: ...
  - Lesson: ...
```

**Standard categories:**
- **Decisions** - Strategic choices with rationale
- **Processes** - SOPs, workflows, procedures
- **Outcomes** - Results from actions/experiments
- **Insights** - Realizations, patterns discovered
- **Bottlenecks** - Problems blocking progress
- **Solutions** - Fixes that worked
- **Resources** - Tools, contacts, references
- **Experiments** - A/B tests, trials with results

### 3. Auto-Retrieval System

Before any task, agent must:

1. **Search** relevant memory files
2. **Retrieve** context on similar past work
3. **Summarize** relevant findings
4. **Reference** sources with line numbers

**Search patterns:**
- By department: `memory/departments/[department].md`
- By project: `memory/projects/[project].md`
- By date range: `memory/YYYY-MM-DD.md`
- Semantic search: `MEMORY.md` + all memory files

### 4. Memory Capture Triggers

**Always capture:**
- Strategic decisions (why, what, how)
- Process changes/SOPs
- Task outcomes (success/failure)
- Bottlenecks discovered or resolved
- Experiments and results
- Vendor/tool evaluations
- Customer feedback insights
- Competitive intelligence

**Capture format:**
```markdown
### [Date] [Time]

**Type:** [Decision/Process/Outcome/Insight/etc]
**Context:** What led to this
**Action:** What was done/decided
**Outcome:** Result
**Lesson:** What we learned
**Tags:** #department #project #category
```

### 5. Memory Maintenance

**Weekly tasks:**
- Review last 7 days of daily memory
- Extract high-value content for MEMORY.md
- Archive completed project memory
- Remove outdated information

**Monthly tasks:**
- Review MEMORY.md for outdated content
- Consolidate department memory files
- Update contact/vendor lists
- Prune low-value entries

## Implementation Checklist

- [ ] Create `memory/` directory structure
- [ ] Create `MEMORY.md` template
- [ ] Set up daily memory file naming convention
- [ ] Define department memory file structure
- [ ] Establish categorization rules
- [ ] Create memory search patterns
- [ ] Set up auto-capture triggers
- [ ] Create weekly maintenance process
- [ ] Test retrieval system with sample queries

## Integration Points

**With Auto-Capture:**
- All logged data tagged and stored by category
- Automatic routing to appropriate memory file

**With Prioritization Engine:**
- Retrieval of historical bottlenecks before task scoring
- Context on what worked previously

**With Department Agents:**
- Department-specific memory files
- SOPs and templates per department

**With Metrics System:**
- Outcomes captured become performance data points
- Lessons learned feed into strategy refinement

## Sample Memory Entry

```markdown
### 2026-03-01 14:30

**Type:** Decision
**Context:** Needed to decide between video editing tools for YouTube pipeline
**Action:** Selected DaVinci Resolve over Premiere Pro
**Outcome:** $0 cost vs $20/month, professional features available
**Lesson:** Free tools often match paid tools for core features
**Tags:** #attract #tools #cost-optimization
```

---

**Next:** See [learning-loop.md](learning-loop.md) for how captured data feeds intelligence.
