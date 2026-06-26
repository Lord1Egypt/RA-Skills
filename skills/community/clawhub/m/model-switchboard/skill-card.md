## Description: <br>
Safely configures OpenClaw AI models by validating role compatibility, maintaining backups, managing fallback chains, and offering CLI and local dashboard workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-bot07](https://clawhub.ai/user/frank-bot07) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and agents use this skill to manage model assignments, fallback chains, task routing, backups, and recovery without directly editing OpenClaw configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled local dashboard can change OpenClaw configuration without authentication or CSRF protections. <br>
Mitigation: Prefer CLI commands for routine changes; run the dashboard only on trusted local machines and do not expose its localhost server. <br>
Risk: The dashboard can save provider credentials to a local .env file, which may expose plaintext keys on shared or untrusted machines. <br>
Mitigation: Avoid saving long-lived provider keys through the UI unless local file permissions and machine access are controlled; rotate credentials if exposure is suspected. <br>
Risk: Incorrect model changes can affect live agent reliability. <br>
Mitigation: Use the skill's dry-run, validation, backup, and restore commands before applying changes, and confirm primary model changes with the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frank-bot07/model-switchboard) <br>
- [Publisher profile](https://clawhub.ai/user/frank-bot07) <br>
- [README](README.md) <br>
- [Architecture](ARCHITECTURE.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local OpenClaw configuration through provided commands; includes backup and rollback workflows.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and CHANGELOG v3.0, released 2026-02-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
