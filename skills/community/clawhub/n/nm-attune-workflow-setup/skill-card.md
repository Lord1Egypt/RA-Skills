## Description: <br>
Configures GitHub Actions CI/CD workflows for testing, linting, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to create or update GitHub Actions workflows for Python, Rust, or TypeScript projects, including testing, linting, build, release, and deployment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CI/CD workflow changes can affect testing, publishing, deployment, and repository secrets. <br>
Mitigation: Review proposed workflow files before committing them, confirm triggers and secrets are intentional, and require explicit approval before broad automation prompts make CI/CD changes. <br>


## Reference(s): <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell, Python, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or modify GitHub Actions workflow files such as test.yml, lint.yml, build.yml, publish.yml, release.yml, and deploy.yml.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
