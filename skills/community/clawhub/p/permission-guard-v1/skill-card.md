## Description:

Permission Guard is an OpenClaw security watchdog that monitors installed skill behavior, flags unauthorized file access, suspicious outbound network calls, and dangerous command patterns, and produces permission audit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyhetech](https://clawhub.ai/user/billyhetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to review agent activity, establish first-run baselines after installing skills, and investigate suspicious file, network, or command behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad home-directory path metadata and active network connections while performing watchdog checks.

Mitigation: Run it only when permission monitoring is needed and review reported paths and destinations before taking action.

Risk: Persistent audit logs under ~/.openclaw may expose sensitive local activity metadata.

Mitigation: Review or delete logs and baselines periodically, and avoid recording commands or URLs that contain secrets.

Risk: Suspicious findings can require human judgment because monitoring signals may be ambiguous.

Mitigation: Treat the skill's output as an alert and recommendation layer; confirm the evidence before removing a skill or escalating remediation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billyhetech/skills/permission-guard-v1)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown activity report with inline shell commands and actionable recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local audit logs and first-run baseline files under ~/.openclaw.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
