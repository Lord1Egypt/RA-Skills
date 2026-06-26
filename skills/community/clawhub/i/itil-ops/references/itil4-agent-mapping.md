# ITIL 4 → Agent Operations Mapping

How traditional ITIL 4 practices translate to autonomous AI agent operations.

## Service Value System

In ITIL 4, value flows through the Service Value Chain. For agents:

| ITIL Concept | Agent Equivalent |
|---|---|
| Service Consumer | The human (your user/operator) |
| Service Provider | The agent + its infrastructure |
| Service | Any capability the agent provides (email check, code review, monitoring) |
| Value | Problems solved, time saved, insights delivered |

## Practice Mappings

### Incident Management
**ITIL:** Restore normal service operation as quickly as possible.
**Agent:** Detect service crashes/failures → classify severity → auto-remediate if possible → alert human for P1/P2 → create tracking ticket.

**Key difference:** Agents can detect AND fix many incidents autonomously. Human escalation is the exception, not the rule.

### Problem Management
**ITIL:** Reduce likelihood and impact of incidents by identifying root causes.
**Agent:** Pattern detection across review cycles → 5 Whys analysis → code/config fixes → known error database.

**Key difference:** Agents have perfect memory of every incident if they log properly. Pattern detection can be automated with state files.

### Change Management
**ITIL:** Maximize successful changes by assessing risk.
**Agent:** Pre-change checklist → risk assessment → rollback plan → execute → post-change verification.

**Key difference:** Agents can auto-verify changes immediately. Standard changes (restart, config bump) can be pre-approved.

### Event Management
**ITIL:** Detect, make sense of, and determine appropriate action for events.
**Agent:** journalctl monitoring → threshold-based classification → informational/warning/exception routing.

### Service Level Management
**ITIL:** Set clear business-based targets for service levels.
**Agent:** Define uptime expectations → track MTTR → monitor cron success rates → report trends.

### Continual Improvement
**ITIL:** Align practices with changing business needs through ongoing improvement.
**Agent:** Regular retrospectives → KPI tracking → process refinement → self-healing improvements.

## Severity ↔ ITIL Priority Matrix

| Impact ↓ / Urgency → | High | Medium | Low |
|---|---|---|---|
| **High** (service down) | P1 | P1 | P2 |
| **Medium** (degraded) | P2 | P3 | P3 |
| **Low** (cosmetic) | P3 | P4 | P4 |

## Agent-Specific Practices

These don't map to traditional ITIL but are critical for agents:

### Memory Integrity Management
- Schema validation on memory files
- Corruption detection and auto-repair
- Promotion sweep performance monitoring

### Session Continuity
- Watchdog timeout management
- Graceful restart handling
- State preservation across restarts

### Cron Health Management
- Consecutive failure tracking
- Timeout tuning based on model performance
- Dead job detection and cleanup

### Multi-Agent Coordination
- Task deduplication across agents
- Agent health cross-checking
- Coordination board hygiene
