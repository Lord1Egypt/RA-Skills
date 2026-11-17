## Description:

Automatically scans GitHub bounty issues, filters them by configured skills and reward criteria, and can generate or post application proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sasamittrrr](https://clawhub.ai/user/sasamittrrr)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to find bounty-labelled GitHub issues that match configured skills, reward thresholds, and competition limits. It is intended to reduce manual bounty discovery and proposal drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act through a user's GitHub account and post public application comments without a preview or confirmation step.

Mitigation: Run it only with a constrained GitHub account or token, review proposed actions before execution, and avoid unattended operation.

Risk: The included configuration contains a hardcoded wallet_address.

Mitigation: Review, replace, or remove the wallet address in config.json before running the skill.

Risk: The current implementation may not actually auto-apply because of a logic bug noted by the security guidance.

Mitigation: Test the workflow manually in a low-impact repository or dry-run process before relying on automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sasamittrrr/skills/github-bounty-hunter)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [config.json](artifact/config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown proposal text, GitHub CLI commands, and JSON configuration or state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post public GitHub issue comments through the user's authenticated GitHub CLI session.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, released 2026-02-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
