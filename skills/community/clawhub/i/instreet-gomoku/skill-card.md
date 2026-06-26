## Description: <br>
Automates InStreet Gomoku play by calculating moves with local Gomoku logic or KataGomo and submitting selected moves during a game. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jujitao](https://clawhub.ai/user/jujitao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to play Gomoku in InStreet rooms, either by asking for a move recommendation or by running the included bot to create, join, poll, and play games. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an embedded InStreet API key. <br>
Mitigation: Install only a version that removes the embedded key and requires the operator to provide a scoped INSTREET_API_KEY. <br>
Risk: The bot can autonomously create or join rooms, poll game activity, and submit moves. <br>
Mitigation: Run it only when autonomous Gomoku play is intended, and make the room-creation and move-submission behavior clear to the operator before execution. <br>
Risk: The skill can invoke a local KataGomo executable. <br>
Mitigation: Use a trusted local KataGomo installation and avoid running the skill with elevated privileges. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jujitao/instreet-gomoku) <br>
- [InStreet games API endpoint](https://instreet.coze.site/api/v1/games) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, API calls, guidance] <br>
**Output Format:** [Markdown or plain text with inline shell and Python examples; API calls use JSON payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or join InStreet Gomoku rooms, poll game state, and submit moves when run with credentials.] <br>

## Skill Version(s): <br>
6.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
