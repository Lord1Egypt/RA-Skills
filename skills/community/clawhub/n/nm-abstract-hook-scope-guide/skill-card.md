## Description: <br>
Select hook scope (plugin, project, global) by audience. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and plugin authors use this skill to decide whether Claude Code hooks belong in plugin, project, or global configuration based on audience, version-control needs, and persistence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hook configurations can execute commands or apply beyond the intended audience when scoped too broadly. <br>
Mitigation: Review the chosen scope, prefer project settings for team rules, and test global hooks before enabling them. <br>
Risk: Examples may involve local file access or command execution in Claude Code settings. <br>
Mitigation: Review proposed hook commands and required permissions before adding them to plugin, project, or user configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-abstract-hook-scope-guide) <br>
- [Publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Claude Code Hooks Documentation](https://docs.anthropic.com/en/docs/claude-code/hooks) <br>
- [Claude Code Settings Configuration](https://docs.anthropic.com/en/docs/claude-code/settings) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with JSON and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides decision criteria and examples for plugin, project, and global hook scopes.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence; artifact frontmatter reports 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
