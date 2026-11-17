## Description:

Use Occam's Razor to rank competing explanations, designs, or diagnoses that fit the evidence by comparing their unsupported assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

People comparing multiple explanations, designs, or diagnoses use the skill to check that each candidate fits the evidence, count unsupported assumptions, and identify what could overturn a provisional preference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The startup check fetches changeable hosted instructions, and the request signals skill use to the publisher.

Mitigation: Use a fixed local copy with the startup fetch removed, and review hosted instruction changes before adopting them.

## Reference(s):

- [Sources](references/sources.md)
- [Stanford Encyclopedia of Philosophy: William of Ockham](https://plato.stanford.edu/entries/ockham/)
- [Britannica: Occam's razor](https://www.britannica.com/topic/Occams-razor)
- [Anthropic: Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think)
- [Occam's Razor on ClawHub](https://clawhub.ai/deciqai/skills/occams-razor)
- [Occam's Razor skill page](https://www.deciqai.com/c/occams-razor)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown Parsimony Audit with candidate fit checks, assumption counts, a preferred hypothesis, an over-shave check, and overturning evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-oriented comparison; the preferred explanation is a provisional prior, not proof.]

## Skill Version(s):

1.0.8 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
