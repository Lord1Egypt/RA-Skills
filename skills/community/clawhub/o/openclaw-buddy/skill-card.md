## Description:

Generates a deterministic virtual pet buddy from a user identifier, including species, rarity, cosmetics, stats, ASCII art, and a personality line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and community agents use this skill to generate a repeatable novelty virtual pet profile from the user's platform identifier or a provided string for chat sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The usage instructions place a user-controlled identifier into a shell command.

Mitigation: Invoke the Node script with a shell-free argument array and validate or restrict custom identifiers before execution.

Risk: The skill can generate repeatable profiles for other people when supplied with their platform identifiers.

Mitigation: Use the current user's identifier by default, disclose identifier use, and avoid third-party platform-ID lookups without consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kylinr/skills/openclaw-buddy)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Formatted message text with companion JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic output for a given identifier; includes bilingual labels, ASCII art, rarity, cosmetics, stats, and a personality description.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
