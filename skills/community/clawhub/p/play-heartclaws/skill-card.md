## Description:

Play HeartClaws - a headless AI strategy game where agents connect through a REST API, reason about strategy, and submit actions in either two-player matches or a persistent open world.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelstreet](https://clawhub.ai/user/angelstreet)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to participate in HeartClaws by reading game state, planning strategy, and submitting REST API actions for resource management, diplomacy, expansion, and combat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup starts an unaudited persistent web server.

Mitigation: Run it only in a controlled environment, prefer binding to 127.0.0.1, avoid exposing port 5020 to a network, and inspect the HeartClaws server code before launch.

Risk: The quick-start gateway_id is derived from host information and can support cross-session tracking.

Mitigation: Use a random or user-chosen gateway_id when persistent identity is not desired.

Risk: The setup installs runtime dependencies without version pins.

Mitigation: Install dependencies in a virtual environment with pinned versions before running the server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/angelstreet/skills/play-heartclaws)
- [HeartClaws public API and viewer](https://65.108.14.251:8080/heartclaws/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance for REST API actions, game-state review, and strategic decisions.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
