## Description: <br>
Performs precise math calculations by executing native operating-system command-line calculators such as bc, python3, or PowerShell instead of relying on model prediction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnnyhou327](https://clawhub.ai/user/johnnyhou327) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to calculate mathematical expressions with local command-line tooling when deterministic numeric output is preferred over model-generated arithmetic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted calculator input can escape into commands on the user's machine. <br>
Mitigation: Use only trusted expressions unless the skill is changed to use a safe math parser, strict input validation, and no shell interpolation. <br>
Risk: The skill executes local command-line tools to compute results. <br>
Mitigation: Review the skill before installing and avoid running it on machines with sensitive files or credentials until the command-execution risk is addressed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnnyhou327/math-utils-native) <br>
- [Publisher profile](https://clawhub.ai/user/johnnyhou327) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text calculation results and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the caller-provided expression as input and returns either the computed result or an execution error message.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
