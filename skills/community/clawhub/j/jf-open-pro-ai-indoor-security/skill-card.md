## Description:

JF Tech indoor security skill for monitoring home spaces, managing indoor security service status, querying alerts and statistics, and managing household member records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate JF Tech indoor security workflows for supported devices, including service toggles, abnormal-alert review, family member records, and household activity statistics.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill can send household monitoring data, device and user identifiers, authorization tokens, and face/member images to JF Tech cloud APIs.

Mitigation: Install only after reviewing the data flows, keep secrets out of command lines where possible, and limit use to authorized devices and accounts.

Risk: The skill can disable indoor security service settings or delete and update household member records.

Mitigation: Require explicit user confirmation before security-service changes or member deletion and update actions.

Risk: Face-image enrollment and household member tracking can affect privacy and consent expectations.

Mitigation: Enroll face images and enable household notifications only with appropriate household consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-indoor-security)
- [JF Tech developer platform](https://developer.jftech.com)
- [JF Tech signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [JF Tech timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [JF Tech package-card usage documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied JF Tech credentials, authorization token, device serial number, user identifier, and service eligibility.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
