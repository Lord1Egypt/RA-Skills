## Description:

Creates and compares one-change-at-a-time ad variations from saved Phantra scenes, with per-variant pricing and later performance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeropage-onryo](https://clawhub.ai/user/zeropage-onryo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and creative teams use this skill to create and compare controlled variations of an existing Phantra ad scene. It helps them review each proposed change and its price before authorizing a render, then revisit which variants performed well.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering variants incurs a quoted credit cost.

Mitigation: Show each variant's quote and wait for explicit approval before rendering it.

Risk: Changing saved rendering defaults can affect future renders.

Mitigation: Use explicit model and frame choices for one-off comparisons, and change saved defaults only when requested.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zeropage-onryo/skills/phantra-ai-ad-variations)

## Skill Output:

**Output Type(s):** [Text, Configuration, Guidance]

**Output Format:** [Markdown conversation with proposed scene changes, variant comparisons, and rendering guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each variant changes one variable; rendering follows review of its quote and explicit approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
