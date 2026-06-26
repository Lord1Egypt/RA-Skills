## Description: <br>
Generates Makefiles with testing, linting, formatting, and automation targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or update standard Makefiles for Python, Rust, or TypeScript projects with common development workflow targets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Makefiles can include targets that install dependencies, publish packages, remove generated files, or build artifacts. <br>
Mitigation: Review the generated Makefile before running targets such as install, publish, clean, or build. <br>
Risk: Broad trigger terms may activate the skill for general automation requests where Makefile generation is not desired. <br>
Mitigation: Use the skill only when Makefile-based automation is explicitly wanted for the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-makefile-generation) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Makefile snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Covers common Python, Rust, and TypeScript Makefile targets; generated Makefiles should be reviewed before targets are run.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
