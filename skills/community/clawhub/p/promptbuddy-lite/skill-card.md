## Description:

Promptbuddy Lite is a zero-dependency Shell skill that rewrites user requests into structured four-layer prompts using role, task, format, and constraint templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steventsang18](https://clawhub.ai/user/steventsang18)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to optimize chat requests into structured prompts before model execution. It is intended for lightweight prompt refinement on Linux and macOS environments without additional runtime dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically rewrite chat prompts before model execution.

Mitigation: Require explicit user opt-in for prompt rewriting and show when rewritten prompt text is being used.

Risk: The installer requests sudo and writes global commands.

Mitigation: Prefer a user-scoped installation path and review installed scripts before granting elevated privileges.

Risk: The feedback workflow can treat a later '1' or '2' reply as feedback and can invoke code from another local skill directory if present.

Mitigation: Use safer per-session feedback state and only call bundled or verified feedback collectors.

## Reference(s):

- [Promptbuddy Lite ClawHub skill page](https://clawhub.ai/steventsang18/skills/promptbuddy-lite)
- [HMAW: Hierarchical Multi-Agent Workflows for Zero-Shot Prompt Optimization](https://arxiv.org/abs/2405.20252)
- [The Prompt Report](https://arxiv.org/abs/2406.06608)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and JSON with structured prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces optimized prompt text and lightweight feedback prompts; no model weights or binary artifacts are produced.]

## Skill Version(s):

3.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
