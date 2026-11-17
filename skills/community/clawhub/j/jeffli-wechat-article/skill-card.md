## Description:

微信公众号文章抓取工具。将微信公众号文章转换为 Markdown 格式，支持图片本地下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert WeChat Official Account articles into Markdown, including article metadata, preserved code blocks, media references, and optional local image copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article content can steer the default image downloader to fetch arbitrary URLs and save unbounded responses locally.

Mitigation: Run the skill in a low-privilege container or virtual environment, use a dedicated output directory, and prefer --no-images for untrusted articles until URL allowlisting and size limits are added.

Risk: The release depends on unpinned Python packages and a browser automation dependency.

Mitigation: Pin and review dependencies before deployment, then scan the environment after installation.

Risk: WeChat may present CAPTCHA, verification pages, or rate limits instead of article content.

Mitigation: Use --no-headless only when manual verification is required, space out batch requests, and review debug HTML before trusting failed conversions.

## Reference(s):

- [Camoufox project](https://github.com/nichochar/camoufox)
- [ClawHub skill page](https://clawhub.ai/jeffli2002/skills/jeffli-wechat-article)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown files with YAML frontmatter, local image files, and text status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-article and batch conversion; image downloading can be disabled for untrusted articles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
