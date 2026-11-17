## Description:

Health Guardian helps agents import Apple Health data, analyze health patterns, and surface anomaly alerts for humans with chronic conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgtreadw](https://clawhub.ai/user/cgtreadw)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill to configure Apple Health import, run local health analysis, and review generated alerts or summaries for caregiving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes highly sensitive health records and the security evidence flags misleading privacy and automation guidance.

Mitigation: Use only with explicit consent from the person whose data is monitored, restrict access to the intended export and data directories, and review alert delivery before installing or scheduling it.

Risk: Health anomaly alerts and summaries can be incomplete or incorrect and may influence care decisions.

Mitigation: Treat outputs as monitoring aids rather than medical advice, and require human review for concerning patterns.

Risk: The setup depends on Health Auto Export and iCloud-synced data while the artifact claims that no data leaves the machine.

Mitigation: Confirm Apple Health export and iCloud sync settings, and document whether any data or alerts leave the device.

## Reference(s):

- [Health Guardian ClawHub Listing](https://clawhub.ai/cgtreadw/skills/health-guardian)
- [Health Auto Export App Store Listing](https://apps.apple.com/app/health-auto-export/id1115567069)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON health data, summaries, and alert records when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
