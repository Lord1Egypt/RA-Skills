## Description:

Executes Jungle Laws to enforce strict rule validation, risk control, consensus, and self-audit for trading, high-stakes decisions, and multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calwedbot-del](https://clawhub.ai/user/calwedbot-del)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to apply strict decision validation and self-audit gates to trading/options decisions, high-stakes task decisions, and multi-agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives itself broad control over agent decisions.

Mitigation: Limit use to explicit trading or audit requests where strict decision-discipline checks are desired.

Risk: The skill asks to write behavior-shaping records into memory.

Mitigation: Require explicit approval before any memory write and remove automatic memory writes when deploying the skill.

Risk: The artifact references files or script names that are not present in the release.

Mitigation: Verify referenced resources before use and rely only on included files unless missing references are supplied.

## Reference(s):

- [Jungle Laws and Warden Protocols](references/laws.md)
- [ClawHub skill page](https://clawhub.ai/calwedbot-del/skills/jungle-executor)
- [Publisher profile](https://clawhub.ai/user/calwedbot-del)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown guidance with optional shell command examples and validation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the agent to apply rule checks, flag violations, and log decision-review outcomes when explicitly approved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
