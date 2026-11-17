## Description:

Provides a runbook for starting, stopping, checking, and troubleshooting docker-mailserver, its cloud SMTP relay, and deferred mail queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain a docker-mailserver deployment, inspect mail queues and logs, and manage a cloud SMTP relay during service checks or delivery failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect production mail services through Docker mailserver and cloud relay start, stop, retry, and queue operations.

Mitigation: Use it only in the intended mailserver environment, review commands before execution, and schedule disruptive operations through the normal operations process.

Risk: The documented relay access uses administrator SSH and disabled strict host-key verification.

Mitigation: Replace administrator SSH with a least-privileged account, enable strict host-key verification, and declare the required credential and SSH config paths before use.

Risk: The end-to-end test sends outbound email to a real address.

Mitigation: Redirect test delivery to a controlled sink address or remove the live outbound test in environments where external email is inappropriate.

## Reference(s):

- [Mailserver Architecture Reference](references/architecture.md)
- [ClawHub Skill Page](https://clawhub.ai/axelhu/skills/mailserver-maintenance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
