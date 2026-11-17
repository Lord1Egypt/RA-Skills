## Description:

Generate, iterate, preview, and export production-ready designs, including landing pages, slide decks, reports, invoices, resumes, business cards, social cards, email newsletters, and 30+ formats, through the NexDoc Design MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amiyapatanaik](https://clawhub.ai/user/amiyapatanaik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agent users use this skill to create, revise, preview, export, and optionally publish NexDoc-generated design deliverables from concise content and design briefs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Desktop stdio setup may run an unpinned npm MCP server.

Mitigation: Prefer the remote OAuth MCP endpoint when available; if stdio is required, verify or pin the npm package version before running it.

Risk: Design workflows can upload sensitive documents, photos, resumes, invoices, contracts, or similar files to NexDoc infrastructure.

Mitigation: Upload only files the user intentionally provides for the design task and treat those files as shared with NexDoc.

Risk: API keys used with stdio MCP can be exposed if printed, echoed, or stored carelessly.

Mitigation: Keep NXD_API_KEY scoped and rotated, and avoid printing or echoing the key.

Risk: Publishing or email notification can disclose generated design content beyond the immediate session.

Mitigation: Use email notification or publishing only when the user explicitly requests it.

## Reference(s):

- [NexDoc Design](https://nexdoc.design)
- [NexDoc Remote MCP Endpoint](https://mcp.nexdoc.design/mcp)
- [NexDoc API Keys](https://app.nexdoc.design/keys)
- [ClawHub Skill Page](https://clawhub.ai/amiyapatanaik/skills/nexdoc-mcp)
- [ClawHub Publisher Profile](https://clawhub.ai/user/amiyapatanaik)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, Files]

**Output Format:** [Markdown guidance with JSON MCP configuration examples, shell command snippets, MCP tool-call instructions, and returned preview or export links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce design previews, exported PDF/HTML/PNG files, email notifications, or public links through NexDoc tools when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
