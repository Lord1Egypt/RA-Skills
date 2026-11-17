## Description:

Secure credential storage system for OpenClaw that encrypts and protects API keys, tokens, and sensitive credentials from memory file compromise.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keven0706](https://clawhub.ai/user/keven0706)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install and configure an encrypted credential vault, migrate plaintext credentials out of memory files, and reference secrets from OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill can expose or lose credentials and that several advertised protections are not implemented.

Mitigation: Use only synthetic secrets in an isolated workspace until the security guidance is addressed and the release is rescanned.

Risk: Credential handling uses temporary script execution and hard-coded OpenClaw paths.

Mitigation: Require fixes for temporary-script execution, hard-coded paths, fail-closed error handling, and vault permission hardening before installing in a real OpenClaw environment.

Risk: The skill migrates credentials from MEMORY.md and modifies that file during migration.

Mitigation: Back up the workspace, verify every migrated secret reference, and confirm MEMORY.md no longer contains plaintext credentials after migration.

Risk: Passphrase mode and vault permissions are called out by security guidance as requiring fixes.

Mitigation: Do not rely on passphrase mode for real credentials until passphrase handling and vault permissions have been reviewed and hardened.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keven0706/skills/openclaw-key-management)
- [Publisher Profile](https://clawhub.ai/user/keven0706)
- [Skill Documentation](artifact/SKILL.md)
- [Usage Examples](artifact/USAGE.md)
- [Test Plan](artifact/TEST_PLAN.md)
- [Project Homepage](https://instreet.coze.site/post/4da5da91-9a33-4f7a-b8a0-1533616baa74)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands, JavaScript examples, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on local OpenClaw credential vault setup, migration, retrieval, backup, and configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
