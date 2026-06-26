## Description: <br>
Task automation, containerization, CI/CD, and experiment tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and ML engineers use this skill to add task automation, container build commands, GitHub Actions CI, and MLflow tracking guidance to MLOps projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CI workflow uses third-party GitHub Actions and can upload coverage data to Codecov. <br>
Mitigation: Review the workflow before enabling it, decide whether Codecov uploads are acceptable for the repository, and pin third-party actions to commit SHAs for sensitive projects. <br>
Risk: The skill references justfile and Dockerfile templates that are not present in the artifact. <br>
Mitigation: Add missing templates only from a trusted source and review them before running build, test, or container commands. <br>


## Reference(s): <br>
- [CI workflow template](references/ci-workflow.yml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash, YAML, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides copy commands and examples for project automation, CI, Docker, and MLflow setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
