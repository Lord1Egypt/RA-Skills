## Description:

OpenCortex adds structured memory files, scheduled distillation and synthesis, principles, and opt-in helper features so OpenClaw agents can preserve and organize long-term knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jd2005l](https://clawhub.ai/user/jd2005l)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to install and maintain a workspace-scoped memory system that structures long-term notes, runs scheduled distillation and synthesis, and optionally configures vault, metrics, and backup helpers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring OpenClaw agents can rewrite long-term workspace memory without direct human interaction.

Mitigation: Install only in a workspace where scheduled memory editing is acceptable, inspect cron messages after setup, and edit or remove recurring jobs if autonomous rewriting is not desired.

Risk: Optional git backup and metrics paths may be affected by workspace-path cron escaping issues identified in the security guidance.

Mitigation: Keep optional git backup and metrics disabled until workspace-path cron escaping is fixed and verified in the target workspace.

Risk: Secret-entry paths can expose sensitive values if real secrets are entered as command-line arguments or stored in file-based passphrase fallback.

Mitigation: Avoid entering real secrets as command-line arguments, prefer system keyring storage for the vault, and enable file-based passphrase storage only when the user accepts that risk.

## Reference(s):

- [OpenCortex Skill Page](https://clawhub.ai/jd2005l/skills/opencortex)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub](https://clawhub.com)
- [OpenCortex Architecture Reference](references/architecture.md)
- [Daily Memory Distillation Instructions](references/distillation.md)
- [Weekly Synthesis Instructions](references/weekly-synthesis.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and workspace configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installer-created workspace files and recurring jobs; optional vault, metrics, voice profiling, infrastructure collection, git backup, and git push features require explicit user opt-in.]

## Skill Version(s):

3.6.7 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
