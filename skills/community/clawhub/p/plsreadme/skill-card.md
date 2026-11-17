## Description:

Shares markdown files and text as clean, readable web links through plsreadme.com using the plsreadme MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[facundolucci](https://clawhub.ai/user/facundolucci)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn README files, PRDs, proposals, notes, or generated markdown/plain text into shareable readable web pages after confirming the content can be public.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local markdown or text may be uploaded to a permanent public link.

Mitigation: Require explicit user confirmation before every upload and avoid sharing sensitive notes, PRDs, proposals, internal documents, or files selected by path unless public release is intended.

Risk: The setup instructions use an unpinned MCP package invocation.

Mitigation: Prefer a pinned, reviewed MCP server version or the constrained remote endpoint before enabling the skill.

## Reference(s):

- [plsreadme MCP endpoint](https://plsreadme.com/mcp)
- [ClawHub skill page](https://clawhub.ai/facundolucci/skills/plsreadme)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses containing a readable URL and raw markdown URL, plus MCP setup snippets when configuration is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploaded content is published as a permanent, publicly accessible link; documented maximum file size is 200KB.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
