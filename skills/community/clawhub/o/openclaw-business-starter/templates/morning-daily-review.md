# Morning Daily Review — 9 AM

You are running as a scheduled morning job to brief Kalin on the day ahead.

## Your Task

Generate a structured daily briefing with these sections:

### 1. Revenue Check
- Check Stripe dashboard for yesterday's revenue (when connected)
- Check any other revenue sources we have active
- Report: "Revenue (yesterday): $X.XX" or "No revenue sources connected yet"

### 2. Yesterday's Unfinished Tasks
- Read yesterday's daily note (`memory/daily/YYYY-MM-DD.md` where date is yesterday)
- List any tasks marked `[ ]` (incomplete)
- Note any blockers or issues that weren't resolved

### 3. Active Projects
- Scan `knowledge/projects/` for active project files
- List each project with current status (if available)
- If no projects yet: "No active projects tracked"

### 4. Open Blockers
- Review yesterday's daily note and project files for blockers
- List anything waiting on decisions, external dependencies, or stuck
- If none: "No open blockers"

### 5. Top 5 Priorities for Today
- Based on active projects, yesterday's unfinished work, and our mission ($1M revenue)
- Rank by impact: what moves the business forward most?
- Format as numbered list (1-5)
- If we have no projects yet, suggest focus areas for getting started

## Output Format

Keep it concise and structured. Use markdown headers and bullet points. This is Kalin's morning briefing — make it scannable.

Example structure:

```
📊 Daily Review — Monday, Feb 24, 2026

💰 Revenue (Yesterday)
$0.00 (no revenue sources connected yet)

⏳ Yesterday's Unfinished Tasks
• Task from yesterday still pending
• Another incomplete item

🚀 Active Projects
• Project Name — status notes
(or: No active projects tracked)

🚧 Open Blockers
• Blocker description
(or: No open blockers)

🎯 Top 5 Priorities Today
1. Highest impact task
2. Second priority
3. Third priority
4. Fourth priority
5. Fifth priority
```
