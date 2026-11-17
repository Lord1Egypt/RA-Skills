## Description:

Generate, iterate, preview, export, and publish production-ready designs (landing pages, slide decks, reports, invoices, resumes, business cards, social cards, email newsletters, and 30+ formats) with NexDoc Design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amiyapatanaik](https://clawhub.ai/user/amiyapatanaik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, revise, preview, export, and publish design assets through NexDoc Design. It is intended for requests involving design layouts, decks, PDFs, pages, cards, reports, invoices, resumes, newsletters, and similar production-ready formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The desktop npx setup path can run an unpinned MCP server package while using an API key.

Mitigation: Prefer the remote OAuth MCP option when available; if the desktop path is required, pin and verify the package and expose only the minimum environment variables.

Risk: A compromised local MCP setup or leaked environment could expose NXD_API_KEY.

Mitigation: Avoid printing API keys, keep the key out of logs, and rotate NXD_API_KEY if compromise is suspected.

Risk: Publishing design output can make generated content publicly reachable.

Mitigation: Publish only after an explicit user request and review returned preview, job, run, and public URL details.

## Reference(s):

- [NexDoc Design homepage](https://nexdoc.design)
- [NexDoc REST API](https://api.nexdoc.design)
- [NexDoc MCP endpoint](https://mcp.nexdoc.design/mcp)
- [NexDoc dashboard and API keys](https://app.nexdoc.design)
- [ClawHub skill page](https://clawhub.ai/amiyapatanaik/skills/nexdoc-design)

## Skill Output:

**Output Type(s):** [guidance, markdown, API Calls, configuration]

**Output Format:** [Markdown guidance with service URLs, identifiers, and API or MCP workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to return preview, job, run, export, publish, status, and charge details when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
