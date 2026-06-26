## Description: <br>
Generator economic dispatch and cost optimization for power systems. Use when minimizing generation costs, computing optimal generator setpoints, calculating operating margins, or working with generator cost functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power-system engineers use this skill to formulate generator economic dispatch problems, choose cost functions, compute generator setpoints, model reserve requirements, and summarize dispatch costs and operating margins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated optimization code or dispatch results could be wrong if cost curves, generator limits, load, or reserve inputs are incomplete or mis-modeled. <br>
Mitigation: Review input data assumptions, generated code, and solver outputs before using results for operational or financial decisions. <br>
Risk: Solver choice and numerical conditioning can affect economic dispatch results. <br>
Mitigation: Use the documented CLARABEL solver guidance for quadratic costs with network constraints and validate outputs against expected power-balance and reserve constraints. <br>


## Reference(s): <br>
- [Generator Cost Functions Reference](references/cost-functions.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wu-uk/grid-dispatch-operator-economic-dispatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, code, configuration] <br>
**Output Format:** [Markdown with Python code blocks and structured dispatch examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optimization formulation guidance, MATPOWER data conventions, reserve constraints, and dispatch summary examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
