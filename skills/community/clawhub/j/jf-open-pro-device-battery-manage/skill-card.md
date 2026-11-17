## Description:

Helps agents query and set low-battery threshold settings for JFTech low-power devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve supported low-battery threshold ranges, inspect the current threshold, and set a validated threshold for bound JFTech battery or solar-powered devices.

### Deployment Geography for Use:

China Mainland, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: The skill handles JFTech UUIDs, app keys, app secrets, device tokens, and access tokens.

Mitigation: Run it only in trusted execution environments, keep credentials out of logs, and rotate any credential or token that may have been exposed.

Risk: The skill can send signed requests and tokens to the configured JF_ENDPOINT.

Mitigation: Use only documented JFTech endpoints and review endpoint configuration before execution.

Risk: The token helper can print device tokens and raw API responses in plaintext.

Mitigation: Avoid running the token helper where console output is captured or shared, and redact logs before distribution.

## Reference(s):

- [JFTech Open Platform Documentation](https://docs.jftech.com)
- [Get Low Battery Threshold Range Configuration](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=9bf993f3140ad9f9b4390fee750ba740&lang=zh)
- [Set Low Battery Threshold Configuration](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=b246b44faa8c4d41a3f10e3de95b892a&lang=zh)
- [ClawHub Skill Page](https://clawhub.ai/jftech/skills/jf-open-pro-device-battery-manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with shell command examples and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech credentials, a bound device, a device token, and a selected JFTech endpoint.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
