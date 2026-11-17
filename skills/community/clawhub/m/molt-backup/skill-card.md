## Description:

Molt helps an OpenClaw agent snapshot brain files, memory notes, cron exports, and redacted configuration to a user-controlled offsite git repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin-marv](https://clawhub.ai/user/robin-marv)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure, run, or schedule backups of OpenClaw workspace memory and operational state to a private git repository they control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may push sensitive OpenClaw memory, cron, and configuration data to an offsite git repository.

Mitigation: Use only a private, dedicated backup repository, treat backup contents as sensitive, and review cron and configuration exports before enabling scheduled backups.

Risk: Credential handling and fallback config redaction may miss secrets in URLs or fields with unusual names.

Mitigation: Prefer SSH or a credential helper instead of tokens in URLs, and inspect config-redacted.json before pushing backups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robin-marv/skills/molt-backup)
- [Publisher profile](https://clawhub.ai/user/robin-marv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, json]

**Output Format:** [Markdown guidance with shell commands; backup artifacts may include Markdown and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update files in a local git clone and push commits to the configured remote repository.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
