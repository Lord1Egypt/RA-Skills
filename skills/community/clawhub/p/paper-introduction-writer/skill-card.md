## Description:

Helps researchers draft, revise, outline, or annotate academic paper introductions using Glasman-Deal's four-component, eleven-sentence model, with support for English drafts and Chinese functional annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junwugit](https://clawhub.ai/user/junwugit)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, graduate students, and academic writers use this skill to plan, draft, revise, or diagnose research-paper introductions. It is especially suited to bilingual workflows that need English introduction text plus Chinese paragraph and sentence function annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A complete-generation task may create English and Chinese Markdown drafts in the current working directory.

Mitigation: For sensitive unpublished research or controlled workspaces, request inline-only output, a specific output path, or a single-language draft.

Risk: Generated drafts can include citation placeholders or practice-only fake references when the user requests an exercise mode.

Mitigation: Review and replace all citation placeholders before reuse, and do not use practice-only fake references in real submissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junwugit/skills/paper-introduction-writer)
- [Four-component model and eleven-sentence structure](references/model-structure.md)
- [Output format specification](references/output-format.md)
- [Discipline-specific introduction templates](references/templates.md)
- [Worked examples](references/examples.md)
- [Gap expression patterns](references/gap-patterns.md)
- [Language toolkit](references/language-toolkit.md)
- [Writing practice mode](references/writing-practice.md)
- [Reader-friendly writing tips](references/writing-tips.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown drafts, paragraph outlines, revision notes, diagnostics, and Chinese functional annotations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For full-generation tasks, the skill may write introduction_en.md and introduction_zh.md in the current working directory; for narrower requests, it can provide inline outlines, diagnostics, single-language drafts, or revision guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
