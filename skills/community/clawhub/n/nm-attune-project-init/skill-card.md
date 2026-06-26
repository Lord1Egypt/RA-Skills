## Description: <br>
Scaffolds new projects with git, CI/CD workflows, pre-commit hooks, and build config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize or update Python, Rust, and TypeScript projects with standard project metadata, git setup, CI/CD workflows, pre-commit hooks, Makefile targets, and build configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may cause the skill to activate for project setup requests that are only loosely related. <br>
Mitigation: Confirm the intended language and setup scope before applying generated project changes. <br>
Risk: Project metadata may include a git-configured author name or email that the user does not want written into generated files. <br>
Mitigation: Review inferred author and email values before accepting generated metadata. <br>
Risk: Template rendering and git setup can create or overwrite project files and configuration. <br>
Mitigation: Review existing-file conflicts and generated diffs, then skip, overwrite, or merge files intentionally. <br>


## Reference(s): <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose project files, metadata values, git initialization, and validation commands for user review.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release evidence; artifact frontmatter is 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
