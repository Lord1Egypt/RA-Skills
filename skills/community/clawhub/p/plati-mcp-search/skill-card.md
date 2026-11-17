## Description:

Find cheapest reliable subscription offers from Plati using the local MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rybnikov](https://clawhub.ai/user/rybnikov)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Plati marketplace listings for low-cost subscription offers, compare seller reliability, and return concise linked options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an unpinned third-party npm MCP server whose code is not included in the skill artifact.

Mitigation: Pin and verify the MCP package before use, inspect its source and publisher, avoid global installation when possible, and run it with limited filesystem and credential access.

Risk: Marketplace results are raw offer data that may be incomplete, stale, or mismatched to the user's intended plan or duration.

Mitigation: Apply explicit plan, duration, account-type, price, and seller filters in the agent response, and include direct listing links so users can verify offers before purchase.

Risk: The artifact's final response template is Russian by default.

Mitigation: Adapt the final response language to the user's locale or request while preserving the required concise numbered-list structure.

## Reference(s):

- [Plati MCP Search on ClawHub](https://clawhub.ai/rybnikov/skills/plati-mcp-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown, typically a short numbered list with direct listing links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final user messages avoid markdown tables and code blocks; results should state filters used and include direct lot links when available.]

## Skill Version(s):

0.1.6 (source: server release metadata, released 2026-02-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
