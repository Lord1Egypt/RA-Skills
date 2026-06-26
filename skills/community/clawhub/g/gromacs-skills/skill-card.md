## Description: <br>
Provides a GROMACS command reference and workflow guidance for agents that need help preparing, running, or analyzing molecular dynamics commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CharlesHahn](https://clawhub.ai/user/CharlesHahn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, computational scientists, and agents use this skill to look up GROMACS commands, common parameters, file formats, and molecular simulation workflow guidance before proposing shell commands or run scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated GROMACS run commands can start long-running or resource-intensive jobs, especially mdrun, mpirun, and GPU-enabled commands. <br>
Mitigation: Review commands before execution; for production or long-running simulations, generate a script for the user to run in the intended compute environment. <br>
Risk: GROMACS command options and file compatibility vary by installed version and local binaries. <br>
Mitigation: Use a trusted local GROMACS installation and check `gmx <command> -h` or version-matched documentation before relying on generated parameters. <br>


## Reference(s): <br>
- [GROMACS command categories](references/command-categories.md) <br>
- [Common GROMACS parameters](references/common-parameters.md) <br>
- [GROMACS manual](https://manual.gromacs.org/) <br>
- [GROMACS GitHub repository](https://github.com/gromacs/gromacs) <br>
- [GROMACS user forum](https://gromacs.bioexcel.eu/) <br>
- [GROMACS tutorials](http://www.mdtutorials.com/gmx/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and scripts should be reviewed before execution and matched to the local GROMACS installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
