## Description: <br>
Provides standardized pytest config, reusable fixtures, and CI integration patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up or audit pytest infrastructure for Python plugin projects, including pyproject.toml settings, reusable conftest.py fixtures, Git workflow test fixtures, mock tool fixtures, and GitHub Actions CI patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CI workflow snippets install project dependencies and may upload coverage from a repository context. <br>
Mitigation: Review dependency installation commands and Codecov/GitHub Actions settings before copying the snippets into a real project. <br>
Risk: Generic pytest, fixture, and coverage examples may not match a project's import paths, markers, or quality thresholds. <br>
Mitigation: Adapt the examples to the target repository and verify them with pytest collection and coverage runs before relying on them in CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-leyline-pytest-config) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Conftest patterns](modules/conftest-patterns.md) <br>
- [Git testing fixtures](modules/git-testing-fixtures.md) <br>
- [Mock fixtures](modules/mock-fixtures.md) <br>
- [CI integration](modules/ci-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TOML, Python, YAML, Makefile, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference patterns for pytest configuration, fixtures, and CI/CD integration; review snippets before copying into a repository.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter states 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
