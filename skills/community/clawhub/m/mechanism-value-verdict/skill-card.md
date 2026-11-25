## Description:

Verdict whether a designed mechanism (pipeline node, role, gate, or ritual) earns its cost: output census, consumer tracing, executor position, cost axis, and same-kind control. Produces an evidence table plus a keep / opt-in / retire verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and maintainers use this skill to assess whether an existing workflow mechanism earns its operating cost. It guides read-only evidence gathering and turns the findings into a keep, opt-in, or retire recommendation with follow-up actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incomplete artifact or telemetry search could be mistaken for proof that a mechanism produces nothing, leading to a misleading verdict.

Mitigation: Search the intended runtime locations, check telemetry when artifacts are absent, and compare a mechanism of the same kind before drawing a conclusion.

Risk: The benign security scan is not a guarantee of zero risk.

Mitigation: Review the skill contents and decide whether they suit the intended use before installing or applying its guidance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zuoyunlai/skills/mechanism-value-verdict)
- [Publisher profile](https://clawhub.ai/user/zuoyunlai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown evidence table with a keep / opt-in / retire verdict and follow-up actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence across five assessment axes and safeguards for applying the recommendation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
