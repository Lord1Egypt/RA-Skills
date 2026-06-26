---
name: kubeblocks
version: "0.2.0"
description: Provision and manage production-grade databases on Kubernetes using KubeBlocks. Use this skill when the user needs a database — MySQL, PostgreSQL, Redis, MongoDB, Kafka, Elasticsearch, Milvus, Qdrant, RabbitMQ, or any other data infrastructure — and has (or is willing to set up) a Kubernetes environment. Trigger phrases include "I need a database", "set up MySQL", "spin up Postgres", "deploy a vector database for RAG", "I need a message queue", or any request involving database provisioning, scaling, backup, restore, monitoring, or troubleshooting on Kubernetes. Also use when the user explicitly mentions KubeBlocks, or wants to manage existing KubeBlocks-managed database clusters.
compatibility:
  required_tools:
    - kubectl
    - helm
  optional_tools:
    - npx
  notes: Requires access to a Kubernetes cluster (kubeconfig). For local development, the skill can create a cluster using Kind, Minikube, or k3d.
---

# KubeBlocks — Databases on Kubernetes, Made Simple

## When To Use This Skill

Use this skill when:

- The user needs a database and has (or is willing to set up) a Kubernetes environment
- The user asks to "set up", "create", "deploy", "spin up", or "provision" a database on Kubernetes
- The user mentions a database engine (MySQL, PostgreSQL, Redis, MongoDB, Kafka, Elasticsearch, Milvus, Qdrant, RabbitMQ, etc.) in the context of deployment or operations
- The user needs database operations on K8s: scaling, backup, restore, monitoring, failover, parameter tuning
- The user is troubleshooting a KubeBlocks-managed database
- The user mentions KubeBlocks directly

**When NOT to use this skill:** If the user only needs a connection string to an existing managed database service (e.g., AWS RDS, Google Cloud SQL), or wants to run a database directly via Docker Compose without Kubernetes, this skill is not the right fit.

If the user doesn't have a Kubernetes cluster yet but wants one, this skill set includes creating a local K8s cluster for development and testing.

## What is KubeBlocks?

KubeBlocks is a Kubernetes operator that manages 30+ database engines on any K8s cluster. It provides a unified API for the full lifecycle — from provisioning and scaling to backup, restore, and observability — across relational, NoSQL, streaming, vector, and graph databases.

- Official docs: https://kubeblocks.io/docs/preview/user_docs/overview/introduction
- Full LLM doc index: https://kubeblocks.io/llms-full.txt
- GitHub: https://github.com/apecloud/kubeblocks

## Quick Status Check

Before performing any operation, verify the current state:

```bash
# Check if KubeBlocks is installed
kubectl -n kb-system get pods

# List all database clusters across namespaces
kubectl get cluster -A

# Check KubeBlocks version
helm list -n kb-system | grep kubeblocks
```

If KubeBlocks is not installed, start with the [install-kubeblocks](skills/kubeblocks-install/SKILL.md) skill. If there is no Kubernetes cluster at all, start with [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md).

## Skill Map

Read the skill that matches the user's intent. Each skill is a self-contained guide with YAML templates, step-by-step workflow, and troubleshooting.

### Getting Started

| User Intent | Skill |
|---|---|
| Create a local K8s test cluster | [create-local-k8s-cluster](skills/kubeblocks-create-local-k8s-cluster/SKILL.md) |
| Install KubeBlocks operator | [install-kubeblocks](skills/kubeblocks-install/SKILL.md) |
| Install/manage database engine addons | [manage-addons](skills/kubeblocks-manage-addons/SKILL.md) |

### Create a Database

| User Intent | Skill |
|---|---|
| Create a MySQL cluster | [addon-mysql](skills/kubeblocks-addon-mysql/SKILL.md) |
| Create a PostgreSQL cluster | [addon-postgresql](skills/kubeblocks-addon-postgresql/SKILL.md) |
| Create a Redis cluster | [addon-redis](skills/kubeblocks-addon-redis/SKILL.md) |
| Create a MongoDB cluster | [addon-mongodb](skills/kubeblocks-addon-mongodb/SKILL.md) |
| Create a Kafka cluster | [addon-kafka](skills/kubeblocks-addon-kafka/SKILL.md) |
| Create an Elasticsearch cluster | [addon-elasticsearch](skills/kubeblocks-addon-elasticsearch/SKILL.md) |
| Create a Milvus (vector DB) cluster | [addon-milvus](skills/kubeblocks-addon-milvus/SKILL.md) |
| Create a Qdrant (vector DB) cluster | [addon-qdrant](skills/kubeblocks-addon-qdrant/SKILL.md) |
| Create a RabbitMQ cluster | [addon-rabbitmq](skills/kubeblocks-addon-rabbitmq/SKILL.md) |
| Create any other database (generic) | [create-cluster](skills/kubeblocks-create-cluster/SKILL.md) |
| Delete a database cluster | [delete-cluster](skills/kubeblocks-delete-cluster/SKILL.md) |

### Day-2 Operations

| User Intent | Skill |
|---|---|
| Stop / Start / Restart a cluster | [cluster-lifecycle](skills/kubeblocks-cluster-lifecycle/SKILL.md) |
| Scale CPU / Memory (vertical) | [vertical-scaling](skills/kubeblocks-vertical-scaling/SKILL.md) |
| Add / remove replicas or shards | [horizontal-scaling](skills/kubeblocks-horizontal-scaling/SKILL.md) |
| Expand storage volume | [volume-expansion](skills/kubeblocks-volume-expansion/SKILL.md) |
| Change database parameters | [reconfigure-parameters](skills/kubeblocks-reconfigure-parameters/SKILL.md) |
| Primary / secondary switchover | [switchover](skills/kubeblocks-switchover/SKILL.md) |
| Upgrade database engine version | [minor-version-upgrade](skills/kubeblocks-minor-version-upgrade/SKILL.md) |
| Rebuild a failed replica | [rebuild-replica](skills/kubeblocks-rebuild-replica/SKILL.md) |
| Upgrade KubeBlocks operator | [upgrade-kubeblocks](skills/kubeblocks-upgrade/SKILL.md) |

### Data Protection

| User Intent | Skill |
|---|---|
| Backup cluster data | [backup](skills/kubeblocks-backup/SKILL.md) |
| Restore from backup / PITR | [restore](skills/kubeblocks-restore/SKILL.md) |

### Security & Networking

| User Intent | Skill |
|---|---|
| Manage database passwords / accounts | [manage-accounts](skills/kubeblocks-manage-accounts/SKILL.md) |
| Configure TLS / mTLS encryption | [configure-tls](skills/kubeblocks-configure-tls/SKILL.md) |
| Expose service externally (LoadBalancer/NodePort) | [expose-service](skills/kubeblocks-expose-service/SKILL.md) |

### Observability

| User Intent | Skill |
|---|---|
| Setup monitoring (Prometheus/Grafana) | [setup-monitoring](skills/kubeblocks-setup-monitoring/SKILL.md) |

### Troubleshooting

| User Intent | Skill |
|---|---|
| Cluster not working, error, failed, stuck, CrashLoopBackOff | [troubleshoot](skills/kubeblocks-troubleshoot/SKILL.md) |

## Decision Tree

Use this when the user's intent needs clarification:

```
User needs a database
├─ Is KubeBlocks installed?
│  ├─ No  → Do they have a K8s cluster?
│  │        ├─ No  → create-local-k8s-cluster → install-kubeblocks
│  │        └─ Yes → install-kubeblocks
│  └─ Yes → Continue below
│
├─ Create a database
│  ├─ Is the engine addon installed?
│  │  ├─ No  → manage-addons → then create cluster
│  │  └─ Yes → Which engine?
│  │           ├─ MySQL/PG/Redis/MongoDB/Kafka/ES/Milvus/Qdrant/RabbitMQ → addon-{engine}
│  │           └─ Other → create-cluster (generic)
│  └─ Don't know which engine? → Recommend based on use case:
│     ├─ Relational / SQL         → addon-postgresql or addon-mysql
│     ├─ Cache / session store    → addon-redis
│     ├─ Document store           → addon-mongodb
│     ├─ Event streaming          → addon-kafka
│     ├─ Full-text search / logs  → addon-elasticsearch
│     ├─ Vector similarity / RAG  → addon-milvus or addon-qdrant
│     └─ Message queue            → addon-rabbitmq or addon-kafka
│
├─ Operate an existing database
│  ├─ Scale CPU/Memory      → vertical-scaling
│  ├─ Add/remove replicas   → horizontal-scaling
│  ├─ Expand disk            → volume-expansion
│  ├─ Change DB config       → reconfigure-parameters
│  ├─ Switchover primary     → switchover
│  ├─ Upgrade DB version     → minor-version-upgrade
│  ├─ Rebuild failed replica → rebuild-replica
│  ├─ Stop / Start / Restart → cluster-lifecycle
│  └─ Delete permanently     → delete-cluster
│
├─ Protect data
│  ├─ Backup                 → backup
│  └─ Restore / PITR         → restore
│
├─ Secure the database
│  ├─ Manage passwords       → manage-accounts
│  ├─ Enable TLS/SSL         → configure-tls
│  └─ Expose externally      → expose-service
│
├─ Monitor                   → setup-monitoring
├─ Upgrade KubeBlocks itself → upgrade-kubeblocks
└─ Something is broken       → troubleshoot
```

## Engine Recommendation Guide

When the user needs a database but hasn't chosen an engine, recommend based on their use case:

| Use Case | Recommended Engine | Why |
|---|---|---|
| Web app backend, relational data, SQL | PostgreSQL | Most versatile, strong ecosystem |
| Legacy app compatibility, MySQL protocol | MySQL | Drop-in for MySQL-dependent apps |
| Caching, sessions, rate limiting | Redis | Sub-millisecond latency, simple API |
| Flexible schema, document storage | MongoDB | Schema-free, horizontal scaling |
| Event streaming, log pipelines | Kafka | High throughput, durable ordered streams |
| Full-text search, log analytics | Elasticsearch | Inverted index, powerful query DSL |
| AI embeddings, similarity search, RAG | Milvus or Qdrant | Purpose-built vector indexes |
| Task queues, pub/sub messaging | RabbitMQ | Flexible routing, multiple protocols |

## Disambiguation Guide

### "Scale" ambiguity

| User says | Skill |
|-----------|-------|
| "scale up", "more CPU", "more memory", "resize" | vertical-scaling |
| "add replicas", "more nodes", "scale out", "add shards" | horizontal-scaling |
| "more disk", "more storage", "expand volume" | volume-expansion |

### "Delete" vs "Stop"

| User says | Skill |
|-----------|-------|
| "delete", "remove", "destroy", "drop" (permanent) | delete-cluster |
| "stop", "pause", "shut down" (temporary, keeps data) | cluster-lifecycle |

### "Upgrade" ambiguity

| User says | Skill |
|-----------|-------|
| "upgrade MySQL/PG version", "patch database" | minor-version-upgrade |
| "upgrade KubeBlocks", "update operator" | upgrade-kubeblocks |

## Safety Patterns

Before performing any cluster-modifying operation, review the [safety-patterns](references/safety-patterns.md) reference. Key rules:

- **Dry-run before apply**: Always run `kubectl apply --dry-run=server` before any real `kubectl apply`.
- **Confirm before destructive actions**: Deletions, scale-in, stop, and terminationPolicy changes require explicit user confirmation. List backups and affected resources first.
- **Credential handling**: Commands like `kubectl get secret ... -o jsonpath` expose database passwords. Only run these when the user explicitly requests credentials, and warn that the output contains sensitive data.
- **kubectl exec**: Entering database pods (`kubectl exec -it`) gives shell access to production data. Always confirm with the user before executing.
- **Production protection**: Clusters with `terminationPolicy: DoNotTerminate` should be treated with extra caution. Recommend backups before risky operations (upgrade, switchover, reconfigure).

## Common Debugging Commands

```bash
kubectl describe cluster <cluster-name> -n <namespace>
kubectl get opsrequest -n <namespace>
kubectl get component -n <namespace>
kubectl logs -n <namespace> <pod-name> -c <container-name>
kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=100
```

## Documentation Links

| Resource | URL |
|---|---|
| Introduction | https://kubeblocks.io/docs/preview/user_docs/overview/introduction |
| Supported Addons | https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons |
| Full LLM Index | https://kubeblocks.io/llms-full.txt |
| GitHub Repository | https://github.com/apecloud/kubeblocks |
| Releases | https://github.com/apecloud/kubeblocks/releases |
