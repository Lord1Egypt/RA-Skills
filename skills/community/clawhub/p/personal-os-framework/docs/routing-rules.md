# Routing Rules

## The Routing Question

Every piece of information that enters your system needs an answer to one question:

**Where does this belong?**

## Categories

| Category | Description | Canonical Location |
|----------|-------------|-------------------|
| Raw Capture | Quick notes, ideas, links | `Inbox/` |
| Task | Actionable work item | `Projects/<name>/TODO.md` |
| Decision | Judgment with rationale | `DECISIONS.md` or `Chronicle/decisions/` |
| Incident | Something that happened | `Chronicle/incidents/` |
| Reference | Useful information | `Knowledge/` |
| Project | Ongoing work container | `Projects/<name>/` |

## Routing Decision Tree

```
Is it actionable?
├── Yes → Is it a single action?
│   ├── Yes → TASK
│   └── No → Can it wait?
│       ├── Yes → TASK (with future date)
│       └── No → INCIDENT
└── No → Is it for later reference?
    ├── Yes → KNOWLEDGE
    └── No → Is it temporary?
        ├── Yes → INBOX
        └── No → REFERENCE
```

## Decision Rules

1. **Raw notes go to Inbox first**. Never decide destination immediately.
2. **Tasks have one owner**. If it's yours, it's in your TODO.
3. **Decisions have rationale**. If there's no why, it's not a decision yet.
4. **Incidents are time-stamped**. Something happened, not will happen.
5. **Knowledge is permanent-ish**. If you'll want it in 6 months, it's knowledge.

## Routing to Projects

A piece of information belongs to a project if:
- It relates to an active project
- It will be needed for project decisions
- It tracks project progress

Otherwise, it belongs in Chronicle (decisions, incidents, knowledge).

## When in Doubt

Default to **Inbox**. It's easier to promote from Inbox than to demote from a wrong location.

## Ambiguity Cases

When you're unsure, log it as an **ambiguity case**:
- What the item was
- What you chose
- Why you chose it

This builds evidence for future routing decisions.

## Examples

| Item | Destination | Reason |
|------|-------------|--------|
| Meeting notes about API design | Project: API | Active project work |
| "We should consider microservices" | Decision | Judgment with rationale |
| Bug in production at 3pm | Incident | Something happened |
| Link to useful CSS article | Knowledge | Reference for later |
| "Maybe rewrite in Go?" | Inbox | Not actionable yet |
