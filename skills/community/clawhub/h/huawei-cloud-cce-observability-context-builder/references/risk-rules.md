# Risk Rules

- Allow automatic R1 read-only queries: alarms, metrics, logs, events, inventory, read-only report generation.
- Prohibit any action requiring `confirm=true` — no mutations allowed.
- Never persist AK/SK, tokens, certificates, or kubeconfig.
- Log output must be sanitized. When suspected secrets are found, describe the hit location only — never copy the original text.
- Charts and reports must only be generated from authorized query results.