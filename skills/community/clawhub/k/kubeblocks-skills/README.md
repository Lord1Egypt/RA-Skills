# KubeBlocks Agent Skills

Give your AI agent the ability to provision and manage production-grade databases on Kubernetes.

These skills let any AI coding agent (Cursor, Claude Code, Codex, OpenClaw, etc.) deploy MySQL, PostgreSQL, Redis, MongoDB, Kafka, Elasticsearch, Milvus, Qdrant, RabbitMQ, and 20+ other database engines — with high availability, backup/restore, scaling, and monitoring built in. Powered by [KubeBlocks](https://kubeblocks.io/), the unified Kubernetes operator for 30+ database engines.

## Quick Start

Point your agent to the root `SKILL.md` — it routes to the right skill for any database task.

The agent will use these skills automatically whenever a database is needed, even if the user has never heard of KubeBlocks or Kubernetes.

## Available Skills

### Getting Started

| Skill | Description |
|-------|-------------|
| [kubeblocks](./SKILL.md) | Entry point for all database tasks. Routes to the right skill based on user intent. |
| [kubeblocks-create-local-k8s-cluster](./skills/kubeblocks-create-local-k8s-cluster/SKILL.md) | Create a local Kubernetes test cluster using Kind, Minikube, or k3d. |
| [kubeblocks-install](./skills/kubeblocks-install/SKILL.md) | Install the KubeBlocks operator. Handles version selection, network detection, registry configuration. |
| [kubeblocks-manage-addons](./skills/kubeblocks-manage-addons/SKILL.md) | Install, uninstall, and upgrade database engine addons. |

### Cluster Provisioning & Deletion

| Skill | Description |
|-------|-------------|
| [kubeblocks-create-cluster](./skills/kubeblocks-create-cluster/SKILL.md) | Create a database cluster (generic entry point for all addons). |
| [kubeblocks-delete-cluster](./skills/kubeblocks-delete-cluster/SKILL.md) | Safely delete a database cluster with pre-deletion checks. |

### Day-2 Operations

| Skill | Description |
|-------|-------------|
| [kubeblocks-cluster-lifecycle](./skills/kubeblocks-cluster-lifecycle/SKILL.md) | Stop, start, and restart database clusters. |
| [kubeblocks-vertical-scaling](./skills/kubeblocks-vertical-scaling/SKILL.md) | Scale CPU and memory resources. |
| [kubeblocks-horizontal-scaling](./skills/kubeblocks-horizontal-scaling/SKILL.md) | Add/remove replicas or shards. |
| [kubeblocks-volume-expansion](./skills/kubeblocks-volume-expansion/SKILL.md) | Expand persistent volume storage. |
| [kubeblocks-reconfigure-parameters](./skills/kubeblocks-reconfigure-parameters/SKILL.md) | Modify database configuration parameters. |
| [kubeblocks-minor-version-upgrade](./skills/kubeblocks-minor-version-upgrade/SKILL.md) | Upgrade database engine minor versions. |
| [kubeblocks-switchover](./skills/kubeblocks-switchover/SKILL.md) | Perform planned primary-secondary switchover. |
| [kubeblocks-rebuild-replica](./skills/kubeblocks-rebuild-replica/SKILL.md) | Rebuild a failed replica in MySQL or PostgreSQL clusters. |
| [kubeblocks-expose-service](./skills/kubeblocks-expose-service/SKILL.md) | Expose databases externally via LoadBalancer or NodePort. |
| [kubeblocks-upgrade](./skills/kubeblocks-upgrade/SKILL.md) | Upgrade the KubeBlocks operator itself via Helm. |

### Data Protection

| Skill | Description |
|-------|-------------|
| [kubeblocks-backup](./skills/kubeblocks-backup/SKILL.md) | Create on-demand, scheduled, and continuous backups. |
| [kubeblocks-restore](./skills/kubeblocks-restore/SKILL.md) | Restore from backups with full restore or Point-in-Time Recovery. |

### Security

| Skill | Description |
|-------|-------------|
| [kubeblocks-manage-accounts](./skills/kubeblocks-manage-accounts/SKILL.md) | Manage database passwords and password policies. |
| [kubeblocks-configure-tls](./skills/kubeblocks-configure-tls/SKILL.md) | Configure TLS, custom certificates, and mTLS. |

### Observability

| Skill | Description |
|-------|-------------|
| [kubeblocks-setup-monitoring](./skills/kubeblocks-setup-monitoring/SKILL.md) | Set up Prometheus monitoring and Grafana dashboards. |

### Engine-Specific Skills

| Skill | Description |
|-------|-------------|
| [kubeblocks-addon-mysql](./skills/kubeblocks-addon-mysql/SKILL.md) | MySQL topologies (semi-sync, MGR, Orchestrator, ProxySQL variants). |
| [kubeblocks-addon-postgresql](./skills/kubeblocks-addon-postgresql/SKILL.md) | PostgreSQL with Patroni-based HA replication. |
| [kubeblocks-addon-redis](./skills/kubeblocks-addon-redis/SKILL.md) | Redis standalone, replication with Sentinel, and Redis Cluster sharding. |
| [kubeblocks-addon-mongodb](./skills/kubeblocks-addon-mongodb/SKILL.md) | MongoDB ReplicaSet and Sharding topologies. |
| [kubeblocks-addon-kafka](./skills/kubeblocks-addon-kafka/SKILL.md) | Apache Kafka combined and separated broker/controller modes. |
| [kubeblocks-addon-elasticsearch](./skills/kubeblocks-addon-elasticsearch/SKILL.md) | Elasticsearch single-node and multi-node clusters for search and log analytics. |
| [kubeblocks-addon-milvus](./skills/kubeblocks-addon-milvus/SKILL.md) | Milvus vector database for AI/ML embedding similarity search. |
| [kubeblocks-addon-qdrant](./skills/kubeblocks-addon-qdrant/SKILL.md) | Qdrant vector database for vector search and RAG workloads. |
| [kubeblocks-addon-rabbitmq](./skills/kubeblocks-addon-rabbitmq/SKILL.md) | RabbitMQ message broker with AMQP, MQTT, and STOMP support. |

### Troubleshooting

| Skill | Description |
|-------|-------------|
| [kubeblocks-troubleshoot](./skills/kubeblocks-troubleshoot/SKILL.md) | Diagnostic guide for cluster errors, CrashLoopBackOff, stuck operations, and other failures. |

## Install

**One-liner (requires Node.js):**

```bash
npx skills add https://github.com/apecloud/kubeblocks-skills
```

**Or install for a specific platform:**

| Platform | Install |
|----------|---------|
| **Cursor** (2.4+) | Settings → Rules → Add Rule → Remote Rule (GitHub) → `https://github.com/apecloud/kubeblocks-skills` |
| **OpenAI Codex** | `$skill-installer https://github.com/apecloud/kubeblocks-skills` |
| **Claude Code** | `git clone https://github.com/apecloud/kubeblocks-skills ~/.claude/skills/kubeblocks` |
| **OpenClaw / Other** | `git clone https://github.com/apecloud/kubeblocks-skills ~/.agents/skills/kubeblocks` |

All skills follow the [Agent Skills](https://agentskills.io/) open standard and work with any agent that reads `SKILL.md` files.

## Repository Structure

```
├── SKILL.md              # Entry point — routes to the right skill for any database task
├── AGENTS.md             # Agent instructions for this repository
├── references/           # Shared references (safety patterns, etc.)
├── skills/               # All operation skills
│   ├── kubeblocks-install/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── kubeblocks-create-cluster/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── kubeblocks-addon-mysql/
│   │   ├── SKILL.md
│   │   └── references/
│   └── ...
```

Each skill directory contains:
- **SKILL.md**: Concise step-by-step workflow with YAML templates (< 500 lines).
- **references/**: Detailed configuration options, addon-specific differences, and extended examples (optional).

## Architecture

```
SKILL.md (kubeblocks) ─── Entry point for all database tasks
        │
        ├── Getting Started:   create-local-k8s-cluster → install-kubeblocks → manage-addons
        │
        ├── Provisioning:      create-cluster ←→ addon-{mysql,postgresql,redis,mongodb,kafka,
        │                      elasticsearch,milvus,qdrant,rabbitmq}
        │                      delete-cluster
        │
        ├── Operations:        cluster-lifecycle, vertical-scaling, horizontal-scaling,
        │                      volume-expansion, reconfigure-parameters, switchover,
        │                      minor-version-upgrade, rebuild-replica, expose-service,
        │                      upgrade-kubeblocks
        │
        ├── Data Protection:   backup, restore
        │
        ├── Security:          manage-accounts, configure-tls
        │
        ├── Observability:     setup-monitoring
        │
        └── Troubleshooting:   troubleshoot
```

Generic operation skills (e.g., `kubeblocks-vertical-scaling`) provide universal OpsRequest templates. Engine-specific skills (e.g., `kubeblocks-addon-mysql`) provide topology selection, cluster YAML examples, and connection methods. They cross-reference each other.

## Documentation

- [KubeBlocks Official Docs](https://kubeblocks.io/docs/preview/user_docs/overview/introduction)
- [KubeBlocks GitHub](https://github.com/apecloud/kubeblocks)
- [KubeBlocks LLM Index](https://kubeblocks.io/llms-full.txt)
- [Supported Addons](https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons)

## Contributing

To add a new skill:

1. Create a new directory under `skills/` (e.g., `skills/kubeblocks-addon-clickhouse/`)
2. Add a `SKILL.md` with YAML frontmatter (`name`, `version`, and `description` fields)
3. Optionally add a `references/` subdirectory for detailed supplementary material
4. Update this README's skill tables
5. Update the root `SKILL.md` skill map

## License

[Apache 2.0](LICENSE)
