## Description:

Generates content draft variations by analyzing reference content, extracting reusable writing patterns, gathering user context, and producing markdown outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and writing-focused agents use this skill to model new articles, posts, or social content on supplied reference examples while preserving a structured drafting workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied URLs may be fetched and X/Twitter links may be routed through a third-party API.

Mitigation: Use public reference material, prefer pasted content or direct non-X/Twitter URLs when privacy matters, and avoid sensitive or private links.

Risk: Fetched web content is reused in generated prompts and drafts without clearly defined safety boundaries.

Mitigation: Review generated meta-prompts and drafts before reuse, especially when source material could be copyrighted, misleading, private, or brand-sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-content-draft-generator)
- [Publisher profile](https://clawhub.ai/user/marjoriebroad)
- [Content Deconstructor](references/content-deconstructor.md)
- [Content Anatomy Generator](references/content-anatomy-generator.md)
- [Content Context Generator](references/content-context-generator.md)
- [Meta Prompt Generator](references/meta-prompt-generator.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text and timestamped markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces content breakdowns, anatomy guides, context questions, meta-prompts, and final draft variations as separate markdown artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
