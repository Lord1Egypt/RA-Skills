## Description:

Create and manage modular portable database pods (SQLite + metadata + embeddings). Includes document ingestion with embeddings for semantic search. Full automation - just ask.

This skill is ready for commercial/non-commercial use.

## Publisher:

[init-v](https://clawhub.ai/user/init-v)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to create local SQLite-backed knowledge pods, ingest documents, run text or semantic search, and export selected pod data for sharing or LLM context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised consent protections are not enforced for all pod operations.

Mitigation: Review every command before execution and manually confirm that the requested pod and agent access are intended.

Risk: Pod exports and LLM-ready Markdown can contain the full sensitive contents of a selected pod.

Mitigation: Avoid health, personal, client, or confidential data until clearer export warnings and sharing controls are added; treat exported files as sensitive.

Risk: Archive import and pod-name handling have weak safeguards.

Mitigation: Import only trusted .vpod files and verify destination names and paths before running import commands.

Risk: Raw SQL query controls are available.

Mitigation: Prefer text and semantic search; run SQL only after reviewing the statement and limiting access to non-sensitive pods.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/init-v/skills/initv-data-pods)
- [Data Pods GitHub repository](https://github.com/init-v/data-pods)
- [Agent Consent Layer Technical Spec](REFERENCES/consent-layer-spec.md)
- [Data Pods Usage Reference](references/usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local SQLite pod directories, .vpod archives, zip exports, and LLM-ready Markdown exports.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
