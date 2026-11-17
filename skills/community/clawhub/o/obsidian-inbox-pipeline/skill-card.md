## Description:

Automates collection from AI news, economic radar, travel reports, RSS, and articles into a structured Obsidian inbox, with optional Telegram/Feishu notifications and cron scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunanjsd](https://clawhub.ai/user/hunanjsd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to automate capture, search, and review of an Obsidian inbox from external information sources. It also supports scheduled runs and optional notification delivery for routine knowledge collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write Obsidian vault files, so broad path settings may affect unintended notes.

Mitigation: Run it under a dedicated low-privilege account and restrict OBSIDIAN_VAULT_PATH and OBSIDIAN_INBOX_DIR to the intended vault and inbox directory.

Risk: Optional Telegram and Feishu delivery can send captured content outside the local vault.

Mitigation: Secure the notification credentials, configure them only when external sending is intended, and leave them unset to disable those channels.

Risk: The daily pipeline can invoke neighboring radar scripts and uses predictable temporary file paths.

Mitigation: Review before installing from cron, avoid untrusted radar_type values, and replace predictable /tmp files with private temporary directories before unattended use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and terminal text output with shell command examples and environment configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes to configured Obsidian vault paths and can optionally send text through Telegram or Feishu when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
