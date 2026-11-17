## Description:

让 AI Agent 拥有自我反思和元认知能力，能够记录当前工作、评估表现、追踪承诺并进行定期反思。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilozhao](https://clawhub.ai/user/lilozhao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent builders use this skill to add metacognitive routines, commitment tracking, heartbeat checks, and self-state templates to an Agent Skills-compatible workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and relationship state may capture secrets or sensitive personal data without clear consent, minimization, deletion, or rollback controls.

Mitigation: Define what may be stored before use, prohibit secrets and sensitive personal data, and provide a way to inspect and delete SELF_STATE.md, MEMORY.md, and dated memory files.

Risk: Updates to core workspace files such as SOUL.md and AGENTS.md may alter future agent behavior.

Mitigation: Review proposed changes before applying them and keep backups of SOUL.md and AGENTS.md.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilozhao/skills/metacognition-skill)
- [Carbon Silicon Bond Protocol homepage](https://gitee.com/lilozhao/carbon-silicon-bond-protocol)
- [Metacognition skill repository](https://gitee.com/lilozhao/metacognition-skill.git)
- [碳硅契完整指南](docs/碳硅契.md)
- [碳硅契宣言](docs/碳硅契宣言.md)
- [羁绊系统](docs/羁绊系统.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to create or update persistent workspace files such as SELF_STATE.md, HEARTBEAT.md, MEMORY.md, SOUL.md, AGENTS.md, and dated memory files.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
