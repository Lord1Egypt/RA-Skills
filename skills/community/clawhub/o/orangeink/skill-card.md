## Description:

Helps create and review Chinese WeChat public-account Markdown and convert it into publishable HTML, a browser copy page, and a draft API payload with static formatting checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aladooo](https://clawhub.ai/user/aladooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Chinese-language WeChat public-account editors use this skill to write, review, and format articles for the WeChat editor or draft API. It generates publishing assets and static checks, but does not publish articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Markdown with raw HTML or scripts may make a generated copy page unsafe to open.

Mitigation: Render and open copy pages only from trusted Markdown; review source content before opening generated pages.

Risk: Skipping static checks can leave formatting problems in publishable output.

Mitigation: Keep checks enabled, review reported issues and image lists, and avoid --no-check for publishable output.

Risk: Opting into remote parity templates introduces an avoidable remote-code trust dependency.

Mitigation: Leave OIMD_REMOTE_TEMPLATE disabled and use a trusted, pinned local index.html for parity checks.

## Reference(s):

- [Orangeink writing guide](references/writing-guide.md)
- [WeChat formatting rules](references/wechat-rules.md)
- [WeChat draft API notes](references/wechat-api.md)
- [WeChat draft/add API documentation](https://developers.weixin.qq.com/doc/service/api/draftbox/draftmanage/api_draft_add.html)

## Skill Output:

**Output Type(s):** [Markdown, HTML, JSON, Guidance]

**Output Format:** [Chinese Markdown guidance, HTML article fragments and copy pages, and JSON draft payloads and checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static formatting checks and an image list accompany rendering; draft payloads require separate submission.]

## Skill Version(s):

1.2.8 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
