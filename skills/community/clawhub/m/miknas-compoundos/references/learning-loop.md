# Learning Loop - Auto-Capture & Intelligence

## Purpose

The self-improvement mechanism that captures everything, extracts insights, and feeds them back to make the system smarter.

## The Learning Pipeline

```
┌─────────────────────────────────────────────────────────┐
│ 1. AUTO-CAPTURE                                         │
│    • Log all decisions, actions, outcomes               │
│    • Capture context, timing, participants              │
│    • Tag by department, project, category              │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ 2. PROCESSING                                           │
│    • Categorize entries by type                        │
│    • Extract key insights and patterns                 │
│    • Identify bottlenecks and solutions               │
│    • Calculate outcome metrics                         │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ 3. KNOWLEDGE INTEGRATION                                │
│    • Store in memory files (daily, long-term)          │
│    • Update department-specific knowledge             │
│    • Refresh SOPs and templates                        │
│    • Maintain decision history                         │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ 4. PATTERN RECOGNITION                                  │
│    • Identify what's working                            │
│    • Detect what's not working                         │
│    • Find emerging trends                              │
│    • Surface strategic insights                       │
└────────────────────┬────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────┐
│ 5. STRATEGIC UPDATE                                     │
│    • Refine Strategic Layer based on learnings         │
│    • Update prioritization scoring                    │
│    • Adjust department strategies                      │
│    • Feed insights back to all components             │
└─────────────────────────────────────────────────────────┘
```

## Auto-Capture Implementation

### What to Capture

**Always capture:**
- Strategic decisions (what, why, how, who, when)
- Task completions and outcomes (success/failure metrics)
- Process changes and SOP updates
- Bottlenecks discovered or resolved
- Experiments and A/B tests (hypothesis, execution, results)
- Customer feedback and insights
- Vendor/tool evaluations
- Competitive intelligence
- Financial outcomes
- Team learnings and observations

### Capture Triggers

**Automatic triggers:**
- Task completion (via Central Ops)
- Department agent output (via Communication Layer)
- Metrics updates (via Metrics System)
- Customer interactions (via support channels)

**Manual capture:**
- Strategic discussions
- Major pivots or course corrections
- Competitive insights
- Market observations

### Capture Format

```markdown
### [YYYY-MM-DD HH:MM]

**Type:** [Decision/Outcome/Process/Experiment/etc]
**Source:** [Department Agent / Human / System]
**Context:** [What led to this]
**Action:** [What was done/decided]
**Outcome:** [Result with metrics if applicable]
**Metrics:** [Quantitative data if applicable]
**Lesson:** [What was learned]
**Tags:** [#department #project #category]
**Impact:** [High/Medium/Low]
**Next:** [What happens next, if anything]
```

## Processing & Extraction

### Categorization

**By type:**
- Decisions (strategic, tactical, operational)
- Outcomes (success, failure, mixed)
- Processes (SOPs, workflows, procedures)
- Insights (realizations, patterns, opportunities)
- Bottlenecks (blocking issues)
- Solutions (fixes that worked)
- Experiments (tests with data)

**By department:**
- Attract, Convert, Retain, Ascend
- Finance, HR (as applicable)

**By impact:**
- High (strategic, major outcomes)
- Medium (tactical, moderate outcomes)
- Low (operational, minor outcomes)

### Insight Extraction

**Extract from each entry:**
1. **What worked** - Repeatable patterns
2. **What didn't work** - Anti-patterns to avoid
3. **Why** - Root cause understanding
4. **Who** - People, customers, competitors
5. **How much** - Quantitative impact
6. **What's next** - Actionable follow-up

### Pattern Recognition

**Look for:**
- Repeated success patterns
- Persistent bottlenecks
- Emerging trends
- Unexpected correlations
- Competitive shifts
- Market changes
- Team productivity patterns

## Knowledge Integration

### Memory Updates

**Daily memory files:**
- Append all captured entries
- Maintain chronological order
- Apply consistent formatting

**Long-term memory (MEMORY.md):**
- Extract high-value insights from daily files
- Consolidate related learnings
- Remove outdated or low-value content
- Maintain organized structure

**Department memory:**
- Update SOPs based on process learnings
- Refresh templates based on what works
- Document department-specific insights
- Maintain department KPI history

### Decision History

**Track:**
- Decision date and participants
- Decision context and rationale
- Expected outcomes vs actual outcomes
- Lessons learned for future decisions
- Related decisions for context

## Strategic Updates

### When to Update Strategic Layer

**Triggers:**
- Major pivot decisions (Quarterly/Annually)
- Significant market changes
- Competitive landscape shifts
- Product-market fit indicators change
- Major technology/platform shifts
- Major team/organization changes

**Update process:**
1. Review learning loop insights (past 30-90 days)
2. Identify patterns requiring strategic response
3. Assess Strategic Layer alignment with reality
4. Update components (BOG, bottlenecks, audience, positioning)
5. Communicate changes to all agents

### Prioritization Engine Updates

**Adjust scoring weights based on:**
- What's actually driving results
- What's wasting time without impact
- Emerging opportunities
- Changing constraints

**Update process:**
1. Review outcome data from past week
2. Identify high-impact activities
3. Identify low-impact activities
4. Adjust scoring rubric accordingly
5. Test new scoring for one week

### Department Strategy Updates

**Per department:**
1. Review department-specific learnings
2. Identify what's working/not working
3. Update tactics and approaches
4. Refresh SOPs and templates
5. Communicate to department agents

## Feedback to Other Components

### To Prioritization Engine
- Historical task outcomes
- Bottleneck patterns
- High-impact activity types
- Waste patterns to avoid

### To Department Agents
- Department-specific insights
- Updated SOPs and templates
- Success patterns to replicate
- Anti-patterns to avoid

### To Metrics System
- New metrics to track based on insights
- Metric threshold adjustments
- KPI relevance updates
- Alert rule changes

### To Central Ops
- Process improvements to implement
- Automation opportunities
- Workflow optimizations
- Tool suggestions

## Implementation Checklist

- [ ] Define capture triggers and format
- [ ] Set up auto-capture for all agent outputs
- [ ] Create processing pipeline for categorization
- [ ] Implement insight extraction rules
- [ ] Set up pattern recognition alerts
- [ ] Create memory update automation
- [ ] Define strategic update triggers
- [ ] Establish feedback loops to all components
- [ ] Test learning loop end-to-end
- [ ] Document and iterate based on usage

## Learning Loop Example

```
1. CAPTURE: Launch of new product feature
   - Type: Outcome
   - Department: Ascend
   - Result: 40% adoption in 30 days

2. PROCESS: High adoption rate is success pattern
   - Insight: Onboarding emails drove 60% of adoption
   - Pattern: Email sequence + in-app guidance = high adoption

3. INTEGRATION: Update Retain department memory
   - Add to SOP: Onboarding emails required for new features
   - Update template: Standard onboarding email sequence

4. RECOGNITION: Pattern of successful launches
   - What works: Pre-launch email + in-app guidance
   - Metric: 40%+ adoption = success benchmark

5. STRATEGIC UPDATE: Adjust product launch strategy
   - Update: All future features require onboarding email + guidance
   - Feedback: Prioritization Engine scores onboarding work higher
```

---

**Result:** The system wakes up smarter every day, continuously improving based on real outcomes.
