## Description:

Calculate PI/PID controller gains using Internal Model Control (IMC) tuning rules for first-order systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and control engineers use this skill to calculate and explain IMC-tuned PI/PID gains for first-order process models after estimating process gain and time constant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: IMC tuning examples may be applied directly to physical equipment without validating process parameters, output limits, or controller behavior.

Mitigation: Review the gains with a qualified engineer, validate parameters, add explicit output limits and anti-windup behavior, simulate the controller, and use supervised staged testing before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with formulas and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides educational controller tuning guidance and sample code; outputs require engineering review before use with physical systems.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
