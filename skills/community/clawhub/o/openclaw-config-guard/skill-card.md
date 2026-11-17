## Description:

Audit and safely repair OpenClaw configuration with deterministic validation, backups, rollback, and change reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soal2](https://clawhub.ai/user/soal2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw configuration, determine whether configuration issues block startup, and apply only documented repairs with backups, rollback, validation, and a clear Markdown report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to inspect and modify local OpenClaw configuration files.

Mitigation: Review proposed configuration changes before allowing writes, require a backup before each write, and verify the configuration again after changes.

Risk: Backup naming may not be hardened enough for shared or adversarial local environments.

Mitigation: Keep the configuration directory private and harden backup handling before relying on it in shared environments.

Risk: Undocumented configuration assumptions could produce incorrect repairs.

Mitigation: Use the listed OpenClaw documentation and local CLI validation as the source of truth, and defer changes when the correct repair is not documented.

## Reference(s):

- [OpenClaw gateway configuration](https://docs.openclaw.ai/gateway/configuration)
- [OpenClaw configuration reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw CLI config](https://docs.openclaw.ai/cli/config)
- [OpenClaw CLI doctor](https://docs.openclaw.ai/cli/doctor)
- [Official source list](references/official-sources.md)
- [ClawHub skill page](https://clawhub.ai/soal2/skills/openclaw-config-guard)
- [Author GitHub profile](https://github.com/soal2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and JSON command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports official sources consulted, active config path, validation results, startup blockers, fixes, deferred issues, recommendations, modified paths, backup path, and restart guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
