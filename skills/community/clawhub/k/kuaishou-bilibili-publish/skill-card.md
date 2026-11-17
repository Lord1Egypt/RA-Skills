## Description:

Automates video uploads, cover selection, titles, keywords, and publishing to Kuaishou, Bilibili, and Douyin through Chrome browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaohei2022](https://clawhub.ai/user/xiaohei2022)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and content operators use this skill to prepare and publish the same video package across Kuaishou, Bilibili, and Douyin from a text configuration file. It supports per-platform publishing, a multi-platform publish-all flow, and a no-publish preview mode for review before final submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Chrome profile for live creator accounts and can publish content to social media platforms.

Mitigation: Run with --no-publish first, verify the account and content in the browser, and avoid publish-all until every destination has been reviewed.

Risk: Proxy environment variables can affect where browser traffic is routed.

Mitigation: Clear KBS_PROXY, HTTPS_PROXY, and HTTP_PROXY unless a trusted proxy is intentionally required.

Risk: Debug and analysis scripts can save page HTML that may contain account or page data.

Mitigation: Avoid debug scripts on sensitive accounts, or protect and delete saved HTML output after troubleshooting.

Risk: Platform page structure changes can make selectors stale and cause failed or incomplete uploads.

Mitigation: Use preview mode after platform changes and update selectors before enabling final publish actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaohei2022/skills/kuaishou-bilibili-publish)
- [Kuaishou Creator Center](https://cp.kuaishou.com/)
- [Bilibili Creator Upload](https://member.bilibili.com/platform/upload/video/frame)
- [Douyin Creator Upload](https://creator.douyin.com/creator-micro/content/upload)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a logged-in Chrome profile; supports no-publish preview mode, per-platform commands, and a publish-all command.]

## Skill Version(s):

1.0.4 (source: server release metadata; pyproject.toml reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
