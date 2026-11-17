## Description:

Persistent learning for AI agents. Open engram format. Your agent learns from corrections, remembers across sessions, and transfers knowledge across domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plur9](https://clawhub.ai/user/plur9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use PLUR Memory to give OpenClaw and compatible tools persistent, shared memory for corrections, preferences, patterns, decisions, and conventions across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memories may capture secrets, sensitive operational details, or stale information and later reinject them into agent context.

Mitigation: Avoid storing secrets or sensitive operational details as memories, review learned engrams, and delete or negatively rate stale or inappropriate memories.

Risk: Shared ~/.plur/ memory can transfer information across tools, sessions, and devices beyond the original interaction.

Mitigation: Install only when shared persistent memory is intended, understand how to inspect and limit local memories, and disable sync when cross-device sharing is not desired.

Risk: The skill instructs installation of an external package that should be trusted before use.

Mitigation: Review the @plur-ai/claw package source and version before installation.

## Reference(s):

- [PLUR Memory ClawHub Page](https://clawhub.ai/plur9/skills/plur-memory)
- [PLUR Website](https://plur.ai)
- [Engram Spec](https://plur.ai/spec)
- [Benchmarks](https://plur.ai/benchmark)
- [GitHub Repository](https://github.com/plur-ai/plur)
- [npm Package](https://npmjs.com/package/@plur-ai/claw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent-memory usage guidance for agents; memory artifacts are stored outside the skill as local engram files.]

## Skill Version(s):

0.10.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
