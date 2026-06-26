# Kubernetes Agent Swarm

A coordinated multi-agent system for Kubernetes and OpenShift platform operations. Seven specialized agents work together as a swarm.

## Agents

| Agent | Code Name | Domain |
|-------|-----------|--------|
| Orchestrator | Jarvis | Task routing, coordination, daily standups |
| Cluster Ops | Atlas | Cluster lifecycle, nodes, upgrades, etcd |
| GitOps | Flow | ArgoCD, Helm, Kustomize, deployments |
| Security | Shield | RBAC, policies, secrets, CVE scanning |
| Observability | Pulse | Metrics, logs, alerts, incident response |
| Artifacts | Cache | Registries, SBOM, image promotion |
| Developer Experience | Desk | Namespace provisioning, onboarding |

## Installation

```bash
clawhub install kubernetes
```

## How It Works

**Instruction-only** — no executable scripts. Each agent receives markdown instructions that describe what kubectl/oc commands to run and how to interpret output. The host's installed CLI tools do the actual work.

## Requirements

- `kubectl` (required)
- `oc` (optional, for OpenShift)
- `helm` (optional, for GitOps agent)
- `KUBECONFIG` cluster access

## Architecture

```
kubernetes/
├── SKILL.md                          # Root — combined swarm
├── skills/
│   ├── orchestrator/SKILL.md         # Jarvis
│   ├── cluster-ops/SKILL.md          # Atlas
│   ├── gitops/SKILL.md               # Flow
│   ├── security/SKILL.md             # Shield
│   ├── observability/SKILL.md        # Pulse
│   ├── artifacts/SKILL.md            # Cache
│   └── developer-experience/SKILL.md # Desk
├── memory/MEMORY.md                  # Long-term memory
├── working/WORKING.md                # Session progress
└── logs/LOGS.md                      # Audit trail
```

## Safety

- Production changes require human approval
- Destructive operations need explicit confirmation
- All actions logged to audit trail
- Least-privilege service accounts recommended

## License

MIT
