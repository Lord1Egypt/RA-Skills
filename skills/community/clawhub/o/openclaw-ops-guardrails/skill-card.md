## Description: <br>
OpenClaw Ops Guardrails standardizes operational health checks, troubleshooting, remote-execution stability, approval and pairing diagnostics, and pre-publication sanitization for OpenClaw gateway and Mac node workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyezir](https://clawhub.ai/user/xyezir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to diagnose OpenClaw gateway and node failures, run read-only health checks, stabilize remote command execution, and prepare sanitized operational notes before external sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting guidance may weaken approval controls by recommending full-access or ask-off settings. <br>
Mitigation: Use any full-access or approval-disabled mode only temporarily, under supervision, and restore the intended approval policy after diagnosis. <br>
Risk: Gateway credentials may be exposed when tokens are passed through shell commands or copied into logs. <br>
Mitigation: Use environment variables, secure prompts, or a credential store for secrets, and redact tokens before sharing command output or notes. <br>
Risk: Operational notes can leak server IPs, domains, API endpoints, callbacks, identifiers, usernames, or local paths. <br>
Mitigation: Apply the bundled sanitization checklist and replace sensitive values with placeholders before publishing or sharing externally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xyezir/openclaw-ops-guardrails) <br>
- [Failure Playbook](references/failure-playbook.md) <br>
- [Publish Sanitization Checklist](references/publish-sanitization-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown troubleshooting guidance with shell command examples and prioritized operational summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces availability summaries, successful checks, failed checks with root causes, residual risks, next steps, and sanitized release notes; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
