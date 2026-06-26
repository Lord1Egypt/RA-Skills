# WORKING.md — Agent Progress Tracking

> This file is the single source of truth for agent progress. MUST be updated at session start and end.

---

## Session Start Protocol

Before starting ANY work, agents MUST:

1. **Read SESSION.md** - Check environment context (dev/qa/staging/prod)
2. **Read this file** - Check current progress
3. **Check cluster access** - Verify can connect to cluster

```bash
# Required at session start
cat working/SESSION.md    # Environment context
cat working/WORKING.md    # Your progress
cat logs/LOGS.md | head -50  # Recent activity
```

---

## Environment Context (from SESSION.md)

| Key | Value |
|-----|-------|
| Environment | |
| Cluster Type | |
| Cluster Name | |
| Permission Level | |

### Environment Constraints

| Environment | Can Delete | Can Modify Prod | Can RBAC | Can Scale | Can Secrets |
|-------------|------------|-----------------|----------|-----------|--------------|
| **dev** | Approval | Approval | Approval | Auto | Approval |
| **qa** | Approval | Approval | Approval | Approval | Approval |
| **staging** | Approval | Approval | Approval | Approval | Approval |
| **prod** | NEVER | NEVER | NEVER | NEVER | NEVER |

---

## Agent Progress Templates

Copy the appropriate template for your agent at session start. Update before ending session.

---

## orchestrator (Jarvis)

### Current Session
- Started: 
- Task: 
- Environment: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## cluster-ops (Atlas)

### Current Session
- Started: 
- Task: 
- Environment: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## gitops (Flow)

### Current Session
- Started: 
- Task: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## security (Shield)

### Current Session
- Started: 
- Task: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## observability (Pulse)

### Current Session
- Started: 
- Task: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## artifacts (Cache)

### Current Session
- Started: 
- Task: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## developer-experience (Desk)

### Current Session
- Started: 
- Task: 
- Environment: 

### Completed This Session
- 

### Remaining Tasks
- 

### Blockers
- None

### Next Action
- 

---

## Context Management Rules

1. **Read at session start** - Always read this file before starting work
2. **Update before ending** - Document what you did and what remains
3. **Commit with update** - Git commit should include WORKING.md changes
4. **Be specific** - "Fixed node drain issue" not "worked on stuff"
5. **Next action clear** - Next agent should know exactly what to do

---

*Last updated: 2026-02-24*
