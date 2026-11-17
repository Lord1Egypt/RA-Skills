## Description:

Converts standard Markdown text into Feishu Post rich-text message JSON, including headings, inline styles, links, mentions, images, lists, code blocks, blockquotes, and horizontal rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killingjacky](https://clawhub.ai/user/killingjacky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to convert Markdown content into Feishu Post JSON for rich-text Feishu messages and bot message payloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed Feishu at-mention input can cause conversion to hang.

Mitigation: Avoid exposing the converter directly to untrusted message input until the parser is fixed, or wrap execution with input size limits and timeouts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killingjacky/skills/markdown-to-feishu-post)

## Skill Output:

**Output Type(s):** [JSON, Code, Shell commands, Guidance]

**Output Format:** [Feishu Post JSON with optional Markdown usage guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts direct Markdown text or a Markdown file path; compact single-line JSON output is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
