## Description: <br>
Generates phased, dependency-ordered implementation tasks from completed specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and implementation agents use this skill after a specification is complete to convert requirements into phased task lists with explicit dependencies, affected files, parallelization markers, and completion criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic triggers such as tasks, planning, implementation, and dependencies may activate the skill in ordinary planning conversations. <br>
Mitigation: Confirm the user is asking to turn a completed specification into an implementation task plan before relying on the output. <br>
Risk: Generated task plans may include incorrect dependencies, unsafe parallelization, or incomplete verification criteria. <br>
Mitigation: Review file overlaps, task ordering, and completion criteria before executing the plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-spec-kit-task-planning) <br>
- [Clawdis homepage](https://github.com/athola/claude-night-market/tree/master/plugins/spec-kit) <br>
- [Task phase structure](modules/phase-structure.md) <br>
- [Task dependency patterns](modules/dependency-patterns.md) <br>
- [Technology stack patterns](modules/tech-stack-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown task plan with phased task entries, dependency fields, affected file paths, and verification criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include parallel markers and code or shell snippets when useful.] <br>

## Skill Version(s): <br>
1.9.13 (source: release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
