## Description: <br>
Generates Git hook scripts that format code, check lint rules, and run tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to create local Git hooks for routine repository checks such as linting and tests before commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes .git/hooks/pre-commit and may replace an existing local hook. <br>
Mitigation: Check existing hook files before running it, use it only in the intended repository, and edit or remove the generated npm lint and test commands if they do not fit the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/git-hooks-generator) <br>
- [Publisher profile](https://clawhub.ai/user/Sunshine-del-ux) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash commands and generated shell script content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local Git hook files when the generated script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
