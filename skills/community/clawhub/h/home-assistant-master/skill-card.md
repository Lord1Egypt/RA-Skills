## Description: <br>
Home Assistant OS (HAOS) operations skill for OpenClaw agents. Use for read-only audits, diagnostics, automation design/review, dashboard UX planning, voice intent mapping, integration risk assessment, backup/restore readiness checks, and maintenance playbooks. Default to read-only; require explicit approval before any write/reload/restart. Apply when users ask to troubleshoot entities/devices/integrations, improve reliability, design automations, or plan safe Home Assistant changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djasha](https://clawhub.ai/user/djasha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to diagnose Home Assistant OS environments, review or design automations, plan dashboards and voice intents, assess integration risks, and prepare safe maintenance playbooks. It is read-first and requires explicit approval before writes, reloads, restarts, updates, or restores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent access to Home Assistant may expose device states, logs, history, traces, and sensitive household context. <br>
Mitigation: Use least-privilege access, store credentials only in secure platform storage, redact sensitive values in outputs, and rotate or revoke tokens if exposure is suspected. <br>
Risk: Writes to entities, security devices, or platform services can change the physical environment or disrupt Home Assistant availability. <br>
Mitigation: Default to read-only diagnostics, preview exact affected entities and services, require explicit confirmation for any write, and use two-step confirmation for sensitive or platform-level actions. <br>
Risk: Troubleshooting or automation recommendations can be incorrect if based on incomplete Home Assistant evidence. <br>
Mitigation: Collect traces, history, logs, integration state, and constraints before diagnosis; prefer official Home Assistant documentation when guidance conflicts. <br>


## Reference(s): <br>
- [Home Assistant Master on ClawHub](https://clawhub.ai/djasha/home-assistant-master) <br>
- [Safety Policy](references/safety-policy.md) <br>
- [Access & Credentials Requirements](references/access-and-credentials.md) <br>
- [Standard Workflows](references/workflows.md) <br>
- [Checklists](references/checklists.md) <br>
- [Canonical Citations](references/citations.md) <br>
- [Home Agent Profile](references/home-agent-profile.md) <br>
- [Home Assistant Documentation](https://www.home-assistant.io/docs/) <br>
- [Home Assistant Automation Documentation](https://www.home-assistant.io/docs/automation/) <br>
- [Home Assistant Security Documentation](https://www.home-assistant.io/docs/configuration/securing/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown with checklists, change previews, diagnostic summaries, and optional inline commands or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; requires platform-provided Home Assistant access for operational diagnostics and approval-gated writes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
