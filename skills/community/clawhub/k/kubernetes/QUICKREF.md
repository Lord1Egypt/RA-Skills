# QUICK REFERENCE — Agent Operating Rules

> Print or keep open. Reference before ANY action.

---

## 🚫 NEVER Do Without Human Approval

| Action | Example |
|--------|---------|
| **DELETE anything** | `kubectl delete pod x` |
| **Modify secrets** | Create/rotate secrets |
| **Change RBAC** | Create roles, bindings |
| **Cluster-wide changes** | CRDs, webhooks, namespaces |
| **Production changes** | Deploy to prod, scale beyond limits |
| **Rollback** | Revert production |
| **Apply unknown YAML** | Unreviewed manifests |

---

## ✅ Always Do

| Action | Why |
|--------|-----|
| **Log to LOGS.md** | Every action must be traceable |
| **Read before modify** | Know current state |
| **Check impact** | What breaks if this fails? |
| **Have rollback plan** | How to undo? |
| **Update agent status** | In agents/AGENTS.md |
| **Escalate when blocked** | Better safe than sorry |

---

## 🔴 Stop & Escalate If

- Error persists after 3 retry attempts
- Cluster availability drops below 99.9%
- Security policy violation detected
- Data integrity concern
- Human denies approval request

---

## 📋 Before Any Cluster Action

```
1. READ: kubectl get <resource> -n <ns>
2. CHECK: Impact assessment
3. LOG: Intent to LOGS.md
4. APPROVE: If required, wait for human OK
5. EXECUTE: Apply change
6. VERIFY: Confirm success
7. LOG: Result to LOGS.md
```

---

## Emergency Contacts

| Issue | Agent | Human |
|-------|-------|-------|
| Cluster down | @Atlas | Escalate immediately |
| Security breach | @Shield | Escalate immediately |
| Data loss | @Atlas | Escalate immediately |
| Other | Relevant agent | Team lead |

---

## Log Locations

| Log | Purpose |
|-----|---------|
| `logs/LOGS.md` | Action audit trail |
| `memory/MEMORY.md` | Long-term learnings |
| `incidents/INCIDENTS.md` | Failures & issues |
| `troubleshooting/TROUBLESHOOTING.md` | Debug knowledge |
| `agents/AGENTS.md` | Agent status |

---

## Severity Levels

| Level | Response | Example |
|-------|----------|---------|
| CRITICAL | Immediate | Cluster down, breach |
| HIGH | < 15 min | Major feature broken |
| MEDIUM | < 1 hour | Degraded performance |
| LOW | Next day | Documentation fix |

---

*Last updated: 2026-02-24*
