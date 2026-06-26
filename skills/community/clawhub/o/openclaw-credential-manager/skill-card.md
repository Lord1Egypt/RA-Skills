## Description: <br>
Consolidates OpenClaw credentials into a secured ~/.openclaw/.env file and provides scanning, validation, GPG encryption, rotation tracking, and cleanup workflows for credential hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teeclaw](https://clawhub.ai/user/teeclaw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw deployments use this skill to discover scattered credential files, consolidate them into a protected env file, validate permissions, and manage encryption and rotation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, migrate, encrypt, back up, and potentially delete local credential files. <br>
Mitigation: Review every scanned path before consolidation or cleanup, keep verified backups, and confirm the migrated credentials work before removing old files. <br>
Risk: Centralizing credentials creates a single high-value secrets file. <br>
Mitigation: Keep ~/.openclaw/.env at mode 600, keep related directories and backups restricted, and verify the file remains excluded from version control. <br>
Risk: The artifact describes storing OPENCLAW_GPG_PASSPHRASE in ~/.openclaw/.env, which server security guidance flags as unsafe. <br>
Mitigation: Prefer gpg-agent, an OS keychain, hardware-backed storage, or manual passphrase entry instead of storing the GPG passphrase in the env file. <br>
Risk: Automated confirmation flags and cleanup commands can remove files before a first-time migration is fully reviewed. <br>
Mitigation: Avoid --yes for first-time migrations, inspect backups, and run cleanup only after dependent workflows have been tested. <br>


## Reference(s): <br>
- [Security Best Practices](artifact/references/security.md) <br>
- [Supported Services](artifact/references/supported-services.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>
- [ClawHub release page](https://clawhub.ai/teeclaw/openclaw-credential-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local credential, backup, metadata, and encrypted secret files when its scripts are executed by the user or agent.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact CHANGELOG, released 2026-02-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
