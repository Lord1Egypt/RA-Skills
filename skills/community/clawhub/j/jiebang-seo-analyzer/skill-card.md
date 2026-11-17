## Description:

网站SEO分析与元数据提取工具，可提取网页标题、描述、关键词、Open Graph、Twitter Card、canonical 等元信息，并执行SEO健康检查与优化建议生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebang-tools](https://clawhub.ai/user/jiebang-tools)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to analyze public webpages, extract page metadata, evaluate SEO health, and receive optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards full user-provided URLs to an external service.

Mitigation: Use only public webpages whose full URL, including path and query string, can safely be shared with www.jiebang.site.

Risk: Private dashboards, signed links, reset links, authenticated pages, internal hostnames, or URLs containing tokens could expose sensitive information.

Mitigation: Do not submit sensitive, internal, authenticated, or token-bearing URLs.

Risk: The security evidence reports use of an admin-style credential.

Mitigation: Review before installing; the publisher should document external processing and replace the admin-style credential with a narrower API token.

## Reference(s):

- [捷帮SEO分析 ClawHub release](https://clawhub.ai/jiebang-tools/skills/jiebang-seo-analyzer)
- [jiebang-tools publisher profile](https://clawhub.ai/user/jiebang-tools)
- [Jiebang SEO service](https://www.jiebang.site)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured JSON with metadata fields, SEO checks, scores, issues, and suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the target webpage, network availability, and the external SEO service.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
