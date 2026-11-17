## Description:

Fetch clean, agent-optimized Markdown from any URL using the markdown.new service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thendcn](https://clawhub.ai/user/thendcn)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve cleaner, token-efficient Markdown from public web pages when normal fetch or browser tools produce noisy or incomplete content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested URLs and resulting page content are handled by the third-party markdown.new service.

Mitigation: Use the skill for public pages only; avoid internal sites, authenticated pages, presigned URLs, API tokens in query strings, and confidential documents.

## Reference(s):

- [Mdnew skill page](https://clawhub.ai/thendcn/skills/mdnew)
- [markdown.new service](https://markdown.new)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Text]

**Output Format:** [Markdown text with an optional estimated token count line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches URL content through markdown.new and may include an x-markdown-tokens estimate when returned by the service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
