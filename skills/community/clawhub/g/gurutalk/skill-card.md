## Description: <br>
Creates, syncs, and manages local persona skill directories backed by Bibliotalk profiles so users can install and converse with figure-specific agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casterkay](https://clawhub.ai/user/casterkay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use GuruTalk to install, update, list, remove, snapshot, and roll back local persona skills for Claude, Codex, and OpenClaw. The skill also guides API-key setup and routes conversations to generated figure-specific skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bibliotalk API key and copies runtime .env files into generated persona skill folders. <br>
Mitigation: Use only trusted local skill directories, avoid sharing or syncing generated persona folders, and rotate the Bibliotalk key if any generated folder is exposed. <br>
Risk: The skill can write or delete local agent skill directories, and security evidence notes weak path containment around base directory overrides. <br>
Mitigation: Review target paths before running create, sync, remove, rollback, or cleanup actions; avoid untrusted --base-dir values; and confirm deletion targets before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/casterkay/gurutalk) <br>
- [Bibliotalk](https://bibliotalk.space) <br>
- [Bibliotalk API](https://api.bibliotalk.space) <br>
- [AgentSkills standard](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script output, and generated local skill files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BIBLIOTALK_API_KEY for Bibliotalk API calls and writes persona skill folders for the selected agent.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
