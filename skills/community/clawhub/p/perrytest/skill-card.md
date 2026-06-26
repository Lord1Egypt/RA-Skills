## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lipairui](https://clawhub.ai/user/Lipairui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to record corrections, command failures, feature requests, and reusable lessons in local markdown learning files so future sessions can apply them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation details in local learning files. <br>
Mitigation: Do not write raw prompts, secrets, credentials, customer data, personal data, or full transcripts into .learnings files. <br>
Risk: Promoted learnings can influence future agent sessions. <br>
Mitigation: Review entries before promoting them into agent memory files such as AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions. <br>
Risk: Hook-based reminders can affect agent behavior across sessions. <br>
Mitigation: Prefer project-level setup, review hook scripts before enabling them, and enable only the hooks needed for the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lipairui/perrytest) <br>
- [Entry Examples](references/examples.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local learning-entry templates, hook setup guidance, and optional skill-scaffolding commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
