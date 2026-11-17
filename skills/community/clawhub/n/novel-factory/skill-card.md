## Description:

Guides an agent through planning, drafting, and reviewing Chinese-language serialized web fiction while maintaining story-continuity notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingyu9495-source](https://clawhub.ai/user/lingyu9495-source)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and content creators use this skill to turn a story idea into an outline, volume plans, chapter drafts, continuity notes, and chapter reviews for Chinese-language web fiction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --clean initialization option can delete earlier generated Markdown drafts and reset story memory.

Mitigation: Back up drafts and notes before using --clean; omit the option when continuing an existing novel.

Risk: Locally stored drafts and story notes may contain private material.

Mitigation: Keep output/ and .learnings/ out of version control when their contents are private.

## Reference(s):

- [Novel Factory on ClawHub](https://clawhub.ai/lingyu9495-source/skills/novel-factory)
- [Prompt guide](references/prompt-guide.md)
- [Plot structures](references/plot-structures.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown drafts, plans, reviews, and continuity notes; optional Mermaid diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores chapter drafts in output/ and story memory in .learnings/.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
