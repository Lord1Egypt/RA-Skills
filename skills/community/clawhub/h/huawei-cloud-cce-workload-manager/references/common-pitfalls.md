# Common Pitfalls & Solutions

This document contains detailed troubleshooting guides for common issues encountered when using the Huawei Cloud CCE Workload Manager skill.

## Pitfall 1: kubectl Not Installed

**Symptom**: `kubectl` command not found or fails with command not recognized

**Root Cause**: kubectl is not installed on the system

**Solution**: Install kubectl first, then verify:

```bash
kubectl version --client
```

If not installed, download and install from the official Kubernetes release page or use package manager. After installation, verify with `kubectl version --client`.

## Pitfall 2: CCE Cluster ID Format Incorrect

**Symptom**: `CreateKubernetesClusterCert` or `ShowCluster` fails with cluster not found error

**Root Cause**: The `--cluster_id` must be a valid CCE cluster UUID, not a cluster name or arbitrary string

**Solution**: Find the correct cluster UUID using `ListClusters`:

```bash
hcloud CCE ListClusters --project_id=<project-id> --cli-region=<region>
```

Use the `id` field from the response as `--cluster_id`. CCE cluster IDs are UUIDs like `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.

## Pitfall 3: UCS --clusterid vs CCE --cluster_id Confusion

**Symptom**: Commands fail with "unknown parameter" or parameter validation errors

**Root Cause**: CCE hcloud CLI uses `--cluster_id` (with underscore), UCS hcloud CLI uses `--clusterid` (no underscore)

**Common Mistakes**:
- ❌ Using `--clusterid=<id>` for CCE operations (UCS style)
- ✅ Using `--cluster_id=<id>` for CCE operations (correct)
- ❌ Using `--cluster_id=<id>` for UCS operations (CCE style)
- ✅ Using `--clusterid=<id>` for UCS operations (correct)

**Affected CCE Operations**: `CreateKubernetesClusterCert`, `ShowCluster`, `ShowClusterEndpoints`, `DeleteCluster`
**Affected UCS Operations**: `DownloadFederationKubeconfig`, `ListClusterGroup`, `ShowClusterGroup`

## Pitfall 13: UCS Federation API DNS Unreachable

**Symptom**: `kubectl cluster-info` with UCS federation kubeconfig returns `dial tcp: lookup <fleet>.fleet.ucs.<region>.myhuaweicloud.com: no such host`

**Root Cause**: UCS federation API server domain requires access via VPC Endpoint (VPCEP). The DNS record only resolves within Huawei Cloud VPC network or through VPCEP configuration.

**Solution**: Ensure network access to the UCS federation VPCEP:

- Run from within a Huawei Cloud VPC (ECS, Cloud Desktop)
- Use VPN to connect to Huawei Cloud VPC
- Configure VPC peering with the UCS fleet's VPC

The VPCEP endpoint ID can be found via `hcloud UCS ShowClusterGroup` in `spec.connectGatewayEndpoints`.

```bash
# Find the VPCEP endpoint
hcloud UCS ShowClusterGroup --clustergroupid=<fleet-id>

# Look for connectGatewayEndpoints in the output
# Example: type=VPCEP, id=<vpcep-id>, region=cn-north-4
```

## Pitfall 4: Kubeconfig Expired

**Symptom**: Previously obtained kubeconfig no longer works — kubectl commands return authentication errors

**Root Cause**: Kubeconfig tokens have expiration periods (default varies, configurable via `--duration`)

**Solution**: Re-create the kubeconfig with a valid duration:

```bash
hcloud CCE CreateKubernetesClusterCert --cluster_id=<cce-cluster-id> --project_id=<project-id> --duration=30 --cli-region=<region>
```

For UCS-managed clusters:

```bash
hcloud UCS CreateClusterKubeconfig --clusterid=<ucs-cluster-id> --cli-region=cn-north-4
```

**Duration Limits**:
- CCE: `--duration` accepts 1-1827 days
- UCS Federation: `--duration` is in days (1-1825)

## Pitfall 5: Wrong Namespace

**Symptom**: `kubectl get pods` returns empty or unexpected results

**Root Cause**: Operating in the default namespace instead of the intended namespace. The default namespace may be empty or contain unrelated resources.

**Solution**: Always specify `-n <namespace>` with kubectl commands:

```bash
kubectl --kubeconfig=<f> get pods -n production
```

❌ **WRONG** — Missing namespace (operates in `default`):

```bash
kubectl --kubeconfig=<f> get pods
```

✅ **Correct** — Always specify namespace:

```bash
kubectl --kubeconfig=<f> get pods -n production
```

## Pitfall 6: RBAC Insufficient Permissions

**Symptom**: kubectl commands return `Forbidden` or `Error from server (Forbidden)` errors

**Root Cause**: The kubeconfig user does not have sufficient RBAC permissions for the requested operation

**Solution**: Check current permissions:

```bash
kubectl --kubeconfig=<f> auth can-i <verb> <resource> -n <namespace>

kubectl --kubeconfig=<f> auth can-i create deployments -n prod

kubectl --kubeconfig=<f> auth can-i delete pods -n staging
```

If permissions are insufficient, create appropriate RBAC bindings:

```bash
kubectl --kubeconfig=<f> create rolebinding <name> --role=<role> --user=<user> -n <namespace>

kubectl --kubeconfig=<f> create clusterrolebinding <name> --clusterrole=<role> --user=<user>
```

## Pitfall 7: Pod in CrashLoopBackOff

**Symptom**: Pod repeatedly crashes and restarts, status shows `CrashLoopBackOff`

**Root Cause**: Application inside the container is failing to start or crashing after startup

**Solution**: Check previous container logs to find the crash reason:

```bash
kubectl --kubeconfig=<f> logs <pod-name> --previous -n <namespace>

kubectl --kubeconfig=<f> describe pod <pod-name> -n <namespace>
```

Common causes:
- Application exits immediately (check `--previous` logs)
- Missing configuration or environment variables
- Failed health check (liveness probe)
- Insufficient resources (OOMKilled)

## Pitfall 8: Image Pull Failed

**Symptom**: Pod status shows `ImagePullBackOff` or `ErrImagePull`

**Root Cause**: Container image cannot be pulled from the registry

**Solution**: Check image pull secrets and verify image path:

```bash
kubectl --kubeconfig=<f> get secrets -n <namespace>

kubectl --kubeconfig=<f> describe pod <pod-name> -n <namespace>
```

Common causes:
- ❌ Missing image pull secret for private registry
- ❌ Incorrect image path or tag
- ❌ Network issues preventing registry access
- ❌ Image does not exist in the specified registry

For private registries, create a secret:

```bash
kubectl --kubeconfig=<f> create secret docker-registry <secret-name> --docker-server=<registry> --docker-username=<user> --docker-password=<password> -n <namespace>
```

## Pitfall 9: PVC Stuck Pending

**Symptom**: PersistentVolumeClaim status remains `Pending` and never binds to a PV

**Root Cause**: No suitable PersistentVolume available or StorageClass configuration issue

**Solution**: Check storage class and PV availability:

```bash
kubectl --kubeconfig=<f> get sc

kubectl --kubeconfig=<f> get pv

kubectl --kubeconfig=<f> describe pvc <pvc-name> -n <namespace>
```

Common causes:
- ❌ StorageClass not found or not configured (CCE uses `csi-disk`, NOT `cce-standard`)
- ❌ No available PV with matching size or access mode
- ❌ Dynamic provisioner not running or not configured
- ❌ Volume quota exceeded in namespace

**CCE StorageClass Names**: Use `csi-disk` for block storage, `csi-sfsturbo` for shared high-performance file storage (500Gi minimum, supports subdirectory creation for cost savings), `csi-obs` for object storage mount, `csi-nas` for general shared file storage. Run `kubectl get sc` to list all available StorageClasses. `cce-standard` is NOT a valid CCE StorageClass.

Reference: [CCE Storage Best Practices](https://support.huaweicloud.com/usermanual-cce/cce_10_0900.html)

## Pitfall 10: Deployment Rollout Stuck

**Symptom**: Deployment rollout does not complete, pods remain in old or transitional state

**Root Cause**: New pods cannot start, or rollout is waiting for conditions that never resolve

**Solution**: Check rollout status and deployment details:

```bash
kubectl --kubeconfig=<f> rollout status deployment/<name> -n <namespace>

kubectl --kubeconfig=<f> describe deployment <name> -n <namespace>

kubectl --kubeconfig=<f> get pods -n <namespace> -o wide
```

Common causes:
- ❌ New ReplicaSet pods failing to start (CrashLoopBackOff, ImagePullBackOff)
- ❌ Insufficient resources to schedule new pods (Pending pods)
- ❌ Readiness probe not passing for new pods
- ❌ MaxUnavailable or maxSurge strategy blocking progress

To undo a failed rollout:

```bash
kubectl --kubeconfig=<f> rollout undo deployment/<name> -n <namespace>
```

## Pitfall 11: Metrics API Not Available

**Symptom**: `kubectl top pods` or `kubectl top nodes` returns `error: Metrics API not available`

**Root Cause**: The metrics-server addon is not installed in the CCE cluster

**Solution**: Install the metrics-server addon via CCE console or hcloud CLI:

```bash
# Check addon availability
hcloud CCE ShowAddonInstance --cluster_id=<cluster-id> --addon_id=metrics-server

# Install via CCE console (recommended) or hcloud CCE InstallAddon
```

After installation, verify:

```bash
kubectl --kubeconfig=<f> top pods -n <namespace>
kubectl --kubeconfig=<f> top nodes
```

## Pitfall 12: PowerShell JSON Patch Escaping

**Symptom**: `kubectl patch` with `-p` JSON fails on Windows PowerShell with escaping errors

**Root Cause**: PowerShell interprets single quotes differently from bash, and double-quoted JSON gets mangled by PowerShell escape rules

**Solution**: Use `--patch-file` instead of inline `-p`:

```bash
# Create patch file
echo '{"spec":{"suspend":true}}' > patch.json

# Apply patch from file
kubectl --kubeconfig=<f> patch cronjob <name> --type merge --patch-file=patch.json -n <namespace>
```

On Linux/macOS bash, inline `-p` works normally:

```bash
kubectl --kubeconfig=<f> patch cronjob <name> -p '{"spec":{"suspend":true}}' -n <namespace>
```

| Error Code          | HTTP Status | Description                  | Recommended Action                    |
| ------------------- | ----------- | ---------------------------- | ------------------------------------- |
| `CCE.001`           | 400         | Invalid parameter            | Check parameter format and rules      |
| `CCE.002`           | 404         | Cluster not found            | Verify cluster_id with ListClusters   |
| `CCE.003`           | 400         | Cluster status unavailable   | Check cluster status with ShowCluster |
| `CCE.004`           | 403         | Permission denied            | Check IAM policies                    |
| `CCE.005`           | 403         | Quota exceeded               | Check quotas, clean up or apply       |
| `CCE.006`           | 401         | Authentication failed        | Regenerate or check credentials       |
| `CCE.007`           | 429         | Too many requests            | Add delay, reduce request rate        |
| `UCS.001`           | 400         | Invalid UCS parameter        | UCS uses --clusterid (no underscore)  |
| `UCS.002`           | 404         | UCS resource not found       | Verify UCS resource exists first      |
| `UCS.004`           | 403         | UCS permission denied        | Check IAM policies                    |
| `Forbidden (RBAC)`  | 403         | kubectl RBAC insufficient    | Check with kubectl auth can-i         |
| `ConnectionRefused` | N/A         | API server unreachable       | Verify network connectivity           |