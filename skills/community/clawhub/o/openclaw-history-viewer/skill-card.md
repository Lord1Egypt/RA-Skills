## Description: <br>
Starts a web service for browsing OpenClaw chat history with session lists, message detail views, JSON API export, automatic session backup discovery, and refresh support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lengyhua](https://clawhub.ai/user/lengyhua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to launch a local history viewer for reading, searching, backing up, refreshing, and exporting OpenClaw conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can serve private OpenClaw conversation history through an unauthenticated web server. <br>
Mitigation: Run it only on a trusted single-user machine, bind it to 127.0.0.1, keep it in the foreground when possible, and stop it when finished. <br>
Risk: The skill includes a delete API that can remove session or backup files. <br>
Mitigation: Avoid the delete API unless you have reviewed the behavior and have a separate backup of any data you may need. <br>
Risk: Exports and backups may contain sensitive conversation content. <br>
Mitigation: Store exported and backed-up files as sensitive data and delete copies that are no longer needed. <br>


## Reference(s): <br>
- [Openclaw History Viewer on ClawHub](https://clawhub.ai/lengyhua/openclaw-history-viewer) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API responses, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a local web server, expose JSON API responses, and create backup or export files containing conversation history.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
