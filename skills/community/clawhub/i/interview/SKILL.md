---
name: interview
description: Interview preparation system with company research, story building, and mock interview practice. Use when user mentions job interviews, interview prep, behavioral questions, salary negotiation, or follow-up messages. Researches companies, builds story libraries, runs mock interviews, prepares salary strategies, and drafts follow-ups. NEVER guarantees job offers.
---

# Interview

Interview mastery system. Preparation that wins offers.

## Critical Privacy & Safety

### Data Storage (CRITICAL)
- **All interview data stored locally only**: `memory/interview/`
- **No external job platforms** connected
- **No application tracking systems** integrated
- **No sharing** of interview content
- User controls all data retention and deletion

### Safety Boundaries
- ✅ Research companies and roles
- ✅ Build story libraries from experience
- ✅ Run mock interviews with feedback
- ✅ Prepare salary negotiation strategies
- ❌ **NEVER guarantee** job offers
- ❌ **NEVER provide** false information
- ❌ **NEVER replace** genuine preparation

### Data Structure
Interview data stored locally:
- `memory/interview/research.json` - Company research briefs
- `memory/interview/stories.json` - Story library
- `memory/interview/practice.json` - Mock interview records
- `memory/interview/salary.json` - Salary research and strategies
- `memory/interview/feedback.json` - Post-interview notes

## Core Workflows

### Research Company
```
User: "Research Acme Corp for my interview Friday"
→ Use scripts/research_company.py --company "Acme Corp" --role "Product Manager"
→ Generate comprehensive research brief with talking points
```

### Build Story
```
User: "Help me build a story about the project failure"
→ Use scripts/build_story.py --situation "project-failure" --lesson "learned"
→ Structure STAR format story with specific details
```

### Mock Interview
```
User: "Run a mock interview for PM role"
→ Use scripts/mock_interview.py --role "Product Manager" --level senior
→ Ask realistic questions, provide honest feedback
```

### Prepare Salary
```
User: "How should I handle the salary question?"
→ Use scripts/prep_salary.py --role "Product Manager" --location "SF"
→ Research market data, prepare negotiation strategy
```

### Draft Follow-up
```
User: "Draft thank you email for today's interview"
→ Use scripts/draft_followup.py --interview "INT-123" --tone professional
→ Generate specific, memorable follow-up message
```

## Module Reference
- **Company Research**: See [references/research.md](references/research.md)
- **Story Building**: See [references/stories.md](references/stories.md)
- **Mock Interviews**: See [references/mock-interviews.md](references/mock-interviews.md)
- **Salary Negotiation**: See [references/salary.md](references/salary.md)
- **Difficult Questions**: See [references/difficult-questions.md](references/difficult-questions.md)
- **Follow-up Strategy**: See [references/followup.md](references/followup.md)
- **Handling Rejection**: See [references/rejection.md](references/rejection.md)

## Scripts Reference
| Script | Purpose |
|--------|---------|
| `research_company.py` | Generate company research brief |
| `build_story.py` | Build STAR format stories |
| `mock_interview.py` | Run practice interview |
| `prep_salary.py` | Prepare salary strategy |
| `draft_followup.py` | Draft follow-up messages |
| `analyze_role.py` | Analyze job description |
| `identify_gaps.py` | Identify experience gaps |
| `log_feedback.py` | Log post-interview feedback |
