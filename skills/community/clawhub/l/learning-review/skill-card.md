## Description: <br>
Learning Review helps an agent turn learning notes into post-learning reviews, weekly internalization reports, and biweekly application checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayf3](https://clawhub.ai/user/mayf3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to review recent learning, identify what should become persistent working guidance, and track whether learned concepts are being applied in daily work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change learning notes and agent-behavior files such as AGENTS.md, TOOLS.md, SOUL.md, MEMORY.md, memory files, or extracted skills. <br>
Mitigation: Require the agent to show proposed changes before editing persistent guidance or memory files, and keep review logs in a dedicated learning/reviews directory unless promotion is explicitly approved. <br>


## Reference(s): <br>
- [Learning Review on ClawHub](https://clawhub.ai/mayf3/learning-review) <br>
- [Directory Structure](references/directory-structure.md) <br>
- [Internalization Guide](references/internalization-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, checklists, cron prompt text, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create review files under learning/reviews and propose or perform updates to persistent agent guidance files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
