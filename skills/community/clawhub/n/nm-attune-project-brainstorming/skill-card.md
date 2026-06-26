## Description: <br>
Guides project ideation via Socratic questioning to produce a validated brief before specification when requirements are unclear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, product owners, and project teams use this skill to turn unclear project ideas into a structured project brief with problem framing, constraints, approach comparison, and decision rationale. It is intended for early planning before detailed specification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may pass project context to downstream skills or subagents and continue into later workflow phases without fresh confirmation. <br>
Mitigation: Avoid sensitive strategy or stakeholder details unless that sharing is acceptable; use standalone or skip options, or explicitly stop after brainstorming when continuation is not desired. <br>
Risk: The workflow writes local planning documents and stores brainstorming state. <br>
Mitigation: Review generated files before sharing or committing them, and remove sensitive details from the project brief or session state. <br>
Risk: Generated planning guidance can contain vague requirements, missing acceptance criteria, or other gaps. <br>
Mitigation: Use the included review loop or a manual review before implementation, and surface unresolved issues to a human reviewer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-project-brainstorming) <br>
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown project brief with structured planning sections, optional shell commands, and local session state JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces docs/project-brief.md, may store brainstorming state, and may continue into review or specification steps unless the user selects a standalone or skip option.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
