# Common Pitfalls & Solutions

This document contains detailed troubleshooting guides for common issues encountered when using the Huawei Cloud CCE Node Failure Diagnoser skill.

## Pitfall 1: Premature Kubelet Blame When Ready=Unknown

**Symptom**: Diagnosis concludes "kubelet failure" when `Ready=Unknown` and lease is stale, without independent kubelet/CRI evidence

**Root Cause**: `Ready=Unknown` + Lease renewal exceeding threshold only proves control plane lost connectivity to the node. The underlying cause could be network interruption, kubelet crash, or CRI failure — without node-side logs, it is impossible to determine which.

**Solution**: When `Ready=Unknown` + Lease stale, conclude "control plane disconnected from node (network link or Kubelet/CRI heartbeat interrupted, requires node-side verification)" rather than prematurely attributing to kubelet or network alone. Only attribute to a specific cause when independent strong evidence exists (e.g., `KubeletSetupFailed`, `ContainerRuntimeNotReady` events).

**Correct**:
- ✅ `Ready=Unknown` + Lease stale + no other evidence → "Control plane disconnected from node (requires node-side verification)"
- ✅ `Ready=Unknown` + Lease stale + `SystemOOM` event → "Memory pressure caused node instability"

**Incorrect**:
- ❌ `Ready=Unknown` + Lease stale → "Kubelet failure" (premature attribution without evidence)
- ❌ `Ready=Unknown` + Lease stale → "Network failure" (premature attribution without evidence)

## Pitfall 2: Marking Unknown Pressure Conditions as Normal

**Symptom**: Pressure conditions with `status=Unknown` and `reason=NodeStatusUnknown` are reported as "normal" or "healthy"

**Root Cause**: When kubelet stops reporting to the control plane (Ready=Unknown), all pressure conditions also become `Unknown` with reason `NodeStatusUnknown`. This only means kubelet stopped reporting — it does NOT mean MemoryPressure or DiskPressure are normal.

**Solution**: Label `Unknown` pressure conditions as "indeterminate" and note that no independent evidence is available:

- ✅ "MemoryPressure: Indeterminate — kubelet stopped reporting; no independent memory evidence available"
- ❌ "MemoryPressure: Normal" (incorrect — Unknown does not equal False/normal)

## Pitfall 3: Single Metric Spike as Root Cause

**Symptom**: A single CPU or memory peak is treated as the definitive root cause of node failure

**Root Cause**: AOM metrics are sampled periodically and a single peak may be a transient spike, not a sustained pressure condition. Without trend data, a single point cannot confirm root cause.

**Solution**: Use the `hours` parameter to gather metric trends over time:

```bash
python3 scripts/huawei-cloud.py huawei_node_failure_diagnose \
  region=cn-north-4 cluster_id=<cluster_id> \
  node_name=<node_name> hours=4 include_metrics=true
```

- ✅ Validate metric spikes with trend data over 1-4 hours
- ✅ Correlate metric trends with Event and Pod symptom evidence
- ❌ Treat a single CPU=95% reading as definitive root cause

## Pitfall 4: Skipping Event/Pod Correlation

**Symptom**: Conclusion formed based on node conditions alone without cross-referencing Event signals and Pod symptoms

**Root Cause**: Node conditions (Ready, MemoryPressure, etc.) are reported by kubelet and may be stale or incomplete. Events and Pod symptoms provide independent evidence that can confirm or contradict condition-based conclusions.

**Solution**: Always follow the workflow in `references/workflow.md`:

1. Check node conditions (liveness triage)
2. Review node events (strong signals)
3. Drill down into pod symptoms
4. Validate with metrics
5. Synthesize conclusion from ALL evidence

- ✅ MemoryPressure=True + SystemOOM Event + Pod OOMKilled → High confidence memory pressure
- ❌ MemoryPressure=True alone → Medium confidence; needs Event/Pod confirmation

## Pitfall 5: Executing Write Actions from This Skill

**Symptom**: Attempting to cordon, uncordon, drain, reboot, or modify vulnerability status directly from this diagnosis skill

**Root Cause**: This skill is designed for read-only diagnosis only. It produces evidence and recommendations but must not execute any write or recovery actions.

**Solution**: Hand off remediation to `huawei-cloud-cce-auto-remediation-runner`:

- ✅ Produce diagnosis report with remediation recommendations
- ✅ Hand off to `huawei-cloud-cce-auto-remediation-runner` for cordon/drain/reboot execution
- ✅ Require explicit user confirmation before any write action
- ❌ Directly execute `kubectl cordon` or `kubectl drain` from this skill

## Pitfall 6: Ignoring CNI Sandbox Failures

**Symptom**: Missing `FailedCreatePodSandBox` events and CNI error patterns in Pod events on the affected node

**Root Cause**: When network/CNI is failing on a node, new Pods stuck in `ContainerCreating` have Pod Events with `FailedCreatePodSandBox` and messages containing CNI/network plugin errors. These are strong network abnormality evidence that should not be overlooked.

**Solution**: Always check Pod events for CNI-related patterns:

- `FailedCreatePodSandBox` + message contains `CNI` → strong network evidence
- `network plugin returns error` → CNI plugin failure
- `timeout waiting for DHCP` → IP allocation failure
- Pods stuck in `ContainerCreating` on the node → possible network issue

## Pitfall 7: Missing Lease Check for NotReady Nodes

**Symptom**: Node NotReady diagnosis completed without checking kube-node-lease renewal evidence

**Root Cause**: Lease staleness is critical evidence for control plane connectivity. A stale lease (>40 seconds since last renewal) combined with `Ready=Unknown` is strong evidence that the control plane lost connection to the node.

**Solution**: Always include lease evidence in diagnosis:

- ✅ Use `huawei_node_failure_diagnose` which automatically checks lease
- ✅ In manual fallback, calculate lease renewal delay from `kube-node-lease/<node_name>` spec.renewTime
- ❌ Skip lease check and rely only on conditions and events

## Pitfall 8: Python Not Installed or Wrong Version

**Symptom**: Dispatcher script fails to execute or returns Python-related errors

**Root Cause**: Python >= 3.6 is required for the dispatcher script and Huawei Cloud SDK packages

**Solution**: Install Python and verify:

```bash
python3 --version
pip3 --version
pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkaom huawei-cloudsdkhss huaweicloudsdkvpc huaweicloudsdkecs huawei-cloudsdkces huawei-cloudsdkevs huawei-cloudsdkeip huawei-cloudsdkelb huawei-cloudsdkiam kubernetes
```

## Pitfall 9: Missing SDK Packages

**Symptom**: `ImportError` or `ModuleNotFoundError` when running the dispatcher script

**Root Cause**: Required Huawei Cloud SDK packages are not installed

**Solution**: Install all required packages:

```bash
pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkaom huawei-cloudsdkhss huawei-cloudsdkvpc huawei-cloudsdkecs huawei-cloudsdkces huawei-cloudsdkevs huawei-cloudsdkeip huawei-cloudsdkelb huawei-cloudsdkiam kubernetes
```

Verify installation:
```bash
pip3 list | grep huaweicloudsdk
```

## Pitfall 10: Wrong Cluster ID or Node Name

**Symptom**: Action returns "cluster not found" or "node not found" errors

**Root Cause**: Incorrect `cluster_id` or `node_name` parameter values

**Solution**: Verify cluster ID and node name before diagnosis:

```bash
python3 scripts/huawei-cloud.py huawei_list_cce_nodes region=cn-north-4 cluster_id=<cluster_id>
```

- ✅ Use cluster UUID from CCE console or ListClusters
- ✅ Use exact node name as shown in CCE console
- ❌ Guess cluster_id or node_name without verification

## Pitfall 11: Credential Not Set or Expired

**Symptom**: Actions return authentication errors (401/403)

**Root Cause**: `HUAWEI_AK` / `HUAWEI_SK` environment variables not set, or credentials expired/invalid

**Solution**: Set environment variables and verify with a read-only action:

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4

python3 scripts/huawei-cloud.py huawei_list_cce_nodes region=cn-north-4 cluster_id=<cluster_id>
```

🚫 Never use `echo $HUAWEI_AK` to verify credentials — use a read-only action instead.

## Pitfall 12: IAM Permission Insufficient

**Symptom**: Actions return 403 Forbidden errors despite valid credentials

**Root Cause**: IAM user lacks required permissions for CCE, AOM, HSS, or VPC services

**Solution**: Check IAM permissions using [IAM Permission Policies](iam-policies.md):

1. Read `references/iam-policies.md`
2. Display the required permission list and policy JSON to the user
3. Guide the user to create a custom policy in the IAM console
4. Pause execution and wait for user confirmation that permissions have been granted

## Common Error Response Reference

| Error Code | HTTP Status | Description | Recommended Action |
|-----------|-------------|-------------|-------------------|
| Auth failure | 401 | Invalid or expired credentials | Check AK/SK environment variables |
| Permission denied | 403 | IAM policy insufficient | See [iam-policies.md](iam-policies.md) |
| Cluster not found | 404 | Invalid cluster_id | Verify with `huawei_list_cce_nodes` |
| Node not found | 404 | Invalid node_name/node_ip | Verify node name in CCE console |
| Rate limited | 429 | Too many API calls | Add delay between invocations |
| SDK import error | N/A | Missing Python packages | Install SDK packages via pip3 |
| Python not found | N/A | Python not installed | Install Python >= 3.6 |