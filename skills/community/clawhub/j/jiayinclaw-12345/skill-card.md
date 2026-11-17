## Description:

从网页URL中提取标题、正文、图片链接等内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuishouxinboda](https://clawhub.ai/user/shuishouxinboda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agents use this skill to fetch a web page and extract structured page content such as title, metadata, cleaned body text, image URLs, and outbound links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to arbitrary user-provided URLs, including private or internal network targets if the runtime permits them.

Mitigation: Run it with egress controls that block localhost, private network ranges, cloud metadata endpoints, intranet hosts, authenticated URLs, and redirects to those destinations.

Risk: Dependency declarations use lower bounds only, so installs may resolve newer package versions that were not reviewed with this release.

Mitigation: Pin and review dependency versions before production deployment.

## Reference(s):

- [API reference](references/api-reference.md)
- [Installation guide](references/installation.md)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The JSON output includes the source URL, page title, meta description, cleaned content, image URLs, links, extraction timestamp, and counts; content is capped at 5000 characters, images at 20, and links at 50.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
