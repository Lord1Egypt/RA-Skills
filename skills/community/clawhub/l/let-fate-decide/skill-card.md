## Description:

Draws four Tarot cards with local randomness to break ties in vague, low-stakes planning and map the spread to practical next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kc0bfv](https://clawhub.ai/user/kc0bfv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill as a creative tie-breaker when a request is ambiguous, low-stakes, or explicitly asks to let fate decide. It should bias a choice among viable approaches, not replace requirements gathering, safety judgment, or deterministic reasoning when those are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-weight a random Tarot interpretation in security, production, data-loss, financial, legal, or other high-impact decisions.

Mitigation: Use the skill only for ambiguous, low-stakes planning and opt out when deterministic reasoning or expert judgment is required.

Risk: A failed entropy read or script error could tempt the agent to invent a draw.

Mitigation: Report the failure and skip the reading; do not simulate cards when the script cannot run.

Risk: Randomized guidance can reinforce an agent's pre-existing preference instead of clarifying the decision.

Mitigation: Treat the spread as a creative nudge, state how cards influenced the choice, and keep safety, requirements, and best practices authoritative.

## Reference(s):

- [Let Fate Decide Skill Page](https://clawhub.ai/kc0bfv/skills/let-fate-decide)
- [Interpretation Guide](references/INTERPRETATION_GUIDE.md)
- [Major Arcana Card Meanings](cards/major.md)
- [Wands Card Meanings](cards/wands.md)
- [Cups Card Meanings](cards/cups.md)
- [Swords Card Meanings](cards/swords.md)
- [Pentacles Card Meanings](cards/pentacles.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON draw result plus concise Markdown interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draw defaults to four cards; the script accepts an optional card count from 1 to 78.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
