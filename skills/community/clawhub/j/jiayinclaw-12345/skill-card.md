## Description: <br>
从网页 URL 中提取页面标题、元描述、正文、图片链接和外部链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuishouxinboda](https://clawhub.ai/user/shuishouxinboda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to extract readable content and link metadata from public webpages for archiving, content review, aggregation, or downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to user-provided URLs, which can expose sensitive URLs or access private/internal services if misused. <br>
Mitigation: Use it only with intended public URLs, avoid localhost, private-network services, internal dashboards, and URLs containing secrets, and run it in an isolated Python environment. <br>
Risk: The skill depends on Python packages for HTTP fetching and HTML parsing. <br>
Mitigation: Install dependencies in an isolated environment and prefer pinned, reviewed dependency versions before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuishouxinboda/jiayinclaw-12345) <br>
- [API Reference](references/api-reference.md) <br>
- [Installation Guide](references/installation.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [Structured JSON by default, with optional plain-text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source URL, title, meta description, cleaned content, image URLs, external links, extraction timestamp, and summary counts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
