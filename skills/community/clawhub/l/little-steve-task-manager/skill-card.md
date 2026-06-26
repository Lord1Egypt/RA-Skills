## Description: <br>
Little Steve Task Manager is a lightweight IM-native task system for quick task operations in chat, with daily summaries and auto status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EchoOfZion](https://clawhub.ai/user/EchoOfZion) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and workflow teams use this skill to manage lightweight task queues directly in IM/chat workflows, including adding, listing, updating, prioritizing, completing, and summarizing tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw task titles or tags can become unsafe when pasted into Bash commands without shell-safe escaping. <br>
Mitigation: Pass task text as safely escaped command arguments, avoid evaluating generated task text, and review commands before execution. <br>
Risk: Persistent JSON task data may retain bundled sample tasks or sensitive task content. <br>
Mitigation: Clear bundled sample tasks before real use and review the local data files and permissions for the intended workflow. <br>
Risk: The security verdict recommends review before installation because the skill relies on raw Bash command execution. <br>
Mitigation: Use the skill only in workflows that safely construct shell arguments and scan or review the artifact before deployment. <br>


## Reference(s): <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/EchoOfZion/little-steve-task-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples, plain-text task list output, and JSON-backed task data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq; commands persist task data in data/tasks.json and read configuration from data/settings.json.] <br>

## Skill Version(s): <br>
0.1.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
