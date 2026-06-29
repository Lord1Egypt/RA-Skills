# Output Schema

```json
{
  "summary": "migration planning summary",
  "source": {
    "region": "cn-north-4",
    "cluster_id": "optional"
  },
  "inventory": {
    "clusters": [],
    "nodepools": [],
    "workloads": [],
    "networking": [],
    "storage": [],
    "configuration": []
  },
  "dependency_matrix": [],
  "migration_batches": [],
  "risks": [],
  "rollback_plan": [],
  "validation_plan": []
}
```

## Field Descriptions

| Field | Description |
|-------|-------------|
| `summary` | High-level migration planning summary describing scope, goal, and outcome |
| `source.region` | Source Huawei Cloud region ID |
| `source.cluster_id` | Source CCE cluster ID (optional if listing multiple clusters) |
| `inventory.clusters` | CCE cluster details (version, network model, status) |
| `inventory.nodepools` | Node pool details (flavor, AZ, autoscaling, count) |
| `inventory.workloads` | Workload details (Deployments, Services, Ingresses, etc.) |
| `inventory.networking` | Networking details (VPC, subnets, security groups, ELB, EIP) |
| `inventory.storage` | Storage details (PVC/PV, EVS, SFS/SFS Turbo) |
| `inventory.configuration` | Configuration details (ConfigMap names, Secret existence only) |
| `dependency_matrix` | Dependency entries with type (ingress/service/storage/config/external) and direction |
| `migration_batches` | Batch entries with resources, validation points, downtime window, and batch order |
| `risks` | Risk entries with severity, category, description, and mitigation |
| `rollback_plan` | Rollback strategy per batch with steps and verification criteria |
| `validation_plan` | Validation steps per batch with expected outcomes |