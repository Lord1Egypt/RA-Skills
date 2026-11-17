## Description:

A Chinese-language interactive game framework for agents that supports text adventures, riddles, quizzes, branching story play, character state, and JSON-style save/load flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyunxiao-ai](https://clawhub.ai/user/yangyunxiao-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to add Chinese-language game play to an agent, including text adventure sessions, puzzle games, branching story responses, player state, and save/load commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad game-related trigger phrases could start game mode during ordinary conversation about games.

Mitigation: Review and narrow activation examples before integrating the skill into an agent.

Risk: The skill is intended for Chinese-language interactive game play, so it may not fit agents or users expecting another language or non-game behavior.

Mitigation: Install it only for agents that should provide Chinese-language game sessions, and expose clear game commands to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangyunxiao-ai/skills/interactive-games)
- [Publisher profile](https://clawhub.ai/user/yangyunxiao-ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown or text responses with JavaScript examples, shell commands, configuration snippets, and JSON-style game state.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Game outputs may include branching choices, player status, inventory, score, hints, and save/load state.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
