## Description: <br>
Helps calculate motor design parameters, including pole-slot combinations, winding factors, flux density, back EMF, torque constants, and related performance estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and motor engineers use this skill to estimate early-stage motor parameters and compare pole-slot, winding, magnetic, back-EMF, and torque options using local calculator scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents or users to run local Python or Node.js calculator scripts. <br>
Mitigation: Confirm the artifact files match the expected motor-parameter purpose and run them in a controlled environment before relying on results. <br>
Risk: Motor-design outputs are simplified estimates and may be unsuitable as final engineering specifications. <br>
Mitigation: Validate calculations with qualified engineering review, domain tools, and project-specific constraints before making design or safety decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and terminal text reports from Python or Node.js calculators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive and command-line modes are available; calculation results are engineering estimates and should be reviewed before design decisions.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
