## Description:

Security vetting for agent skills before installation, including checks for dangerous Bash commands, sensitive file access, network exfiltration, obfuscated code, and other security risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjshysst-dot](https://clawhub.ai/user/hjshysst-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to scan ClawHub or OpenClaw skills before installation or update and decide whether to block, warn, or proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner is advisory and can miss risky skill instructions because it uses simple pattern checks.

Mitigation: Pair scan results with manual review or a stronger scanner before installing untrusted skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjshysst-dot/skills/pangshu-skill-vetter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown, including CLI reports and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity counts, findings, verdicts, and install guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
