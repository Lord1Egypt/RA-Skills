## Description:

一个智能Logo提取和处理的MCP服务器，支持从网站URL自动识别并提取Logo图标，并提供图像处理和矢量转换功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to extract a site's best logo URL or analyze logo attributes such as size, format, and quality through the XiaoBenYang remote API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls a remote API, so website URLs and request parameters may be sent to an external service.

Mitigation: Review what data is sent before use and avoid submitting sensitive or restricted URLs.

Risk: The API key may be stored in plaintext in a local .env file.

Mitigation: Use a limited-scope XiaoBenYang API key, avoid high-value credentials, and prefer a secret store or session-only configuration when available.

Risk: Code and documentation contain inconsistent references, including unrelated gaokao naming.

Mitigation: Review the skill behavior and remove unrelated references before normal deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/logo-analyze)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown summary of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and returns raw remote API data for user-facing summarization.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
