## Description: <br>
Multi Agent Workflow helps an agent split complex work into subtasks, assign content, research, development, or review roles, and aggregate task status and results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn a complex prompt into smaller assigned work items, then use the generated role and task data to coordinate follow-on agent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive or secret information placed in task prompts could be carried into later agent sessions if the generated output is reused. <br>
Mitigation: Avoid including secrets or highly sensitive data in prompts, and review generated subtasks before passing them to other agents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dxie48892-jpg/multi-agent-workflow) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Usage README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance, shell commands] <br>
**Output Format:** [JSON responses and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs local task splits, role assignments, role capabilities, and task status summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
