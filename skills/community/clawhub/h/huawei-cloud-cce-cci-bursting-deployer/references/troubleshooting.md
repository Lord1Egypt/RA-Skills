# Troubleshooting

| Symptom | Likely cause | Action |
| --- | --- | --- |
| `bursting-cceaddon-*` Pods stay Pending or restart repeatedly | Physical nodes do not have enough headroom for the addon | Run `huawei_check_cce_cci_node_capacity`. Preview node pool expansion when the conservative warning baseline is not met. Use the official addon resource formula for production sizing. |
| `virtual-kubelet` components restart or the virtual node never becomes Ready | The addon received a VPC subnet UUID instead of the Neutron subnet UUID | Run precheck and pass `cci_subnet_id` from `spec.eni_network`. |
| CCI pod is `ImagePullBackOff` or times out while pulling an image | SWR, SWR API, or OBS-compatible VPCEP is missing, or the smoke image is from a public namespace that is not usable through the tenant VPCEP path | Run `huawei_ensure_cce_cci_vpcep`, verify endpoint status, then use `huawei_discover_cce_cci_smoke_images` and retry with a tenant-owned SWR image. |
| Docker Hub image pull times out | CCI capacity has no direct public path to Docker Hub | Use a regional SWR image for verification. |
| Workload pods stay Pending and mention a `virtual-kubelet.io/provider` taint | The workload is not using the CCI bursting scheduling profile | Use the smoke action or add `bursting.cci.io/burst-to-cci: enforce` to the workload template labels. |
| OBS gateway endpoint creation fails | The OBS service name does not match the tenant or region setup | Obtain the exact `obs_endpoint_service_name` through the Huawei Cloud service ticket. |
| Addon log reports a region mismatch such as `northchina` or `southchina` | The installed addon version or site-specific parameters expect a different region representation | Run `huawei_diagnose_cce_cci_bursting_addon`. Verify the installed addon version and its supported configuration. Do not apply a hard-coded mapping automatically. |
| Addon log reports missing project ID or IAM denied | The regional project ID is missing or the CCI bursting agency permissions are incomplete | Check the `project_id` shown in setup preview. Pass `project_id` explicitly when IAM auto-resolution is unavailable and verify the agency permissions. |
| No virtual node appears and `bursting-status` reports `enableBurstingNode=false` | The installed addon is not enabling the global bursting node | Run `huawei_diagnose_cce_cci_bursting_addon`. Treat the ConfigMap as diagnostic evidence and use the vendor-supported addon configuration path; do not patch the internal ConfigMap automatically. |
| Multiple active `bursting-cceaddon-*` ReplicaSets appear | An addon rollout may be incomplete or abnormal | Inspect the owning Deployment and rollout state. Do not automatically delete ReplicaSets because inactive ReplicaSets are normal rollback history. |
