# Human Resources Skill

A people-operations skill for Claude Code and skill-using agents. Helps with recruiting, onboarding, performance management, policy guidance, and compensation analysis. Works standalone with your input, and gets richer when you connect your HRIS, ATS, and other tools.

## Sub-Skills

Each sub-skill handles a specific HR domain. Some are invoked with a slash command; others trigger automatically when the topic comes up.

| Sub-Skill | Slash Command | When It Activates |
|---|---|---|
| `draft-offer` | `/human-resources /draft-offer` | Drafting offer letters and total comp packages |
| `onboarding` | `/human-resources /onboarding` | New hire prep, Day 1 schedules, 30/60/90 plans |
| `performance-review` | `/human-resources /performance-review` | Self-assessments, manager reviews, calibration prep |
| `policy-lookup` | `/human-resources /policy-lookup` | HR policy questions — PTO, benefits, expenses, remote work |
| `comp-analysis` | `/human-resources /comp-analysis` | Compensation benchmarking, band analysis, equity modeling |
| `people-report` | `/human-resources /people-report` | Headcount, attrition, diversity, and org health reports |
| `recruiting-pipeline` | `/human-resources /recruiting-pipeline` | Pipeline status, hiring velocity, candidate tracking |
| `org-planning` | `/human-resources /org-planning` | Headcount planning, team structure, reorg design |
| `interview-prep` | `/human-resources /interview-prep` | Interview plans, question banks, scorecards |

## Example Workflows

### Drafting an Offer
```
/human-resources /draft-offer Senior Engineer, L5, San Francisco
```
Provide role, level, location, and comp details. Get a complete offer letter with terms, equity breakdown, and benefits summary.

### Onboarding a New Hire
```
/human-resources /onboarding Jamie Lee, Product Manager, Growth team, starting June 23
```
Get a pre-start checklist, Day 1 schedule, Week 1 plan, 30/60/90-day goals, and a key contacts table.

### Preparing for Performance Reviews
```
/human-resources /performance-review calibration
```
Get calibration prep, rating distribution templates, and discussion guides for the team.

### Compensation Benchmarking
```
/human-resources /comp-analysis Staff Engineer, L6
```
Get market percentile bands, band placement analysis, and equity refresh recommendations.

### Anything HR-Related (Auto-Triggered)
Just ask naturally:
```
What does our recruiting pipeline look like this quarter?
Who should we hire next on the data team?
How should we structure interviews for a Head of Design?
```
The relevant sub-skill activates automatically.

## Standalone + Supercharged

Every sub-skill works without any integrations — just provide context directly. Connecting tools unlocks additional capabilities:

| Sub-Skill | Standalone | Supercharged With |
|---|---|---|
| `draft-offer` | Provide comp details manually | HRIS (comp bands, headcount approval), ATS (candidate details) |
| `onboarding` | Describe your process | HRIS (org chart, tools access), knowledge base (wikis, runbooks), calendar (Day 1 events) |
| `performance-review` | Manual input | HRIS (review history), project tracker (completed work) |
| `policy-lookup` | Paste handbook content | Knowledge base (employee handbook, policy docs), HRIS (employee-specific details) |
| `comp-analysis` | Upload CSV or describe bands | Compensation data (market benchmarks), HRIS (current employee comp) |
| `people-report` | Upload data | HRIS (live employee data), chat (share summaries) |
| `recruiting-pipeline` | Provide pipeline details | ATS (live candidate data) |
| `org-planning` | Describe current structure | HRIS (headcount, reporting structure) |
| `interview-prep` | Describe the role | ATS (job description, scorecard history) |

## Connectors

See [CONNECTORS.md](CONNECTORS.md) for the full list of supported integrations and how `~~placeholder` references work in sub-skills.

| Category | Examples |
|---|---|
| **HRIS** | Workday, BambooHR, Rippling, Gusto |
| **ATS** | Greenhouse, Lever, Ashby, Workable |
| **Knowledge base** | Notion, Atlassian (Confluence), Guru, Coda |
| **Compensation data** | Pave, Radford, Levels.fyi |
| **Chat** | Slack, Microsoft Teams |
| **Calendar** | Google Calendar, Microsoft 365 |
| **Email** | Gmail, Microsoft 365 |

