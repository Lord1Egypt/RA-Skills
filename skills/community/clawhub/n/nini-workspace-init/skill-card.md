## Description: <br>
Workspace Init guides an agent through collecting project details, scaffolding a dev-config-template workspace, cloning sub-repositories, configuring OpenSpec and development environments, and validating the setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize or update a multi-repo workspace from dev-config-template, including project metadata, repository layout, OpenSpec configuration, local development setup, and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied repository URLs may clone unintended or untrusted code into the workspace. <br>
Mitigation: Review the target directory and every repository URL before confirming setup or template updates. <br>
Risk: Dependency installation in cloned repositories can execute code from those projects and package ecosystems. <br>
Mitigation: Install dependencies only for repositories and package sources the user has reviewed and intends to trust. <br>
Risk: Generated CLAUDE.md and workspace configuration files can change agent behavior and project workflow. <br>
Mitigation: Review generated CLAUDE.md, repos.json, OpenSpec config, and workspace files before committing or using the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/niracler/nini-workspace-init) <br>
- [dev-config-template](https://github.com/niracler/dev-config-template) <br>
- [Release v0.3.0](https://github.com/niracler/skill/releases/tag/v0.3.0) <br>
- [CLAUDE.md placeholder fields](references/claude-md-fields.md) <br>
- [OpenSpec configuration template](references/config-template.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON, YAML, Markdown, and VS Code workspace configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive setup flow that may write workspace files, clone user-specified repositories, install dependencies, create commits, and report validation results.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
