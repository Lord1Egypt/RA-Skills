## Description: <br>
G.workspace connects OpenClaw agents and Discord slash commands to a locally running G.workspace REST API for shared workspace file management, version history, and review tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luojingwei123](https://clawhub.ai/user/luojingwei123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to add Discord slash commands and agent tools that manage shared G.workspace files, references, members, workspace creation, and review tasks through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord/OpenClaw commands and agent tools can mutate shared workspace state, including file deletion, trash management, workspace creation, task claiming, and task completion. <br>
Mitigation: Add confirmation and role checks for delete, empty-trash, workspace creation, and task-completion actions before production use. <br>
Risk: Workspace metadata and file information may be exposed through Discord commands or agent tool responses. <br>
Mitigation: Install only where Discord channel access and backend permissions are tightly controlled, and avoid storing sensitive files unless those controls are appropriate. <br>
Risk: The plugin depends on a trusted locally running G.workspace backend service. <br>
Mitigation: Run the backend in the documented web-only mode, keep the REST endpoint bound to the intended local service, and verify the configured port before enabling the plugin. <br>


## Reference(s): <br>
- [ClawHub G.workspace release](https://clawhub.ai/luojingwei123/gworkspace) <br>
- [Publisher profile](https://clawhub.ai/user/luojingwei123) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-formatted text responses, shell command snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [OpenClaw command and tool responses can reflect REST-backed changes to shared workspace state.] <br>

## Skill Version(s): <br>
3.2.1 (source: evidence.release.version and artifact/plugin/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
