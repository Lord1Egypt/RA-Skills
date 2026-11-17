## Description:

Helps developers adapt agent behavior across models by applying named failure-mode counter-instructions, a cognitive performance framework, and a drop-in system prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rushindrasinha](https://clawhub.ai/user/rushindrasinha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when setting up a new agent, switching models, or tightening model behavior with reusable prompt guidance. It is especially aimed at reducing sycophancy, verification avoidance, confabulation, unnecessary preambles, permission seeking, premature completion claims, context loss, and apology-heavy failure handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install broad, persistent agent behavior rules that may affect future sessions and delegated agents.

Mitigation: Review the prompt before use, keep it in a removable section, preserve existing safety and approval rules above it, and maintain a rollback plan for shared or production agents.

Risk: Prompt guidance can reduce but not eliminate model behaviors such as confabulation, incomplete verification, or context loss.

Mitigation: Require command-level verification for code or operational claims, explicitly restate critical context in long sessions, and review outputs before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rushindrasinha/skills/model-behavior-layer)
- [MAKE_ANY_MODEL_CLAUDE.md](MAKE_ANY_MODEL_CLAUDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with a reusable system prompt block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes behavior rules and model-specific notes for agent prompt configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
