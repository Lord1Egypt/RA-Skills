# Orchestration Files Guide

How to set up and maintain the lightweight state files that give your AI agent persistent context across sessions.

## The Core Three

These three files handle 90% of cross-session continuity. Start here.

### status.md

Current state of everything you're working on. The agent reads this first every session.

```markdown
# Status

## Active
| Project | State | Next |
|---------|-------|------|
| Auth system | Login flow complete, OAuth pending | Add Google SSO |
| Landing page | Design approved, copy in progress | Finalize hero section |

## Blocked
- Payments integration: waiting on Stripe approval

## Recently Completed
| Date | What |
|------|------|
| 2026-03-24 | Deployed auth system to staging |
| 2026-03-23 | Completed user research interviews (5/5) |
```

**Rules:**
- Keep it scannable. One line per workstream.
- Move completed items to the "Recently Completed" table (keep the last 5-7).
- Update as changes happen, not at end of day.

### tasks.md

Prioritized task list. The agent uses this to understand what's next and what's overdue.

```markdown
# Tasks

## In Progress
- [ ] Add Google SSO to auth flow #product
- [ ] Write landing page hero copy #marketing

## High Priority
- [ ] Fix invite email (no link attached) #bug
- [ ] Schedule user interview with Sarah #research

## Normal
- [ ] Set up error tracking (Sentry) #ops
- [ ] Update README for new contributors #docs
```

**Rules:**
- Use `#tags` for filtering by project area.
- `- [ ]` for open, `- [x]` for done (move to an archive periodically).
- Group by priority, not by project.

### decisions.md

Living log of decisions with enough context to understand *why* months later.

```markdown
# Decisions

## 2026-03-25: Chose Cloudflare Tunnel over direct port exposure
**Context:** Needed to expose OpenClaw gateway on Lightsail.
**Options:** Direct port 443, nginx reverse proxy, Cloudflare Tunnel.
**Decision:** Cloudflare Tunnel. Eliminates ports 80/443 from attack surface. Access enforces Google OAuth before reaching gateway.
**Trade-off:** Adds Cloudflare dependency. Acceptable for single-user deployment.

## 2026-03-24: Telegram over WhatsApp for agent channel
**Context:** Needed messaging channel for OpenClaw.
**Options:** WhatsApp, iMessage (BlueBubbles), Telegram.
**Decision:** Telegram. WhatsApp linking failed (phone-side issue). iMessage requires macOS bridge. Telegram has best bot API and fastest plugin support.
```

**Rules:**
- One entry per decision. Include context, options considered, and the trade-off.
- Newest first.
- Don't delete old decisions. They're the institutional memory.

## Optional Files

### context-map.md

An index that tells the agent where to find deep context for each project area. Saves the agent from searching blindly.

```markdown
# Context Map

## Product
- Architecture: [[product/architecture/system-design]]
- Current sprint: [[product/sprints/sprint-12]]
- Feature specs: [[product/features/]]

## Research
- User interviews: [[company/customer-discovery/]]
- Competitive analysis: [[company/market-research/competitive-landscape]]

## Operations
- Legal docs: [[company/legal/]] (read-only)
- Hiring: [[company/hiring/open-roles]]
```

### scratchpad.md

Working memory. The agent writes here mid-session for things that don't belong in status or tasks yet. Clear it daily or at end of session.

### learnings.md

Operational knowledge the agent discovers across sessions. CLI quirks, SDK behaviors, environment-specific notes, user preferences.

```markdown
# Learnings

## Tools
- Obsidian Headless requires Node.js 22+ on Ubuntu
- `openclaw gateway start` overwrites the systemd service file on every run

## User Preferences
- Tristin prefers plan-before-action. State the approach before executing.
- Never use em dashes in written output.
```

## Maintenance

### Daily
- Update `status.md` as work progresses
- Check off completed tasks in `tasks.md`
- Clear `scratchpad.md` of stale notes

### Weekly
- Archive completed tasks older than 7 days
- Review `decisions.md` for any missing entries
- Check `learnings.md` for anything that should be promoted to a rule or convention
