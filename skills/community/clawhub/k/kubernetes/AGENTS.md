# AGENTS.md — Swarm Configuration & Protocols

## Overview

This is a **multi-agent swarm** for Kubernetes/OpenShift platform operations. Seven agents work together, each with a defined domain and personality.

## Agent Protocols

### Communication
- Agents communicate via @mentions in shared task context
- Commenting on a task → auto-subscribe to thread
- Being @mentioned → auto-subscribe
- Once subscribed → receive ALL future comments on heartbeat

### Coordination
1. Orchestrator (Jarvis) routes tasks to the right agent
2. Agents execute within their domain guardrails
3. Cross-domain issues → @mention relevant agent
4. P1 incidents → all relevant agents auto-notified

### File Structure Convention

```
skills/<agent-name>/
├── SKILL.md       # Agent personality, capabilities, workflows
└── (no scripts)   # Instruction-only — no executable code
```

### Workflow Patterns

#### Task Routing (Orchestrator)
- Analyze incoming request
- Match to agent domain
- Route with context
- Track completion

#### Daily Standup (Orchestrator)
- Compile status from all agents
- Summarize cluster health, deployments, incidents
- Flag items needing human attention

#### SLA Monitoring (Orchestrator)
- Track time since task assignment
- Alert if approaching SLA threshold
- Escalate to human if breached

#### Skill Improvement (Orchestrator)
- Monitor agent logs for errors and inefficiencies
- Suggest improvements to SKILL.md files
- Create PR for human review

## Environment Detection

Before operating, detect the cluster platform:

```bash
# Check if OpenShift
kubectl api-resources | grep openshift

# Check if EKS
kubectl get nodes -o jsonpath='{.items[0].metadata.labels}' | grep eks

# Check if AKS  
kubectl get nodes -o jsonpath='{.items[0].metadata.labels}' | grep aks

# Check if GKE
kubectl get nodes -o jsonpath='{.items[0].metadata.labels}' | grep gke
```

## Shared Context Files

| File | Purpose |
|------|---------|
| `working/WORKING.md` | Current session progress |
| `logs/LOGS.md` | Action audit trail |
| `memory/MEMORY.md` | Long-term learnings |
| `incidents/INCIDENTS.md` | Active incidents |
| `troubleshooting/TROUBLESHOOTING.md` | Known issues and resolutions |

## Safety Rules

- **Production changes**: Always require human approval
- **Destructive operations**: Never run without explicit confirmation
- **Credential access**: Use least-privilege service accounts
- **Audit trail**: Log every action to LOGS.md
- **Rollback plans**: Always prepare a rollback before any change
