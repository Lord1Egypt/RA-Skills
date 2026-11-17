## Description:

Search open-access research papers by keyword and retrieve full metadata including title, authors, abstract, and full text by CORE ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to search CORE open-access research papers and retrieve paper metadata or full text through the configured MCP connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are routed through the pipeworx.io MCP gateway.

Mitigation: Avoid submitting confidential research topics, proprietary prompts, credentials, or personal data unless the gateway operator and its relationship to CORE are verified.

Risk: The skill has a low-trust quality assessment and is marked for quarantine review in the server evidence.

Mitigation: Review the artifact and deployment configuration before listing or installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-core-research)
- [CORE API endpoint](https://api.core.ac.uk/v3)
- [Pipeworx CORE research MCP gateway](https://gateway.pipeworx.io/core-research/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses containing research paper titles, authors, abstracts, full text, and related metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on CORE API availability and the configured pipeworx.io MCP gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
