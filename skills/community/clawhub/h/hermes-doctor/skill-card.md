## Description:

Hermes Doctor helps agents diagnose and recover Hermes Agent failures involving authentication, provider switching, credential pools, HERMES_HOME redirection, gateway locks, stale configuration, and backup or migration problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT

## Use Case:

Developers, SREs, and agent operators use this skill to triage Hermes Agent incidents, identify likely root causes, and apply guided recovery steps for credentials, provider routing, configuration paths, and runtime state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting steps may expose sensitive authentication data in command output, request dumps, .env files, auth.json files, or backup archives.

Mitigation: Use redacted presence checks, interactive secret entry, encrypted backups, and avoid pasting raw dumps, secret files, or archives into chat or support tickets.

Risk: Credential edits or deletions can disrupt other providers, applications, or Hermes profiles.

Mitigation: Require explicit confirmation before deleting or editing credentials, back up affected files first, scope changes to the confirmed HERMES_HOME, and verify with Hermes diagnostic commands.

Risk: Backup and migration workflows can duplicate sensitive credential stores across machines.

Mitigation: Prefer encrypted backups, keep archives local unless explicitly approved, and re-enter API keys on the destination system when possible.

## Reference(s):

- [Hermes Doctor repository](https://github.com/dongsheng123132/hermes-doctor)
- [Hermes Doctor ClawHub page](https://clawhub.ai/dongsheng123132/skills/hermes-doctor)
- [Hermes Agent project](https://github.com/NousResearch/hermes-agent)
- [Auth / 401 Troubleshooting](references/auth-troubleshooting.md)
- [Credential Pool and Rotation](references/credential-pool-and-rotation.md)
- [Fallback Provider Chain and Rate Limits](references/fallback-and-rate-limit.md)
- [Hermes Doctor and Dump Usage](references/doctor-and-dump.md)
- [HERMES_HOME Paths and Config](references/config-and-paths.md)
- [Provider Switching](references/provider-switch.md)
- [Backup and Migration](references/backup-and-migrate.md)
- [Triage Checklist](templates/triage-checklist.md)
- [Known Hermes Issues](assets/known-issues.json)
- [Hermes Agent issue #16394](https://github.com/NousResearch/hermes-agent/issues/16394)
- [Hermes Agent issue #15914](https://github.com/NousResearch/hermes-agent/issues/15914)
- [Hermes Agent issue #3685](https://github.com/NousResearch/hermes-agent/issues/3685)
- [Hermes Agent issue #16677](https://github.com/NousResearch/hermes-agent/issues/16677)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, YAML snippets, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance should be redacted before sharing because troubleshooting may touch credentials, request dumps, auth.json, .env files, backups, and user-level environment variables.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
