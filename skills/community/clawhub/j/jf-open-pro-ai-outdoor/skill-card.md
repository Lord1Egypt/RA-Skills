## Description:

JF Tech outdoor security skill for managing vehicle detection, abnormal alerts, smart detection, sensitivity settings, detection areas, push plans, and related monitoring features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and query JF Tech outdoor security devices, including alarm settings, AI detection modes, detection regions, notification plans, vehicle records, statistics, and device credential synchronization.

### Deployment Geography for Use:

China, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill can change live outdoor security device settings, including AI analysis, alarm configuration, detection regions, notification plans, vehicle records, and device credentials.

Mitigation: Manually confirm every update, delete, disable, and credential-sync action before execution, especially commands that alter service state or stored device data.

Risk: Credentials, identifiers, alarm data, uploaded images, and device credentials may be sent to the configured JF Tech API endpoint.

Mitigation: Use environment variables or a secret manager, avoid passing secrets on the command line when possible, restrict logs, and rotate credentials that were exposed in command histories or captured output.

Risk: Server security evidence marks the release as suspicious because sensitive device-management capabilities require careful review.

Mitigation: Install only when the intended use is JF Tech outdoor security device management and review the skill before deployment.

## Reference(s):

- [JF Tech Developer Platform](https://developer.jftech.com)
- [JF Tech Signature Algorithm Documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh)
- [JF Tech Timestamp Algorithm Documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh)
- [JF Tech Outdoor Security API Documentation](https://docs.jftech.com/)
- [ClawHub Skill Page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-outdoor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JF Tech account, device, app credentials, authorization token, and selected regional API endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
