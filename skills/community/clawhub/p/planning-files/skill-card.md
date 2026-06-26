## Description: <br>
File-based planning for complex tasks that uses persistent markdown files as working memory to survive context resets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to organize multi-step implementation or research work by creating and maintaining task_plan.md, findings.md, and progress.md in the project workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent planning notes may contain task details, research findings, errors, or other information that should not be committed or shared. <br>
Mitigation: Review or delete task_plan.md, findings.md, and progress.md before committing, sharing, or switching tasks. <br>
Risk: The helper scripts create or inspect planning files in the current working directory. <br>
Mitigation: Run the scripts only from the intended project workspace and review generated files before relying on them. <br>


## Reference(s): <br>
- [Planning With Files on ClawHub](https://clawhub.ai/wpank/planning-files) <br>
- [Manus Context Engineering Principles](references/manus-principles.md) <br>
- [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, markdown templates, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or checks local planning files in the project workspace when the bundled helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
