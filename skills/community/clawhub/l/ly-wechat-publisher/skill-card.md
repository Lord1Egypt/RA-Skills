## Description:

Automatically prepares AI news content and creates WeChat Official Account drafts using configurable HTML templates and schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to generate daily AI news material and place it into a WeChat Official Account draft workflow for review and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WeChat Official Account credentials and can create drafts in the connected account.

Mitigation: Install only for accounts where draft-creation authority is acceptable, keep AppID and AppSecret tightly controlled, and review generated drafts before publishing.

Risk: AppSecret may be exposed if supplied on the command line or stored in a broadly readable local configuration file.

Mitigation: Prefer a protected secret store or environment variable, restrict local configuration permissions, and rotate the secret if exposure is possible.

Risk: Documented installation examples include privileged or pipe-to-shell commands that can increase system-level exposure.

Mitigation: Verify installers independently, pin trusted package versions, and avoid sudo or curl-to-shell installation steps unless reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/403914291/skills/ly-wechat-publisher)
- [ClawHub publisher profile](https://clawhub.ai/user/403914291)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, generated HTML content, and WeChat draft status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates WeChat draft content and local status, usage, token-cache, log, and result files during execution.]

## Skill Version(s):

1.1.0 (source: server release metadata and changelog, released 2026-03-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
