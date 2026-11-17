## Description:

Helps agents create structured context handoffs when switching models or transferring work, preserving task status, decisions, constraints, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujun2508](https://clawhub.ai/user/lujun2508)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to summarize project state, completed work, active blockers, constraints, team roles, and next actions when handing work from one model or agent to another.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive credentials or private context may be copied into CONTEXT_TRANSFER or MEMORY.md during handoff.

Mitigation: Prohibit raw passwords, tokens, API keys, cookies, private keys, and recovery codes; use secret-manager references or environment variable names instead.

Risk: A handoff may be sent to another model or agent without clear user control.

Mitigation: Require explicit user approval before any handoff content is shared with another model or agent.

## Reference(s):

- [Quick Transfer Template](references/quick-transfer-template.md)
- [ClawHub skill page](https://clawhub.ai/lujun2508/skills/model-context-transfer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown CONTEXT_TRANSFER summaries and optional generated Markdown handoff files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project state, file paths, API/tool references, team roles, warnings, and prioritized next steps.]

## Skill Version(s):

1.0.0 (source: release evidence and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
