## Description:

Million-word novel writing engine that turns long-form fiction into transactional writing, where each chapter is committed as prose plus declared state changes and checked against gates for forbidden zones, foreshadowing state, and prose-vs-state consistency before commit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT-0

## Use Case:

External authors, writing agents, and developers use this skill to draft or continue long-form fiction while preserving world state, character knowledge, object ownership, foreshadowing, and timeline consistency across chapters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance runs unpinned code fetched live from an external GitHub repository.

Mitigation: Inspect the referenced repository before use, prefer a pinned commit or signed release, and run it in a restricted environment without unnecessary credentials or private files exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongsheng123132/skills/origin-writer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces writing workflow guidance, transaction-file structure, state-management commands, and verification guidance for long-form fiction projects.]

## Skill Version(s):

1.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
