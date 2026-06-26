## Description: <br>
Generate short-lived, mobile-friendly ngrok preview links for local artifacts and share them in Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wynnsu](https://clawhub.ai/user/wynnsu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to expose selected local task outputs through a temporary ngrok preview link for remote viewing, especially on mobile devices. It is intended for narrow, per-task artifacts rather than broad directories or persistent hosting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files or directories can be published to a public ngrok URL. <br>
Mitigation: Verify each --source path before use and include only narrow, non-sensitive task outputs. <br>
Risk: The advertised expiry is not enforced automatically for a running tunnel. <br>
Mitigation: Use short TTLs and run the down command with --delete-session-dir or cleanup when the preview is no longer needed. <br>
Risk: Broad paths can expose credentials, logs, configuration, or unrelated workspace files. <br>
Mitigation: Avoid home directories, workspace roots, credential folders, logs, and config files. <br>


## Reference(s): <br>
- [ngrok download documentation](https://ngrok.com/download) <br>
- [ngrok-preview Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/wynnsu/ngrok-preview) <br>
- [Publisher profile](https://clawhub.ai/user/wynnsu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The up command returns a public URL, expiry timestamp, session ID, stop command, and status command.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
