# Memory Persistence

> **Maintain critical state and context across session compression**
> Priority: HIGH | Category: State Management

## Overview

OpenClaw sessions compress over time, losing context. Your agent forgets decisions, preferences, and learned patterns. This skill ensures critical information persists across sessions.

## The Problem

```yaml
scenario: "Multi-day project"
session_1:
  - "Made decision on authentication approach"
  - "Learned specific project convention"
  - "Discovered environment quirk"

session_2:
  - "Session compressed"
  - "Decision forgotten"
  - "Convention ignored"
  - "Quirk rediscovered painfully"

result: "Repeated work, inconsistent approaches, wasted tokens"
```

## The Solution: File-Based Memory System

### Memory Architecture

```
~/.openclaw/workspace/
├── MEMORY.md              # Long-term facts & decisions
├── USER.md                # User preferences & context
├── AGENTS.md              # Agent identities & roles
├── LESSONS.md             # Learned patterns & anti-patterns
├── CONTEXT.md             # Project-specific context
└── STATE.md               # Current session state
```

### MEMORY.md - Long-Term Facts

```markdown
# Memory

> **Persistent facts across all sessions**
> Last Updated: [Timestamp]

## Project Identity

**Name**: [Project Name]
**Type**: [Web App | CLI Tool | Library | etc]
**Stack**: [Tech stack]
**Repository**: [URL]

## Critical Decisions

### [Category]: [Decision]
**Date**: [YYYY-MM-DD]
**Decision**: [What was decided]
**Reasoning**: [Why this approach]
**Alternatives Considered**: [What was rejected]
**Impact**: [What this affects]

### Example: Authentication Approach
**Date**: 2026-03-10
**Decision**: Use JWT with refresh token pattern
**Reasoning**: Stateless, scales horizontally, matches existing infrastructure
**Alternatives Considered**: Session-based (rejected - doesn't scale), OAuth (rejected - overkill)
**Impact**: All API endpoints must validate JWT

## Environment Facts

### Development
- **Node Version**: v20.x
- **Package Manager**: pnpm
- **Database**: PostgreSQL 15
- **Cache**: Redis 7

### Production
- **Host**: AWS ECS
- **Database**: RDS PostgreSQL
- **CDN**: CloudFront
- **Monitoring**: Datadog

## Known Issues

### [Issue Name]
**Description**: [What's wrong]
**Workaround**: [How to handle]
**Status**: [Known | Under Investigation | Scheduled Fix]

### Example: Database Connection Timeout
**Description**: Lambda functions timeout connecting to RDS
**Workaround**: Use connection pooling with 5 min timeout
**Status**: Scheduled Fix - Q2 2026

## Conventions

### Code Style
- **Indentation**: 2 spaces
- **Quotes**: Single quotes
- **Semicolons**: Required
- **Naming**: camelCase for variables, PascalCase for classes

### Git Conventions
- **Branch Format**: feature/ticket-description
- **Commit Format**: type(scope): description
- **PR Template**: Use .github/PULL_REQUEST_TEMPLATE.md

### Testing Conventions
- **Unit Tests**: co-located with source
- **Integration Tests**: tests/integration/
- **E2E Tests**: tests/e2e/
- **Coverage Target**: 80%

## Dependencies

### Critical Libraries
- **[Library]**: [Version] - [Why critical, how to use]
- **[Library]**: [Version] - [Why critical, how to use]

### Integration Patterns
- **[Pattern Name]**: [How to integrate correctly]

## Performance Characteristics

### Known Bottlenecks
- **[Operation]**: [Limitation]
- **[Operation]**: [Limitation]

### Optimization Rules
- **[Rule 1]**: [Why it matters]
- **[Rule 2]**: [Why it matters]

## Security Context

### Credentials Management
- **Method**: [Environment variables | Vault | etc]
- **Rotation**: [Schedule]
- **Emergency Access**: [Process]

### Sensitive Data
- **[Data Type]**: [How to handle]
- **[Data Type]**: [How to handle]

## External Services

### [Service Name]
- **Purpose**: [What it's for]
- **API Docs**: [Link]
- **Auth Method**: [How to authenticate]
- **Rate Limits**: [Limits]
- **Known Quirks**: [Gotchas]

## Project History

### Major Milestones
- **[Date]**: [Milestone] - [Notes]

### Architecture Changes
- **[Date]**: [Change] - [Reasoning]
```

### USER.md - User Preferences

```markdown
# User Profile

> **Who I am, how I work, what I prefer**
> Last Updated: [Timestamp]

## Identity
**Name**: [Your Name]
**Role**: [Developer | Engineer | Architect | etc]
**Timezone**: [Your TZ]
**Working Hours**: [Your hours]

## Communication Preferences

### Update Style
- **Verbosity**: [Concise | Detailed | Verbose]
- **Format**: [Bullet points | Tables | Paragraphs]
- **Frequency**: [Real-time | Hourly | End of day]

### Decision Preferences
- **Autonomy Level**: [High | Medium | Low]
- **Escalation Threshold**: [When to escalate]
- **Approval Required For**: [What needs sign-off]

## Work Preferences

### Code Style Preferences
- **Preferred Patterns**: [What you like]
- **Disliked Patterns**: [What you hate]
- **Non-Negotiables**: [Deal breakers]

### Tool Preferences
- **Editor**: [VS Code | Vim | etc]
- **Terminal**: [Specific shell/setup]
- **Browser**: [Dev preferences]

### Workflow Preferences
- **Task Breaking**: [How granular]
- **Testing Approach**: [TDD | Test after | etc]
- **Documentation**: [Inline | Separate | Both]

## Quality Standards

### Code Quality
- **Clean Code**: [Yes | No | Maybe]
- **Comments**: [Required | Minimal | When complex]
- **Type Safety**: [Strict | Loose | None]

### Testing Standards
- **Coverage Expectation**: [%]
- **Test Types Required**: [Unit | Integration | E2E]
- **Mock Philosophy**: [When to mock]

## Risk Tolerance

### Deployment
- **Deploy Frequency**: [Feature flags | Direct | etc]
- **Rollback Tolerance**: [How conservative]
- **Production Changes**: [How careful]

### Technical Debt
- **Tolerance**: [Low | Medium | High]
- **Paydown Strategy**: [How to handle]

## Learning & Growth

### Current Focus Areas
- **[Topic]**: [Learning goal]
- **[Topic]**: [Learning goal]

### Preferred Learning Style
- **[Style]**: [How you learn best]

## Context Notes

### Current Projects
- **[Project]**: [Role, goals, status]

### Upcoming Deadlines
- **[Date]**: [What's due]

### Blocked Items
- **[Item]**: [What's blocking]
```

### LESSONS.md - Learned Patterns

```markdown
# Lessons Learned

> **Patterns that work, anti-patterns to avoid**
> Last Updated: [Timestamp]

## Success Patterns 🎯

### [Pattern Name]
**Discovered**: [Date]
**Context**: [When it applies]
**Pattern**: [What to do]
**Why It Works**: [Explanation]

### Example: Database Query Pattern
**Discovered**: 2026-03-08
**Context**: PostgreSQL queries in Lambda functions
**Pattern**: Always use prepared statements with connection pooling
**Why It Works**: Prevents injection, handles timeouts, reduces cold start time

## Anti-Patterns 🚫

### [Anti-Pattern Name]
**Discovered**: [Date]
**Context**: [When this happens]
**Problem**: [What goes wrong]
**Solution**: [What to do instead]

### Example: Direct DB Connections in Loops
**Discovered**: 2026-03-05
**Context**: Processing multiple records
**Problem**: Opens new connection per iteration, exhausts pool
**Solution**: Batch operations, single connection per request

## Error Patterns ⚠️

### [Error Type]
**Symptom**: [What you see]
**Root Cause**: [Why it happens]
**Fix**: [How to resolve]
**Prevention**: [How to avoid]

### Example: "Task not found" in ECS
**Symptom**: ECS task definition not found during deployment
**Root Cause**: Task definition ARN not updated after changes
**Fix**: Run `aws ecs register-task-definition` before deploy
**Prevention**: Always verify task definition version before deploy

## Optimization Wins ⚡

### [Optimization]
**Before**: [Metric]
**After**: [Metric]
**Technique**: [What was done]
**Applicability**: [When to use]

## Debugging Shortcuts 🔍

### [Problem Type]
**Quick Check**: [What to check first]
**Common Cause**: [Most likely reason]
**Fast Fix**: [Quickest resolution]

## External Knowledge

### [Topic]
**Source**: [Where learned]
**Key Takeaways**:
- [Point 1]
- [Point 2]
**Retention**: [Why this matters]
```

### STATE.md - Current Session State

```markdown
# Current State

> **Snapshot of right now - for session recovery**
> Last Updated: [Timestamp]

## Active Session
**Session ID**: [UUID]
**Started**: [Timestamp]
**Model**: [Current model]
**Agent**: [Current agent]

## Current Work

### Active Task
**Task ID**: [T-XXX]
**Task**: [Task name]
**Status**: [in_progress | blocked | etc]
**Started**: [Timestamp]
**Last Progress**: [Timestamp]

**Where I Am**:
- [ ] [Step 1 - completed]
- [ ] [Step 2 - in progress]
- [ ] [Step 3 - pending]

**Context**:
- [Relevant context needed to resume]

### Blocked On
- **[Blocker]**: [Description]
- **Resolution Required**: [What's needed]

## Session Context

### Recent Decisions
1. **[Decision]** - [Why]
2. **[Decision]** - [Why]

### Assumptions Made
- **[Assumption 1]**: [Basis]
- **[Assumption 2]**: [Basis]

### Environment State
- **Branch**: [Current branch]
- **Uncommitted Changes**: [Yes | No]
- **Running Services**: [What's up]
- **Open Files**: [What's open]

## Quick Resume

To continue this session:
1. Review current task above
2. Check recent decisions for context
3. Verify environment state matches
4. Continue from "Where I Am" step
```

## Memory Update Rules

### WHEN to Update Memory

```yaml
triggers_for_memory_update:
  critical_updates:
    - "Any architectural decision"
    - "Any user preference learned"
    - "Any pattern discovered"
    - "Any major error encountered"
    - "Any environment quirk found"

  periodic_updates:
    - "Every task completion"
    - "Every session start"
    - "Every escalation"
    - "Every major milestone"
```

### WHAT to Remember

```yaml
memory_categories:
  always_remember:
    - "Architectural decisions"
    - "User preferences"
    - "Working conventions"
    - "Critical errors and fixes"
    - "Environment-specific behavior"

  sometimes_remember:
    - "Minor implementation details"
    - "Temporary workarounds"
    - "Opinions on approaches"

  never_remember:
    - "Transient state (logs, temps)"
    - "Opinionated preferences without user input"
    - "Generic programming knowledge"
```

### HOW to Update

```yaml
update_protocol:
  1: "Identify what type of information this is"
  2: "Select appropriate memory file"
  3: "Find or create appropriate section"
  4: "Write in structured, searchable format"
  5: "Include timestamp and context"
  6: "Cross-reference if related to other entries"
```

## Memory Quality Standards

### Good Memory Entry

```markdown
### PostgreSQL Connection Timeout in Lambda
**Date**: 2026-03-10
**Context**: Lambda functions timing out when connecting to RDS
**Root Cause**: Default connection timeout too long, Lambda gives up first
**Solution**: Set connection timeout to 5 seconds, use connection pooling
**Code**: `connectionTimeoutMillis: 5000` in Sequelize config
**Impact**: Reduced cold start time from 8s to 2s
**Tags**: lambda, database, performance
```

### Bad Memory Entry

```markdown
Database stuff broke, fixed with timeout.
```

## Session Recovery Protocol

### When Session Compresses

```yaml
recovery_steps:
  1: "Review STATE.md for current work"
  2: "Review MEMORY.md for relevant context"
  3: "Review LESSONS.md for applicable patterns"
  4: "Review USER.md for preferences"
  5: "Resume work with full context"
```

### Verification

After session recovery:

```yaml
verify:
  - "Current task matches STATE.md"
  - "Approach align with MEMORY.md decisions"
  - "Patterns follow LESSONS.md"
  - "Style matches USER.md preferences"
```

## Memory Search Protocol

### Before Starting Work

```python
def search_memory(task_description):
    """
    Search memory for relevant context before starting work
    """
    queries = [
        extract_keywords(task_description),
        extract_domain(task_description),
        extract_tech_stack(task_description)
    ]

    for query in queries:
        results = search_files(['MEMORY.md', 'LESSONS.md'], query)
        for result in results:
            print(f"Found relevant: {result}")

    return results
```

## Integration with Other Skills

```yaml
docs_first:
  - "Search memory for existing patterns"
  - "Check MEMORY.md for related decisions"

execution_discipline:
  - "Update LESSONS.md after failures"
  - "Update MEMORY.md after architectural decisions"

task_autonomy:
  - "Read USER.md before selecting tasks"
  - "Update STATE.md with current work"
```

## Key Takeaway

**Session compression is inevitable. Memory persistence is optional.** Choose wisely.

---

**Related Skills**: All skills benefit from proper memory persistence
