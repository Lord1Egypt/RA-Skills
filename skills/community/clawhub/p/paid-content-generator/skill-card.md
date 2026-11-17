## Description:

AI内容生成器 - 小红书文案、视频脚本、多平台内容一键生成。接入SkillPay收费，每次调用0.001 USDT。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ffffff9331](https://clawhub.ai/user/ffffff9331)

### License/Terms of Use:

MIT

## Use Case:

External creators and developers use this skill to generate template-based Xiaohongshu posts, video scripts, public-account articles, and adapted social content after a SkillPay billing check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded billing API key and external SkillPay charging behavior.

Mitigation: Remove and rotate the embedded key, require SKILLPAY_API_KEY from the environment, and review billing behavior before installation.

Risk: The release evidence reports automatic deduction of 0.001 USDT per generation and transmission of the supplied user ID to SkillPay.

Mitigation: Require explicit user consent before charges and disclose what user identifier is sent to the billing service.

Risk: The release evidence says the description overstates AI capability because the current generator is template-based.

Mitigation: Clarify that generated outputs are template-based unless a real model-backed generator is added and documented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ffffff9331/skills/paid-content-generator)
- [SkillPay billing service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text content printed to the command line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLPAY_API_KEY and performs a SkillPay billing check before generation.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
