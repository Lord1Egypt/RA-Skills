## Description: <br>
Deep AI safety guardrails workflow for reducing harmful outputs, misuse, and policy violations in LLM products through policy definition, input/output filtering, monitoring, escalation, and false-positive handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product teams, and safety reviewers use this skill to plan AI guardrails for LLM products, including policy scope, threat modeling, layered controls, monitoring, escalation, and appeals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guardrail telemetry and review workflows can expose sensitive user or enterprise content if logging is not designed carefully. <br>
Mitigation: Redact sensitive content, restrict reviewer access, define retention periods, and document who can inspect logs before using the workflow in production. <br>
Risk: Overly broad guardrails can block legitimate user requests or create inconsistent user experiences. <br>
Mitigation: Measure false positives by locale and use case, sample borderline cases for review, and provide an appeals or policy-iteration path where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/guard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown guidance and checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance-only workflow; no code execution, install hooks, credential use, or hidden privileged behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
