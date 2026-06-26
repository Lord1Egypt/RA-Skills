## Description: <br>
Decomposes complex user requests into executable subtasks, identifies required capabilities, searches for existing skills at skills.sh, and creates new skills when no solution exists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpzhengcn](https://clawhub.ai/user/jpzhengcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break complex workflow requests into manageable subtasks, map each subtask to required capabilities, search for matching skills, and draft an execution plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend installing, creating, or using third-party skills that may change an agent setup. <br>
Mitigation: Review each recommended or generated skill, prefer trusted publishers, and approve changes to the agent setup deliberately before installation or use. <br>
Risk: Task decomposition or capability mapping may produce incomplete or unsuitable execution plans for a user's actual workflow. <br>
Mitigation: Review the proposed subtasks, dependencies, required capabilities, and verification steps before running commands or creating new skills. <br>


## Reference(s): <br>
- [Capability Types Reference](references/capability_types.md) <br>
- [skills.sh](https://skills.sh/) <br>
- [ClawHub Skill Page](https://clawhub.ai/jpzhengcn/openclaw-super-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with structured reports, YAML-style plans, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend existing skills, propose new skill files, and outline verification steps for each subtask.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
