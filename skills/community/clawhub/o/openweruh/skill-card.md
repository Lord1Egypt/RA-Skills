## Description:

Proactive screen context processor that analyzes screen.context payloads, applies a configured persona mode, and decides whether an observation warrants a proactive user notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fikriaf](https://clawhub.ai/user/fikriaf)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process active screen context through modes such as skeptic, researcher, focus, guardian, and silent. It helps decide whether to send a concise proactive notification or remain silent for later summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects active screen content, which may include sensitive information.

Mitigation: Use it only after confirming how to disable screen inspection and whether sensitive apps or sites can be excluded.

Risk: Silent mode can record observations for later summaries without sending immediate notifications.

Mitigation: Confirm where observations or summaries are stored, how long they are retained, and whether silent mode is enabled before installation.

Risk: Activity tracking and proactive notifications can be disruptive or privacy-sensitive if thresholds and modes are unclear.

Mitigation: Review the configured persona mode and notification thresholds before deployment, and keep interventions limited to clearly warranted cases.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fikriaf/skills/openweruh)
- [OpenWeruh Response Examples](artifact/references/examples.md)
- [OpenWeruh Modes](artifact/references/modes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown notification text, or no user-facing message when intervention is not warranted.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interventions begin with the OpenWeruh label and are kept under two sentences; silent mode may record observations for later summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
