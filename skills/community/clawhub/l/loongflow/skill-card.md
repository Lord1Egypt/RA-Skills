## Description:

LoongFlow helps agents run PEES iterations and optional evolutionary search to improve code, algorithms, prompts, or other tasks toward a target score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freshmand](https://clawhub.ai/user/freshmand)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose a PEES mode, launch iterative agent work, and monitor optimization tasks where a single pass is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch autonomous optimization work and create recurring monitoring behavior.

Mitigation: Require explicit user approval before starting background work or creating a recurring cron, and review the task scope before execution.

Risk: Engine mode can install mutable remote code from GitHub.

Mitigation: Pin and review the engine source before installation or execution.

Risk: Engine setup can expose part of an API key in command output.

Mitigation: Remove API-key echoing and avoid logging secrets before using engine mode.

Risk: Monitoring can read task and log content across configured workspaces and send progress summaries.

Mitigation: Scope monitoring to one approved workspace and one intended recipient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freshmand/skills/loongflow)
- [LoongFlow GitHub Repository](https://github.com/baidu-baige/LoongFlow)
- [Native PEES Mode](references/native-pees.md)
- [LoongFlow Engine Mode](references/engine-mode.md)
- [LoongFlow Monitoring](references/monitoring.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create task records, engine configuration, background work, progress summaries, and notification commands after the user selects a mode.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
