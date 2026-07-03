# Pressure-Test Workflow

## 1. Scope and Preconditions

Confirm the cluster, workload, namespace, container target port, ingress controller, ELB, traffic model, VUs, duration, and output directory. Start with a low-traffic baseline.

The standard route is:

`pod -> service -> nginx-ingress -> elb`

`huawei_prepare_cce_pressure_test_route` creates or patches only the
workload-facing ClusterIP Service and Ingress. It discovers an existing
nginx ingress controller LoadBalancer address. It does not silently create
a chargeable ELB. For a non-Deployment workload, pass `selector_json`
explicitly.

If no reusable ELB exists, inspect candidate subnets with `huawei_list_vpc_subnets`, then preview:

```text
huawei_create_elb
region=cn-north-4
name=<elb-name>
vip_subnet_cidr_id=<elb-vip-subnet-network-id>
availability_zone_list=<az1,az2>
l4_flavor_id=<optional-l4-flavor-id>
l7_flavor_id=<optional-l7-flavor-id>
```

Review the billable resource fields and apply only after explicit approval with `confirm=true`. The action does not create an EIP automatically.

## 2. Route Preparation

For a clean Java lab, preview `huawei_deploy_cce_pressure_test_java_sample`,
then apply it with `confirm=true`. The action creates an isolated Namespace,
a ConfigMap containing a small Java HTTP server, and a Deployment with
readiness and liveness probes. It exposes `/healthz`, `/api/hello`,
and `/api/work` on port `8080`.

Preview:

```text
huawei_prepare_cce_pressure_test_route
region=cn-north-4
cluster_id=<cluster-id>
namespace=<business-namespace>
workload_name=<deployment-name>
target_port=8080
```

Apply only after approval:

```text
confirm=true
```

If the Ingress uses a host rule, pass `host` during route preparation and pass the same value as `host_header` when generating or running the client.

## 3. Client Preparation

Generate the k6 manifest before creating any Job:

```text
huawei_generate_cce_pressure_test_client
target_url=http://<elb-address>/<path>
namespace=pressure-test
model=keepalive
vus=10
duration_seconds=60
```

Supported models:

| Model | Purpose |
| --- | --- |
| `short` | Disable connection reuse and observe new connection pressure. |
| `keepalive` | Reuse connections for a steady HTTP baseline. |
| `ramp` | Increase traffic in stages and then scale down. |

## 4. Traffic Run

Preview `huawei_run_cce_pressure_test`, then apply with `confirm=true`.
The action ensures the client namespace exists, creates a ConfigMap and Job,
waits by default, records desired replicas, ready replicas, and running pods,
and extracts the compact k6 summary from logs.

## 5. Observability

Run `huawei_collect_cce_pressure_test_observability` after each phase. Pass:

- `elb_id` for ELB QPS, active connections, layer-7 response time, and 2xx ratio.
- `label_selector` to keep Pod metrics scoped to the workload.
- Pod CPU and memory are collected from node metrics when `aom_instance_id` is not provided.

## 6. Elasticity Evaluation

Run at least two phases:

| Phase | Purpose |
| --- | --- |
| Baseline | Establish traffic, latency, success rate, CPU, memory, and replica curves. |
| Elasticity | Apply an approved HPA or replica change, repeat traffic, and compare scale-up delay and resource waterlines. |

Use `huawei_scale_cce_workload` for a deliberate manual scale test. Preview first and apply only with `confirm=true`. For HPA tuning, use the existing HPA actions and retain a rollback manifest.

## 7. Report

Run `huawei_generate_cce_pressure_test_report` with the run JSON and optional observability JSON. The output contains Markdown, HTML, and SVG curve artifacts.
