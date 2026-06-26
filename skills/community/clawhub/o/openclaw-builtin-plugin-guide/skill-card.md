## Description: <br>
查询 OpenClaw 的内置插件清单、当前启用或禁用的插件列表，以及单个插件的详细说明。适用于用户想看全部内置插件、启用状态、禁用状态、插件详情、插件说明文档时。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henryczq](https://clawhub.ai/user/henryczq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to list bundled plugins, check which plugins are enabled or disabled in the current environment, and inspect details for a specific plugin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the local OpenClaw CLI and reports plugin status, diagnostics, capabilities, and documentation excerpts from the user's environment. <br>
Mitigation: Install it only when local OpenClaw catalog inspection is intended, keep a trusted openclaw binary on PATH, and review returned environment details before sharing them. <br>
Risk: Plugin details may show enabled plugins that are currently failing to load. <br>
Mitigation: Describe those plugins as enabled but failed when status is error, matching the artifact's stated handling guidance. <br>


## Reference(s): <br>
- [OpenClaw 内置插件说明](references/builtin-plugins.md) <br>
- [ClawHub skill release](https://clawhub.ai/henryczq/openclaw-builtin-plugin-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or text summaries with optional shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local OpenClaw plugin status, diagnostics, capabilities, and documentation excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
