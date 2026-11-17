## Description:

DC power flow analysis for power systems. Use when computing power flows using DC approximation, building susceptance matrices, calculating line flows and loading percentages, or performing sensitivity analysis on transmission networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power-system engineers use this skill to apply DC power-flow approximations, build susceptance matrices, compute line flows and loading percentages, and prepare linear constraints for dispatch or contingency studies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable helper reads a user-supplied power-network JSON file.

Mitigation: Run it only on input data you intend to analyze.

Risk: DC power flow is a linearized approximation and may not capture AC power-flow behavior.

Mitigation: Confirm the documented DC assumptions are appropriate before using results for operational decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with Python code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an executable Python helper that reads a local power-network JSON file and requires NumPy.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
