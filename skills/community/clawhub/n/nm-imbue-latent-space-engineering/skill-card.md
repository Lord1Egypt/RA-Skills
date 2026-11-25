## Description:

Shapes agent behavior via instruction framing and style transfer

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this guidance when composing delegation prompts, writing agent instructions, coordinating reviews, and producing code or prose that should match an existing style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-framing techniques may be applied as guarantees or without checking whether they fit the model and task; the skill describes parts of its evidence base as limited.

Mitigation: Treat techniques as heuristics and check the resulting output against the delegate, task, and available context.

Risk: Competitive review framing can encourage inflated issue counts.

Mitigation: Require evidence for each finding and prioritize by severity, as the skill recommends.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-imbue-latent-space-engineering)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Human-readable guidance, prompt text, examples, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise procedural guidance with examples and selection criteria for prompt-framing techniques.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
