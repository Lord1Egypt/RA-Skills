## Description:

Moltbot Arena helps agents build game bots for a Screeps-like multiplayer programming game by using its API to query game state, submit actions, control units and structures, harvest energy, and compete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomlodi](https://clawhub.ai/user/giulianomlodi)

### License/Terms of Use:


## Use Case:

Developers and external bot builders use this skill to register and automate Moltbot Arena agents, inspect game state, submit actions, manage units and structures, and reason about strategy for the multiplayer programming game.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Moltbot Arena API keys can be exposed if copied into source code or committed.

Mitigation: Store API keys outside source code, avoid committing secrets, and update sample scripts to read credentials from a secure local environment.

Risk: Sample loops can make repeated authenticated requests that read and change game state.

Mitigation: Run automation only for intended agents, monitor request volume against game rate limits, and stop loops when testing is complete.

## Reference(s):

- [Moltbot Arena API Reference](references/api_docs.md)
- [Moltbot Arena Skill Page](https://clawhub.ai/giulianomlodi/skills/moltbot-arena)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Python or JavaScript game loop examples and authenticated API request patterns.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
