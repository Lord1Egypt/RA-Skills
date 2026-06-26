## Description: <br>
Generates phased, dependency-ordered implementation tasks from specifications after the specification is complete and before implementation starts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn completed specifications and implementation plans into phased, dependency-ordered task lists before implementation begins. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation words may cause the skill to appear during generic planning or implementation conversations. <br>
Mitigation: Confirm the task is specifically about converting a completed specification into implementation tasks before relying on the output. <br>
Risk: The referenced Night Market or Claude Code plugin may include agents, hooks, or commands beyond this Markdown-only skill. <br>
Mitigation: Review the referenced plugin separately before installing any additional components. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/nm-spec-kit-task-planning) <br>
- [Skill Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/spec-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown task lists with phased task entries, dependencies, file paths, and completion criteria.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tasks use TASK-NNN identifiers, phase labels, dependency fields, and [P] markers for parallel work.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
