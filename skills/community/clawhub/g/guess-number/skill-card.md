## Description:

Play a four-digit number guessing game where each guess receives feedback on how many digits are correct in both value and position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lydia9781](https://clawhub.ai/user/lydia9781)

### License/Terms of Use:

MIT-0

## Use Case:

Users and assistant agents use this skill to host a four-digit number guessing game, start a new round, validate guesses, and return concise position-match feedback after each legal guess.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes temporary game state files in its script directory while a game is active.

Mitigation: Install only where local temporary files in the skill directory are acceptable, and clean up secret.txt and step.txt after interrupted games.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lydia9781/skills/guess-number)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text game prompts and feedback with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores temporary secret.txt and step.txt files in the script directory while a game is active.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
