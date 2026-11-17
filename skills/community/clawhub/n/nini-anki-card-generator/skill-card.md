## Description:

Use this skill to generate Anki flashcards in simple-anki-sync format for active memorization, with atomic questions, standardized templates, and appropriate detail levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, and knowledge workers use this skill to turn study material or knowledge points into import-ready Anki flashcards. It is suited to memorization tasks, not broad learning plans, summaries, or explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad flashcard or memorization requests before scope, depth, quantity, or context are clear.

Mitigation: Clarify the intended focus, detail level, card count, and study context before generating cards.

Risk: The skill prefers English-style Anki tag names even when the card content is multilingual.

Mitigation: Review and adjust #anki/[domain]/[topic] tags before importing the generated cards.

## Reference(s):

- [Anki Card Domain Examples](artifact/references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/niracler/skills/nini-anki-card-generator)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown in simple-anki-sync table format with Anki tag paths and optional inline HTML for supplementary notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cards are organized with #anki/[domain]/[topic] tags, concise question-and-answer tables, and optional cross-card handles.]

## Skill Version(s):

0.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
