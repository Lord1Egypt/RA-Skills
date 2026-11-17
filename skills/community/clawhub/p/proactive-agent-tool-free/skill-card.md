## Description: <br>
A Markdown-only agent skill that helps an AI agent proactively suggest next steps, persist working memory, ask clarifying reverse prompts, apply safety reminders, and attempt basic self-repair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual agent users use this skill to add proactive task suggestions, simple memory persistence, reverse prompting, safety reminders, and self-repair routines to SKILL.md-compatible agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and agent-behavior file writes can preserve sensitive or incorrect context. <br>
Mitigation: Review proposed memory and configuration writes, keep backups, and avoid using the skill with sensitive prompts or private project data unless controls are in place. <br>
Risk: Shell command use and local configuration inspection can expose credentials or change workspace state. <br>
Mitigation: Use a low-risk workspace, inspect commands before approval, and constrain command execution and network access where possible. <br>
Risk: External API or network use may send local context outside the workspace. <br>
Mitigation: Approve network calls explicitly, redact secrets, and disable external access when working with confidential data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/proactive-agent-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local memory or configuration writes and command execution; users should review actions before approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
