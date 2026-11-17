## Description:

Captures agent learnings, errors, corrections, and feature requests so recurring knowledge can be logged, reviewed, and promoted into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckyjin](https://clawhub.ai/user/luckyjin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to record corrections, errors, feature requests, and non-obvious discoveries in project-local learning logs. They can review those logs and promote broadly applicable lessons into agent memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable agent memory can retain sensitive or low-quality information if learning entries are captured without review.

Mitigation: Keep logs project-local, redact secrets before logging, and review proposed writes before promoting entries into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, Copilot instructions, or other agent memory files.

Risk: Optional reminders and hooks can become too broad when configured globally or with empty matchers.

Mitigation: Install hooks only when persistent learning is deliberately desired, prefer project-level scoping, avoid user-level or global hooks, and narrow matchers to relevant workflows where possible.

Risk: Cross-session transcript or message features can expose more context than intended.

Mitigation: Avoid cross-session transcript and message features unless explicitly needed for the task and approved for the workspace.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/luckyjin/skills/my-test-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and reusable templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-local learning, error, and feature-request entries; optional hooks emit reminder text.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
