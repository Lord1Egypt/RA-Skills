## Description:

Inspect and maintain a Mac through repeatable terminal-first checks for disk usage, large files, launch agents, login items, power settings, sleep/wake behavior, networking, and OpenClaw health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benboby](https://clawhub.ai/user/benboby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support teams, and Mac users use this skill to inspect storage, performance, startup behavior, power settings, networking, and OpenClaw health before choosing maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance recommendations may include deleting files or changing startup items, power settings, installed software, firewall, SSH, or other security-sensitive settings.

Mitigation: Review and approve those actions before execution; prefer read-only checks and reversible changes first.

Risk: System inspection can expose local paths, process names, network details, logs, or security warnings.

Mitigation: Share only details needed for the maintenance decision and avoid exposing unrelated sensitive local information.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown maintenance summaries with command suggestions and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes read-only inspection first, groups findings by risk, and asks for confirmation before higher-risk changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
