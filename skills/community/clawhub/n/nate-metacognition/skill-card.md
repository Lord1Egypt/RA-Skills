## Description:

Self-reflection engine for AI agents. Extracts patterns from session transcripts into a weighted graph with Hebbian learning and time decay. Compiles a token-budgeted lens of active self-knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeycacciatore3](https://clawhub.ai/user/joeycacciatore3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain cross-session self-knowledge by extracting recurring patterns from transcripts, reinforcing or decaying insights, and compiling a compact metacognition lens for future agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent cross-session memory can preserve conversation-derived behavior rules that influence future agent responses.

Mitigation: Review generated insights before allowing them to shape future behavior, and periodically prune entries that are stale, incorrect, or sensitive.

Risk: The cron workflow can repeatedly add or reinforce self-reflection entries without direct review.

Mitigation: Enable scheduled runs only in trusted workspaces and require review of newly generated insights before continued use.

Risk: Security evidence reports that extracted text may be sent to an environment-chosen embeddings URL despite localhost-only claims.

Mitigation: Constrain EMBEDDINGS_URL to trusted local services, or leave embeddings disabled when processing sensitive content.

Risk: The extract command may read sensitive files if path restrictions and destination validation are not sufficient.

Mitigation: Avoid running extract on sensitive paths and restrict the workspace and readable memory paths before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/joeycacciatore3/skills/nate-metacognition)
- [Project Homepage](https://github.com/meimakes/metacognition)
- [OpenClaw](https://openclaw.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown lens, CLI text output, and JSON-backed memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes memory/metacognition.json and scripts/metacognition-lens.md; the compiled lens is token-budgeted.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
