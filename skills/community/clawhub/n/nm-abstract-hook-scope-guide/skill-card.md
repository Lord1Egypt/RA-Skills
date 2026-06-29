## Description: <br>
Select hook scope (plugin, project, global) by audience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to decide whether Claude Code hooks belong in a plugin, a shared project configuration, or a personal global configuration. It helps authors account for audience, version control, persistence, and hook security implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook examples that write logs, read tool input, or apply globally can run with the user's account permissions across projects if copied without review. <br>
Mitigation: Review each hook before use, prefer the narrowest appropriate scope, and test global hooks carefully before enabling them broadly. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-abstract-hook-scope-guide) <br>
- [OpenClaw Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks) <br>
- [Claude Code Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no tool calls or commands are executed by the skill itself.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
