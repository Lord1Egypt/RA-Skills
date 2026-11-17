## Description:

AgentGuard is trust middleware for credential management, permission scopes, human approval workflows, and audit trails for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendwealth](https://clawhub.ai/user/sendwealth)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure credential vaulting, permission checks, human approval gates, audit logging, and optional 1Password or Feishu integrations for AI agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Current artifacts may expose credentials or weaken approval controls if used with real secrets.

Mitigation: Do not use with real secrets until the default password is removed, approvals are authenticated, and credential handling has been reviewed.

Risk: Shell-based 1Password calls, unvalidated agent IDs, and loose webhook or file-permission handling can create command, identity, or data-access risks.

Mitigation: Replace shell-based credential calls with safe argument-based execution, validate agent identifiers, and tighten webhook and file permissions before deployment.

Risk: The server security verdict is suspicious because the security-tool purpose is stronger than the implementation and documentation evidence.

Mitigation: Review and scan the package carefully before installation, and treat it as unsuitable for production secret management until the listed security gaps are closed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sendwealth/skills/nano-agentguard)
- [AgentGuard README](https://github.com/openclaw/agentguard#readme)
- [1Password comparison](docs/1PASSWORD-COMPARISON.md)
- [Credit score system](docs/CREDIT-SCORE.md)
- [Feishu integration](docs/FEISHU-INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline JavaScript, JSON, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Node.js >=18; covers local vault files, approval requests, audit logs, and optional 1Password or Feishu integrations.]

## Skill Version(s):

0.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
