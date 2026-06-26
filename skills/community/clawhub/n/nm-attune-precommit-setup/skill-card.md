## Description: <br>
Configures pre-commit hooks for linting, type checking, formatting, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up layered pre-commit quality gates, CI checks, and troubleshooting patterns for code repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated pre-commit and CI configurations may run local scripts and external tools during commits or continuous integration. <br>
Mitigation: Review generated hook entries, local script paths, external hook repositories, and CI services before enabling them in a project. <br>
Risk: Documented cache-cleanup commands delete matching cache directories. <br>
Mitigation: Run cleanup commands only after checking the target paths and limiting them to disposable pre-commit, Python, pytest, or mypy caches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-precommit-setup) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with YAML, TOML, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces pre-commit, CI, type-checking, testing, and troubleshooting recommendations for repository quality gates.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
