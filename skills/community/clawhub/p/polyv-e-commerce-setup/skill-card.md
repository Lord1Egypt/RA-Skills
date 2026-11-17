## Description:

一键配置电商直播环境（频道、商品、优惠券）

This skill is ready for commercial/non-commercial use.

## Publisher:

[polyv](https://clawhub.ai/user/polyv)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and PolyV operators use this skill to configure an e-commerce live streaming environment, including channel, product, and coupon setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable remote npm code with npx polyv-live-cli@latest.

Mitigation: Use a pinned, reviewed PolyV CLI version before installing or executing the setup commands.

Risk: The skill passes a sensitive AppSecret in plaintext command arguments.

Mitigation: Avoid pasting AppSecret into chat or shell history; prefer a secure local prompt or secret manager, and rotate the AppSecret if it appeared in transcripts, logs, or shell history.

## Reference(s):

- [PolyV Console](https://console.polyv.net/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes credential-handling guidance for AppID and AppSecret setup.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
