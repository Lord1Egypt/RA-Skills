## Description:

JF Open Pro AI Pet Care helps developers integrate JF Tech pet-care APIs for service status, pet profile management, abnormal alert queries, and pet behavior statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration engineers use this skill to connect applications and automation workflows to JF Tech pet-care services, including pet profile management, abnormal alert retrieval, and behavior reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live JF Tech credentials and authorization tokens may be exposed during setup or command execution.

Mitigation: Use least-privilege, revocable credentials; avoid storing secrets in TOOLS.md or shell history; and prefer environment-variable or secret-manager handling.

Risk: Delete, switch, and set-config actions can make real remote changes to pet profiles, monitoring state, and alert behavior.

Mitigation: Review commands before execution and wrap destructive or alert-disabling operations with explicit confirmation checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jftech/skills/jf-open-pro-ai-pet-care)
- [JF Tech Developer Platform](https://developer.jftech.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with Python code, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live JF Tech credentials and network access to JF Tech APIs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
