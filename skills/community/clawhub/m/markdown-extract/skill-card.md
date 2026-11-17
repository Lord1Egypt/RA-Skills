## Description:

Extract clean Markdown from a supplied URL using the markdown.new API with auto, AI, or browser extraction methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aviclaw](https://clawhub.ai/user/aviclaw)

### License/Terms of Use:


## Use Case:

Developers and content workflows use this skill to convert web pages into clean Markdown for downstream reading, summarization, editing, or documentation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied target URLs are sent to markdown.new for extraction.

Mitigation: Avoid using the skill with private intranet pages, localhost services, cloud metadata endpoints, presigned links, or URLs containing tokens or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aviclaw/skills/markdown-extract)
- [Publisher profile](https://clawhub.ai/user/aviclaw)
- [markdown.new API endpoint](https://markdown.new/)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON]

**Output Format:** [JSON response containing extracted Markdown on success or an error message on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports auto, ai, and browser extraction methods; network requests are sent to markdown.new.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
