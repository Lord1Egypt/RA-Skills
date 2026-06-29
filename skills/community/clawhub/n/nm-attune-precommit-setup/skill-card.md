## Description: <br>
Configures pre-commit hooks for linting, type checking, formatting, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up pre-commit quality gates for new or existing repositories, including global linters, type checks, tests, component-specific hooks, validation hooks, and matching CI checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pre-commit configurations and local hook scripts can affect commit flow and may run project Makefiles or local commands. <br>
Mitigation: Review the generated .pre-commit-config.yaml, local hook scripts, and CI workflow before enabling them, then test on a branch before team-wide rollout. <br>
Risk: The optional Codecov upload in the CI example can share CI coverage data with an external service. <br>
Mitigation: Confirm Codecov is approved for the repository and configure its permissions and token handling, or omit the upload step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-precommit-setup) <br>
- [OpenClaw metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks) <br>
- [ruff pre-commit](https://github.com/astral-sh/ruff-pre-commit) <br>
- [mypy pre-commit mirror](https://github.com/pre-commit/mirrors-mypy) <br>
- [Bandit](https://github.com/PyCQA/bandit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, TOML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only artifact; generated configurations and scripts require user review before use.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
