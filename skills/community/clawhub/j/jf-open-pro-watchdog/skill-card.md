## Description:

Monitors selected areas in JF camera captures using visual comparison to flag missing objects, obstructions, and other scene changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Camera operators and facility teams configure monitored areas, compare live captures with baseline images, and review alerts for missing objects, blocked routes, or unexpected activity.

### Deployment Geography for Use:

Mainland China, Asia, Europe, and North America (listed JF API regions)

## Known Risks and Mitigations:

Risk: Camera captures and stored baseline images may contain sensitive surveillance footage.

Mitigation: Limit camera access and review where captures and baselines are stored, shared, and retained.

Risk: API credentials and device passwords may be exposed through scheduled tasks, chat, notifications, or monitor configuration.

Mitigation: Keep live secrets in environment variables or a secret store, restrict configuration access, and never include secrets in task text or notifications.

Risk: Blurry, dark, or changed camera views can make visual assessments unreliable.

Mitigation: Review indeterminate results and verify important alerts against the captured images before acting.

## Reference(s):

- [ClawHub jf-watchdog release](https://clawhub.ai/jftech/skills/jf-open-pro-watchdog)
- [JF Open Platform documentation](https://docs.jftech.com)
- [JF cloud capture pricing](https://aops.jftech.com/#/pricing?lang=zh&tab=MEDIA_PROCESSING)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Configuration]

**Output Format:** [Markdown inspection report with annotated images; JSON monitor configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Per-region normal, abnormal, or indeterminate status with supporting descriptions and baseline comparisons.]

## Skill Version(s):

1.0.1 (source: ClawHub release; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
