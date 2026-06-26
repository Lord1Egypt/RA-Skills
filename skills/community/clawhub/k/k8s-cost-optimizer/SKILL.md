---
name: k8s-cost-optimizer
description: Find and rank Kubernetes cost-saving opportunities from kubectl, metrics-server, kube-state-metrics, and cloud billing. Identifies overprovisioned CPU/memory requests and limits, idle namespaces and workloads, oversized PersistentVolumes, unused LoadBalancer services, expensive node types, missing HorizontalPodAutoscalers, and clusters that haven't adopted spot/preemptible/Graviton nodes. Outputs a ranked list of recommendations with $/month savings estimates and ready-to-apply YAML patches. Covers EKS, GKE, and AKS specifics including instance pricing, savings plans, committed-use discounts, and reservation strategies. Use when asked to cut a Kubernetes cloud bill, right-size workloads, plan a spot migration, build a FinOps report, or tune HPA settings. Triggers on "kubernetes cost", "k8s cost", "eks cost", "gke cost", "aks cost", "right-size", "rightsize", "kubecost", "opencost", "vpa", "hpa", "spot instances", "preemptible", "savings plan", "node pool", "pod requests", "finops".
metadata:
  tags: ["kubernetes", "k8s", "eks", "gke", "aks", "finops", "cost-optimization", "rightsizing", "autoscaling", "spot-instances", "kubecost", "opencost", "platform-engineering", "devops"]
---

# Kubernetes Cost Optimizer

Audit a Kubernetes cluster (or fleet) and produce a ranked list of cost-saving actions with concrete dollar estimates. Looks at requests/limits vs actual usage, idle workloads, expensive node types, missing autoscaling, public LBs, oversized PVs, and unused capacity. Acts as a senior FinOps engineer who has cut six- and seven-figure cloud bills without breaking workloads.

## Usage

Invoke this skill when a Kubernetes bill is too high, when a quarterly FinOps review is due, or when leadership has asked for "30% off the cloud."

**Basic invocation:**
> Audit my EKS cluster for cost savings
> Cut my GKE bill — here's kubectl top + node list
> What's the highest-ROI optimization I can ship this week?

**With context:**
> Here's metrics-server data for 30 days, the node list, and the AWS bill
> I have 14 namespaces — which ones are idle?
> We're 100% on-demand m5 nodes — what's the spot migration plan?

The agent produces a ranked recommendation list (highest $/month savings first), per-recommendation YAML patches or commands, and a four-week implementation plan that respects production safety.

## How It Works

### Step 1: Data Collection

Cost optimization without data is guesswork. The agent collects from four sources and joins them:

| Source | What It Provides | How To Pull |
|--------|------------------|-------------|
| **kubectl + metrics-server** | Real CPU/memory usage per pod, per node | `kubectl top pods -A`, `kubectl top nodes` |
| **kube-state-metrics / Prometheus** | Requests, limits, replicas, deployment-level history | PromQL: `kube_pod_container_resource_requests`, 30-day window |
| **Cloud billing** | $/node-hour, instance type, region, sustained-use | AWS Cost Explorer, GCP billing export, Azure Cost Management |
| **Cluster object inventory** | Namespaces, services, PVCs, ingress, jobs, cronjobs | `kubectl get all,pvc,svc -A -o json` |

Data **window** matters. The agent prefers 30 days; 7 days for fast-moving clusters; 90 days for capacity planning. Anything under 7 days is too short — diurnal and weekly patterns dominate the noise.

If Kubecost or OpenCost is installed, the agent uses the cluster's per-namespace cost allocation directly. Otherwise it computes allocations from node price × pod-share-of-node.

### Step 2: The Cost Recommendation Catalog

The agent runs the cluster against a fixed set of recommendation **types**, each with a detection rule and a savings formula.

**C1. Overprovisioned CPU requests**

```
Detection:
  for each container,
    p99(cpu_usage over 30d) < 0.50 * cpu_request
    AND container has >7 days of data
    AND deployment is not a known-bursty type (cron, batch, init)

Savings estimate:
  ($/cpu-hour for the node pool) × (request - p99usage) × 24 × 30 × replicas

Action:
  patch container.resources.requests.cpu down to ceil(p95 × 1.3)
```

**C2. Overprovisioned memory requests**

```
Detection:
  p99(memory_working_set over 30d) < 0.50 * memory_request

Savings:
  ($/GiB-hour for the node pool) × (request - p99usage) × 24 × 30 × replicas

Action:
  patch container.resources.requests.memory down to ceil(p99 × 1.25)
  NOTE: never set requests below working-set-p99 — OOMKills kill the savings
```

**C3. Limits == requests (no burst)**

```
Detection:
  cpu_limit == cpu_request for stateless workloads
  (typical anti-pattern: "treat limits as guaranteed quota")

Savings:
  None directly — but C1 dominates after limits are unblocked

Action:
  raise limits or remove (for cpu); keep limits for memory
```

**C4. Idle namespace**

```
Detection:
  sum(p95 cpu over 30d) across all pods in ns < 0.05 cores
  AND sum(p95 memory) < 200 MiB
  AND no recent kubectl apply (last_modified > 30 days)

Savings:
  All allocated capacity (request × node $)

Action:
  warn → tag → archive (Helm release deleted, namespace archived)
```

**C5. Idle deployment / statefulset**

```
Detection:
  replicas > 0 AND p99(cpu) < 0.02 cores AND request_count == 0 over 30d
  (request_count from ingress-controller or service mesh)

Savings:
  replicas × pod_cost / month

Action:
  scale to zero (KEDA cron, or just `kubectl scale --replicas=0`)
```

**C6. Oversized PersistentVolume**

```
Detection:
  for each PVC, kubelet_volume_stats_used / capacity < 0.3
  AND age > 30 days

Savings:
  ($/GB-month for storage class) × (capacity - used × 1.5)

Action:
  - On EKS gp3: shrink not supported. Migrate via snapshot → smaller PV.
  - On GKE pd-balanced: same — snapshot migration.
  - On AKS managed-disks: same. Plan downtime.
```

**C7. Unused LoadBalancer service**

```
Detection:
  Service type=LoadBalancer
  AND no NetworkPolicy hits
  AND no ingress traffic in 30d (cloud LB metrics)

Savings:
  AWS NLB:  ~$22/mo + $0.006/LCU-hr → $25-50/mo typical
  GCP LB:   ~$18/mo per forwarding rule
  Azure LB: ~$25/mo standard tier

Action:
  delete service or convert to ClusterIP behind a shared ingress
```

**C8. Expensive node type**

```
Detection:
  Node pool uses x86 on a workload that's arch-independent
  AND no GPU/specialized requirement
  AND newer-gen / Graviton / Tau alternative is cheaper per CPU-hour

Savings:
  AWS: m5 → m7g (Graviton)  ~20% cheaper, similar perf
  GCP: n2 → t2d (Tau AMD)   ~28% cheaper, comparable perf
  Azure: Dsv3 → Dpdsv5 (Arm) ~20% cheaper

Action:
  add Arm/AMD node pool, taint, set tolerations on workloads,
  recompile multi-arch images (most public images are already multi-arch)
```

**C9. Missing HorizontalPodAutoscaler**

```
Detection:
  Deployment with stable replica count > 3
  AND p95/p50 cpu ratio > 2.5x (variance)
  AND no HPA / KEDA / Karpenter scaler attached

Savings:
  (max_replicas - avg_replicas) × pod_cost
  typical: 30-60% of deployment's compute

Action:
  emit HPA YAML targeted at p50 of recent CPU
```

**C10. No spot / preemptible / Spot VM adoption**

```
Detection:
  Cluster is 100% on-demand
  AND has stateless workloads (Deployments without local volume requirements)
  AND tolerates interruption (replicas > 1, restart-safe)

Savings:
  AWS Spot:        60-90% off on-demand
  GCP Preemptible: 60-91% off (24h max lifetime)
  GCP Spot VMs:    60-91% off (no time limit, lower preemption rate)
  Azure Spot:      60-90% off (eviction subject to capacity)

Action:
  - Tag stateless workloads with affinity for spot pool
  - Add a managed-on-demand fallback pool sized to baseline
  - Use Karpenter (AWS) / cluster-autoscaler with multiple ASGs / Azure Spot Priority Mix
```

**C11. Missing pod disruption budgets / wrong topology spread**

```
Detection:
  Workload running on spot but no PDB
  OR PDB minAvailable >= replicas (always blocks eviction)

Savings:
  Indirect — wrong PDB blocks spot benefits

Action:
  set PDB minAvailable = replicas - 1 (or maxUnavailable = 25%)
  add topologySpreadConstraints across zones
```

**C12. Stale CronJobs and Jobs**

```
Detection:
  Job/CronJob age > 90 days, never succeeded recently
  OR successfulJobsHistoryLimit unset (default 3 retains 3, no cleanup)

Savings:
  Small per-cluster but accumulates: PVC retention, image-pull, scheduling churn

Action:
  set ttlSecondsAfterFinished, prune old job objects, remove dead cronjobs
```

**C13. Image pull cost (GCR / ECR / ACR cross-region)**

```
Detection:
  Cluster in region X pulls from registry in region Y
  → cross-region egress charges

Savings:
  Egress cost (typically $0.02-0.09/GB) × image-size × pod-restarts

Action:
  replicate registry into cluster region
  enable image-pull-policy: IfNotPresent
  pre-pull common images via DaemonSet
```

**C14. Reserved capacity / Savings Plans / CUDs not purchased**

```
Detection:
  Stable baseline > 70% of cluster running 24/7 for 90+ days
  AND no savings plans or CUDs in cloud account

Savings:
  AWS Compute Savings Plan: 30-66% off depending on commitment
  GCP CUD: 20-57% off (1-year and 3-year)
  Azure Reservations: 30-72% off

Action:
  size commitment to baseline (not peak)
  use Savings Plans (flexible) over RI (rigid) on AWS
```

**C15. Logs / metrics / traces ingestion cost**

```
Detection:
  Cluster sends 100% of logs to managed observability (Datadog, NewRelic, Splunk)
  AND log volume > 1 TB/month
  AND no sampling on chatty namespaces (kube-system, ingress-controller)

Savings:
  Often the largest single line item — Datadog logs at $0.10/GB ingested adds
  up fast; one chatty pod can cost $5,000/mo

Action:
  - Drop INFO logs from kube-system, controller-manager
  - Sample debug logs at 1%
  - Route to S3 + Athena for cold logs
```

### Step 3: Ranking The Recommendations

Recommendations are ordered by **expected savings × implementation safety / implementation effort**. The agent renders this as a table:

```
Rank  Type  Description                              $/mo saved  Effort  Risk
1     C1    Right-size payments-api requests         $4,200      2 hrs   Low
2     C10   Migrate stateless to spot (Karpenter)    $3,800      2 days  Med
3     C8    Move backend pool to Graviton            $2,100      1 day   Low
4     C15   Drop kube-system DEBUG logs in Datadog   $1,900      1 hr    Low
5     C7    Delete 4 unused NLBs                     $190        30 min  Low
6     C9    HPA on the api-gateway deployment        $850        2 hrs   Low
7     C6    Shrink 3 oversized PVs                   $310        4 hrs   Med
... etc
```

**Effort** is hours-of-engineering. **Risk** is Low/Med/High based on user-facing blast radius.

### Step 4: Right-Sizing Methodology

C1 and C2 dominate most clusters' savings. The agent applies a careful methodology:

```
1. WINDOW
   30 days minimum. Cover at least one full release cycle.
   Exclude windows containing incidents (skewed up) or maintenance
   windows (skewed down).

2. PERCENTILE
   Memory: p99 working_set × 1.25 = new request
   CPU:    p95 × 1.3            = new request
   Why different: memory OOMKills are catastrophic, CPU throttling is
   recoverable.

3. FLOOR
   Never below 50m CPU / 64Mi memory — startup probes need headroom.
   For Java/JVM: use the JVM's heap-max as memory floor.
   For Go: 2x the runtime's resident set.

4. LIMITS
   CPU limits: REMOVE for most workloads (CFS throttling causes more
              latency than it saves money).
   Memory limits: KEEP at request × 1.5 — OOM is a controlled failure.

5. STAGED ROLLOUT
   Apply to a canary deployment (1 of N replicas) for 48h.
   Monitor: error rate, latency p99, restart count, OOMKill count.
   If clean, roll out to remaining replicas.
   If regression, revert; widen the window or raise the percentile.

6. VPA RECOMMENDATION MODE
   For unfamiliar workloads, run VPA in `recommendOnly` mode for 7+
   days. Use its target as a sanity-check on the agent's calculation.
```

### Step 5: Cloud-Specific Specifics

**EKS (AWS):**

- **Karpenter** beats cluster-autoscaler on EKS for cost: provisions exactly the right node, mixes instance types, adopts spot natively. Migrating to Karpenter is often a 15-25% saving on its own.
- **Graviton (m7g, c7g, r7g)**: ~20% cheaper than equivalent x86. Multi-arch images are required; check `docker manifest inspect`.
- **Spot via Karpenter**: set `karpenter.sh/capacity-type: spot` in the NodePool; add an on-demand fallback pool.
- **EKS control-plane** is $0.10/hr per cluster — cluster consolidation is sometimes the right move (one prod, one staging, one dev rather than per-team clusters).
- **AWS Compute Savings Plan**: covers EC2, Fargate, Lambda; flexible across instance families. Buy at baseline, not peak.
- **EBS gp3** is cheaper than gp2 at equal IOPS — easy migration via volume modify.

**GKE:**

- **Autopilot** mode: no node management, charged per pod-second. Often cheaper for low-utilization clusters; more expensive for dense clusters.
- **Spot VMs** preferred over old Preemptible (no 24h cap, lower preemption rate).
- **CUDs** apply to vCPU and memory committed for 1y or 3y; flexible across instance families with the new "flex CUD."
- **T2D / Tau**: AMD-based, ~28% cheaper for general-purpose workloads.
- **GKE control-plane** is free for one zonal cluster per project; regional clusters cost extra.
- **Cluster Autoscaler** scales node pools but cannot create new pools — pre-create spot/Graviton pools with appropriate taints.

**AKS:**

- **AKS control-plane** is free (Azure pays); only nodes are billed.
- **Spot node pools** require explicit provisioning; eviction policy `Deallocate` keeps disks but releases compute.
- **Reserved Instances** apply at the VM-family level (Dsv5, Esv5); commit to baseline.
- **Arm-based Dpsv5/Dpdsv5**: ~20% cheaper; multi-arch images required.
- **Cluster Autoscaler** is the only scaler (no Karpenter equivalent); pool consolidation is more manual.

### Step 6: Safety Constraints

The agent never proposes changes that risk data loss or sustained outage. Specifically:

| Action | Hard Constraint |
|--------|----------------|
| Right-size memory | Never set request below historic working-set p99 |
| Migrate to spot | Never for: databases, message brokers, stateful sets without proper PDB, single-replica deployments |
| Shrink PV | Never in-place; always snapshot → smaller PV with cutover window |
| Delete idle namespace | Only after 14-day notice + tag + archive (Helm uninstall preserves manifests) |
| Migrate to Arm | Only after multi-arch image verified with `docker manifest inspect` |
| Remove HPA | Never; only adjust |
| Reduce replicas below PDB minAvailable | Never; adjust PDB first or keep replicas |

### Step 7: Implementation Plan (4 Weeks)

```
WEEK 1 — QUICK WINS (LOW RISK, HIGH ROI)
Mon  Run audit: collect kubectl + Prom + billing data
Tue  Identify C1/C2 candidates with > $500/mo savings each
Wed  Apply right-size patches to canary replicas
Thu  Monitor canary 48h
Fri  Roll out to full deployments; baseline new bill

WEEK 2 — IDLE & UNUSED
Mon  Identify idle namespaces (C4) and idle deployments (C5)
Tue  Tag with `cost-review: pending-deletion`; notify owners
Wed  Scale-to-zero on confirmed idle workloads
Thu  Delete unused LBs (C7); delete oversized PVs (C6 staged)
Fri  Tally savings; update FinOps dashboard

WEEK 3 — STRUCTURAL (NODE STRATEGY)
Mon  Add Karpenter (EKS) / Spot pool (GKE/AKS)
Tue  Add taints and tolerations on stateless workloads
Wed  Drain a small percentage to spot; observe interruption rate
Thu  Add Graviton/Arm pool; pin one workload as canary
Fri  Roll out to remaining stateless workloads

WEEK 4 — COMMITMENTS & OBSERVABILITY
Mon  Compute baseline post-optimization
Tue  Purchase Savings Plan / CUDs at 70% of baseline
Wed  Tune logs/metrics ingestion (C15)
Thu  Add cost dashboards: per-namespace, per-team showback
Fri  Postmortem + savings report; schedule next quarter audit
```

### Step 8: FinOps Reporting

The agent produces a weekly / monthly report:

```markdown
## Cluster: prod-us-east-1
### Savings achieved this month: $14,820 (-31%)

| Category | $ saved | % of total |
|----------|--------|-----------|
| Right-size requests (C1+C2) | $6,420 | 43% |
| Spot migration (C10)        | $4,100 | 28% |
| Graviton (C8)               | $2,100 | 14% |
| Logs ingestion (C15)        | $1,900 | 13% |
| LB cleanup (C7)             |   $300 |  2% |

### Remaining opportunities: $9,400/mo
- HPA rollout pending on api-gateway: ~$850/mo
- Savings Plan not yet purchased: ~$8,000/mo (commit 1-year)
- Oversized PVs not yet migrated: ~$310/mo

### Risks accepted
- Spot interruption rate: 3.2%/day (within budget of 5%)
- Right-sized memory on cart-svc near p99 — monitoring OOMKills
```

## Worked Examples

### Example 1: Right-Size A Java API

**Input:**

```
Deployment: payments-api
Replicas: 12
Container: payments
  resources.requests.cpu: 2
  resources.requests.memory: 4Gi
  resources.limits.cpu: 2
  resources.limits.memory: 4Gi
Metrics (30d):
  cpu_usage    p50: 0.18  p95: 0.31  p99: 0.52
  memory_used  p50: 1.8Gi p95: 2.1Gi p99: 2.4Gi
Node pool: m5.2xlarge on-demand, ~$0.384/hr/instance
```

**Recommendation:**

```yaml
resources:
  requests:
    cpu: 500m       # was 2;   p95 × 1.3 ≈ 0.4, floor 500m
    memory: 3Gi     # was 4Gi; p99 × 1.25 = 3Gi
  limits:
    memory: 4Gi     # keep memory limit at 1.5x request (3Gi → 4Gi)
    # cpu limit removed
```

**Savings:** (2 - 0.5 cpu) × $0.0384/cpu-hr × 24 × 30 × 12 replicas = ~$497/mo
Plus memory: (4 - 3 GiB) × ~$0.0048/GiB-hr × 24 × 30 × 12 = ~$41/mo
**Total: ~$540/mo just on this deployment.**

### Example 2: Spot Migration For A Stateless Fleet

**Input:** EKS cluster, 60 nodes (m5.xlarge on-demand), 80% of workloads are stateless web/api.

**Plan:**

1. Install Karpenter, add a NodePool with `karpenter.sh/capacity-type: spot`, instance types `m5,m5a,m6i,m6a,m7g.xlarge` (mixed for availability).
2. Keep an on-demand pool sized to the **stateful baseline** (databases, message queues, single-replica services).
3. Apply node affinity on stateless deployments: prefer spot, fallback on-demand.
4. Set PDBs `maxUnavailable: 25%` on every spot-eligible deployment.
5. Roll out workloads to spot in three waves (frontend → mid-tier → workers).
6. Monitor `karpenter_nodes_terminated{reason="interrupted"}` — interruption rate target < 5%/day.

**Savings:** ~70% of compute on the stateless fleet × $0.192/hr m5.xlarge × 50 nodes × 24 × 30 = **~$4,840/mo savings**.

### Example 3: Idle Namespace Cleanup

**Audit output:**

```
Namespace        cpu_p95  mem_p95   age   last_apply  recommendation
---------------  -------  --------  ----  ----------  --------------
demo-2024-q3     0.01     45Mi      9mo   8mo ago     archive
sandbox-alice    0.00     12Mi      6mo   5mo ago     archive
hackathon        0.02     180Mi     14mo  13mo ago    archive
```

**Action:** tag, notify owners, archive after 14 days. Combined savings: full reclaim of ~6 nodes worth of allocation = ~$830/mo.

## Output

The agent produces:

- **Ranked recommendation list** — every C-type with $/month estimate, effort, risk
- **Per-recommendation YAML patch** — kubectl-apply-ready or Helm-values diff
- **Right-sizing report** — per-deployment requests/limits before/after
- **Node strategy plan** — Karpenter / spot / Graviton migration steps
- **Idle inventory** — namespaces, deployments, LBs, PVs flagged for cleanup
- **FinOps dashboard spec** — Grafana / Datadog panel definitions for ongoing tracking
- **4-week implementation plan** — daily checklist with safety gates
- **Cloud-specific notes** — EKS/GKE/AKS particulars relevant to this cluster
- **Pre-purchase commit plan** — Savings Plans / CUDs / Reservations sized to post-optimization baseline

## Common Scenarios

### "Our EKS bill jumped 40% this quarter"
The agent diffs current cluster against a baseline 90 days ago: new namespaces, new deployments, replica creep, node pool growth, log ingestion delta. Most jumps are one-off: a new team, a stuck rollout, a logging misconfig. Identify and reverse, then run the standard audit.

### "We can't move to spot because we have stateful workloads"
The agent splits the cluster: stateful pool stays on-demand (with reserved instances), stateless moves to spot. The mistake to avoid is one node pool serving both; taints and tolerations are mandatory.

### "Our requests look right but the bill is still high"
Probably nodes, not pods. Look at node utilization (`kubectl top nodes`); if average node utilization is below 50%, the cluster is over-provisioned at the node layer (binpacking failure or large pod requests blocking dense placement). Karpenter / cluster-autoscaler tuning beats per-pod right-sizing here.

### "Should I use VPA in auto mode?"
No, in most production clusters. VPA in auto mode restarts pods when it adjusts requests — that's a disruption budget hit on every change. Use `recommendationOnly` and apply manually, or use VPA with a long `targetRef` change budget.

### "Kubecost says one thing, AWS Cost Explorer says another"
Kubecost allocates *cluster cost to namespaces*; AWS bills *resources*. The deltas: cluster control-plane cost (in AWS but not Kubecost by default), cross-region egress, registry transfer, NAT gateway. Reconcile both before claiming savings.

## Tips For Best Results

- Provide at least 30 days of metrics — anything shorter misses the weekend pattern and over-rightsizes
- Share both `kubectl get all -A -o json` and a Prometheus snapshot — neither alone is enough
- State the cloud provider (EKS / GKE / AKS) and region — pricing varies materially
- Identify any workloads under SLAs or compliance constraints — those get conservative sizing margins
- Include the previous quarter's bill — flat-rate analysis misses growth-driven savings
- Mention any committed-spend agreements (EDP, GCP commitment, Azure MCA) — recommendations adjust to maximize commit utilization
- If running Kubecost or OpenCost, include its allocation export — the agent uses it directly instead of recomputing

## When NOT To Use

- **Brand-new cluster (< 30 days old)** — not enough data; metrics will mislead. Wait until the cluster has had a full month including a release cycle.
- **Single-tenant cluster running one workload at near 100% utilization** — already optimized; further savings are at the cloud-commit layer, not Kubernetes.
- **Non-Kubernetes workloads (ECS, Cloud Run, App Service)** — different scaling primitives and cost models; use a serverless cost optimizer instead.
- **Cluster with strict regulatory pinning** (FedRAMP, PCI-DSS regions, sovereign cloud) — instance type and region freedom is constrained; many recommendations don't apply.
- **Pre-production performance test environments** — these are intentionally over-provisioned; right-sizing them invalidates load-test results.
- **Clusters where the cost is dwarfed by other line items** (e.g. $2k/mo K8s vs $50k/mo data warehouse) — optimize the bigger line first.
