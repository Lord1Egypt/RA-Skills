## Description:

Feed lobsters in the Lobster Farmer game by calling the local CLI command `lobster-farmer feed` with `--model`, `--input-tokens`, `--output-tokens`, and optional `--emotion`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murongg](https://clawhub.ai/user/murongg)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to feed model-specific lobsters through the Lobster Farmer local CLI, simulate token usage, batch-feed multiple models, and report updated growth metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start the local Lobster Farmer service and run feed commands that mutate local game state.

Mitigation: Install only when using the Lobster Farmer local CLI, and review model, token, emotion, and port values before single or batch feed actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/murongg/skills/lobster-farmer-feeder)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model name, input and output token values, emotion, lobster total tokens, feed count, and size.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
