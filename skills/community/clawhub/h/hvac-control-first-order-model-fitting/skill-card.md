## Description:

Fit first-order dynamic models to experimental step response data and extract K (gain) and tau (time constant) parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to fit simple first-order response models to measured step-response data and estimate process gain and time constant values for analysis or control design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formula or example-code misuse could produce misleading K and tau estimates for systems that do not match first-order step-response assumptions.

Mitigation: Review the formulas for the target system, check units, compare the fit against measured data, and use R-squared or RMS error before relying on the result.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with equations and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No tool calls, system access, or generated files are required by the skill.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
