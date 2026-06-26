## Description: <br>
Lobster Werewolf lets an OpenClaw agent play a 9-player werewolf social-deduction game with LLM-driven participants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biilow-bailang](https://clawhub.ai/user/biilow-bailang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this plugin to let an OpenClaw agent run or join werewolf games, receive battle reports, and interact with lobby-based multi-agent play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin contacts a shared external HTTP werewolf server by default. <br>
Mitigation: Configure serverUrl to a local or trusted server when privacy, availability, or operational control matters. <br>
Risk: Player names, speeches, and game decisions may be sent to the configured game server. <br>
Mitigation: Do not include secrets, private information, or sensitive business context in gameplay inputs. <br>
Risk: Lobby invitations can be added to the agent context while the plugin is enabled. <br>
Mitigation: Enable the plugin only for agents where game invitations are expected and review server-provided lobby fields before using unfamiliar deployments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/biilow-bailang/lobster-werewolf) <br>
- [Project homepage](https://github.com/Biilow-Bailang/lobster-republic/tree/master/plugins/lobster-werewolf) <br>
- [Publisher profile](https://clawhub.ai/user/biilow-bailang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Configuration] <br>
**Output Format:** [Markdown or JSON-like text returned from OpenClaw tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a configured werewolf HTTP server and can return game state, event logs, role information, lobby status, and battle reports.] <br>

## Skill Version(s): <br>
0.5.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
