# Risk Rules & Guardrails

## Hard Constraints (NEVER violate)

### H1: No Skip-Version Upgrades

CCE does NOT support skipping intermediate versions. Any attempt to skip will fail at API validation.

**Rationale**: Kubernetes API compatibility, etcd data schema, and component version dependencies require sequential upgrades.

### H2: Control Plane Before Nodes

Upgrade order is mandatory: control plane first → then nodes → then addons.

**Rationale**: kube-apiserver must be at target version before kubelet can upgrade. Nodes register with apiserver; incompatible kubelet causes registration failures.

### H3: Patch Version Latest Before Major Upgrade

Current patch version must be the latest available before upgrading to a new major version.

**Rationale**: CCE pre-check validates patch version. Non-latest patch versions block major version upgrade.

### H4: No Concurrent Cluster Operations

During upgrade, do NOT perform: cluster hibernation, node delete, node pool resize, node cordon/drain, addon install/uninstall.

**Rationale**: Concurrent operations conflict with upgrade state machine, causing failures or data loss.

### H5: Do Not Pause Between Control Plane and Node Upgrades

For v1.15→v1.19 upgrade specifically, do NOT use PauseUpgradeClusterTask between control plane and node phases.

**Rationale**: v1.19 apiserver treats v1.15 kubelet registration labels as illegal. Nodes may stay NotReady if paused.

### H6: Verify Business Webhook SAN Before v1.19+ Upgrade

Before upgrading to v1.19+, verify all custom webhook certificates include Subject Alternative Names (SAN) field.

**Rationale**: Go v1.15 deprecates CommonName in X.509 certificates. v1.19+ apiserver rejects webhooks without SAN.

### H7: PSP Migration Before v1.25 Upgrade

PodSecurityPolicy is removed in v1.25. Must complete PSP→PSA migration before v1.25 upgrade.

**Rationale**: PSP API and admission controller are deleted in v1.25. Remaining PSP resources block upgrade.

## Soft Constraints (SHOULD follow, exceptions documented)

### S1: Upgrade During Low-Traffic Window

Schedule upgrades during business low-traffic periods (typically 2-6 AM or weekends).

**Rationale**: Node upgrade makes nodes temporarily unschedulable. API Server has brief interruption during control plane upgrade.

### S2: Keep ≥2 Nodes Per Node Pool

Maintain at least 2 nodes per node pool during upgrade for workload redundancy.

**Rationale**: Single-node pool has zero redundancy. If that node fails during upgrade, all workloads on that pool are disrupted.

### S3: Business Verification After Each Phase

After control plane upgrade and after node pool upgrade, run business health verification.

**Rationale**: Catch issues early at each phase boundary rather than discovering all problems at the end.

### S4: Monitor Upgrade Progress Continuously

Check ShowUpgradeWorkFlow status every 5-10 minutes during active upgrade.

**Rationale**: Early detection of stuck or failed upgrade tasks allows faster intervention.

### S5: Backup Before Major Version Upgrade

Perform CBR/EVS backup of control nodes before major version upgrade.

**Rationale**: etcd auto-backup covers etcd data only. Full disk backup covers component configs and images.

## Rollback Strategies

### Strategy 1: Pause and Investigate

```bash
hcloud CCE PauseUpgradeClusterTask --cluster_id=<cluster-id> --cli-region=<region>
```

Use when: upgrade task fails but cluster is still functional. Pause to investigate root cause.

### Strategy 2: Cancel Upgrade Workflow

```bash
hcloud CCE UpgradeWorkFlowUpdate \
  --cluster_id=<cluster-id> \
  --upgrade_workflow_id=<workflow-id> \
  --status.phase=Cancel \
  --cli-region=<region>
```

Use when: upgrade is irrecoverably broken. Cancel to stop all upgrade activities.

### Strategy 3: Backup Restore

Restore from etcd auto-backup (created during upgrade) or CBR/EVS manual backup (created before upgrade).

Use when: upgrade causes cluster data corruption or control plane failure.

**Limitation**: Backup restore only works if upgrade has NOT been completed successfully. Post-upgrade operations (e.g., cluster spec change) invalidate backup rollback capability.

### Strategy 4: Node Drain and Skip

For failed individual nodes: drain workloads → skip the node → continue upgrade on remaining nodes → fix the skipped node separately after upgrade completes.

Use when: individual node upgrade fails but cluster control plane is healthy.

## Guardrails

1. **Assessment only**: This skill generates assessment reports and execution previews. It does NOT auto-execute upgrade commands.
2. **Two-step confirmation**: All execution preview commands require explicit user confirmation (`confirm=true` equivalent) before actual execution.
3. **No modification during upgrade**: Do not change cluster specs, node pools, or addons while upgrade is in progress.
4. **Rollback plan required**: Every upgrade plan must include a rollback strategy before starting execution.
5. **Version lifecycle check**: Verify target version is NOT EOS before planning upgrade.