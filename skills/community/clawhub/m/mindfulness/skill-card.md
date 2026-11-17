## Description:

Track mindfulness habits, run guided meditations, and improve calm focus with adaptive routines, reflective logs, and context-aware practice plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to run short guided mindfulness practices, track sessions, and receive adaptive recommendations for building a sustainable routine. It supports coaching and habit formation, not clinical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mindfulness session logs, state ratings, routine plans, and recommendation notes may be retained locally in ~/mindfulness/.

Mitigation: Confirm local file writes before saving, limit stored details to practice-relevant information, and adjust setup preferences for activation and proactive suggestions.

Risk: Mindfulness coaching can be misread as clinical support during severe distress or crisis.

Mitigation: Keep the skill scoped to practice support and direct crisis, self-harm risk, or severe distress to immediate professional or emergency support.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/mindfulness)
- [Setup and activation flow](artifact/setup.md)
- [Memory structure and templates](artifact/memory-template.md)
- [Practice modes](artifact/practice-modes.md)
- [Session log template](artifact/session-log-template.md)
- [Guided meditations](artifact/guided-meditations.md)
- [Recommendation rules](artifact/recommendation-rules.md)
- [Reflection prompts](artifact/reflection-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured session logs, routine plans, reflections, and recommendation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only skill; optional local mindfulness notes are stored only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
