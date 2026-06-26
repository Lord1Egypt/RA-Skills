## Description: <br>
Manage Kleinanzeigen listings through the KleinClaw OpenClaw plugin and embedded miniclaw runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyazar](https://clawhub.ai/user/ilyazar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare, verify, publish, update, delete, download, or extend Kleinanzeigen listings through the KleinClaw OpenClaw plugin while keeping credentials and account state outside chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The authoritative security scan marked the bundle suspicious because a related review helper defaults to running nested Codex with sandboxing and approvals disabled. <br>
Mitigation: Review before installing in sensitive repositories, use no-yolo mode for the autoreview helper unless full filesystem authority is intentional, and treat admin or migration commands as production-impacting operations that require careful confirmation. <br>
Risk: Kleinanzeigen listing operations may affect live account state or expose sensitive account configuration if handled carelessly. <br>
Mitigation: Use only KleinClaw tools, keep credentials, browser profiles, cookies, session data, and full config files out of chat, and require explicit user confirmation for mutating actions. <br>


## Reference(s): <br>
- [KleinClaw plugin](https://clawhub.ai/plugins/kleinclaw) <br>
- [Kleinanzeigen Helper ClawHub page](https://clawhub.ai/ilyazar/kleinanzeigen-helper) <br>
- [Prerequisites / Install](references/install.md) <br>
- [Workflow](references/workflow.md) <br>
- [Non-negotiables](references/non-negotiables.md) <br>
- [Tool Selection](references/tool-selection.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with tool-selection recommendations and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces sanitized, user-facing instructions and action summaries; mutating Kleinanzeigen operations require explicit confirmation through KleinClaw tools.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
