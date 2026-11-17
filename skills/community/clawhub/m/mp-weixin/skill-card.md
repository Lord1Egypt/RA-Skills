## Description:

mp-weixin helps agents use Python scripts to extract metadata and body content from WeChat Official Account article URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse mp.weixin.qq.com article links, collect article metadata, and convert article content into structured data for archiving, monitoring, or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make network requests from the user's environment and does not enforce its stated WeChat-only URL scope.

Mitigation: Run it in an isolated environment and provide only intended mp.weixin.qq.com article URLs.

Risk: The skill documentation discusses CAPTCHA and anti-bot workarounds.

Mitigation: Do not use logged-in cookies or attempt to bypass CAPTCHA or platform anti-bot controls.

Risk: Extracted article content may be copied to /tmp/wechat_article.json.

Mitigation: Treat that file as copied article data and remove, relocate, or protect it according to the intended retention policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/mp-weixin)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [Beautiful Soup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests documentation](https://docs.python-requests.org/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Code]

**Output Format:** [Markdown guidance with bash and Python examples; extractor results are returned as structured JSON and summarized as terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The direct extractor script can write copied article data to /tmp/wechat_article.json.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
