## Description: <br>
Implements Manus-style file-based planning to help agents organize multi-step work, track findings and progress, and recover context after /clear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[othmanadi](https://clawhub.ai/user/othmanadi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep complex, multi-step work organized through persistent planning files, progress logs, findings, session recovery, and optional completion gating. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local agent session logs for the current project and surface prior conversation snippets during session recovery. <br>
Mitigation: Avoid using it in repositories or sessions where prompts, command arguments, or tool outputs may contain secrets. <br>
Risk: Automatic plan-file injection can place project planning content back into the agent context. <br>
Mitigation: Use attested or scoped plan modes for automatic injection and review planning files before allowing them to guide work. <br>
Risk: Gated long-running work can influence when an agent stops. <br>
Mitigation: Use gated mode only when completion criteria in task_plan.md are current and acceptable for the task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/othmanadi/planning-with-files) <br>
- [Publisher profile](https://clawhub.ai/user/othmanadi) <br>
- [Planning With Files reference](references/reference.md) <br>
- [Planning With Files examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown planning files, hook messages, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates task_plan.md, findings.md, progress.md, and optional scoped .planning files in the user's project.] <br>

## Skill Version(s): <br>
3.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
