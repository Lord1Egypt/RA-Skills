## Description:

LLM as Judge helps agents use a different model as a judge to review complex plans, code, architecture, security-sensitive work, production deployment decisions, or repeated failed attempts before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngmeyer](https://clawhub.ai/user/ngmeyer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to request cross-model review for high-stakes or complex work, including architecture, system design, security review, financial or trading systems, and large implementation plans. The skill supplies activation criteria, model-pairing guidance, verdict expectations, and judge prompt templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed material may include private code, customer data, secrets, incident details, payment or authentication logic, or trading system information that could be exposed to a judge model provider.

Mitigation: Use only approved judge model providers and redact sensitive content before invoking this workflow.

## Reference(s):

- [Judge Prompt Templates](artifact/references/judge-prompts.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown guidance and judge prompt templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review criteria, verdict formats, scored feedback structures, and actionable recommendations for an agent workflow.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
