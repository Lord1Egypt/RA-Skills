## Description:

Converts Markdown articles into WeChat Official Account-compatible inline-styled HTML and can upload them to a WeChat draft box with front matter, tables, code blocks, lists, and image handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koraihub](https://clawhub.ai/user/koraihub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to prepare Markdown articles for WeChat Official Accounts, either as local preview HTML or as drafts uploaded through the WeChat API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft mode sends article content and images to WeChat.

Mitigation: Use --convert-only for local preview when upload is not needed, and run --draft only with intended content and authorized WeChat credentials.

Risk: Markdown image references can cause local files to be uploaded in draft mode without strong path limits or confirmation.

Mitigation: Process only trusted Markdown, review local image paths before draft upload, and restrict image references to the article directory.

Risk: Generated local preview HTML may contain converted article content.

Mitigation: Store preview output only in trusted locations and review or sanitize generated HTML before sharing it.

Risk: Dependencies are specified with minimum versions rather than pinned versions.

Mitigation: Pin and review dependency versions before deployment in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/koraihub/skills/md2wechat-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/koraihub)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated HTML files and WeChat draft API submissions when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; draft mode requires WECHAT_APPID, WECHAT_SECRET, and network access to WeChat.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
