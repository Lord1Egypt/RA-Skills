## Description:

Detect AI-generated content and humanize it to sound natural.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyt84](https://clawhub.ai/user/fyt84)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to draft, check, humanize, and verify text with the humantext.pro MCP service. It is intended for workflows where users need a content quality report and revised natural-sounding text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text is sent to a third-party service for detection and humanization.

Mitigation: Do not process confidential, regulated, personal, legal, or proprietary text unless humantext.pro's data handling is acceptable.

Risk: The workflow can be used to misrepresent authorship or bypass disclosure rules.

Mitigation: Use it only where content policies, academic rules, platform rules, and workplace disclosure requirements permit this kind of rewriting.

Risk: The MCP server is installed through an unpinned npx package.

Mitigation: Pin and review the @humantext/mcp-server package before running it.

Risk: The skill requires a HUMANTEXT_API_KEY secret.

Mitigation: Protect the API key, avoid logging it, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fyt84/skills/humantext-content-pipeline)
- [humantext.pro](https://humantext.pro)
- [humantext.pro API docs](https://humantext.pro/api/docs)
- [humantext MCP server package](https://www.npmjs.com/package/@humantext/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with prose, reports, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-detection scores, humanized text, credit-use notes, and setup guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
