# CCE to CCI 2.0 Bursting Workflow

## Action sequence

| Step | Action | Mutation | Purpose |
| --- | --- | --- | --- |
| 1 | `huawei_precheck_cce_cci_bursting` | No | Resolve cluster networking, subnet roles, and addon state. |
| 2 | `huawei_check_cce_cci_node_capacity` | No | Inspect physical-node addon headroom. Preview node pool expansion when the conservative warning baseline is not met. |
| 3 | `huawei_ensure_cce_cci_vpcep` | Only with `confirm=true` | Reuse or create SWR, SWR API, and OBS-compatible VPCEPs. |
| 4 | `huawei_setup_cce_cci_bursting` | Only with `confirm=true` | Ensure VPCEPs, install `virtual-kubelet` if absent, and apply CCI network and project parameters. |
| 5 | `huawei_verify_cce_cci_bursting` | No | Verify addon state, virtual node readiness, and optional workload result. Failed verification includes read-only addon diagnostics. |
| 6 | `huawei_discover_cce_cci_smoke_images` | No | Discover tenant-owned SWR basic images through namespace, repository, and tag queries. |
| 7 | `huawei_deploy_cce_cci_smoke_workload` | Only with `confirm=true` | Create or patch a small Deployment forced to CCI capacity. Omit `image` to prefer a tenant-owned SWR image. |
| 8 | `huawei_verify_cce_cci_bursting` | No | Confirm test pods reach `Running` on `bursting-node` or `virtual-kubelet`. |

## Physical node headroom

`huawei_precheck_cce_cci_bursting` includes NodeCheck automatically.
For a small validation cluster, the action warns when it cannot find
a schedulable physical node with at least 2 vCPU and 4 GiB of
currently unrequested capacity, or when fewer than two schedulable
physical nodes are available.

The 2C/4GiB value is a conservative warning baseline, not a platform
hard limit. Size production addon resources with the official formula
and the expected number of synchronized resources and concurrent
requests.

When NodeCheck warns:

1. Run `huawei_list_cce_nodepools`.
2. Preview `huawei_resize_cce_nodepool` for an existing pool, or preview `huawei_create_cce_nodepool` for a new pool.
3. Prefer SSH keypair authentication for a new node pool. The existing cluster-management action also supports password mode and performs SHA-512 salted encryption plus base64 encoding automatically.
4. Apply the selected capacity change only after explicit user approval, then rerun precheck.

## Subnet roles

| Parameter | ID type | Used by |
| --- | --- | --- |
| `cci_subnet_id` | Neutron subnet UUID | `virtual-kubelet` addon `networkID`, `subnet_id`, and `subnets[].subnetID` |
| `vpcep_subnet_id` | VPC subnet UUID | VPCEP interface endpoint placement |

For a Turbo/ENI cluster, `huawei_precheck_cce_cci_bursting` normally resolves `cci_subnet_id` from `spec.eni_network`. Pass `vpcep_subnet_id` explicitly when a larger or dedicated endpoint subnet is preferred.

## Examples

Preview:

```powershell
python scripts/huawei-cloud.py huawei_precheck_cce_cci_bursting region=cn-north-4 cluster_id=<cluster-id> vpcep_subnet_id=<vpc-subnet-id>
python scripts/huawei-cloud.py huawei_setup_cce_cci_bursting region=cn-north-4 cluster_id=<cluster-id> vpcep_subnet_id=<vpc-subnet-id>
```

Apply after approval:

```powershell
python scripts/huawei-cloud.py huawei_setup_cce_cci_bursting region=cn-north-4 cluster_id=<cluster-id> vpcep_subnet_id=<vpc-subnet-id> confirm=true
python scripts/huawei-cloud.py huawei_deploy_cce_cci_smoke_workload region=cn-north-4 cluster_id=<cluster-id> replicas=2 confirm=true
python scripts/huawei-cloud.py huawei_verify_cce_cci_bursting region=cn-north-4 cluster_id=<cluster-id> namespace=cci2-burst-lab workload_name=cci2-burst-demo
```

If the precheck reports that OBS information is missing, obtain the exact service name through the Huawei Cloud service ticket and pass:

```powershell
obs_endpoint_service_name=<exact-service-name> route_table_ids=<route-table-id>
```

## Project ID

The setup action resolves the regional Huawei Cloud project ID from
the environment or IAM API and writes it to the addon values. Pass
`project_id=<regional-project-id>` explicitly when IAM
auto-resolution is unavailable.

## Smoke image selection

The smoke workflow prefers a tenant-owned SWR basic image because CCI image pulling through VPCEP may not work for public namespaces.

```powershell
python scripts/huawei-cloud.py huawei_discover_cce_cci_smoke_images region=cn-north-4
python scripts/huawei-cloud.py huawei_deploy_cce_cci_smoke_workload region=cn-north-4 cluster_id=<cluster-id> replicas=2 confirm=true
```

The discovery action follows this fixed basic-edition sequence:

1. `ListNamespaces`
2. `ListReposDetails --namespace=<tenant-namespace>`
3. `ListRepositoryTags --namespace=<tenant-namespace> --repository=<repository>`

Do not substitute SWR enterprise-instance APIs unless the target image is intentionally stored in an enterprise instance.

Official references:

- [CCI 2.0 environment configuration](https://support.huaweicloud.com/intl/zh-cn/usermanual-cci2/cci_01_0024.html)
- [CCI 2.0 cloud bursting setup](https://support.huaweicloud.com/intl/zh-cn/usermanual-cci2/cci_01_0025.html)
- [CCE cloud native hybrid deployment addon](https://support.huaweicloud.com/usermanual-cce/cce_10_0135.html)
- [CCI image pulling FAQ](https://support.huaweicloud.com/intl/en-us/cci_faq/cci_faq_0095.html)
