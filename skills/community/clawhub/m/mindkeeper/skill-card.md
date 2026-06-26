## Description: <br>
Time Machine for Your AI's Brain - version control for agent context files, used when users ask about changes in SOUL.md, AGENTS.md, MEMORY.md, or other agent context files, want to undo, rollback, or compare versions, or need a checkpoint before risky edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhao6741](https://clawhub.ai/user/liuhao6741) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users install this skill so an agent can inspect history, show diffs, create checkpoints, and guide preview-first rollback for AI context and memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables persistent tracking and rollback of AI context and memory files, which can expose sensitive content if those files contain secrets. <br>
Mitigation: Avoid storing secrets in tracked context files and review tracked files before enabling ongoing history. <br>
Risk: First-use setup may install the external mindkeeper-openclaw plugin and restart Gateway. <br>
Mitigation: Require explicit user confirmation before plugin installation or Gateway restart, and review the plugin before approving setup in sensitive environments. <br>
Risk: Rollback can restore older file content that changes the active agent context. <br>
Mitigation: Inspect rollback previews carefully and execute rollback only after confirmation. <br>


## Reference(s): <br>
- [Mindkeeper ClawHub page](https://clawhub.ai/liuhao6741/mindkeeper) <br>
- [Mindkeeper homepage](https://github.com/seekcontext/mindkeeper) <br>
- [mindkeeper-openclaw package](https://www.npmjs.com/package/mindkeeper-openclaw) <br>
- [Mindkeeper support](https://github.com/seekcontext/mindkeeper/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline tool calls and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of mind_status, mind_history, mind_diff, mind_snapshot, and preview-first mind_rollback; setup commands require user confirmation.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
