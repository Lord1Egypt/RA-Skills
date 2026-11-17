## Description:

Task automation, containerization, CI/CD, and experiment tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers and ML engineers use this skill to add common MLOps automation patterns to a project, including task runner commands, Docker builds, GitHub Actions CI, and MLflow tracking examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CI workflow template uses external services and mutable dependencies, including GitHub Actions, Python build installation, uv dependency sync, Docker builds, and Codecov upload.

Mitigation: Review the workflow before copying it into a repository, pin actions and build dependencies, add least-privilege workflow permissions, and confirm Codecov upload is acceptable for the project.

Risk: Project automation templates may not match a target repository's package layout, test paths, Docker context, or release process.

Mitigation: Adapt the copied commands and templates to the target project and run them in a controlled branch or CI environment before using them for sensitive repositories.

## Reference(s):

- [CI workflow template](references/ci-workflow.yml)
- [MLOps Coding Course](https://github.com/MLOps-Courses/mlops-coding-skills)
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/mlops-automation-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, Python, YAML, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces copyable project automation guidance and template references; review commands and workflow settings before execution.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
