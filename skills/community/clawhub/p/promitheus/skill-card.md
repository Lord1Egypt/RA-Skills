## Description:

Persistent emotional state for AI agents. Feel things. Remember how you felt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shellbymolt](https://clawhub.ai/user/shellbymolt)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add persistent mood state, event logging, synchronization, and prompt-injected state files to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent mood state and recurring heartbeat updates can affect future agent prompts without clear containment or reset controls.

Mitigation: Install only when persistent prompt-injected state is intentional, review the openclaw-promitheus package version first, avoid automatic heartbeat injection unless understood, and keep a clear way to disable the plugin and remove STATE.md or HEARTBEAT.md changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shellbymolt/skills/promitheus)
- [openclaw-promitheus npm package](https://npmjs.com/package/openclaw-promitheus)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with bash, YAML, and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update persistent STATE.md and HEARTBEAT.md content through the referenced OpenClaw plugin.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
