## Description: <br>
Helps agents diagnose and recover Hermes Agent failures involving authentication, provider switching, credential pools, HERMES_HOME path resolution, gateway locks, stale configuration, and backup recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongsheng123132](https://clawhub.ai/user/dongsheng123132) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to triage Hermes Agent incidents, inspect redacted diagnostics, identify configuration or credential drift, and choose repair steps for authentication and provider-routing failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting steps may expose API keys, Authorization headers, OAuth tokens, or credential files. <br>
Mitigation: Use redacted diagnostics where possible, do not paste raw terminal output into chats or tickets, and redact secrets before sharing logs. <br>
Risk: Repair steps may modify .env, auth.json, config.yaml, registry values, running processes, or credential locations. <br>
Mitigation: Start with read-only checks, confirm the exact HERMES_HOME, back up affected files, and require explicit user approval before any destructive or state-changing action. <br>
Risk: Backups and migrations can copy sensitive credentials between machines or into insecure storage. <br>
Mitigation: Encrypt or tightly restrict backups and avoid moving credentials unless the user has approved the destination and access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongsheng123132/hermes-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/dongsheng123132) <br>
- [Project homepage](https://github.com/dongsheng123132/hermes-doctor) <br>
- [Auth / 401 troubleshooting](references/auth-troubleshooting.md) <br>
- [Backup and migration](references/backup-and-migrate.md) <br>
- [Config and paths](references/config-and-paths.md) <br>
- [Credential pool and rotation](references/credential-pool-and-rotation.md) <br>
- [Doctor and dump diagnostics](references/doctor-and-dump.md) <br>
- [Fallback and rate limit handling](references/fallback-and-rate-limit.md) <br>
- [Provider switch troubleshooting](references/provider-switch.md) <br>
- [Hermes triage checklist](templates/triage-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and troubleshooting checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local Hermes configuration, credential, and diagnostic files; sensitive values should remain redacted.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
