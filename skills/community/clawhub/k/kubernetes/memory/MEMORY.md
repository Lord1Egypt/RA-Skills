# MEMORY.md — Persistent Agent Learning

> Append-only learning log. Only store important long-term insights.

---

## Last Updated
<!-- UPDATE_TIMESTAMP -->

---

## Learned: Repository Foundation

### Context
Initial setup of cluster-agent-swarm-skills repository. Contains skills for 7 specialized agents managing Kubernetes/OpenShift operations.

### Decision
Established comprehensive logging infrastructure including MEMORY.md, LOGS.md, INCIDENTS.md, and TROUBLESHOOTING.md to enable persistent agent memory and audit trails.

### Why
Without structured memory, agents lose context between sessions. This repository serves as the single source of truth for cluster operations automation.

### Future Implication
All future agent actions should update relevant log files. Important learnings should be documented here for swarm-wide awareness.

---

## Template: Add New Learning

```
## Learned: <topic>

### Context
<what happened>

### Decision
<what was decided>

### Why
<reasoning>

### Future Implication
<how this affects future actions>
```

---

## Critical Rules (Always Remember)

1. **NEVER delete without human approval** — Any deletion action requires explicit human consent
2. **Human review mandatory** — Important decisions require human-in-the-loop
3. **Log everything** — Every action must be traceable
4. **Reliability first** — System stability > new features
5. **Security default** — Deny by default, approve by exception
