# Notion Brain — Page Map

Use this file to decide **where** content belongs after it clears the quality gate.

## Canonical destinations

| Content type | Default destination | Notion ID | Notes |
|---|---|---|---|
| Research summary | 🧠 Knowledge Hub | `YOUR_KNOWLEDGE_HUB_PAGE_ID` | Use for reusable synthesis, market scans, tool comparisons, strategy research |
| Decision memo | 🧠 Knowledge Hub | `YOUR_KNOWLEDGE_HUB_PAGE_ID` | Use for durable choices, tradeoffs, rationale, and decision records |
| Project plan | 💼 Work Hub | `YOUR_WORK_HUB_PAGE_ID` | Use when the plan is operational and work-facing |
| Project status | 💼 Work Hub | `YOUR_WORK_HUB_PAGE_ID` | If it is company execution or meeting follow-through |
| Project plan/status with cross-domain strategic value | 🧠 Knowledge Hub | `YOUR_KNOWLEDGE_HUB_PAGE_ID` | Use when it is more knowledge asset than work execution |
| Article draft | ✍️ Content Hub | `YOUR_CONTENT_HUB_PAGE_ID` | Use for article drafts, outlines, newsletters, and longer-form content |
| Security audit report | 🧠 Knowledge Hub | `YOUR_KNOWLEDGE_HUB_PAGE_ID` | Durable audits and recommendations live here unless a dedicated work project requires Work Hub |
| Financial snapshot | 💰 Finance Hub | `YOUR_FINANCE_HUB_PAGE_ID` | Use for monthly/weekly summaries, account snapshots, allocation notes |
| Weekly rollup | 🧠 Knowledge Hub | `YOUR_KNOWLEDGE_HUB_PAGE_ID` | Use for personal or operator-level synthesis, wins, blockers, and direction |
| Contact note | 🧠 Knowledge Hub | `YOUR_KNOWLEDGE_HUB_PAGE_ID` | Use for people context, relationship intelligence, and notes worth reusing |
| Meeting prep | 💼 Work Hub | `YOUR_WORK_HUB_PAGE_ID` | Use for agendas, talking points, pre-reads, and desired outcomes |
| Quick capture | 📥 Inbox DB | `YOUR_INBOX_DB_ID` | Use when worth saving but not worth full structuring yet |

## Routing heuristics

### Send to Knowledge Hub when the content is:
- reusable knowledge
- a durable decision or rationale
- a synthesis across tools, meetings, or sources
- personal operating context that should stay findable
- an audit, brief, or memo the owner may revisit later

### Send to Work Hub when the content is:
- directly tied to active execution
- an internal plan, meeting artifact, or status note
- work-specific rather than broadly reusable knowledge

### Send to Content Hub when the content is:
- written for eventual publishing or refinement
- an article, post, outline, draft, or concept note

### Send to Finance Hub when the content is:
- financial, portfolio, cashflow, budget, or account oriented
- useful as a finance snapshot rather than general knowledge

### Send to Inbox DB when the content is:
- worth preserving but not yet sorted
- partial, rough, or captured quickly
- a seed that may later be promoted into a full page

## Future: two-way sync via webhooks

Notion supports webhooks. When enabled, changes made directly in Notion (for example, adding a contact or updating a project) could automatically sync back to agent memory. This would close the loop between Notion-as-UI and workspace-as-agent-memory. Not yet wired — see `references/mcp-commands.md` for details.

## Non-routes

Do not route through this skill for:
- 💪 Health & Fitness: `YOUR_HEALTH_PAGE_ID`
- 🏡 Home: `YOUR_HOME_PAGE_ID`
- property, vehicle, or equipment tracking workflows

Those require their own workflows.

## Tie-breakers

If content could go in more than one place, use this order:
1. **Work Hub** if it is primarily for active execution
2. **Content Hub** if it is primarily a draft meant to be published or iterated as content
3. **Finance Hub** if the primary retrieval intent is financial review
4. **Knowledge Hub** if it is a durable knowledge artifact
5. **Inbox DB** if still ambiguous but worth saving

## Suggested title patterns

- Research Summary — {topic} — {YYYY-MM-DD}
- Decision Memo — {decision}
- Project Plan — {project}
- Project Status — {project} — {YYYY-MM-DD}
- Draft — {title}
- Security Audit — {system} — {YYYY-MM-DD}
- Financial Snapshot — {period}
- Weekly Rollup — {YYYY-[W]WW}
- Contact Note — {person}
- Meeting Prep — {meeting or account} — {YYYY-MM-DD}
- Capture — {short subject} — {YYYY-MM-DD}
