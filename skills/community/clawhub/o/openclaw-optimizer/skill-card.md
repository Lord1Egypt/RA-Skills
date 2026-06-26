## Description: <br>
OpenClaw Optimizer helps users optimize and troubleshoot OpenClaw workspaces for cost-aware model routing, provider configuration, context management, cron automation, multi-agent architecture, skills, and agent identity audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacob-bd](https://clawhub.ai/user/jacob-bd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to audit, optimize, and troubleshoot OpenClaw deployments. It focuses on provider setup, model routing, cost and context reduction, cron automation, backups, rollback planning, and identity-file reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad OpenClaw administration reach, including guidance around profile writes, cron and config mutations, identity files, repairs, and resets. <br>
Mitigation: Require explicit user confirmation before each write, mutation, repair, reset, or persistent setting change. <br>
Risk: The skill may persist sensitive deployment knowledge in profile or configuration files. <br>
Mitigation: Do not store full secrets, token fragments, or unnecessary network details; review profile and configuration diffs before applying changes. <br>
Risk: Remote sync, self-update, and destructive repair workflows can affect local or remote environments. <br>
Mitigation: Review exact commands, diffs, remote destinations, expected impact, and rollback steps before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacob-bd/openclaw-optimizer) <br>
- [OpenClaw Optimizer - Provider Reference](references/providers.md) <br>
- [OpenClaw Optimizer - Troubleshooting Reference](references/troubleshooting.md) <br>
- [OpenClaw Optimizer - CLI Reference](references/cli-reference.md) <br>
- [OpenClaw Optimizer - Agent Identity Optimizer Reference](references/identity-optimizer.md) <br>
- [OpenClaw Optimizer - Update Log](metadata/update-log.md) <br>
- [System Profile Template](systems/TEMPLATE.md) <br>
- [OpenClaw issue 8663](https://github.com/openclaw/openclaw/issues/8663) <br>
- [OpenClaw issue 21494](https://github.com/openclaw/openclaw/issues/21494) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with prioritized findings, exact CLI commands, configuration patches, and rollback steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory by default; the skill proposes changes and rollback steps before approved mutations.] <br>

## Skill Version(s): <br>
1.19.0 (source: server release metadata and SKILL.md header; aligned with OpenClaw v2026.3.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
