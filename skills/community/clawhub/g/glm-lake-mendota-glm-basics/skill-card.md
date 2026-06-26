## Description: <br>
Basic usage of the General Lake Model (GLM) for lake temperature simulation. Use when you need to run GLM, understand input files, or modify configuration parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run GLM lake temperature simulations, understand required input files, and adjust Fortran namelist configuration parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes local GLM command examples that assume GLM is installed and available on the user's PATH. <br>
Mitigation: Confirm GLM is installed from a trusted source before running the command examples. <br>
Risk: The command example changes to /root, which may not be the user's actual model directory. <br>
Mitigation: Run GLM from the directory that contains the intended glm3.nml and boundary condition files. <br>
Risk: The Python example overwrites glm3.nml while modifying configuration parameters. <br>
Mitigation: Back up glm3.nml before applying scripted parameter changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/glm-lake-mendota-glm-basics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Fortran namelist, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local command examples and configuration-editing guidance; review paths and file changes before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
