## Description:

Fetch and save WeChat Official Account articles with full content and images, including image downloads, JSON export, and full-page screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to archive, save, or analyze WeChat Official Account articles. It supports single-article and batch capture workflows that preserve article text, metadata, images, and screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reaches remote sites and stores downloaded content from user-supplied article URLs.

Mitigation: Use a contained environment with restricted outbound network access, a quota-limited output directory, and verified HTTPS mp.weixin.qq.com article URLs.

Risk: The virtual-environment wrapper can run a caller-selected script path.

Mitigation: Avoid the arbitrary --script wrapper option and invoke the intended fetch.py or batch_fetch.py scripts directly.

Risk: Weak URL handling and broad helper scripts can reach or execute more than users expect.

Mitigation: Review the skill before installation, avoid running it as root, and test with a small set of known-good articles before batch use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/robertstarry-gif/skills/liuzln-openclaw-skills-wechat-article-fetcher)
- [Playwright Python documentation](https://playwright.dev/python/)
- [WeChat Open Platform](https://open.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command and Python examples; fetched article data is saved as JSON plus image and screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated outputs may include local article directories containing article.json, article.png, and downloaded image files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
