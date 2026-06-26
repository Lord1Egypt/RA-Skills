## Description: <br>
Habitica is a CLI skill for listing, creating, updating, and completing Habitica tasks, rewards, quests, party chat, inventory, and user stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TONYUNTURN](https://clawhub.ai/user/TONYUNTURN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Habitica users and agents use this skill to inspect and manage Habitica tasks, stats, party activity, quests, and batch habit-tracking actions from a shell-backed workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Habitica API token that can read and modify the user's Habitica account. <br>
Mitigation: Keep ~/.habitica private, do not commit or share it, and install the skill only when that account access is acceptable. <br>
Risk: State-changing commands can delete or update tasks, score habits, send party chat, accept quests, cast skills, or force a new day. <br>
Mitigation: Require explicit user confirmation before running delete, party-send, quest-accept, cast, cron, or bulk scoring actions. <br>
Risk: Batch operations or repeated API calls can unintentionally modify multiple tasks or trigger service rate limits. <br>
Mitigation: Review the full batch plan before execution and respect the documented 30-second interval between automated calls. <br>


## Reference(s): <br>
- [ClawHub Habitica Skill](https://clawhub.ai/TONYUNTURN/habitica-skill) <br>
- [Habitica API](https://habitica.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance, API calls] <br>
**Output Format:** [Plain text and Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Habitica user ID and API token; commands may read or modify Habitica account state.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
