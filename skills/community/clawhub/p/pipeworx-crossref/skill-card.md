## Description:

Search academic papers by keyword, look up metadata by DOI, and fetch journal info via Crossref.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and research-support teams use this skill to search scholarly works, verify DOI metadata, retrieve journal details, and support bibliography or citation-analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented client setup runs an unpinned npm package at install or runtime.

Mitigation: Pin mcp-remote to a reviewed exact version before deploying the skill.

Risk: Queries are sent through a hosted gateway and may expose sensitive research interests or confidential citation data.

Mitigation: Use the skill only in a restricted environment and avoid sending sensitive or confidential queries through the gateway.

## Reference(s):

- [Pipeworx Crossref homepage](https://pipeworx.io/packs/crossref)
- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-crossref)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Markdown, JSON]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns Crossref search results and metadata through MCP tool calls; requires curl for the documented direct request example.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
