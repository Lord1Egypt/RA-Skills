## Description:

Six-system behavior engine that adds editorial voice, selective silence, urgency-aware timing, ambient pings, daily context, and engagement adaptation to OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add opinionated voice, selective silence, urgency-based timing, ambient pings, daily message context, and engagement adaptation to proactive OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores local message and engagement history.

Mitigation: Use a per-user state directory, define retention and deletion rules, and review stored state before deploying in sensitive or shared-host environments.

Risk: The skill can generate proactive pings with incomplete cadence enforcement.

Mitigation: Disable or gate micro-initiations until users opt in and cadence tracking is reviewed for the deployment.

Risk: The optional bulk stack install may add packages outside this skill.

Mitigation: Install additional stack packages only after each package is independently reviewed and trusted.

## Reference(s):

- [Systems Overview](references/systems-overview.md)
- [Customization Guide](references/customization.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate proactive notification text and tuning guidance for cadence, silence thresholds, urgency scoring, and local state behavior.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
