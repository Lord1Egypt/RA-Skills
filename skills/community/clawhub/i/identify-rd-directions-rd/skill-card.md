## Description:

Convert a concrete engineering, scientific, manufacturing, or technical project requirement into evidence-backed R&D directions, including requirement analysis, bounded technical issues, research questions, tasks, targets, deliverables, patent and literature evidence, standards and engineering cases, relevant organizations, search logs, and synchronized Markdown and HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Engineers, R&D teams, and technical reviewers use this skill to decompose concrete project requirements into evidence-backed research directions, validation tasks, and report artifacts. It is suited for R&D direction planning, not legal, patentability, freedom-to-operate, safety, regulatory, investment, or funding decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled renderer writes report files and may overwrite intended outputs when overwrite behavior is enabled.

Mitigation: Run the skill only in a trusted output directory that untrusted users cannot write to, and use overwrite behavior only for exact target files that are intended to be replaced.

Risk: Generated Markdown may preserve payload-derived Markdown constructs that could mislead readers or unsafe viewers.

Mitigation: Review generated Markdown before sharing and open it with a sanitizing viewer.

Risk: Security evidence marks the release as suspicious because file-writing and Markdown-safety issues remain unresolved.

Mitigation: Review the skill before installing it in automated or privileged environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/identify-rd-directions-rd)
- [PatSnap Advanced Patent Search MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-search)
- [PatSnap Patent Briefing MCP](https://open.patsnap.com/marketplace/mcp-servers/patent-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, guidance]

**Output Format:** [Validated JSON payload with synchronized Markdown and self-contained HTML reports plus concise handoff text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are deterministic views of one reviewed canonical payload; external searches are used only when requested and available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
