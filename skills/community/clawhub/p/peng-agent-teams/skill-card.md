## Description: <br>
Interact with Microsoft Teams - send messages, read channels, manage reactions <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[penglovemeng](https://clawhub.ai/user/penglovemeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to interact with Microsoft Teams through the agent-teams CLI, including reading team state, listing channels and messages, sending messages, managing reactions, and handling files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can extract a local Microsoft Teams session token and act through the user's Teams account. <br>
Mitigation: Install only when that account access is acceptable; prefer a test or low-risk account and avoid sensitive teams or files. <br>
Risk: Credentials, agent memory, or saved team snapshots may remain on disk after use. <br>
Mitigation: Remove ~/.config/agent-messenger/teams-credentials.json, ~/.config/agent-messenger/MEMORY.md, and any saved team-snapshot JSON files when they are no longer needed. <br>
Risk: The skill can send, delete, upload, and react to Teams content through the active account. <br>
Mitigation: Review intended channel, team, and file targets before running commands, especially in production or sensitive workspaces. <br>


## Reference(s): <br>
- [Authentication Guide](references/authentication.md) <br>
- [Common Patterns](references/common-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/penglovemeng/peng-agent-teams) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands depend on an installed agent-teams CLI and an active Microsoft Teams desktop session.] <br>

## Skill Version(s): <br>
1.10.6 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
