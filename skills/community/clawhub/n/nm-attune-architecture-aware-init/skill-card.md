## Description: <br>
Selects an architecture paradigm through project-context gathering and research before scaffolding a project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when starting a project whose architecture is undecided and the choice needs research, trade-off analysis, scaffolding, and an ADR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scaffolding or template guidance could alter a project structure in ways that do not match the intended architecture. <br>
Mitigation: Apply examples in an empty or dedicated project directory first, then review the generated structure before using it in an existing project. <br>
Risk: Broad triggers such as architecture or research may activate the skill for requests where architecture scaffolding is not intended. <br>
Mitigation: Confirm the user wants architecture selection or scaffolding before following the workflow. <br>
Risk: Architecture recommendations based on online research can become stale or depend on weak sources. <br>
Mitigation: Review the research synthesis, source quality, and project constraints before accepting the selected paradigm. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-attune-architecture-aware-init) <br>
- [Attune Plugin Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and structured project-scaffolding guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce an architecture recommendation, trade-off synthesis, directory layouts, configuration hints, and an ADR template.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
