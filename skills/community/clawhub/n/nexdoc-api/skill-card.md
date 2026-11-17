## Description:

Generate, iterate, preview, export, and publish production-ready designs across landing pages, slide decks, reports, invoices, resumes, business cards, social cards, email newsletters, and other formats by calling the NexDoc Design REST API with an NXD_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amiyapatanaik](https://clawhub.ai/user/amiyapatanaik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to call the NexDoc Design API when they need to create, edit, preview, export, or publish generated design assets programmatically and no NexDoc MCP tools are connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design text, instructions, and selected files are sent to NexDoc.

Mitigation: Use the skill only when that data transfer is acceptable, and avoid sending secrets or regulated data unless policy permits it.

Risk: The skill depends on an NXD_API_KEY credential.

Mitigation: Keep the API key private, do not print it in responses or logs, and direct users to the NexDoc key page when a key is missing.

Risk: Generated designs can be made public through the publish endpoint.

Mitigation: Publish only after an explicit user request and report the resulting public URL when publishing is requested.

## Reference(s):

- [NexDoc Design API endpoint reference](artifact/reference.md)
- [NexDoc Design](https://nexdoc.design)
- [NexDoc API keys](https://app.nexdoc.design/keys)
- [NexDoc API base endpoint](https://api.nexdoc.design)
- [ClawHub skill page](https://clawhub.ai/amiyapatanaik/skills/nexdoc-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request bodies, job and run identifiers, preview URLs, export download URLs, publish URLs when explicitly requested, status, charge information, and error details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
