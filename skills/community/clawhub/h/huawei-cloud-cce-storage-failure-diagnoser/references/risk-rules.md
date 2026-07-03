# Risk Rules

- Auto-execution is allowed for read-only queries on PVC, PV, StorageClass, Pod, Node, Event, VolumeAttachment, NetworkPolicy, Kubelet `/stats/summary`, Everest CSI logs, EVS/SFS/SFS Turbo, security groups, and VPC ACLs.
- Allowed to generate Markdown diagnosis reports, read-only verification command suggestions, and recovery plans.
- Never delete PVC/PV/Pod, patch finalizers, force-detach/attach EVS, or modify StorageClass, StorageClass parameters, PV reclaim policy, IAM delegations, AK/SK Secrets, security groups, ACLs, or VPC routes.
- Never execute `kubectl exec`, node SSH, packet capture, stress testing, `fsck`, `dmesg` collection, or active NFS/OBS read/write probes unless the user explicitly requests and confirms the risk.
- Any action that changes the data plane or control plane must be handed off to `huawei-cloud-cce-auto-remediation-runner`, with impact scope, rollback method, data consistency risk, and verification standards output first.
- When PVC is Terminating, never directly suggest removing the `kubernetes.io/pvc-protection` finalizer; must first prove there are no Pod references and no business data risk.
- In EVS residual mount or read-only filesystem scenarios, never suggest force-unmount, force-attach, or direct restart of database-class workloads before confirming filesystem consistency.