## Description:

Connector-agnostic Postgres + pgvector memory ingestion and retrieval with incremental cursor history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosathanasoulis](https://clawhub.ai/user/marcosathanasoulis)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to initialize and operate a Postgres and pgvector memory layer that normalizes heterogeneous records, tracks incremental connector cursors, ingests JSON or connector data, and searches stored chunks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher can execute unbundled Python code from outside the reviewed skill while forwarding database credentials and the user environment.

Mitigation: Run it only in trusted projects after verifying the installed openclaw_memory package, and avoid exposing unrelated secrets in the process environment.

Risk: Database credentials and memory data may expose sensitive account or connector information.

Mitigation: Use dedicated least-privilege database credentials limited to the required memory tables and process only data you are authorized to store.

Risk: Custom connectors can introduce unreviewed data access or ingestion behavior.

Mitigation: Review and trust connector code before running it, then validate connector authentication and configuration before ingestion.

## Reference(s):

- [OpenClaw Universal Memory on ClawHub](https://clawhub.ai/marcosathanasoulis/skills/openclaw-universal-memory)
- [Scheduling reference](docs/SCHEDULING.md)
- [Connector setup walkthrough](docs/CONNECTOR_SETUP_WALKTHROUGH.md)
- [Connector contributing guide](docs/CONNECTOR_CONTRIBUTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides database setup, connector validation, ingestion, search, event inspection, and doctor checks.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
