## Description: <br>
A cross-session handoff protocol for Claude Code and other AI agents that freezes work context into a local handoff.md file and restores execution in a later session after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Allen-Cao](https://clawhub.ai/user/Allen-Cao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to pause long-running AI-agent work, preserve the minimum execution state, and resume that work across sessions, agents, or devices without re-explaining the task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Handoff files may persist sensitive task context or regulated data on local or synced storage. <br>
Mitigation: Review handoff contents before syncing or sharing them, avoid saving secrets or regulated data, and prefer a local-only HANDOFF_ROOT for sensitive projects. <br>
Risk: Session identifiers in handoff files may expose cross-session linkage. <br>
Mitigation: Remove Session ID values when cross-session linkage is sensitive in the deployment environment. <br>


## Reference(s): <br>
- [Templates V2](artifact/references/templates.md) <br>
- [Handoff V2 Usage Documentation](artifact/使用文档.md) <br>
- [ClawHub Release Page](https://clawhub.ai/Allen-Cao/handoff-session) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown handoff files, concise recovery previews, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or reads local handoff.md files under the configured HANDOFF_ROOT; default location is ~/.agents/handoff_context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
