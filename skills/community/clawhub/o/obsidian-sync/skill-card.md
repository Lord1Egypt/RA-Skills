## Description: <br>
Sync files between a Clawdbot workspace and Obsidian through a local server for two-way synchronization with the OpenClaw Obsidian plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AndyBold](https://clawhub.ai/user/AndyBold) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Obsidian/OpenClaw users use this skill to run an authenticated sync server that lets markdown notes be listed, read, and written between an Obsidian vault and a Clawdbot workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync server can read and overwrite files in configured workspace folders. <br>
Mitigation: Install it only when that file access is intended, narrow SYNC_ALLOWED_PATHS to the minimum needed, and use backups or versioning for important notes. <br>
Risk: Exposing the server beyond localhost can make the sync API reachable from other systems. <br>
Mitigation: Keep SYNC_BIND set to localhost unless remote access is intentional, and expose it only through a controlled channel such as the documented Tailscale setup. <br>
Risk: Anyone with the sync token can call the read and write endpoints. <br>
Mitigation: Protect SYNC_TOKEN or CLAWDBOT_TOKEN, rotate it if exposed, and avoid storing it in shared files or logs. <br>


## Reference(s): <br>
- [Obsidian Sync on ClawHub](https://clawhub.ai/AndyBold/obsidian-sync) <br>
- [obsidian-openclaw](https://github.com/AndyBold/obsidian-openclaw) <br>
- [Obsidian42 BRAT](https://github.com/TfTHacker/obsidian42-brat) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes markdown files under configured workspace subdirectories when the sync server is running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
