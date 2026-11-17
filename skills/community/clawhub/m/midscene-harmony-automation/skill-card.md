## Description:

Vision-driven HarmonyOS NEXT device automation using Midscene and HDC to inspect screenshots, interact with visible UI, launch apps, validate screen states, and collect reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quanru](https://clawhub.ai/user/quanru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to automate and verify HarmonyOS NEXT apps or device workflows through screenshot-driven UI actions, HDC commands, assertions, and report review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over a connected HarmonyOS device through Bash, HDC commands, Midscene UI actions, and mutable npm runtime execution.

Mitigation: Use it only with trusted devices, a trusted npm registry, and a trusted model provider; avoid sensitive screens unless necessary.

Risk: Raw HDC shell commands can perform low-level device operations beyond visible UI automation.

Mitigation: Review each raw shell command before execution and prefer explicit user confirmation before any device-changing action.

Risk: Screenshots and prompts may be sent to external vision model providers configured through environment variables.

Mitigation: Configure credentials locally and avoid exposing secrets, personal data, or production information to untrusted providers.

## Reference(s):

- [Midscene.js](https://midscenejs.com)
- [Midscene Model Configuration](https://midscenejs.com/model-common-config)
- [DevEco Studio](https://developer.huawei.com/consumer/cn/deveco-studio/)
- [ClawHub Skill Page](https://clawhub.ai/quanru/skills/midscene-harmony-automation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples, environment variable configuration, and report consumption instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automation may generate screenshots, HTML reports, Markdown report exports, or JSON report exports through Midscene commands.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
