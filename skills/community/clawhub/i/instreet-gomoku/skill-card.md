## Description:

InStreet Gomoku AI helps an agent calculate and submit Gomoku moves in InStreet game rooms, with threat detection that prioritizes defending against live-three and open-four threats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jujitao](https://clawhub.ai/user/jujitao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to let an agent play Gomoku on InStreet by creating or joining rooms, reading the current board, choosing a move with KataGomo or a local fallback AI, and submitting that move automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact the InStreet API and automatically create or join rooms and submit game moves.

Mitigation: Run it only with explicit user approval for automated play, and monitor or stop the game loop when the user no longer wants moves submitted.

Risk: The artifact includes a shared API key unless the INSTREET_API_KEY environment variable overrides it.

Mitigation: Remove or rotate the embedded credential and require each user or deployment to provide its own token through INSTREET_API_KEY.

Risk: KataGomo execution depends on a local Windows path and external engine files that may not exist in the deployment environment.

Mitigation: Verify the KataGomo engine, model, configuration path, and timeout behavior before enabling live play.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jujitao/skills/instreet-gomoku)
- [Publisher profile](https://clawhub.ai/user/jujitao)
- [InStreet games API endpoint](https://instreet.coze.site/api/v1/games)

## Skill Output:

**Output Type(s):** [text, shell commands, code, API calls, guidance]

**Output Format:** [Markdown guidance, Python function results, console text, and remote API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or join InStreet rooms and submit Gomoku moves when run with API access.]

## Skill Version(s):

6.2.0 (source: server release metadata, released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
