## Description: <br>
DC power flow analysis for power systems. Use when computing power flows using DC approximation, building susceptance matrices, calculating line flows and loading percentages, or performing sensitivity analysis on transmission networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Power-system engineers and grid-dispatch developers use this skill to compute DC approximations, build susceptance matrices, calculate line flows and loading percentages, and shape linear flow constraints for dispatch or contingency analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted, malformed, or unexpectedly large network JSON can cause local script errors or unnecessary resource use. <br>
Mitigation: Run the helper only on trusted network JSON files and review input size and structure before processing. <br>
Risk: DC power-flow assumptions can misstate real AC-system behavior when lossless-line, flat-voltage, or small-angle approximations do not hold. <br>
Mitigation: Treat results as linear approximations and validate operational decisions with appropriate AC power-flow analysis and engineering review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/grid-dispatch-operator-dc-power-flow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides local DC power-flow formulas, implementation guidance, and a helper script for MATPOWER-style network JSON.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
