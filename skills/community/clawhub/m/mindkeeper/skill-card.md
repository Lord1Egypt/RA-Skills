## Description:

Mindkeeper guides an agent through version history, diffs, checkpoints, and rollback workflows for agent context files such as SOUL.md, AGENTS.md, MEMORY.md, and skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuhao6741](https://clawhub.ai/user/liuhao6741)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Mindkeeper to inspect changes to agent context files, compare versions, create checkpoints before risky edits, and guide rollback with preview and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill bootstraps an external Gateway plugin that can watch and version sensitive agent context files.

Mitigation: Review or pin the plugin package before installation, verify the plugin source or package, and approve installation and Gateway restart only after that review.

Risk: Rollback workflows can change active agent context files.

Mitigation: Preview rollback diffs first, require explicit user confirmation before execution, and reload the session after a successful rollback.

Risk: History and diff outputs may expose sensitive information contained in tracked context files.

Mitigation: Review displayed history and diffs before sharing them outside the local workspace.

## Reference(s):

- [Mindkeeper project homepage](https://github.com/seekcontext/mindkeeper)
- [mindkeeper-openclaw plugin package](https://www.npmjs.com/package/mindkeeper-openclaw)
- [Mindkeeper ClawHub listing](https://clawhub.ai/liuhao6741/skills/mindkeeper)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with tool-call instructions and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup and use of mind_* tools; plugin installation, Gateway restart, and rollback execution require explicit confirmation.]

## Skill Version(s):

1.2.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
