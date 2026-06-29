# Upgrade Window Estimation

## Estimation Formula

```
T_total = T_control_plane + T_node_batches + T_addons + T_verify + T_buffer

T_control_plane = 10-30 min (control node count and etcd data size dependent)
T_node_batches = Σ(batch_i * T_per_node_in_batch)
T_addons = Σ(addon_j * T_per_addon)
T_verify = 30 min (cluster + node + addon + business verification)
T_buffer = 20% * (T_control_plane + T_node_batches + T_addons + T_verify)
```

## Node Upgrade Batch Strategy

### Batch Size and Progression

Node upgrade uses an exponential batch strategy:

```
Batch 1: 1 node (canary test)
Batch 2: 4 nodes
Batch 3+: max_batch_size nodes per batch (default 20, configurable 1-40)
```

**Batch scope**: `Cluster` (all node pools share batch counter) or `NodePool` (each pool has independent batch counter)

### Per-Node Upgrade Time

| Factor | Time | Description |
|--------|------|-------------|
| Base time | 5-15 min | Drain → upgrade components → uncordon → verify Ready |
| OS upgrade | +10-30 min | If node OS needs upgrade (e.g., EulerOS patch) |
| Runtime switch | +15-25 min | Docker → Containerd runtime migration |
| Large image count | +5-10 min | If node has >1000 images, drain takes longer |
| Certificate rotation | +3-5 min | If >1000 certificates on node |

**Typical per-node time**: 8-12 minutes for in-place upgrade without OS/runtime change.

### Control Plane Upgrade Time

| Cluster Size | Estimated Time | Notes |
|--------------|---------------|-------|
| Small (≤3 nodes) | 10-15 min | Few etcd entries, fast API server restart |
| Medium (3-10 nodes) | 15-20 min | More etcd data, longer component restart |
| Large (10+ nodes) | 20-30 min | Large etcd dataset, extended upgrade process |

### Addon Upgrade Time

| Addon Type | Time per Addon | Notes |
|------------|----------------|-------|
| Core addons (CoreDNS, Metrics) | 5-8 min | Quick version bump |
| CSI drivers (Everest) | 8-12 min | Needs storage reconciliation |
| Ingress controllers | 10-15 min | ELB configuration updates |
| DaemonSet plugins | 5-10 min | Rolling update across all nodes |

### Verification Time

| Verification Type | Time | Description |
|-------------------|------|-------------|
| Cluster status | 5 min | ShowCluster status.phase=Available |
| Node status | 10 min | All nodes Ready, no NotReady |
| Addon status | 5 min | All addons running |
| Business verification | 10 min | Pod health, Service connectivity, DNS resolution |
| New node scheduling | 5 min | Test Pod creation on upgraded nodes |

## Estimation Examples

### Example 1: Small Cluster (3 nodes, 3 addons) v1.23→v1.25

```
T_control_plane = 15 min (small cluster)
T_node_batches = (1*8 + 2*8) = 16 min  [Batch1: 1node, Batch2: 2nodes]
T_addons = 3 * 8 min = 24 min
T_verify = 30 min
T_buffer = 20% * (15+16+24+30) = 17 min
T_total = 15+16+24+30+17 = 102 min ≈ 1h 42min
```

### Example 2: Medium Cluster (10 nodes, 5 addons) v1.21→v1.23

```
T_control_plane = 20 min (medium cluster)
T_node_batches = (1*10 + 4*10 + 5*10) = 100 min  [Batch1: 1node, Batch2: 4nodes, Batch3: 5nodes]
T_addons = 5 * 10 min = 50 min
T_verify = 30 min
T_buffer = 20% * (20+100+50+30) = 40 min
T_total = 20+100+50+30+40 = 240 min = 4h
```

### Example 3: Large Cluster (30 nodes, 8 addons) v1.25→v1.27

```
T_control_plane = 25 min (large cluster)
T_node_batches = (1*12 + 4*12 + 20*12 + 5*12) = 360 min  [Batch1: 1node, Batch2: 4nodes, Batch3: 20nodes, Batch4: 5nodes]
  Note: Batch4 has only 5 nodes because 1+4+20=25 out of 30 total
T_addons = 8 * 12 min = 96 min
T_verify = 30 min
T_buffer = 20% * (25+360+96+30) = 102 min
T_total = 25+360+96+30+102 = 613 min ≈ 10h 13min
```

### Example 4: Multi-Hop Upgrade v1.19→v1.28 (4 hops)

```
Each hop = full upgrade cycle (pre-check → upgrade → verify)

Hop 1: v1.19→v1.21  T = ~2h (10 nodes, 4 addons)
Hop 2: v1.21→v1.23  T = ~2h
Hop 3: v1.23→v1.25  T = ~2h
Hop 4: v1.25→v1.27→v1.28  T = ~4h (v1.25→v1.27 needs Docker→Containerd check)

Total = 10h+ (with 20% buffer per hop = 12h+)
```

## Buffer Recommendations

| Scenario | Buffer % | Reason |
|----------|----------|--------|
| First-time upgrade | 30% | Unknown environment, higher risk |
| Repeat upgrade (similar cluster) | 20% | Known baseline, moderate risk |
| Patch-only upgrade | 10% | Low risk, minimal changes |
| Emergency upgrade | 50% | High pressure, unexpected issues likely |

## Window Scheduling Recommendations

1. **Start time**: Begin 2 hours before business low-traffic period
2. **End time**: Ensure upgrade completes before business high-traffic period starts
3. **Communication**: Notify stakeholders of expected duration and potential impact
4. **Contingency**: If upgrade takes longer than estimated, have rollback plan ready
5. **Monitoring**: Real-time monitoring during upgrade (ShowUpgradeWorkFlow every 5-10 min)