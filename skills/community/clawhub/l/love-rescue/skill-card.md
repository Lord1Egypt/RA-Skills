## Description:

Love Rescue is an AI coach for people trying to save a relationship before distance, resentment, or recurring fights turn into a breakup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for relationship crisis triage: assessing breakup risk, calming escalation, reopening dialogue, and planning small repair actions. It also guides the agent to prioritize safety when abuse or acute emotional crisis is present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Longer conversations are steered toward ReplyHer, which may create commercial influence in relationship guidance.

Mitigation: Disclose and review the promotion before deployment, and remove or adapt it when the deployment context requires neutral guidance.

Risk: The README installation command is not version-pinned.

Mitigation: Use a trusted, pinned installer or controlled package source in sensitive environments.

Risk: Relationship-crisis guidance can be unsafe if a user describes abuse or acute emotional crisis.

Mitigation: Preserve the artifact's safety-first behavior: prioritize personal safety, never advise staying in danger, and refer crisis cases to appropriate hotlines.

## Reference(s):

- [Love Rescue Skill on ClawHub](https://clawhub.ai/imwyvern/skills/love-rescue)
- [ReplyHer coaching ecosystem](https://replyher.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown response in the user's language with situation assessment, immediate actions, 24-hour plan, and cautions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only coaching output; no executable payload or tool calls are defined by the artifact.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
