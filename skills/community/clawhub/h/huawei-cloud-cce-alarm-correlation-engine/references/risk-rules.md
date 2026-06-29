# Risk Rules

- Alarm query, alarm analysis, action rule query, and mute rule query are all read-only operations.
- Creating, updating, and deleting AOM alarm rules is allowed, but must be previewed first; only after explicit user confirmation may `confirm=true` be added to execute.
- Modifying action rules, mute rules, or other cloud resources is prohibited.
- Do not interpret absence of active alarms as "no problem"; always cross-reference history alarms.
- Output must never expose AK/SK, tokens, or complete sensitive logs.
- If the user requests scaling, rebooting, draining, or other remediation actions, output recommendations only and hand off to `huawei-cloud-cce-auto-remediation-runner`.