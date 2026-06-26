## Description: <br>
OpenClaw Shield is a cloud security guardrail for Codex and OpenClaw workflows that checks shell, file, network, and package actions before execution and redacts sensitive output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Eilaiwangwh](https://clawhub.ai/user/Eilaiwangwh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to apply pre-execution security checks, source trust classification, taint-aware decisioning, metadata endpoint blocking, audit logging, and sensitive output redaction in cloud-server agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guardrail relies on a shield.py runtime checker that evidence says is missing or path-mismatched. <br>
Mitigation: Verify the checker implementation and installed path before relying on blocking or redaction behavior. <br>
Risk: The artifact guidance allows Shield errors or a disable file to bypass checks. <br>
Mitigation: Choose and document a fail-closed or explicit owner-approval policy before deployment. <br>
Risk: Audit logs and redacted outputs may contain sensitive operational information. <br>
Mitigation: Define storage location, access controls, retention, and append-only logging before use. <br>


## Reference(s): <br>
- [Permission Matrix and Source Classification](references/permission-matrix.md) <br>
- [Detection and Redaction Rules](references/detection-and-redaction.md) <br>
- [Cloud Boundaries and Configuration](references/cloud-boundaries-config.md) <br>
- [Audit Events and Deployment Playbook](references/audit-and-playbook.md) <br>
- [OpenClaw Shield ClawHub Page](https://clawhub.ai/Eilaiwangwh/openclaw-shield-v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes pass, warn, confirm, block, and redaction guidance for agent actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
