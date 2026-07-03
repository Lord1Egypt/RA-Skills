# Pressure-Test Risk Rules

## R0 Read-Only

- Generate k6 client manifests.
- Inspect Services, Ingresses, HPA, and ELB evidence.
- Generate Markdown, HTML, and SVG reports.

## R1 Reviewed Kubernetes Changes

- Create or patch the workload-facing Service and Ingress.
- Create or patch the isolated Java sample Namespace, ConfigMap, and Deployment.
- Ensure the k6 client namespace exists, then create a ConfigMap and Job that sends traffic.

Always preview these actions. Apply them only after explicit approval with `confirm=true`.

## R2 Capacity Changes

- Create a chargeable ELB after reviewing subnet, AZ, flavor, and protection settings.
- Scale workload replicas.
- Change HPA behavior or target utilization.
- Change node autoscaler bounds.

Use the existing remediation or HPA actions. Show the exact change, expected traffic impact, rollback command, and validation checks before applying `confirm=true`.

## Operational Limits

- Start with low VUs and short duration.
- Confirm the test target and namespace before sending traffic.
- Do not test production traffic paths without an approved window.
- Stop raising traffic when success rate drops, latency rises sharply, or resource waterlines exceed the agreed limit.
- Mirror the k6 image to regional SWR when public image pulls are unavailable.
