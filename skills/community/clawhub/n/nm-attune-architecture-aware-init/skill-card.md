## Description: <br>
Selects architecture paradigm via research before scaffolding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when starting a project with an undecided architecture. It gathers project context, researches current practices, selects an architecture paradigm, adapts scaffolding, and records the decision in an ADR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Web research can surface outdated, low-quality, or mismatched architecture guidance. <br>
Mitigation: Review cited sources and validate the recommendation against the captured project constraints before using it. <br>
Risk: Scaffolding steps can create or modify project files and configuration. <br>
Mitigation: Use a new or backed-up target directory and review generated structure, configuration, and ADR content before adoption. <br>
Risk: The separate full Claude Code plugin may include agents, hooks, commands, or scripts beyond this skill. <br>
Mitigation: Inspect those plugin components before installing or enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-architecture-aware-init) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, code snippets, directory layouts, and ADR content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project files and configuration when scaffolding steps are followed.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
