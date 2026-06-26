## Description: <br>
LessonLoop captures high-value user feedback as compact local memory and promotes durable behavior rules when justified while avoiding verbose reflection loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevengaojn2010](https://clawhub.ai/user/stevengaojn2010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use LessonLoop to capture explicit corrections, preferences, repeated mistakes, and new operating rules as compact local memory so future sessions can apply them without continuous self-reflection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User corrections, preferences, or sensitive details may be persisted in local memory files and LessonLoop logs. <br>
Mitigation: Avoid storing secrets or sensitive personal details, review memory entries periodically, and delete entries that should not affect future sessions. <br>
Risk: Scripts write to a configured workspace path, so an incorrect path can place memory files in an unintended location. <br>
Mitigation: Configure and review the workspace path before using write scripts. <br>


## Reference(s): <br>
- [LessonLoop ClawHub page](https://clawhub.ai/stevengaojn2010/lessonloop) <br>
- [README](README.md) <br>
- [Lesson types](references/lesson-types.md) <br>
- [Ollama first-pass template](references/ollama-pass-template.md) <br>
- [LessonLoop status/report format](references/status-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local Markdown memory files and JSONL LessonLoop event logs when scripts are used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
