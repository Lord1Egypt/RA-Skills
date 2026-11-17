## Description:

Meta Knowledge Base helps agents build, organize, search, and query a local knowledge base from conversations, documents, files, URLs, and other user-provided content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create a local knowledge base, ingest selected content, perform semantic or hybrid search, and answer questions with source snippets from retained knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic capture and durable local storage may retain conversations or files beyond user expectations.

Mitigation: Enable ingestion only for explicitly approved sources, document consent expectations, and define retention or deletion practices before use.

Risk: The knowledge base may store secrets, credentials, private mailboxes, or broad home-directory content if pointed at sensitive locations.

Mitigation: Exclude sensitive paths and data classes, review inputs before ingestion, and avoid using the tool for confidential material unless appropriate controls are in place.

Risk: Dependency installation from broad package names may introduce supply-chain or environment risk.

Mitigation: Install in an isolated environment and use pinned, reviewed package versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/meta-knowledge-base)
- [Publisher profile](https://clawhub.ai/user/jason-aka-chen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local knowledge-base APIs and example usage for ingestion, search, Q&A, graph access, export, and management.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
