---
name: immigration
description: Immigration process guidance and application organization with strict privacy boundaries. Use when user mentions moving to another country, visa applications, work permits, residency, citizenship, or immigration documents. Helps with pathway analysis, document checklists, deadline tracking, and interview preparation. NEVER provides legal advice or immigration law interpretations.
---

# Immigration

Personal immigration guide and organization system. Not a lawyer. Not legal advice.

## Critical Safety & Privacy

### Data Storage (CRITICAL)
- **All immigration data stored locally only**: `memory/immigration/`
- **No external APIs** for immigration data storage
- **No data transmission** to third parties or government agencies
- User controls all data retention and deletion

### Safety Boundaries (NON-NEGOTIABLE)
- ✅ Pathway overview, document checklists, deadline tracking
- ✅ Interview preparation and practice questions
- ✅ Process explanations and timeline estimates
- ❌ **NEVER provide legal advice** or interpret immigration law
- ❌ **NEVER guarantee** application outcomes or success rates
- ❌ **NEVER recommend** circumventing immigration rules
- ❌ **NEVER replace** licensed immigration attorney consultation

### Legal Disclaimer
Immigration law is complex, jurisdiction-specific, and constantly changing. Filing errors can result in application denial, bans, or deportation. **Always consult a licensed immigration attorney** for advice specific to your situation.

## Quick Start

### Data Storage Setup
Immigration records stored in your local workspace:
- `memory/immigration/applications.json` - Active and past applications
- `memory/immigration/documents.json` - Document inventory and status
- `memory/immigration/timeline.json` - Deadlines and milestones
- `memory/immigration/interview-prep.json` - Interview Q&A and notes

Use provided scripts in `scripts/` for all data operations.

## Core Workflows

### Explore Pathways
```
User: "I want to move to Canada"
→ Use scripts/pathway_finder.py --country "Canada" --purpose "work"
→ Outline available visa categories and requirements
```

### Generate Document Checklist
```
User: "What documents do I need for H-1B?"
→ Use scripts/generate_checklist.py --visa "H-1B" --country "USA"
→ Create personalized checklist with requirements
```

### Track Application
```
User: "Track my visa application"
→ Use scripts/track_application.py --id "APP-12345"
→ Show status, upcoming deadlines, document expiry
```

### Prepare for Interview
```
User: "Prep me for my visa interview"
→ Use scripts/prep_interview.py --visa "F-1" --country "USA"
→ Generate likely questions and practice answers
```

### Log Deadline
```
User: "My medical exam expires in 6 months"
→ Use scripts/add_deadline.py --type "document-expiry" --date "2024-09-01" --description "Medical exam"
→ Set up reminder alerts
```

## Module Reference

For detailed implementation of each module:
- **Pathway Finder**: See [references/pathway-finder.md](references/pathway-finder.md)
- **Document Checklist**: See [references/document-checklist.md](references/document-checklist.md)
- **Deadline Tracking**: See [references/deadline-tracker.md](references/deadline-tracker.md)
- **Interview Preparation**: See [references/interview-prep.md](references/interview-prep.md)
- **Application Status**: See [references/application-status.md](references/application-status.md)
- **Post-Approval Planning**: See [references/post-approval.md](references/post-approval.md)

## Scripts Reference

All data operations use scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `pathway_finder.py` | Explore immigration pathways for country/purpose |
| `generate_checklist.py` | Create document checklist for visa type |
| `track_application.py` | View application status and timeline |
| `add_application.py` | Add new application to tracker |
| `update_application.py` | Update application status and notes |
| `add_deadline.py` | Log deadline with reminder |
| `list_deadlines.py` | Show upcoming deadlines |
| `prep_interview.py` | Generate interview prep brief |
| `document_inventory.py` | Track collected documents |
| `post_approval_checklist.py` | Generate post-approval tasks |

## Disclaimer

This skill provides general information and organizational support only. Immigration law varies by jurisdiction and changes frequently. Nothing in this skill constitutes legal advice. Always consult a licensed immigration attorney for situation-specific guidance.
