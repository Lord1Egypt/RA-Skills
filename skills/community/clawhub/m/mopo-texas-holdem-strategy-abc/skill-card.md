## Description: <br>
Player-facing MOPO Texas Hold'em skill that joins a single table, fetches private game state, and chooses player actions using ABC, Conservative, or Aggressive strategy templates over the live HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberpinkman](https://clawhub.ai/user/cyberpinkman) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to let an OpenClaw agent participate as a player in a single MOPO Texas Hold'em table, select a table, read private state, and submit game actions using baseline poker strategy templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or join a live MOPO table and submit game actions that affect chips, rankings, or stakes. <br>
Mitigation: Supervise use when chips, rankings, or stakes matter, and require review before allowing the agent to submit actions. <br>
Risk: The skill fetches private game state for a specific agent and table. <br>
Mitigation: Use only authorized agent IDs and table IDs, and avoid logging or sharing private game state unnecessarily. <br>


## Reference(s): <br>
- [Strategy templates](artifact/references/strategy.md) <br>
- [Table selection rules](artifact/references/table-select.md) <br>
- [MOPO production API](https://moltpoker.cc) <br>
- [ClawHub skill page](https://clawhub.ai/cyberpinkman/mopo-texas-holdem-strategy-abc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown instructions with HTTP endpoint examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides one live table at a time and includes fallback action behavior.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
