## Description: <br>
Configures GitHub Actions CI/CD workflows for testing, linting, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add or update GitHub Actions workflows for Python, Rust, or TypeScript projects, including testing, linting, type checking, build, release, and deployment pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow changes can affect deploy, publish, release, or secret-using jobs. <br>
Mitigation: Review generated workflow files before committing them, especially jobs that use secrets or release/deploy permissions. <br>
Risk: Inline shell scripts in workflows can mask command failures if pipeline exit codes are not handled correctly. <br>
Mitigation: Use pipefail or explicit exit-code handling for complex workflow shell steps before integrating them. <br>


## Reference(s): <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-workflow-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline YAML, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose GitHub Actions workflow files and commands that should be reviewed before commit.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
