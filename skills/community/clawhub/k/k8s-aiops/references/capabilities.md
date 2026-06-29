# k8s-aiops Capabilities

51 MCP tools (37 read / 14 write). Every tool is wrapped with `@governed_tool`
(audit + policy + budget + risk-tier; undo where a clean inverse exists). Returns
are high-signal summaries — `_get` / `_describe` tools add detail for a single object.

## Read tools

| Tool | Returns | Risk |
|------|---------|:----:|
| `pod_list` | name, namespace, phase, ready, restarts, node, age | low |
| `pod_get` | + host_ip, pod_ip, containers | low |
| `pod_describe` | status, conditions, container states + restart counts, recent events | low |
| `pod_logs` | trailing log lines (default 100) | low |
| `deployment_list` / `deployment_get` | replicas summary / + strategy, images | low |
| `rollout_status` | desired/updated/available/unavailable + paused | low |
| `rollout_history` | revisions (from replicasets) with images | low |
| `statefulset_list` / `statefulset_get` | desired/ready/current / + service, images | low |
| `daemonset_list` / `daemonset_get` | desired/ready/available / + images | low |
| `replicaset_list` | name, namespace, desired/ready, age | low |
| `job_list` / `job_get` | completions, succeeded/failed/active | low |
| `cronjob_list` / `cronjob_get` | schedule, suspend, active, last schedule | low |
| `service_list` | name, namespace, type, cluster IP, ports | low |
| `ingress_list` / `ingress_get` | class, hosts / + path→backend rules | low |
| `endpoints_list` | ready addresses + ports | low |
| `configmap_list` / `configmap_get` | key count / keys + values | low |
| `secret_list` | names, types, key NAMES only (values redacted) | low |
| `pvc_list` / `pvc_get` | status, capacity, class / + access modes | low |
| `pv_list` | capacity, status, claim, class | low |
| `storageclass_list` | provisioner, reclaim policy, default | low |
| `node_list` / `node_describe` | status, roles / capacity, allocatable, conditions, taints | low |
| `namespace_list` | name, phase, age | low |
| `pod_top` / `node_top` | CPU/mem via metrics-server (graceful if absent) | low |
| `cluster_info` | server version, node/ready/namespace counts | low |
| `api_resources` | available API groups + versions | low |
| `event_list` | type, reason, object, namespace, message, age | low |

## Write tools

| Tool | Effect | Risk | Undo |
|------|--------|:----:|------|
| `scale_deployment` | set replica count | medium | scale back to `previous_replicas` |
| `scale_statefulset` | set replica count | medium | scale back to `previous_replicas` |
| `rollout_restart_deployment` | patch `restartedAt` annotation | medium | none (pods already rolling) |
| `rollout_pause` / `rollout_resume` | toggle `spec.paused` | medium | each other |
| `rollout_undo_deployment` | roll back to a prior revision | **high** | none |
| `set_deployment_image` | update a container image | medium | restore `previous_image` |
| `delete_pod` | delete a pod | medium | none (controller recreates) |
| `delete_deployment` | delete deployment + pods | **high** | none |
| `delete_job` | delete a job + pods | **high** | none |
| `create_namespace` | create a namespace | medium | `delete_namespace` |
| `delete_namespace` | delete namespace + everything in it | **high** | none |
| `cordon_node` / `uncordon_node` | toggle schedulability | medium | each other |
| `drain_node` | cordon + evict pods (skips DaemonSet/mirror) | **high** | partial: `uncordon_node` |

## Token-budget notes

- List tools accept a `namespace` filter to keep responses small; events and pod
  listings also accept `limit` / `label_selector` where applicable.
- Prefer `pod_get` / `deployment_get` over re-listing when you already have a name.
- The runaway guard trips on tight poll loops — wait between repeated list calls.

## Design notes / Kubernetes-client assumptions

- Authentication is delegated to the kubeconfig; the skill never touches raw
  credentials (works with client certs, tokens, and EKS/GKE/AKS exec plugins).
- Typed Api clients (`CoreV1Api`, `AppsV1Api`, `BatchV1Api`, `NetworkingV1Api`,
  `StorageV1Api`, `CustomObjectsApi`, `ApisApi`, `VersionApi`) are cached per kube
  context in a module dict — third-party client objects are never monkey-patched.
- `secret_list` reads only key NAMES from `secret.data` — secret values are never
  read, returned, or logged, and no tool exposes them.
- `pod_top` / `node_top` use the `metrics.k8s.io/v1beta1` API; when metrics-server
  is absent the 404/503 is caught and returned as `{available: false, message}`.
- `ApiException` is translated centrally at the connection layer into a teaching
  `K8sApiError` (404/403/409/5xx), so agents see actionable messages, not tracebacks.
