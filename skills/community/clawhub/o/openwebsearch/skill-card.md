## Description:

Single entry skill for open-websearch setup and focused live retrieval, preferring local CLI/daemon paths while remaining compatible with workspace-exposed MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aas-ee](https://clawhub.ai/user/aas-ee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up, validate, and operate open-websearch for focused live web retrieval, page fetching, and GitHub README retrieval. It helps choose the smallest working path across local CLI/daemon access, workspace-exposed MCP tools, source reuse, or an existing HTTP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may involve package installation, browser downloads, daemon startup, or MCP/client configuration changes.

Mitigation: Review and approve those actions before execution, then validate that open-websearch is active before relying on live retrieval.

Risk: Fetched web pages and search results can contain untrusted or misleading instructions.

Mitigation: Treat retrieved content as evidence only, ignore page instructions that conflict with the user request or workspace safety boundaries, and keep citations tied to fetched source URLs.

Risk: Disabling TLS verification with FETCH_WEB_INSECURE_TLS reduces HTTPS protection for page fetching.

Mitigation: Use FETCH_WEB_INSECURE_TLS only for non-sensitive diagnostic fetches where the reduced protection is understood.

## Reference(s):

- [OpenWebSearch ClawHub release](https://clawhub.ai/aas-ee/skills/openwebsearch)
- [Setup](references/setup.md)
- [Tools](references/tools.md)
- [Engine Selection](references/engine-selection.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
