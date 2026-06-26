## Description: <br>
Huo15 OpenClaw Enhance is a third-party OpenClaw plugin that adds memory, planning, routing, upload and share bridges, diagnostics, status, and workflow tools without modifying OpenClaw core behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to add an enhancement suite for memory, task planning, status visibility, model routing, file upload and sharing flows, diagnostics, and workflow support around OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin is a broad default-on enhancement suite with memory, routing, upload, bridge, and persistence behavior. <br>
Mitigation: Review the enabled modules before deployment and disable features that are not needed for the target OpenClaw environment. <br>
Risk: Upload, share, dashboard, bridge, and memory export features can expose or persist sensitive local data. <br>
Mitigation: Limit use to trusted workspaces, review generated links and file paths, and avoid enabling upload/share or memory export modules unless their data flow is required. <br>
Risk: Bundled LaunchAgent scripts and generated launchctl commands can schedule file movement or deletion under the user's account. <br>
Mitigation: Run scheduled-task setup only after manually reviewing the command and confirming that the scheduled file operations are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-huo15-openclaw-enhance) <br>
- [Project homepage](https://cnb.cool/huo15/ai/huo15-openclaw-enhance) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Claude Code documentation](https://docs.claude.com/en/docs/claude-code/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON-like tool results, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include OpenClaw tool results, diagnostic summaries, generated commands, status data, and file upload or share links.] <br>

## Skill Version(s): <br>
6.7.13 (source: server release evidence, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
