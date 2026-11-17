## Description:

Knowledge Vault helps an agent ingest URLs and documents, summarize key points, save structured entries in a local searchable vault, and recall saved knowledge later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn saved web links, videos, PDFs, repositories, and other content into structured digests, searchable local vault entries, collections, read-later queues, exports, and memory-backed recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can overwrite existing vault data during initialization.

Mitigation: Back up existing vault files before setup and review SETUP-PROMPT.md before running any initialization steps.

Risk: Setup trusts a locally discovered skill path before loading files.

Mitigation: Use an explicit trusted skill path and verify it before copying configuration, scripts, or reading skill instructions.

Risk: Vault files and memory summaries may retain confidential or regulated content.

Mitigation: Avoid ingesting sensitive content unless local storage and host memory retention are acceptable, and redact sensitive values before memory writes.

Risk: The dashboard companion spec includes destructive routes before complete access-control and recovery behavior is defined.

Mitigation: Treat the dashboard as incomplete until authentication, authorization, confirmation, and recovery behavior are implemented and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/normieclaw-knowledge-vault)
- [Nollio publisher profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Security audit](artifact/SECURITY.md)
- [Setup prompt](artifact/SETUP-PROMPT.md)
- [Dashboard companion kit spec](artifact/dashboard-kit/DASHBOARD-SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with JSON data files, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local vault JSON files, export Markdown files, and long-term memory summaries when enabled by the host platform.]

## Skill Version(s):

1.0.3 (source: evidence.release.version; changelog notes v1.0.3 security fixes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
