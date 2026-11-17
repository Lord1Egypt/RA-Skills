## Description:

Generator economic dispatch and cost optimization for power systems, including generation cost minimization, optimal generator setpoints, operating margins, and generator cost functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power-system engineers use this skill to formulate economic dispatch problems, apply MATPOWER generator and cost-function conventions, compute generator dispatch and reserves, and summarize operating cost and margin outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dispatch recommendations can be misleading if solver assumptions, generator limits, cost coefficients, load data, or reserve requirements do not match the real operating case.

Mitigation: Review generated dispatch code, input data, solver status, and optimization assumptions before using outputs for operational or financial decisions.

Risk: The skill includes reference code for economic dispatch and reserve co-optimization but does not validate complete power-system feasibility on its own.

Mitigation: Use appropriate power-flow or OPF validation, including network constraints where required, before relying on dispatch setpoints.

## Reference(s):

- [Generator Cost Functions Reference](references/cost-functions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Python code examples and structured output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides mathematical formulations, solver guidance, dispatch output fields, and total cost/load/reserve summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
