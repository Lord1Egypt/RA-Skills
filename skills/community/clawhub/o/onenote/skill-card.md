## Description:

Manage OneNote notebooks, sections, pages, and page content via Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a Microsoft account through ClawLink and manage OneNote notebooks, sections, pages, and HTML page content from an agent chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and allowlist an unpinned external ClawLink plugin that handles Microsoft OAuth tokens and OneNote data.

Mitigation: Install only if the user trusts ClawLink and the ClawHub plugin distribution, review Microsoft OAuth consent permissions before connecting, and revoke the Microsoft connection or remove the plugin when it is no longer needed.

Risk: The skill can create, update, copy, or delete OneNote notebooks, sections, pages, and page content.

Mitigation: Confirm the target resource and intended effect before every write or delete operation, and use preview or describe steps for unfamiliar or ambiguous tools.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/onenote)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=onenote-notes)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [Microsoft Graph OneNote API Overview](https://learn.microsoft.com/en-us/graph/api/resources/onenote)
- [Microsoft Graph Notebook Resource](https://learn.microsoft.com/en-us/graph/api/resources/notebook)
- [Microsoft Graph Page Resource](https://learn.microsoft.com/en-us/graph/api/resources/page)
- [Microsoft Graph Section Resource](https://learn.microsoft.com/en-us/graph/api/resources/section)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown, HTML]

**Output Format:** [Markdown with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OneNote page creation and updates require valid HTML content.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
