# Risk Rules

- Only run read-only discovery and report generation.
- Do not patch, delete, scale, restart, cordon, drain, or change traffic.
- Treat downstream consumers as inferred unless backed by APM, service mesh, access logs, or explicit dependency metadata.
- Static Kubernetes topology can prove possible propagation paths, not real request volume or business criticality.
- Recovery actions must be handed to `huawei-cloud-cce-auto-remediation-runner` and must use preview-first confirmation.
