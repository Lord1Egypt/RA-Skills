# Risk Rules

- Inspection allows only R1 read-only actions.
- Prohibited mutation actions: auto-scaling, deletion, drain, reboot, hibernate, awake.
- Inspection reports must never contain AK/SK, tokens, certificates, or full kubeconfig.
- Anomalies produce only recommendations; remediation actions must be separately confirmed via `huawei-cloud-cce-auto-remediation-runner`.