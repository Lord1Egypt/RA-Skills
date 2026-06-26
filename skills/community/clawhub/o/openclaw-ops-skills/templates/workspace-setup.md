# OpenClaw Workspace Templates

> **Essential workspace files for production-ready agent operations**

## Quick Start

```bash
# Create workspace directory
mkdir -p ~/.openclaw/workspace

# Copy these templates to workspace
cp *.md ~/.openclaw/workspace/

# Set proper permissions
chmod 600 ~/.openclaw/workspace/*.md

# Restart OpenClaw
openclaw restart
```

---

## USER.md Template

```markdown
# User Profile

> **Who I am, how I work, what I prefer**
> Last Updated: [UPDATE_THIS]

## Identity
**Name**: [Your Name]
**Role**: [Developer | Engineer | Architect | DevOps | etc]
**Timezone**: [Your TZ]
**Working Hours**: [e.g., 09:00-18:00 UTC-5]

## Communication Preferences

### Update Style
- **Verbosity**: [Concise | Detailed | Verbose]
- **Format**: [Bullet points | Tables | Paragraphs]
- **Frequency**: [Real-time | Hourly | End of day]

### Decision Preferences
- **Autonomy Level**: [High (decide without asking) | Medium (ask for clarification) | Low (confirm everything)]
- **Escalation Threshold**: [When to escalate - e.g., after 2 failures, any blocker, security issues]
- **Approval Required For**:
  - [e.g., Database migrations]
  - [e.g., Production deployments]
  - [e.g., New dependencies]

## Work Preferences

### Code Style Preferences
- **Preferred Patterns**: [e.g., Functional over OOP, composition over inheritance]
- **Disliked Patterns**: [e.g., Deep nesting, callback hell]
- **Non-Negotiables**: [e.g., Always use TypeScript, never use var]

### Tool Preferences
- **Editor**: [VS Code | Vim | Neovim | JetBrains]
- **Terminal**: [specific shell or config]
- **Browser for Development**: [Chrome DevTools | Firefox DevTools]
- **Git Client**: [CLI | GitHub Desktop | etc]

### Workflow Preferences
- **Task Breaking**: [Fine-grained (1-2 hour tasks) | Coarse-grained (half-day tasks)]
- **Testing Approach**: [TDD | Test-after | Test-only-for-critical]
- **Documentation**: [Inline only | Separate docs | Both]

## Quality Standards

### Code Quality
- **Clean Code**: [Yes - strictly follow | No - pragmatic | Maybe - case by case]
- **Comments**: [Required on all functions | Only for complex logic | Minimal]
- **Type Safety**: [Strict (no any) | Loose (any OK) | None (JavaScript)]

### Testing Standards
- **Coverage Expectation**: [% minimum coverage]
- **Test Types Required**: [Unit only | Unit + Integration | All types]
- **Mock Philosophy**: [Mock everything external | Mock only slow services]

## Risk Tolerance

### Deployment
- **Deploy Frequency**: [Feature flags required | Direct to main | Release branches]
- **Rollback Tolerance**: [Very conservative (test extensively) | Moderate | Quick iterations]
- **Production Changes**: [Requires approval window | Any time | Weekdays only]

### Technical Debt
- **Tolerance**: [Zero tolerance | Low OK | Medium OK | High OK]
- **Paydown Strategy**: [Immediate | Next sprint | Scheduled monthly]

## Environment

### Development
- **OS**: [Windows | macOS | Linux]
- **Primary Language(s)**: [e.g., Python, JavaScript, Go]
- **Package Managers**: [e.g., npm, pip, cargo]

### Common Tools
- **Docker**: [Yes | No]
- **Kubernetes**: [Yes | No]
- **Cloud Provider**: [AWS | GCP | Azure | None]

## Learning & Growth

### Current Focus Areas
- **[Topic 1]**: [Learning goal]
- **[Topic 2]**: [Learning goal]
- **[Topic 3]**: [Learning goal]

### Preferred Learning Style
- **[Style]**: [Hands-on | Reading | Videos | Mentoring]

## Context Notes

### Current Projects
1. **[Project Name]**
   - **Role**: [Your role]
   - **Goals**: [What you're trying to achieve]
   - **Status**: [On track | Blocked | etc]

2. **[Project Name]**
   - **Role**: [Your role]
   - **Goals**: [What you're trying to achieve]
   - **Status**: [On track | Blocked | etc]

### Upcoming Deadlines
- **[Date]**: [What's due]
- **[Date]**: [What's due]

### Blocked Items
- **[Item]**: [What's blocking] - [Since when]
```

---

## AGENTS.md Template

```markdown
# Agent Configuration

> **Agent identities, roles, and routing**
> Last Updated: [UPDATE_THIS]

## Agents

### Primary Agent
**Name**: [e.g., Operator]
**Role**: [General operations, task management, automation]
**Model**: [Default model - e.g., Sonnet 4.6]
**Skills**: [Key skills this agent uses]

### Specialist Agents

#### [Agent Name]
**Role**: [Specific role - e.g., Code Writer]
**Model**: [e.g., Codex GPT-5.3]
**Skills**: [Relevant skills]
**Trigger**: [When to use this agent]

#### [Agent Name]
**Role**: [Specific role - e.g., Security Auditor]
**Model**: [e.g., Opus 4.6]
**Skills**: [Relevant skills]
**Trigger**: [When to use this agent]

## Routing Rules

### Task Type Routing
```yaml
development_tasks:
  agent: "Code Writer"
  model: "codex-gpt-5.3"
  reasoning: "Best for code generation"

operational_tasks:
  agent: "Operator"
  model: "sonnet-4-6"
  reasoning: "Good balance of capability and cost"

complex_reasoning:
  agent: "Analyst"
  model: "opus-4-6"
  reasoning: "Maximum capability for complex problems"

routine_tasks:
  agent: "Operator"
  model: "kimi-k2.5"
  reasoning: "Cost-effective for routine work"
```

## Collaboration Patterns

### Handoff Protocol
**When**: [When to switch agents]
**How**: [How to transfer context]
**Verification**: [How to verify handoff successful]

### Conflict Resolution
**When agents disagree**: [How to resolve]
**Escalation**: [When to involve user]
```

---

## SOUL.md Template

```markdown
# Operating System

> **Core methods, planning discipline, and execution loops**
> Last Updated: [UPDATE_THIS]

## Core Methods

### Execution Loop
```
BUILD → TEST → DOCUMENT → DECIDE → (repeat)
```

1. **BUILD**: Make smallest meaningful change
2. **TEST**: Validate against expected behavior
3. **DOCUMENT**: Record results in progress-log.md
4. **DECIDE**: Iterate, escalate, close, or re-plan

### Primary Principles
- **Validate results, don't guess**
- **Keep decisions transparent**
- **Maintain audit trails**
- **Learn from failures**

## Planning Discipline

### Planning Trigger
- All non-trivial requests start with planning
- Define scope before building
- Set clear "done" criteria

### Planning Output
Before any work:
- [ ] Scope defined
- [ ] Success criteria specified
- [ ] Constraints identified
- [ ] Dependencies listed

### Re-Planning Trigger
Stop and re-plan when:
- Fact base changes significantly
- Three iterations fail on same approach
- New information invalidates plan

## Execution Standards

### Before Starting Work
- [ ] Read documentation (docs-first.md)
- [ ] Check scope boundaries (scope-control.md)
- [ ] Review lessons learned (LESSONS.md)
- [ ] Understand context (MEMORY.md)

### During Work
- [ ] Update progress-log.md each cycle
- [ ] Never skip testing
- [ ] Document decisions
- [ ] Stay within scope

### After Work
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Lessons learned recorded
- [ ] Todo.md updated

## Quality Gates

### Definition of Done
A task is complete when:
- [ ] All success criteria met
- [ ] Tests passing (no regressions)
- [ ] Code reviewed (if applicable)
- [ ] Documentation updated
- [ ] Progress logged

### Final Question
**"Would a senior engineer approve this as production-ready?"**
If NO: Not done. Iterate.
If YES: Complete.

## Escalation Rules

Escalate immediately when:
- Security issue identified
- Data loss risk detected
- Scope boundary unclear
- Three failures on same issue
- External dependency blocked

## Learning Loop

### After Each Failure
1. Document in LESSONS.md:
   - What failed
   - Root cause
   - How to prevent

2. Update relevant skills:
   - Add prevention check
   - Update procedure

3. Before next similar task:
   - Review LESSONS.md
   - Apply prevention

### Continuous Improvement
- Weekly review of LESSONS.md
- Identify patterns
- Update skills accordingly
```

---

## MEMORY.md Template

```markdown
# Memory

> **Persistent facts and decisions across all sessions**
> Last Updated: [UPDATE_THIS]

## Project Identity

**Name**: [Project Name]
**Type**: [Web App | CLI Tool | Library | API | etc]
**Repository**: [URL]
**Primary Language**: [Language]
**Stack**: [Tech stack summary]

## Critical Decisions

### [Category]: [Decision Title]
**Date**: [YYYY-MM-DD]
**Decision**: [What was decided]
**Reasoning**: [Why this approach]
**Alternatives Considered**: [What was rejected]
**Impact**: [What this affects]
**Status**: [Active | Superseded | Deprecated]

### Example: Authentication Approach
**Date**: 2024-03-10
**Decision**: Use JWT with refresh token pattern
**Reasoning**: Stateless, scales horizontally
**Alternatives**: Session-based (rejected), OAuth (overkill)
**Impact**: All API endpoints validate JWT
**Status**: Active

## Environment Facts

### Development
- **Runtime**: [e.g., Node 20.x, Python 3.11]
- **Package Manager**: [npm/pnpm/pip]
- **Database**: [PostgreSQL 15 | MongoDB | etc]
- **Cache**: [Redis 7 | Memcached | etc]

### Production
- **Host**: [AWS | GCP | Azure | Vercel | etc]
- **Database**: [RDS | Cloud SQL | etc]
- **CDN**: [CloudFront | Cloudflare | etc]
- **Monitoring**: [Datadog | New Relic | etc]

## Known Issues

### [Issue Name]
**Description**: [What's wrong]
**Workaround**: [How to handle for now]
**Status**: [Known | Under Investigation | Scheduled Fix]
**Date Added**: [YYYY-MM-DD]

## Conventions

### Code Style
- **Indentation**: [2 spaces | 4 spaces | tabs]
- **Quotes**: [Single | Double]
- **Semicolons**: [Required | Optional]
- **Naming**: [camelCase | snake_case | PascalCase]

### Git Conventions
- **Branch Format**: [feature/ticket-name | etc]
- **Commit Format**: [type(scope): description]
- **PR Template**: [Location or requirements]

### Testing
- **Unit Tests**: [Location and pattern]
- **Integration Tests**: [Location and pattern]
- **Coverage Target**: [%]

## Performance Characteristics

### Known Limitations
- **[Operation]**: [Limitation]
- **[Operation]**: [Limitation]

### Optimization Rules
- **[Rule 1]**: [Why it matters]
- **[Rule 2]**: [Why it matters]

## External Services

### [Service Name]
- **Purpose**: [What it's for]
- **API Docs**: [Link]
- **Auth Method**: [How to authenticate]
- **Rate Limits**: [Limits]
- **Common Issues**: [Gotchas]
```

---

## Todo.md Template

```markdown
# Todo.md

## Last Updated
**Timestamp**: [UPDATE_THIS]
**Agent**: [Agent Name]
**Session**: [Session ID]

## Task Statistics
- **Total**: [N]
- **Pending**: [N]
- **In Progress**: [N]
- **Completed**: [N]
- **Blocked**: [N]

---

## Active Tasks [PRIORITY: HIGH]

### [T-001] [Task Title]
**Status**: pending | in_progress | completed | blocked
**Priority**: critical | high | medium | low
**Assigned**: [Agent Name]
**Created**: [Timestamp]
**Updated**: [Timestamp]

**Description**: [Clear, actionable description]

**Definition of Done**:
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]

**Dependencies**: [T-000 or 'none']
**Blocks**: [T-002, T-003 or 'none']

**Progress Notes**:
- [YYYY-MM-DD HH:MM] [Note]

---

## Pending Tasks [PRIORITY: MEDIUM]
[Same structure as Active Tasks]

---

## Backlog [PRIORITY: LOW]
[Same structure as Active Tasks]

---

## Completed Today

### [T-XXX] [Task Title] - Completed at [HH:MM]
[Brief summary of what was done]

---

## Blocked Tasks

### [T-XXX] [Task Title] - Blocked since [HH:MM]
**Blocker**: [Description]
**Action Required**: [What needs to happen]
```

---

## progress-log.md Template

```markdown
# Progress Log

## Statistics
- **Session Start**: [Date/Time]
- **Last Update**: [Date/Time]
- **Total Cycles**: [N]
- **Tasks Completed**: [N]
- **Current Task**: [Task Name]

---

## [YYYY-MM-DD]

### [HH:MM] - Cycle #[N]: [Brief Title]
**Status**: completed | failed | in_progress | blocked
**Task**: [T-XXX] [Task Name]
**Agent**: [Agent Name]
**Model**: [Model Used]

#### Phase: BUILD
**Changes Made**:
- [File 1]: [Brief description]
- [File 2]: [Brief description]

#### Phase: TEST
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| [Test name] | [Expected] | [Actual] | [Pass/Fail] |

#### Phase: DECISION
**Outcome**: [ITERATE | ESCALATE | CLOSE | RE-PLAN]
**Reasoning**: [Why]

---

### [HH:MM] - Task Completed: [Task Name]
**Task ID**: [T-XXX]
**Duration**: [X minutes]
**Summary**: [What was accomplished]

---

## Daily Summaries

### [YYYY-MM-DD] - Overnight Work Summary
**Work Period**: [Start] - [End]
**Tasks Completed**: [N]
**Tasks Failed**: [N]

#### Completed Tasks
1. **[Task]** - [Summary]

#### Issues Discovered
- [Issue] - [Impact]

---
```

---

## Installation Instructions

```bash
# 1. Navigate to your OpenClaw workspace
cd ~/.openclaw/workspace

# 2. Create backup of existing files (if any)
mkdir -p backup
cp *.md backup/ 2>/dev/null || true

# 3. Copy templates
cp /path/to/templates/*.md .

# 4. Edit with your information
nano USER.md
nano MEMORY.md
# ... etc

# 5. Set proper permissions
chmod 600 *.md

# 6. Restart OpenClaw
openclaw restart
```

---

## Template Maintenance

Update these templates when:
- Adding new projects
- Changing preferences
- Major environment changes
- Learning significant lessons

Recommended: Review and update monthly.
