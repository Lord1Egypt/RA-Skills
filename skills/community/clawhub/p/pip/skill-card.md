## Description:

Use pip for Python package install, upgrade, freeze, and dependency file workflows with virtual environments first. Use when handling requirements.txt, pip install errors, pipx vs pip decisions, or reproducible Python dependency setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Python project dependencies, create virtual environments, install or pin requirements, and troubleshoot common pip failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation can run untrusted dependency code or install unexpected versions.

Mitigation: Review requirements and package names before installing; pin versions or use hashes for sensitive projects.

Risk: Global pip installs can alter the user's system Python environment.

Mitigation: Prefer project-local virtual environments with --venv and use python3 -m pip to avoid interpreter mismatch.

Risk: The helper confirms package removal with -y during uninstall.

Mitigation: Review uninstall package names before execution and prefer running inside a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jvy/skills/pip)
- [Publisher profile](https://clawhub.ai/user/jvy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose package installation, virtual environment, requirements, freeze, and uninstall commands for user review before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
