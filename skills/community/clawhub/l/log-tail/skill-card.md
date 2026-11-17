## Description:

Stream recent logs from systemd journal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xejrax](https://clawhub.ai/user/xejrax)

### License/Terms of Use:


## Use Case:

Developers and system operators use this skill to inspect recent systemd journal logs, optionally scoped to a service unit and followed in real time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Journal logs can contain hostnames, usernames, service errors, filesystem paths, or secrets emitted by other programs.

Mitigation: Review log output before sharing it externally and scope commands to the minimum service unit and line count needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xejrax/skills/log-tail)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May surface local journal log content that can include hostnames, usernames, paths, service errors, or secrets emitted by other programs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
