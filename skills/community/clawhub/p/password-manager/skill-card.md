## Description:

A fully local password management skill for OpenClaw with AES-256-GCM encryption, password generation, and sensitive info detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixsonwang](https://clawhub.ai/user/jixsonwang)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to manage local credential vault entries, generate strong passwords, check password strength, and detect sensitive values in chat or text before saving them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Master passwords or saved secrets may be exposed through chat, command-line arguments, environment variables, or plaintext retrieval options.

Mitigation: Do not place master passwords or saved secrets in chat, command-line arguments, or long-lived environment variables; reveal plaintext secrets only when necessary and clear related outputs or history.

Risk: Vault and cache files contain sensitive material and depend on local filesystem protections.

Mitigation: Store vault, cache, backup, and log files with restrictive permissions and treat each as a sensitive asset.

Risk: Safety-critical backup and restore behavior should not be assumed reliable from the current documentation.

Mitigation: Verify backup and restore with a non-production test vault before relying on the skill for recovery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jixsonwang/skills/password-manager)
- [Skill Documentation](SKILL.md)
- [OpenClaw Hook Documentation](hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, Markdown, and structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return authentication prompts, password strength assessments, generated passwords, vault entry metadata, or plaintext secrets when explicitly requested.]

## Skill Version(s):

1.0.4 (source: package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
