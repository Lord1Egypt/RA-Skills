## Description:

Import question decks, retain attempts and review dates, summarize practice and export answer-hidden queues. Use for Study Coach and Mistake Review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External learners use the skill to build or import question decks, practice one question at a time, record attempts and feedback, review due items, and prepare answer-hidden study queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved study records may contain private information; hiding answers in an export does not encrypt the stored deck.

Mitigation: Use the intended workspace and keep saved study records and exports private.

Risk: This review covers the bundled release, not future installer versions, the optional connected assistant, or the host model's handling of study content.

Mitigation: Prefer a reviewed installer version over @latest and consider how connected services and the host model handle study content.

## Reference(s):

- [Input contract](references/input.md)
- [README and usage guide](README.md)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-study-coach)
- [MochiLab assistant setup](https://mochilab.bz/Skills/Connect.aspx?lang=en)

## Skill Output:

**Output Type(s):** [Guidance, Text, Analysis, Markdown, CSV]

**Output Format:** [Conversational study prompts and feedback, plus Markdown review plans and CSV review queues]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports omit answers by default; saved study records persist in the active workspace.]

## Skill Version(s):

1.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
