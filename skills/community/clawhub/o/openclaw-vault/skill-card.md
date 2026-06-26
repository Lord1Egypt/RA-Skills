## Description: <br>
Audits credential exposure, detects misconfigured permissions, inventories credential files, and flags stale credentials in local agent workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to run local credential lifecycle checks across agent workspaces, review exposure vectors, and inventory files that may need permission changes or rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local files that may contain credentials and can print findings to the terminal. <br>
Mitigation: Run it only against an explicit workspace and treat all output as sensitive. <br>
Risk: Some commands can change file permissions or move files into or out of quarantine. <br>
Mitigation: Use protect, fix-permissions, quarantine, and unquarantine only when those local changes are intended and a backup or clean version-control state exists. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/AtlasPA/openclaw-vault) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text reports with tables, status lines, and exit codes; agent guidance may include Markdown and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python standard library only; no network calls are documented.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
