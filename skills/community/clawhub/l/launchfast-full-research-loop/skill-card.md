## Description:

Complete Amazon FBA product research pipeline using the LaunchFast MCP that runs product research, IP checks, supplier sourcing, and PPC keyword research, then compiles the findings into a downloadable HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockchainhb](https://clawhub.ai/user/blockchainhb)

### License/Terms of Use:


## Use Case:

External Amazon FBA sellers and marketplace analysts use this skill to run a full product opportunity workflow from a product keyword, including market research, IP risk checks, supplier sourcing, PPC keyword research, and a shareable HTML report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include product titles, supplier names, keywords, or other returned text from external research results.

Mitigation: Escape returned research text as plain text before writing the standalone HTML report.

Risk: The report is saved to a user-selected local path and could overwrite or expose sensitive files if the path is chosen carelessly.

Mitigation: Use a non-sensitive output path and confirm the destination before saving or sharing the report.

Risk: The workflow depends on LaunchFast MCP tools for market, IP, supplier, and keyword data.

Mitigation: Install only when those tools are trusted and available, and review generated findings before making business or legal decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates and summary plus a standalone HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the LaunchFast MCP tools for product research, IP checks, supplier sourcing, and Amazon keyword research.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
