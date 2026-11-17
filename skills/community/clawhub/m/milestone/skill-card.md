## Description:

Milestone is a local command-line activity logger for recording entries, reviewing recent history and statistics, searching logs, and exporting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use Milestone to keep local terminal-based activity notes, inspect recent activity and aggregate statistics, search entries, and export reports in JSON, CSV, or text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Milestone stores user-entered activity entries in plaintext under ~/.local/share/milestone.

Mitigation: Avoid entering passwords, tokens, private customer data, or sensitive prompts; review local file permissions before storing private notes.

Risk: The security guidance reports unreliable command behavior, including duplicate dispatch and Bash local-scope issues.

Mitigation: Review command behavior in a non-sensitive local environment before relying on logs or exports.

## Reference(s):

- [Milestone on ClawHub](https://clawhub.ai/ckchzh/skills/milestone)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain terminal text with optional JSON, CSV, or text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local plaintext log files under ~/.local/share/milestone.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
