## Description:

Autonomous orchestrator for manifest work items through the development lifecycle

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Summon to run manifest-backed work items through intake, build, quality, and ship stages. It can resume interrupted sessions and stop when work is complete or configured budgets are reached.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Issue-derived text may be inserted into shell commands, creating a command-execution risk.

Mitigation: Review how issue text enters commands and validate or quote that input before execution; treat the scan as incomplete because referenced paths were missing.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/egregore)
- [Summon on ClawHub](https://clawhub.ai/athola/skills/nm-egregore-summon)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON state files]

**Output Format:** [Pipeline actions and JSON state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run continuously until dismissed unless configured as bounded; stops when configured budgets are reached.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
