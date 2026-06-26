## Description: <br>
Transform prototypes into distributable Python packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ML engineers use this skill to convert notebook-style prototypes into Python package scaffolds with a src layout, separated domain, I/O, and application layers, and starter training code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package scaffold script writes files under src and tests in the current directory. <br>
Mitigation: Run it from the intended project directory and avoid directories with important existing src or tests files unless they are backed up. <br>
Risk: Unexpected package names can produce confusing paths or invalid Python package names. <br>
Mitigation: Use a simple Python package name containing only letters, numbers, and underscores. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated Python package files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local src and tests package scaffolding when the bundled shell script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
