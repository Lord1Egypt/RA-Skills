## Description:

Identity Guess Game is a Chinese-language multiplayer deduction game host that assigns each player a secret identity, collects three rounds of clues, manages guesses, calculates scores, and updates a leaderboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loongfay](https://clawhub.ai/user/loongfay)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to host a group identity-guessing game in Chinese-language chat sessions. The agent coordinates private identity delivery, clue collection, guessing, score settlement, and leaderboard display.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports avoidable command risks around player-controlled input.

Mitigation: Review before installing, avoid interpolating raw chat text into shell commands, and pass values through a safe argv-array or stdin wrapper.

Risk: The security review reports file-write risks and retained player or game data.

Mitigation: Validate group identifiers before use and periodically clear scripts/data when retained game state or leaderboard history is not wanted.

Risk: The game depends on keeping assigned identities private until settlement.

Mitigation: Send identities only by direct message, confirm private delivery before starting play, and do not disclose identities in group chat if delivery fails.

Risk: The security verdict is suspicious despite no listed risk findings.

Mitigation: Use only in groups that expect a Chinese-language game host and review the skill before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loongfay/skills/identity-guess-game)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Chinese-language game-host messages with structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON files for game state and cumulative rankings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
