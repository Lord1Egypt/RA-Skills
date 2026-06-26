## Description: <br>
Automatically syncs local and cloud OpenClaw configuration files through a private GitHub Gist with workspace detection, previews, backups, and token-based setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayShna](https://clawhub.ai/user/JayShna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to synchronize OpenClaw identity, user, tool, and skill files across local and cloud environments while previewing changes and keeping backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill syncs sensitive OpenClaw identity, user, tool, and skill files through a GitHub Gist. <br>
Mitigation: Review diffs before pulling or pushing, and only pull from a Gist fully controlled by the user. <br>
Risk: The GitHub token is stored locally with weak protection. <br>
Mitigation: Use a minimally scoped gist-only GitHub token, protect or revoke the token if the machine is shared, and rotate it if exposure is suspected. <br>
Risk: Pipe-to-shell installation can execute installer behavior before review. <br>
Mitigation: Prefer manual installation and inspect the artifact files before running the installer. <br>


## Reference(s): <br>
- [OpenClaw Sync Bridge ClawHub Page](https://clawhub.ai/JayShna/openclaw-sync-bridge) <br>
- [JayShna ClawHub Publisher Profile](https://clawhub.ai/user/JayShna) <br>
- [GitHub Personal Access Tokens](https://github.com/settings/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and sync guidance for an agent; the installed bridge writes local configuration files and synchronizes selected OpenClaw files with a GitHub Gist.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
