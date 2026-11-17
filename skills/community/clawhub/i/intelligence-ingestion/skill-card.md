## Description:

Analyze and evaluate URLs, links, articles, tweets, and external information sources for strategic value, then classify, score, store structured notes in Obsidian, update a Strategic Landscape, and generate draft skills when new capabilities are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sarahmirrand001-oss](https://clawhub.ai/user/sarahmirrand001-oss)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agent operators use this skill to ingest URLs or pasted external content into a local knowledge workflow, producing strategic assessments, Obsidian notes, memory updates, landscape updates, and isolated draft skills for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent local knowledge-base and agent-memory changes from external content.

Mitigation: Test with a disposable or backed-up Obsidian vault first, then review created notes, memory entries, and landscape updates before relying on them.

Risk: Untrusted URLs or pasted content can be transformed into draft skills.

Mitigation: Keep generated skills in skills/_drafts, inspect them before activation, and scan or review each draft before moving it into an active skills directory.

Risk: URL ingestion may fetch external content and expand through fallback retrieval paths.

Mitigation: Avoid sensitive or untrusted URLs unless the operator is prepared to review the resulting local artifacts and any network-derived content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sarahmirrand001-oss/skills/intelligence-ingestion)
- [Model Context Protocol skill schema](https://spec.modelcontextprotocol.io/2025-03/skill.json)
- [Intelligence Ingestion homepage](https://intelligence-ingestion.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, draft skill definitions, configuration guidance, and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local notes, memory entries, Strategic Landscape updates, and draft skill files when configured.]

## Skill Version(s):

2.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
