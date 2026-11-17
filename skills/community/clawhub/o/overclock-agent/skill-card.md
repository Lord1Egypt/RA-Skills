## Description:

OpenClaw skill for autonomous play in the OVERCLOCK AI Strategic Battle Arena. Executes battles, card purchases, strategy changes, and game monitoring via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senti-1000ma](https://clawhub.ai/user/senti-1000ma)

### License/Terms of Use:


## Use Case:

External users and autonomous agents use this skill to play and test the OVERCLOCK AI Strategic Battle Arena by checking game state, buying card packs, changing strategy, running battles, checking leaderboards, and reporting bugs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous gameplay can make game-state changes, including battles and strategy updates, without further human judgment.

Mitigation: Require user approval for autonomous sessions and scope each run to a specific player ID.

Risk: Card-pack purchase endpoints can spend money or game currency.

Mitigation: Require explicit approval and a spending cap before any pack purchase.

Risk: The artifact documents two different API hosts, which can lead agents to call the wrong service.

Mitigation: Clarify the intended API host before routine use and configure agents to use only that host.

Risk: The log endpoint may expose operational details beyond normal gameplay state.

Mitigation: Review log access expectations with the publisher and avoid retrieving logs unless the task explicitly requires bug investigation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/senti-1000ma/skills/overclock-agent)
- [OVERCLOCK Agent Skill](artifact/SKILL.md)
- [OVERCLOCK QA Mission](artifact/MISSION_QA.md)
- [OVERCLOCK OpenClaw Agent API Reference](artifact/resources/API.md)
- [Primary OVERCLOCK API host](https://overclock-903028338458.us-central1.run.app)
- [Alternate OVERCLOCK API host](https://synth-colosseum-wukg3jhefq-uc.a.run.app)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with HTTP endpoint, header, JSON body, and bash-style examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a player ID header to scope game state; card-pack purchase and battle endpoints are rate limited.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
