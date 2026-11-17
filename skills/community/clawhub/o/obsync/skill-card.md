## Description:

Obsidian Sync CLI for syncing vaults on headless Linux servers with full end-to-end encryption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bpauli](https://clawhub.ai/user/bpauli)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to have an agent provide guidance and commands for configuring obsync to sync Obsidian vaults on headless Linux servers. It is intended for users with an Obsidian Sync subscription who need headless or always-on vault synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Password handling could expose Obsidian account credentials or end-to-end encryption passwords through shell commands, shell history, exported environment variables, startup files, or systemd units.

Mitigation: Prefer interactive prompts, a protected keyring, or a dedicated secret manager; avoid embedding real passwords in commands or exported variables.

Risk: The skill installs and uses a mutable third-party CLI that can access Obsidian account data, vault contents, and sync encryption secrets.

Mitigation: Install only if the upstream obsync project is trusted, review or pin a known release before always-on sync, and limit account and system access where practical.

## Reference(s):

- [ClawHub Obsync Skill](https://clawhub.ai/bpauli/skills/obsync)
- [obsync upstream project](https://github.com/bpauli/obsync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands or settings involving Obsidian credentials and encryption passwords; review before execution.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
