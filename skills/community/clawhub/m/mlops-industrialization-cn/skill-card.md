## Description:

Transform prototypes into distributable Python packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to turn notebook-style machine learning prototypes into Python packages with a src layout, layered modules, and starter training code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package generator can write or overwrite files outside the intended package directory if given a crafted package name.

Mitigation: Run the generator only with a simple trusted package name and avoid slashes or dot-dot path components.

Risk: The generator writes predictable files such as features.py, data.py, train.py, and test package initializers.

Mitigation: Run it in a clean project or review existing files before execution to avoid unintended overwrites.

## Reference(s):

- [MLOps Coding Course](https://github.com/MLOps-Courses/mlops-coding-skills)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated Python package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Package names should be simple trusted identifiers when using the generator script.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
