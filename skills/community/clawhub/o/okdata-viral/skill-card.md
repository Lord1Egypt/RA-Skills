## Description:

Collects a social post’s title, text, engagement, and available video transcript into one row for an AI to analyze.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to gather a post’s content and engagement across 13 supported social platforms, then analyze why it performed well.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a documented external API connection, and the security scan is incomplete.

Mitigation: Before installing, consider whether you are comfortable with the API connection and the data involved; treat the benign verdict as inconclusive because the scan could not resolve multiple local path-like references.

## Reference(s):

- [okdata viral skill guide (English)](https://okdata.online/skills/viral/?src=skill-okdata-viral)
- [okdata viral skill guide (Chinese)](https://okdata.online/zh/skills/viral/?src=skill-okdata-viral)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [A Markdown table of post details and available transcript, followed by a concise analysis, charge amount, and data source.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One post per run; fields vary by platform, and unavailable metrics are left blank.]

## Skill Version(s):

0.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
