## Description: <br>
Mjolnir Shadow (雷神之影) helps OpenClaw users create rotating, GPG-encrypted backups to WebDAV storage and restore workspace, configuration, strategy, and skill data when recovery is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[king6381](https://clawhub.ai/user/king6381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure encrypted recurring backups, upload them to WebDAV storage, and restore OpenClaw workspace state after data loss, migration, or system rebuilds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic restore paths can overwrite live OpenClaw data and restart OpenClaw. <br>
Mitigation: Back up the current ~/.openclaw directory first, prefer manual restore initially, and inspect downloaded archives before running --auto or restore-kit. <br>
Risk: The bare-metal restore kit can install system software, perform global npm installs, and start or restart OpenClaw. <br>
Mitigation: Run the restore kit only on systems where those changes are acceptable and only after trusting the publisher, WebDAV server, and backup archives. <br>
Risk: GPG passphrases supplied through environment variables can be exposed by local environment handling or operator error. <br>
Mitigation: Prefer gpg-agent or a secure secret store and avoid putting plaintext passphrases in cron commands or world-readable files. <br>


## Reference(s): <br>
- [Configuration Reference](artifact/references/config-reference.md) <br>
- [Project homepage](https://github.com/king6381/mjolnir-shadow) <br>
- [ClawHub release page](https://clawhub.ai/king6381/mjolnir-shadow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local encrypted configuration files, WebDAV backup archives, and restore operations outside the rendered response.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
