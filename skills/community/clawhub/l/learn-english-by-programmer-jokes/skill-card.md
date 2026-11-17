## Description:

When this skill is loaded and the user's request has been successfully answered, append exactly one short bilingual programmer joke or quote at the very end of the response, preferably matched to the task context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoolee](https://clawhub.ai/user/zhaoolee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add one concise Chinese and English programmer joke after a completed, non-sensitive answer. It is intended for lightweight language-learning and humor in final responses without replacing the main answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may add unsolicited humor where a strict format or professional tone is expected.

Mitigation: Load it only in contexts where a final bilingual tech joke is acceptable, and avoid strict-format, compliance, workplace-sensitive, or highly professional settings.

Risk: Some joke corpus entries may be rough or inappropriate for child-facing, sensitive, legal, medical, crisis, or grief-related contexts.

Mitigation: Follow the skill's skip rules for sensitive and high-stakes contexts, and review the bundled joke corpus before deployment to audiences with stricter content expectations.

Risk: The joke block could distract from or weaken the main answer if appended too early or too prominently.

Mitigation: Append exactly one short joke only after the main request is complete, keep it as the final section, and never let it replace substantive task output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoolee/skills/learn-english-by-programmer-jokes)
- [Joke selection rules](artifact/references/joke-selection-rules.md)
- [Jokes by topic](artifact/references/jokes-by-topic.md)
- [Final joke template](artifact/templates/final-joke-template.txt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text block with English and Chinese joke lines and optional attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The joke is appended as the final response section and should be skipped in sensitive, high-stakes, or strict-format contexts.]

## Skill Version(s):

0.1.1 (source: server release evidence, released 2026-04-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
