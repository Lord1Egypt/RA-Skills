## Description:

Record, organize, search, and connect personal knowledge with note templates, metadata extraction, search, and lightweight knowledge graph exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture, search, organize, summarize, and explore relationships in user-owned personal notes or supplied knowledge. It supports English and Chinese workflows for note capture, metadata extraction, search, review, and lightweight concept graph exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ingest action may be mistaken for durable storage.

Mitigation: Treat ingest results as draft note output unless the surrounding environment separately saves the returned draft.

Risk: Search or analysis can rely on local sample data when no user knowledge base is supplied.

Mitigation: Disclose when results come from the local sample/index and avoid claiming access to private notes unless supplied or connected by the environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/personal-knowledge-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Human-facing Markdown or structured JSON-like objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include note templates, tags, entities, ranked search results, summaries, review prompts, and lightweight graph connections.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill.json; frontmatter reports v0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
