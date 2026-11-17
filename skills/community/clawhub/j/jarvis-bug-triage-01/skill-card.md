## Description:

Jarvis Bug Triage 01 helps agents triage production bugs with repro isolation, risk-first fixes, repeatable steps, quality gates, and practical outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xammarie](https://clawhub.ai/user/xammarie)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to turn production bug reports or messy development notes into evidence-backed triage, ranked findings, and an action plan with acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger language may be applied to security-sensitive, credential-related, infrastructure, or production-changing work.

Mitigation: Use judgment before applying the skill to sensitive work and review any commands or changes the agent proposes before execution.

Risk: Triage output may include incorrect or incomplete recommendations if the supplied evidence is weak.

Mitigation: Apply the skill's evidence-backed claims, explicit assumptions, quality gates, and fallback-plan checks before acting on recommendations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with concise summaries, ranked findings, action plans, risk mitigations, checklists, and commands where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, persistence, credential handling, or hidden behavior is identified in the provided security evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
