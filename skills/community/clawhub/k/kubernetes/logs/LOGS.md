# LOGS.md — Agent Action Audit Trail

> Append EVERY agent action to this file. Format: Most recent first.

---

## 2026-02-24T00:00:00Z — Initial Setup

### Agent: system-initialization
### Action: Created logging infrastructure
### Reason: Enable persistent agent memory and audit trails for swarm operations
### Target: memory/, logs/, incidents/, troubleshooting/ directories
### Result: SUCCESS
### Next Action: Begin normal agent operations with logging

---

## Template: Log New Action

```
## [TIMESTAMP UTC]

### Agent: <agent-name>
### Action: <what was done>
### Reason: <why>
### Target: <file/system/resource>
### Result: SUCCESS | FAILURE | PARTIAL | BLOCKED
### Next Action: <planned next step>
```

---

## Log Categories

| Category | When to Log |
|----------|-------------|
| `CLUSTER_ACTION` | Any kubectl/oc command execution |
| `SKILL_EXECUTION` | Running a skill script |
| `SKILL_IMPROVEMENT` | Identified need to update/improve a skill or script |
| `DECISION` | Agent makes a decision |
| `APPROVAL_NEEDED` | Requires human approval |
| `ESCALATION` | Escalating to human or another agent |
| `ERROR` | Any error or failure |
| `SECURITY` | Security-related action |
| `RELIABILITY` | Reliability/availability impact |

---

## Required Fields Per Entry

- **Timestamp**: ISO 8601 UTC
- **Agent**: Which agent acted
- **Action**: What was done (imperative, e.g., "create", "read", "approve")
- **Reason**: Why this action was taken
- **Target**: What was affected (file, resource, cluster)
- **Result**: SUCCESS | FAILURE | PARTIAL | BLOCKED | PENDING_APPROVAL
- **Next Action**: What happens next
- **Skill Improvement** (optional): If SKILL_IMPROVEMENT category, add:
  - `Skill`: Which skill/script needs improvement
  - `Improvement Type`: SCRIPT_FIX | NEW_CAPABILITY | REFERENCE_DOC | WORKFLOW_CHANGE
  - `Suggested Fix`: Brief description of what should change

---

## SKILL_IMPROVEMENT Log Template

When an agent identifies a skill needs improvement during troubleshooting or cluster activities:

```
## [TIMESTAMP UTC]

### Agent: <agent-name>
### Action: <what was done>
### Reason: <why>
### Target: <file/system/resource>
### Result: SUCCESS | FAILURE | PARTIAL | BLOCKED | PENDING_APPROVAL
### Category: SKILL_IMPROVEMENT
### Skill: <skill-name>/<script-or-file>
### Improvement Type: SCRIPT_FIX | NEW_CAPABILITY | REFERENCE_DOC | WORKFLOW_CHANGE
### Suggested Fix: <description of improvement>
### Next Action: <planned next step>
```

---

## Security Logging Requirements

All actions involving the following MUST be logged with HIGH priority:
- Secret handling (read, write, rotate)
- RBAC changes
- Network policy modifications
- Cluster-wide resources
- Production environment changes
- User credential operations
- Deletion of any resource

---

## Approval Workflow Logging

```
### Approval Requested
### Approver: <human-user>
### Requested By: <agent-name>
### Request Type: DELETE | MODIFY_PROD | RBAC_CHANGE | SECRET_WRITE | CLUSTER_WIDE
### Target: <resource>
### Status: PENDING | APPROVED | REJECTED
### Response: <human response>
```
