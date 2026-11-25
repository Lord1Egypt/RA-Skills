## Description:

Automates desktop applications by turning a plain-language goal or a single intent into screen-aware actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lahfir](https://clawhub.ai/user/lahfir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to automate desktop applications with a whole natural-language goal or to resolve one action at a time while keeping the interaction plan in their control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screen descriptions sent to the configured decision service can include private document or form content; the security review is incomplete.

Mitigation: Verify that the configured endpoint is expected and trusted, use --no-values when practical, and avoid sensitive screens or data unless you understand what will be transmitted.

## Reference(s):

- [jev-desktop on ClawHub](https://clawhub.ai/lahfir/skills/jev-desktop)
- [Publisher profile: lahfir](https://clawhub.ai/user/lahfir)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell command examples, JSON action results, and text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a clone of agent-desktop and TYPESAFE_API_KEY; screen descriptions may be sent to the configured decision endpoint.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
