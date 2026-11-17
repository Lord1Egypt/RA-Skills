## Description:

Monitor one or more GitHub repositories and send low-noise alerts with configurable policy modes (major_only, balanced, verbose). Use when setting up recurring repo watch, release/security monitoring, PR merge tracking, and daily digest workflows via OpenClaw cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samwei12](https://clawhub.ai/user/samwei12)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to set up recurring monitoring for one or more GitHub repositories, with low-noise alerts for releases, security-relevant changes, merged PRs, and daily digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect repository list, notification target, schedule, timezone, or state-file path could create unwanted monitoring behavior or alerts.

Mitigation: Confirm these installation parameters before deployment and update them deliberately when repositories or recipients change.

Risk: Recurring checks rely on stored monitoring cursors to avoid resending old events.

Mitigation: Use a persistent state-file path and inspect or reset the state intentionally if alert history or deduplication behavior needs to change.

Risk: The artifact defaults to Chinese headings and trigger phrases for brief and detailed output modes.

Mitigation: Adjust the output instructions before use when another language is required.

## Reference(s):

- [GitHub Monitor on ClawHub](https://clawhub.ai/samwei12/skills/github-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown brief impact summaries with on-demand event details and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default responses are concise and impact-first; detailed event lists are produced only when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
