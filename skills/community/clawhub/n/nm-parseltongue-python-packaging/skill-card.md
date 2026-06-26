## Description: <br>
Python package creation and PyPI distribution via pyproject.toml and entry points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create Python packages, configure pyproject.toml, define entry points, manage uv workflows, and prepare PyPI publishing or CI/CD release pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing commands can make package artifacts public and may use publishing credentials. <br>
Mitigation: Review uv publish targets and credentials before running publishing commands, and use TestPyPI when validating a release. <br>
Risk: Cleanup commands can delete local build artifacts from the current project. <br>
Mitigation: Run destructive cleanup commands only from the intended project directory after confirming the paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-parseltongue-python-packaging) <br>
- [Homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/parseltongue) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, TOML, YAML, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples for project layout, pyproject.toml configuration, uv workflows, entry points, and GitHub Actions publishing.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
