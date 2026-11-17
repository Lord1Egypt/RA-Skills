## Description:

OpenClaw Ops Guardrails standardizes operational checks, remote-execution troubleshooting, approval and pairing diagnostics, CLI-only node setup, and pre-publication sanitization for OpenClaw gateway and Mac node workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyezir](https://clawhub.ai/user/xyezir)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run OpenClaw health checks, diagnose approval, pairing, system.run, and gateway failures, and prepare sanitized troubleshooting notes before external release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary approval bypass with full execution access can expose real OpenClaw nodes to unintended commands.

Mitigation: Keep approval checks enabled by default; require explicit operator approval for any temporary exception, scope it to the exact node and command, and restore the previous approval policy immediately after testing.

Risk: Troubleshooting output can leak credentials, endpoint details, identifiers, or local paths when shared externally.

Mitigation: Run the publish sanitization checklist before external release and replace sensitive values with placeholders such as <gateway-token>, <api-endpoint>, <local-path>, and <node-name>.

## Reference(s):

- [OpenClaw Ops Guardrails ClawHub Page](https://clawhub.ai/xyezir/skills/openclaw-ops-guardrails)
- [xyezir Publisher Profile](https://clawhub.ai/user/xyezir)
- [Failure Playbook](references/failure-playbook.md)
- [Publish Sanitization Checklist](references/publish-sanitization-checklist.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown with inline shell commands and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status summaries, successful checks, failed checks with root causes, residual risks, prioritized next steps, sanitized documents, and release notes.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
