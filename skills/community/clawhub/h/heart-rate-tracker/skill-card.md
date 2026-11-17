## Description:

Heart Rate Tracker helps users record heart-rate readings, monitor exercise heart rates, review wellness trends, receive abnormal-rate alerts, and generate basic statistical reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to log resting and exercise heart-rate readings, request basic heart-health trend analysis, configure abnormal heart-rate thresholds, and produce statistical wellness reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles heart-rate data and may present health-related analysis that users could mistake for medical guidance.

Mitigation: Treat all analysis as wellness information only, avoid diagnostic claims, and review where heart-rate data is stored or transmitted before deployment.

Risk: The release declares an unexplained `curl` requirement and documents a mutable `npx clawhub@latest` install command.

Mitigation: Pin the installer version and remove the `curl` requirement or document exact network destinations and consent behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/heart-rate-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/kaising-openclaw1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides wellness tracking guidance and command examples; health-related use requires review before deployment.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
