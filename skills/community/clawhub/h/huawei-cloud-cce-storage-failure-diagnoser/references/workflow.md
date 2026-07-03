# Workflow

## Reusable Capabilities and Gaps

The current repository already provides the following reusable capabilities:

- Kubernetes objects: `huawei_get_cce_pvcs`, `huawei_get_cce_pvs`, `huawei_get_cce_pods`, `huawei_get_kubernetes_nodes`, `huawei_get_cce_events`, `huawei_get_pod_logs`.
- Huawei Cloud storage: `huawei_list_evs`, `huawei_get_evs_metrics`, `huawei_list_sfs`, `huawei_list_sfs_turbo`.
- Network supplementary evidence: `huawei_list_security_groups`, `huawei_list_vpc_acls`, reusing the security group/ACL approach from `huawei-cloud-cce-network-failure-diagnoser`.
- Logging and reporting: Pod logs, AOM/LTS logs, and Markdown/HTML report-style diagnoser output patterns are already available.
- The external `huawei-cloud` skill also covers ECS/EVS/VPC/ELB/EIP/SFS, CCE Pod/PVC/PV/Event, Pod logs, AOM/LTS, network diagnosis, workload diagnosis, and full report generation. This skill reuses its read-only tools and the "collect evidence step-by-step, then output a complete report" workflow.

Atomic capabilities added by this skill:

- `huawei_get_cce_storageclasses`: Read StorageClass provisioner, parameters, and `volumeBindingMode`.
- `huawei_get_cce_volumeattachments`: Read VolumeAttachment `attached`, `attachError`, `detachError`.
- `huawei_get_cce_node_stats_summary`: Proxy-read node `/stats/summary` via API Server, parse PVC `usedBytes/capacityBytes` and inode.
- `huawei_get_cce_everest_csi_logs`: Read Everest CSI driver/controller log snippets in `kube-system`, auto-sanitized.
- `huawei_storage_failure_diagnose`: One-shot orchestration of PVC/PV/SC/Pod/Node/Event/VolumeAttachment/CSI logs/stats, producing structured findings and a Markdown report.

Capabilities still requiring manual intervention or future extension:

- Does not execute `kubectl exec`, node SSH, `dmesg`, local `fsck`, or active NFS/OBS connectivity probes.
- Does not directly call cloud-side detach/force-detach, modify IAM delegations, expand PVC, or delete finalizers.
- ConfigMap/Secret `resourceVersion` has no natural update timestamp; only `managedFields.time`, Pod timestamps, and FailedMount events can serve as circumstantial evidence.

## Input and Main Flow

Minimum input: `region`, `cluster_id`. Recommended additional parameters:

- `namespace`, `pvc_name`: Prioritize when PVC is Pending, Terminating, or capacity-exhausted.
- `pod_name`: Prioritize when Pod is Pending, ContainerCreating, or Running with I/O anomalies.
- `failure_symptom`: Examples: "PVC Pending", "FailedMount mount.nfs timeout", "OBS 403", "Read-only file system", "no space left on device", "PVC Terminating".

Main flow:

1. Call `huawei_storage_failure_diagnose` with defaults `include_stats=true`, `include_logs=true`, `include_cloud=false`.
2. If cloud-side supplementary evidence is needed, set `include_cloud=true`; this reads EVS/SFS/SFS Turbo and security group/ACL read-only information based on the matched storage type.
3. If the primary tool returns `report_markdown`, use that Markdown as the main output body; do not discard the evidence matrix.
4. If the primary tool fails, follow the four-stage manual fallback below.

## Stage 1: Provisioning Failures

Entry criteria: PVC `status=Pending`.

Common prerequisite:

- Read StorageClass `volumeBindingMode`.
- If `WaitForFirstConsumer` and no associated Pod, output "Normal behavior: awaiting Pod scheduling to trigger dynamic provisioning" with high confidence.

Branches:

- EVS: PVC event matches `FailedProvisioning` + `QuotaExceeded` -> EVS cloud disk quota insufficient.
- SFS/SFS Turbo: Event matches `Subnet IP insufficiency`, or provisioning failure returns `400/403` with text pointing to subnet/mount/IP -> VPC subnet available IP or mount target allocation issue.
- OBS: Event matches `BucketAlreadyExists` or `InvalidBucketName` -> Bucket name conflict or invalid naming.

## Stage 2: Scheduling and Binding Failures

Entry criteria: PVC `Bound`, associated Pod `Pending/Unschedulable`.

EVS:

- Read PV `spec.nodeAffinity`, typically reflecting a single AZ.
- Read Pod `nodeSelector`, tolerations, and FailedScheduling events.
- Query Ready node labels, taints, and scheduling events.
- If `volume node affinity conflict` appears, or no Ready nodes exist in the PV AZ, or all AZ nodes are blocked by intolerable taints/resource exhaustion, output "EVS single-AZ attribute prevents Pod from scheduling to the storage AZ".

Local:

- Read PV `nodeAffinity` bound node.
- If that node is `Ready=False/Unknown`, output "Local storage host node is down/offline" with highest confidence.

## Stage 3: Attach/Mount Failures

Entry criteria: Pod stuck in `ContainerCreating`, or events include `FailedAttachVolume`/`FailedMount`.

EVS:

- Filter VolumeAttachment by PV and target Node.
- VolumeAttachment does not exist: K8s control plane has not issued the attach instruction.
- `attached=false` and `attachError` matches max/limit/exceed: ECS per-node attached disk count upper limit.
- `attached=false` and `attachError` matches in-use/attached/lock/status: EVS occupied by residual node or underlying lock not released.
- `attached=true` but FailedMount: Cloud-side attach succeeded; enter host-side kernel/filesystem mount failure branch.

SFS/SFS Turbo:

- FailedMount text contains `mount.nfs` and `timed out`: Suspected network data-plane blocking.
- Output SFS endpoint, NetworkPolicy circumstantial evidence, and highlight need to check node security groups, SFS security groups, VPC ACL, and port 2049.

OBS:

- Read Everest CSI logs, combined with PV/event keywords.
- Matches `403 Forbidden`, `SignatureDoesNotMatch`, `failed to save temporary ak sk file`, `obsfs: ak size is invalid`, `fuse_opt_parse fail`: IAM delegation changed, AK/SK Secret invalid, Secret field/format error, or bucket permission anomaly.

Permission anomalies:

- When events show `permission denied`, `forbidden`, `access denied`, output as an independent permission candidate; OBS 403 should prioritize the OBS credential branch.

## Stage 4: Runtime and Teardown Anomalies

Capacity and inode:

- Parse PVC `usedBytes/capacityBytes` and `inodesUsed/inodes` from `/stats/summary`.
- Capacity usage > 95%: Capacity exhausted, highest confidence.
- Inode usage > 95%: Inode exhausted (too many small files), highest confidence.

Read-only filesystem:

- User symptom or event contains `Read-only file system`.
- If the same node has `DiskPressure`, `KernelOops`, or similar events, output "Host node triggered Linux read-only protection mechanism"; recommend migrating workloads and checking node underlying storage link.

ConfigMap/Secret subPath:

- Pod uses ConfigMap/Secret `subPath` mount.
- Subsequently `FailedMount`, `subPath`, `not a directory`, `stale file handle` events appear -> subPath mount point protection/deadlock issue.

PVC deletion protection:

- PVC has `deletionTimestamp` and finalizers include `kubernetes.io/pvc-protection`.
- Iterate all Pods; if any still reference the PVC, output "Deletion protection active: please delete residual Pods first" with highest confidence.

## Conclusion Synthesis

Conclusions are ranked by evidence strength, not by fixed stage priority:

1. Clear event/state fields directly pointing to cloud quota, bucket name, VolumeAttachment, capacity, or PVC protection: High confidence.
2. Scheduling events consistent with PV nodeAffinity/node labels: High confidence; resource-insufficiency text alone: Medium-high confidence.
3. NFS timeout, read-only filesystem, I/O errors: Typically medium confidence; requires cloud-side security group/node log supplementary evidence.
4. When no clear match exists, output evidence gaps; never write guesses as conclusions.