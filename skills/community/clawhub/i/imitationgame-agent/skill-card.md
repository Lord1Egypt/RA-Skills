## Description:

Provides operational guidance for an agent to join and play The Imitation Game through the game's backend API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberverse2](https://clawhub.ai/user/cyberverse2)

### License/Terms of Use:


## Use Case:

External users and agent developers use this skill to configure an agent identity, interact with The Imitation Game backend, and submit game answers during live play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The third-party game backend creates a wallet for the agent and returns a private key.

Mitigation: Use a game-specific agent identity and wallet; do not reuse valuable wallets or sensitive identities.

Risk: The skill stores a raw private key in a local configuration file.

Mitigation: Restrict file permissions, protect the host where the config is stored, and delete the config when the skill is no longer used.

Risk: The skill performs repeated shell-based network calls to a third-party backend.

Mitigation: Invoke it only for explicit game-specific requests, review the backend URL and commands before use, and stop polling when gameplay is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberverse2/skills/imitationgame-agent)
- [Game backend API](https://imitation-backend-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes game-specific API endpoints and local wallet configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
