## Description:

Knowledge Bridge ingests, categorizes, deduplicates, summarizes, searches, explains, and backfills insight records into a local knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base maintainers use this skill to move insight-engine records into a local SQLite and LlamaIndex knowledge base, then inspect stored knowledge through ingestion, search, statistics, backfill, and explanation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports local Python code from a db directory outside the artifact, so the executed backend may not match the reviewed release files.

Mitigation: Install only when the local backend module is trusted and verify the imported knowledge_bridge.py before running the skill.

Risk: Ingest and backfill actions can bulk-write records into a persistent SQLite knowledge database.

Mitigation: Back up the knowledge database, confirm the referenced db directory is controlled, and run ingest or backfill only when permanent additions are intended.

## Reference(s):

- [Bilibili: Diffusion Schrodinger Bridge explainer](https://www.bilibili.com/video/BV1dsYieMEvj)
- [Bilibili: Knowledge-Driven Perception webinar](https://www.bilibili.com/video/BV12z4y1a775)
- [ClawHub skill page](https://clawhub.ai/534422530/skills/knowledge-bridge)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON-compatible results with concise status, count, search result, statistics, or explanation fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands include ingest, stats, backfill, search <query>, and explain <term>.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
