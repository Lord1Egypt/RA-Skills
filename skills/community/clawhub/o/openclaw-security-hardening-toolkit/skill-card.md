## Description:

Secures OpenClaw by auditing instance exposure, protecting credentials, verifying skill safety, enforcing gateway token access, and enabling session sandboxing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebrierfox](https://clawhub.ai/user/thebrierfox)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit and harden OpenClaw deployments against exposed gateways, credential leakage, unsafe skill installation, weak access controls, and post-compromise recovery gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential inspection commands may expose or print sensitive tokens during an audit.

Mitigation: Replace token checks with redacted checks and approve credential scans explicitly before execution.

Risk: Broad process-kill commands may terminate unrelated local services during incident response.

Mitigation: Review process matches before terminating them and preserve logs before containment actions.

Risk: Plaintext external IP checks may disclose instance metadata or network context to a third-party service.

Mitigation: Avoid the plaintext ifconfig.me probe or replace it with an approved internal reachability check.

Risk: Persistent scheduling guidance could create credential-rotation jobs without a reviewed rollback path.

Mitigation: Do not create cron-based credential rotation until the script, schedule, ownership, logging, and rollback plan are reviewed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thebrierfox/skills/openclaw-security-hardening-toolkit)
- [Publisher profile](https://clawhub.ai/user/thebrierfox)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides checklists, command examples, configuration snippets, and incident response guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
