## Description:

Skill Extractor helps an agent identify reusable procedures from completed multi-step conversations, draft SKILL.md files, save them locally, and search or suggest related skills later.

This skill is ready for commercial/non-commercial use.

## Publisher:

[livangy](https://clawhub.ai/user/livangy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill after completing complex tasks to turn useful workflows into reusable skill documents and retrieve related local skills for future tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived instructions may be persisted into reusable skills without enough sanitization or retention controls.

Mitigation: Review generated skills before saving or reusing them, avoid conversations containing secrets or private data, and delete old generated skills and indexes when no longer needed.

Risk: Generated skills may contain incorrect, misleading, or unsafe procedures if treated as approved guidance immediately.

Mitigation: Treat extracted skills as drafts until they are manually reviewed, sanitized, and approved for reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/livangy/skills/niuniu-skill-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown skill drafts, JSON analysis/search results, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated skill drafts and a local search index when invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
