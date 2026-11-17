## Description:

Discover and explore APIs on the Motie marketplace using the motie CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saucedocs](https://clawhub.ai/user/saucedocs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Motie marketplace APIs, fetch route documentation, and invoke selected API routes with the Motie CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a broad third-party API CLI that may send searches, parameters, or request data to external services.

Mitigation: Use it only for explicit Motie or API-marketplace tasks, and avoid private or sensitive data unless the user has consented.

Risk: The Motie CLI requires an API key and can be installed globally through npm.

Mitigation: Prefer the MOTIE_API_KEY environment variable, avoid exposing credentials in command history, and pin or verify the CLI package before global installation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/saucedocs/skills/motie-cle-beta)
- [Motie beta portal](https://beta.motie.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls through a third-party CLI that requires a Motie API key.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
