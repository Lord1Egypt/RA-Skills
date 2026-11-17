## Description:

Publishes Markdown to a public URL and returns the link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuvadm](https://clawhub.ai/user/yuvadm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agents use this skill to publish Markdown content to a public hosted page and return the resulting link. It is appropriate when the user explicitly wants to share, publish, host, or receive a link for Markdown content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown content can be sent to a public third-party URL that is hard to change after publishing.

Mitigation: Before publishing, verify that the file contains no secrets, private data, customer information, or confidential material, and require explicit confirmation before running the curl command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuvadm/skills/markdown-publish)
- [markdown.page agent guide](https://markdown.page/llms.txt)
- [markdown.page API reference](https://markdown.page/api.md)
- [markdown.page FAQ](https://markdown.page/faq.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and returned URL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes content to a public URL and may report service errors such as malformed content, oversized pages, unsupported content type, or rate limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
