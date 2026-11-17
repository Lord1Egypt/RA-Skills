## Description:

Provides Chinese-language GROMACS molecular dynamics command reference guidance for agents that need help choosing commands, parameters, file formats, and workflow steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleshahn](https://clawhub.ai/user/charleshahn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, computational scientists, and agents use this skill to prepare, run, troubleshoot, and analyze GROMACS molecular dynamics workflows while checking local command help for version-specific options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated GROMACS commands or run scripts can consume substantial compute or overwrite simulation outputs, especially production mdrun jobs.

Mitigation: Review generated commands, file paths, resource settings, and scripts before execution; production runs should be executed by the user in the intended compute environment.

Risk: GROMACS command-line options vary by installed version, so stale parameters can fail or produce unintended behavior.

Mitigation: Run gmx <command> -h locally and compare generated commands against the installed GROMACS version before use.

## Reference(s):

- [GROMACS command categories](references/command-categories.md)
- [Common GROMACS parameters](references/common-parameters.md)
- [GROMACS manual](https://manual.gromacs.org/)
- [GROMACS GitHub repository](https://github.com/gromacs/gromacs)
- [GROMACS user forum](https://gromacs.bioexcel.eu/)
- [GROMACS tutorials](http://www.mdtutorials.com/gmx/)
- [ClawHub skill page](https://clawhub.ai/charleshahn/skills/gromacs-skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and parameter tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce example GROMACS commands and run scripts for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
