## Description:

Consolidates OpenClaw API keys and credentials into a secured .env file, with scanning, validation, GPG encryption guidance, rotation tracking, and backup hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teeclaw](https://clawhub.ai/user/teeclaw)

### License/Terms of Use:


## Use Case:

Developers and operators of OpenClaw deployments use this skill to find scattered credentials, consolidate them into ~/.openclaw/.env, validate permissions and formats, encrypt high-value secrets, track rotation, and clean up migrated credential files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad control over sensitive local credentials, which could expose or damage credentials if used without review.

Mitigation: Review the scanner output, target files, backups, and commands before running consolidation, cleanup, encryption, or GPG setup steps.

Risk: Storing a GPG passphrase in the same .env file can undermine the protection provided by encrypted secrets.

Mitigation: Use a separate secret store, interactive prompt, or controlled agent cache for passphrases instead of placing the GPG passphrase alongside protected credentials.

Risk: Sourcing generated .env files as shell code can treat credential values as executable shell input.

Mitigation: Load .env values with a parser that preserves quoting and treats values as data rather than shell commands.

Risk: Cleanup and GPG setup steps can remove migrated files or change local GPG behavior.

Mitigation: Verify secure backups and understand local GPG changes before running cleanup.py --confirm or setup-gpg.sh.

## Reference(s):

- [OpenClaw Credential Manager on ClawHub](https://clawhub.ai/teeclaw/skills/openclaw-credential-manager)
- [Security Best Practices](references/security.md)
- [Supported Services](references/supported-services.md)
- [Credential Consolidation Rule](CONSOLIDATION-RULE.md)
- [Core Principle](CORE-PRINCIPLE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, and local file or configuration changes when scripts are executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run credential scanning, consolidation, encryption, validation, rotation tracking, and cleanup workflows.]

## Skill Version(s):

2.0.0 (source: release evidence and CHANGELOG, released 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
