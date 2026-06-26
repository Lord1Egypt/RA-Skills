## Description: <br>
Orchestrates Spec Driven Development by coordinating spec, plan, and task skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to coordinate spec-driven development workflows, load complementary planning skills, and track specification, plan, and task artifacts across speckit commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic planning and workflow triggers may cause the skill to appear during ordinary planning discussions. <br>
Mitigation: Prefer explicit /speckit-* command invocation or disable the skill when working outside spec-driven projects. <br>
Risk: The skill guides agents to read or update planning artifacts such as spec.md, plan.md, and tasks.md. <br>
Mitigation: Review proposed artifact changes before using them as implementation instructions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/athola/nm-spec-kit-speckit-orchestrator) <br>
- [Project homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/spec-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command references and checklist-style progress items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces planning and orchestration guidance for spec, plan, task, checklist, and implementation workflows.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
