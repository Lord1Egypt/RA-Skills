## Description:

Deploy LightRAG as a shared knowledge graph for OpenClaw agents, enabling cross-agent knowledge queries, daily log indexing, and entity relationship search when memory_search is not enough.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to deploy and operate a shared LightRAG knowledge graph across multiple agent workspaces. It helps agents query historical decisions, cross-agent findings, and entity relationships from indexed logs and documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Centralizing multiple agents' memory into a persistent graph can expose sensitive or private information across workspaces.

Mitigation: Use explicit file allowlists, skip profile, private, security, and trading logs unless reviewed, and define deletion and access-control procedures before indexing real data.

Risk: Indexed text may be processed by an OpenAI-compatible provider when non-local models are configured.

Mitigation: Prefer local models for sensitive data and review provider settings before sending logs, documents, or agent memory to an external service.

Risk: Optional daily auto-indexing can continuously ingest new logs without human review.

Mitigation: Disable the cron job by default or restrict it to reviewed paths with clear retention and deletion procedures.

Risk: Using a floating container image tag can pull unreviewed runtime changes.

Mitigation: Pin the LightRAG container image to a reviewed digest before production use.

## Reference(s):

- [Skill README](artifact/README.md)
- [ClawHub Skill Page](https://clawhub.ai/mosoonpi-ai/skills/lightrag-knowledge-base)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Docker Compose, environment configuration, Python scripts, Bash commands, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment steps, query and insert scripts, optional cron auto-indexing, monitoring checks, and security guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
