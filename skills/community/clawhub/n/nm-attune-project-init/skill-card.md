## Description: <br>
Scaffolds new projects with git, CI/CD workflows, pre-commit hooks, and build config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize or update Python, Rust, and TypeScript projects with common development infrastructure, including git, CI workflows, pre-commit hooks, Makefile targets, and starter configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to modify the current project directory by adding scaffolding files, git setup, hooks, and CI configuration. <br>
Mitigation: Review proposed file changes and overwrite prompts before applying them, preferably in a clean working tree or disposable project directory. <br>
Risk: The artifact references an external Attune plugin script that is not included in the release artifact. <br>
Mitigation: Inspect the external script before installing or running it, and treat its behavior as outside the verified artifact. <br>
Risk: Generated project defaults may not match an existing repository's conventions or constraints. <br>
Mitigation: Validate generated Makefile targets, dependency configuration, CI workflows, and tests before committing the scaffolded changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-project-init) <br>
- [Attune homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration/code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or create project scaffolding files, git setup, hooks, and CI configuration after user review.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
