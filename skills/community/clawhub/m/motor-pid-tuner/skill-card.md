## Description:

Calculates and diagnoses PI/PID tuning for motor FOC current, speed, and position loops, with simulation, stability analysis, protection thresholds, and embedded code generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and motor-control engineers use this skill to calculate and diagnose PMSM, BLDC, and brushed DC motor controller gains, assess tuning behavior, and generate reports or embedded code. Treat calculated gains and stability results as proposals that require independent review before hardware use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags motor-control calculation correctness concerns that could lead to unsafe tuning decisions.

Mitigation: Independently review gain conversion and stability analysis; avoid safety-critical motor tuning until those concerns are resolved, and validate reviewed settings under appropriately limited test conditions before hardware use.

## Reference(s):

- [Motor PID Tuner on ClawHub](https://clawhub.ai/liujycode/skills/motor-pid-tuner)
- [Publisher profile: liujycode](https://clawhub.ai/user/liujycode)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, HTML, Code]

**Output Format:** [Structured tuning results, reports, and generated C or MATLAB code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on supplied motor parameters and selected analysis mode; reports may include gain values, response plots, and protection thresholds.]

## Skill Version(s):

1.1.0 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
