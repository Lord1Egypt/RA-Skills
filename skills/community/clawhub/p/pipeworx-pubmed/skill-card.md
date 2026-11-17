## Description:

Search PubMed for biomedical articles by keyword, author, or MeSH term, and retrieve article metadata and structured abstracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to search PubMed, inspect article metadata, and retrieve abstracts for biomedical literature review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Biomedical searches may reveal sensitive health interests or unpublished research topics to a third-party gateway.

Mitigation: Use non-sensitive queries unless gateway.pipeworx.io is acceptable for the workflow, or use a direct official NCBI/PubMed workflow when sensitivity is a concern.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-pubmed)
- [Pipeworx PubMed MCP gateway](https://gateway.pipeworx.io/pubmed/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns PubMed IDs, article metadata, and abstract text with section labels.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
