## Description:

Provides local CPU, memory, disk, load, and bounded process diagnostics to help assess capacity and troubleshoot resource contention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyeque](https://clawhub.ai/user/iyeque)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check local resource availability before demanding tasks and investigate CPU, memory, disk, or process contention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process diagnostics may expose local process metadata, and optional owner attribution can reveal usernames or service accounts.

Mitigation: Allow local diagnostics only when appropriate; use --include-owners only when owner attribution is specifically needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/iyeque/skills/iyeque-local-system-info)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown guidance and shell commands; diagnostic results are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only, point-in-time local diagnostics; process listings are limited to 1–100 entries.]

## Skill Version(s):

1.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
