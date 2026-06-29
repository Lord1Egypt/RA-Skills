# Common Pitfalls & Solutions

This document contains detailed troubleshooting guides for common issues encountered when using the CCE Network Failure Diagnoser skill.

## Pitfall 1: Missing cluster_id Parameter

**Symptom**: Diagnosis action fails with missing or invalid cluster ID error

**Root Cause**: The `cluster_id` parameter is required for all CCE actions. If the user only provides a cluster name, the ID must be resolved first.

**Solution**: Provide `cluster_id` directly or set the `HW_CCE_CLUSTER_ID` environment variable. If only a cluster name is known, query `huawei_list_cce_clusters` first to resolve the ID.

```bash
# Set cluster ID via environment variable
export HW_CCE_CLUSTER_ID=<cluster-id>

# Or provide explicitly in command
python3 scripts/huawei-cloud.py huawei_network_failure_diagnose region=cn-north-4 cluster_id=<cluster-id> namespace=default
```

## Pitfall 2: Wrong failure_symptom Category

**Symptom**: Diagnosis pipeline misdirected to wrong stage, findings don't match user's actual problem

**Root Cause**: Using a wrong symptom category (e.g., `ingress_502_504` for an in-cluster Service unreachable issue) causes the pipeline to focus on north-south (Ingress/ELB) diagnosis when the real issue is east-west (Service/NetworkPolicy).

**Solution**: Always confirm the symptom type with the user before running diagnosis. Valid symptom values:

| Symptom Value | Diagnosis Focus |
|---------------|----------------|
| `domain_unresolvable` | DNS path (Stage 2) |
| `in_cluster_service_unreachable` | East-west Service/Policy (Stage 3) |
| `service_intermittent` | East-west with readiness flapping check |
| `external_access_failed` | North-south Ingress/ELB (Stage 4) |
| `ingress_502_504` | North-south Ingress Controller + ELB |

## Pitfall 3: Ignoring Node-Level Root Cause

**Symptom**: Upper-layer diagnosis shows Service/DNS anomalies, but the real root cause is node-level (NotReady, pressure)

**Root Cause**: If nodes are NotReady, upper-layer diagnosis may be pruned. The pipeline correctly prunes when node-level issues are detected, but users may try to skip node-layer check or misinterpret pruned results.

**Solution**: Do not skip the node-layer check even when the symptom appears to be Service/DNS-level. When `pipeline_pruned=true`, review node-level findings first and cross-reference with `huawei-cloud-cce-node-failure-diagnoser`.

## Pitfall 4: Confusing K8s-Side and Cloud-Side Unhealthy

**Symptom**: ELB backend shows unhealthy but K8s Pod is Ready, or vice versa

**Root Cause**: ELB backend unhealthy does not always mean the K8s Pod is unhealthy. The disconnect can be caused by:
- Cloud security group not allowing NodePort or health check port
- ELB health check port mismatch with K8s Service targetPort
- Node IPVS/Iptables/kube-proxy sync delay
- Different health check thresholds between ELB and K8s readiness probe

**Solution**: Always check both sides together:

```bash
# Check K8s-side Pod readiness
python3 scripts/huawei-cloud.py huawei_get_cce_pods region=cn-north-4 cluster_id=<cluster-id> namespace=default

# Check cloud-side ELB backend status
python3 scripts/huawei-cloud.py huawei_get_elb_backend_status region=cn-north-4 elb_id=<elb-id>
```

## Pitfall 5: Over-Interpreting Insufficient Evidence

**Symptom**: Diagnosis concludes "Service selector mismatch" or "backend crash" without checking Pod events and logs

**Root Cause**: When EndpointSlice has 0 ready endpoints, it could be selector mismatch, readiness flapping, or Pod crash. Jumping to a single conclusion without checking all evidence leads to incorrect diagnosis.

**Solution**: Always check Pod events and logs before concluding on endpoint issues:

```bash
# Check Pod events
python3 scripts/huawei-cloud.py huawei_get_cce_events region=cn-north-4 cluster_id=<cluster-id> namespace=default

# Check Pod logs
python3 scripts/huawei-cloud.py huawei_get_pod_logs region=cn-north-4 cluster_id=<cluster-id> namespace=default pod_name=<pod-name>
```

When evidence is insufficient, explicitly state "evidence insufficient" rather than presenting guesses as conclusions.

## Pitfall 6: Not Checking NetworkPolicy for East-West Issues

**Symptom**: In-cluster Service unreachable, diagnosis only checks Service/Endpoint but not NetworkPolicy

**Root Cause**: NetworkPolicy blocking has 100% confidence when confirmed, but is easily overlooked. Many clusters have default deny policies or restrictive policies that block inter-namespace traffic.

**Solution**: Always check NetworkPolicy in the target namespace for east-west Service issues:

```bash
# The one-shot diagnosis includes NetworkPolicy check automatically
python3 scripts/huawei-cloud.py huawei_network_failure_diagnose region=cn-north-4 cluster_id=<cluster-id> namespace=default failure_symptom=in_cluster_service_unreachable
```

If using individual actions, explicitly check NetworkPolicy objects in the namespace.

## Pitfall 7: Missing Cloud-Side Evidence for North-South Issues

**Symptom**: External access failure diagnosed with only K8s-side evidence, missing ELB/EIP/NAT/SecurityGroup configuration

**Root Cause**: North-south (external access) failures often involve cloud-side configuration (ELB health check, security group rules, EIP/NAT routing) that is invisible from K8s-side objects alone.

**Solution**: Always supplement north-south diagnosis with cloud-side evidence:

```bash
# Check ELB backend health
python3 scripts/huawei-cloud.py huawei_get_elb_backend_status region=cn-north-4 elb_id=<elb-id>

# Check security groups
python3 scripts/huawei-cloud.py huawei_list_security_groups region=cn-north-4

# Check EIP and NAT
python3 scripts/huawei-cloud.py huawei_list_eip region=cn-north-4
python3 scripts/huawei-cloud.py huawei_list_nat region=cn-north-4
```

## Pitfall 8: Environment Check Not Run Before Diagnosis

**Symptom**: Diagnosis commands fail with SDK import errors, dependency errors, or credential validation errors

**Root Cause**: The environment check script validates Python, dependencies, SDK, credentials, and service availability. Skipping it means undetected environment issues.

**Solution**: Always run the environment check script first:

```bash
# Linux / macOS
skill action=exec: bash skill://scripts/check_env.sh

# Windows
skill action=exec: powershell -ExecutionPolicy Bypass -File skill://scripts/check_env.ps1
```

## Common Error Reference

| Error | Cause | Resolution |
|-------|-------|------------|
| SDK import failure | Python dependencies not installed | Run environment check script or `pip install` dependencies |
| Credential validation failure | AK/SK not configured or invalid | Set `HW_ACCESS_KEY` and `HW_SECRET_KEY` environment variables |
| Cluster not found | Invalid `cluster_id` | Verify cluster ID with `huawei_list_cce_clusters` |
| Permission denied (IAM) | Insufficient IAM permissions | See `references/iam-policies.md` and create custom policy |
| Kubeconfig expired | CCE certificate expired | Re-obtain kubeconfig via CCE API (auto-handled by script) |