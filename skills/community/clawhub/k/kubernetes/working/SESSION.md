# Cluster Session Context

> This file tracks the current agent's working context including environment, cluster details, and permissions.

---

## Current Session

### Agent
- **Name**: 
- **Session Started**: 
- **Task**: 

### Environment Context
- **Environment**: dev | qa | staging | prod
- **Cluster Name**: 
- **Cluster Type**: openshift | kubernetes | eks | aks | gke | rosa | aro
- **Cluster Version**: 
- **Context Name**: 
- **Namespace**: 

### Cluster Information (Populated on First Run)

#### Cluster Details
| Component | Version |
|-----------|---------|
| Platform | |
| Kubernetes API | |
| etcd | |
| Controller Manager | |
| Scheduler | |
| Kubelet | |
| Kube-proxy | |

#### Key Components
| Component | Version | Namespace |
|-----------|---------|-----------|
| ArgoCD / Flux | | |
| Prometheus | | |
| Grafana | | |
| Ingress/Nginx | | |
| Service Mesh | | |
| cert-manager | | |
| Vault | | |

#### Operator Versions (OpenShift/OLM)
| Operator | Version | Namespace |
|----------|---------|-----------|
| | | |

### Permission Context
- **Can Delete**: NO
- **Can Modify Prod**: NO
- **Can Create RBAC**: NO
- **Requires Approval**: YES (see AGENTS.md)

### Change Constraints by Environment

| Environment | Delete | Modify Prod | RBAC | Scale | Secrets |
|-------------|-------|------------|------|-------|---------|
| **dev** | Approval | Approval | Approval | Auto | Approval |
| **qa** | Approval | Approval | Approval | Approval | Approval |
| **staging** | Approval | Approval | Approval | Approval | Approval |
| **prod** | NEVER | NEVER | NEVER | NEVER | NEVER |

---

## Session Activity Log

| Timestamp | Action | Details |
|-----------|--------|---------|
| | | |

---

*This file is updated at session start and whenever context changes.*
