## Description:

KLYC-PMM helps agents initialize, back up, recover, synchronize, search, and distill long-term text memory through the Kunlun Yaochi service, with optional DeepSeek-based distillation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sylncn](https://clawhub.ai/user/sylncn)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to manage persistent text memory for AI agents, including initialization, backup, recovery from a token or link, automated file synchronization, semantic search, and optional memory distillation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can continuously upload sensitive workspace files.

Mitigation: Review exactly which files will be uploaded and where before installation, and avoid enabling watch behavior for workspaces containing sensitive files that should not leave the machine.

Risk: The recovery token or link functions as a secret.

Mitigation: Treat the recovery token/link as a password and avoid pasting it into chats, logs, shell history, or other shared locations.

Risk: Custom API endpoints can redirect memory and credential-related flows to untrusted services.

Mitigation: Use the default service endpoint unless a custom endpoint is fully trusted and reviewed.

Risk: Daemon installation may create persistent synchronization behavior.

Mitigation: Prefer disabling or avoiding the daemon until persistence behavior and fail-closed client-side encryption have been reviewed.

Risk: The package overstates encryption protections according to the security summary.

Mitigation: Do not rely on advertised encryption claims without review; inspect the upload path and encryption behavior before use.

## Reference(s):

- [PMM Full Architecture](artifact/references/pmm-full-architecture.md)
- [Pay Skill Packaging Standard](artifact/references/pay-skill-spec.md)
- [Kunlun Yaochi Homepage](https://kunlunyaochi.com)
- [SkillHub SkillPay Reference](https://skillhub.cn/skillpay)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing output may guide local script execution, HTTPS API use, file synchronization, and memory recovery workflows.]

## Skill Version(s):

9.3.12 (source: SKILL.md frontmatter, skill.json, _meta.json, CHANGELOG.md released 2026-09-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
