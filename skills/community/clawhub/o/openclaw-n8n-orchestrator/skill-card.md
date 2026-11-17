## Description:

Builds OpenClaw-to-n8n orchestration guidance, templates, validation checks, and deployment patterns for credential-isolated workflow automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktopper](https://clawhub.ai/user/ktopper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent engineers use this skill to create OpenClaw skill directories and n8n webhook workflows that route external API actions through credential-isolated n8n pipelines. It also supports Gateway ingress, bidirectional proxy orchestration, deployment guidance, and ClawHub publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production installation may carry risky deployment and agent-expansion guidance.

Mitigation: Review the skill before production use and keep agent expansion, persistent memory, and vault-loading patterns behind explicit human approval, provenance tracking, audit logs, and deletion controls.

Risk: Gateway or n8n exposure could allow unintended workflow or agent invocation.

Mitigation: Keep the OpenClaw Gateway bound to localhost or a private network, use least-privilege gateway tokens, and disable direct /tools/invoke unless it is strictly required.

Risk: Unpinned packages or containers can change behavior after deployment.

Mitigation: Pin package and container versions before production installation.

Risk: Pipe-to-shell installers and generated shell triggers can increase execution risk.

Mitigation: Remove pipe-to-shell installers, require human review before execution, and prefer the zero-dependency Node.js trigger template or reviewed sanitized shell scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ktopper/skills/openclaw-n8n-orchestrator)
- [Deployment Reference: OpenClaw + n8n](references/deployment.md)
- [OpenClaw Gateway API Reference](references/gateway-api.md)
- [n8n-claw Architecture Reference](references/n8n-claw-architecture.md)
- [ClawHub Publishing Reference](references/publishing.md)
- [Security Reference: OpenClaw + n8n Credential Isolation](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML, JSON, shell, JavaScript, Python, and Docker Compose snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw skill directory templates, webhook trigger templates, deployment configuration, validation commands, and security hardening guidance.]

## Skill Version(s):

2.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
