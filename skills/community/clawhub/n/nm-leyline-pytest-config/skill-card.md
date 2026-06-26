## Description: <br>
Provides standardized pytest configuration, reusable fixtures, and CI integration patterns for Python project test infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up or audit pytest configuration, shared fixtures, Git test helpers, mocks, and CI test workflows for Python plugins and projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Git fixture examples and generated commands could affect real repositories if copied without review. <br>
Mitigation: Keep fixture code limited to temporary test directories and review Git commands before running them in real repositories. <br>
Risk: Broad pytest and testing triggers may invoke this skill during general testing conversations. <br>
Mitigation: Confirm the guidance applies to the current Python pytest task before adopting configuration, fixture, or CI changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-leyline-pytest-config) <br>
- [Project homepage from package metadata](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Pytest Configuration Modules](modules/README.md) <br>
- [Conftest Patterns](modules/conftest-patterns.md) <br>
- [Git Testing Fixtures](modules/git-testing-fixtures.md) <br>
- [CI Integration](modules/ci-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TOML, YAML, Python, and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API keys or external services are required; review generated fixture and Git command examples before applying them.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
