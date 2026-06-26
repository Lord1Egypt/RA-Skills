# Insight Tag Taxonomy

## Standard Tags

### pattern
Recurring behaviors, structures, or phenomena observed across sessions or data.

**Use when:**
- Same issue appears multiple times
- User consistently makes similar choices
- Systematic behavior is identified

**Examples:**
- "Pattern: User always validates before publishing"
- "Pattern: Memory files grow large after 2 weeks"

### learning
New understanding, skill, or knowledge acquired.

**Use when:**
- New capability is discovered
- Better way of doing things is found
- Understanding deepens on a topic

**Examples:**
- "Learning: Bash scripts run faster than Node for file ops"
- "Learning: User prefers concise summaries"

### decision
Choices made and the rationale behind them.

**Use when:**
- Architecture decision is made
- Tool is selected over alternatives
- Approach is chosen

**Examples:**
- "Decision: Use SQLite over JSON for large datasets"
- "Decision: Prioritize MVP over completeness"

### risk
Potential issues, concerns, or threats identified.

**Use when:**
- Something might go wrong
- Technical debt is identified
- Security concern is noted

**Examples:**
- "Risk: No backup strategy for memory files"
- "Risk: Skill dependencies not documented"

### opportunity
Potential improvements, optimizations, or wins.

**Use when:**
- Better way is spotted
- Efficiency gain is possible
- New capability could be added

**Examples:**
- "Opportunity: Cache validation results"
- "Opportunity: Automate daily reports"

### user-preference
User-specific preferences or working styles.

**Use when:**
- User expresses a preference
- Working pattern is observed
- Customization need is identified

**Examples:**
- "User preference: Output in Markdown"
- "User preference: Morning standup format"

### technical
Technical findings, constraints, or capabilities.

**Use when:**
- Technical limitation found
- New tool capability discovered
- Integration behavior noted

**Examples:**
- "Technical: API rate limit is 100/min"
- "Technical: jq not available on all systems"

### process
Workflow, methodology, or procedural insights.

**Use when:**
- Better workflow identified
- Process improvement noted
- Methodology lesson learned

**Examples:**
- "Process: Validate before packaging"
- "Process: Review skills weekly"

## Tag Combinations

Tags can be combined for richer categorization:

- `pattern` + `user-preference`: Recurring user behavior
- `risk` + `technical`: Technical risk
- `learning` + `process`: Process improvement learned
- `decision` + `technical`: Technical decision

## Creating New Tags

New tags should be:
1. Generic enough to apply to multiple insights
2. Specific enough to be meaningful
3. Documented in this file
4. Reviewed periodically for relevance
