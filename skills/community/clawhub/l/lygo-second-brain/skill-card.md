## Description:

LYGO Second Brain helps agents operate a local Obsidian and Ollama knowledge vault for ingesting sources, indexing and searching notes, building consensus, and generating wiki pages from vault content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to maintain a local second-brain workflow over an Obsidian-style markdown vault with Ollama-based inference. It supports requested vault ingest, indexing, semantic search, consensus checks, and wiki page generation while keeping push, publish, remote inference, and permaweb actions gated by explicit user consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact depends on mutable package execution and external Python code outside the artifact.

Mitigation: Install in a constrained environment only after verifying the ClawHub package version and the intended lygo-protocol-stack checkout.

Risk: Vault notes may contain secrets or PII and can be committed locally by the workflow.

Mitigation: Treat LYGO_VAULT_ROOT as sensitive, avoid storing secrets in notes, and review content before committing or sharing.

Risk: Push, publish, remote inference, and permaweb actions can expose private vault content or move data outside the local environment.

Mitigation: Keep local Ollama as the default and require explicit user request before push, publish, remote inference, or permaweb actions.

Risk: PDF ingest invokes pdftotext on supplied documents.

Mitigation: Ingest PDFs only from trusted sources and prefer constrained execution for document processing.

## Reference(s):

- [Agent Contract](references/AGENT_CONTRACT.md)
- [Security Guidance](references/SECURITY.md)
- [LYGO Protocol Stack Repository](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [ClawHub Skill Page](https://clawhub.ai/deepseekoracle/skills/lygo-second-brain)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local vault operations that write to LYGO_VAULT_ROOT when the user requests them.]

## Skill Version(s):

1.0.0 (source: skill metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
