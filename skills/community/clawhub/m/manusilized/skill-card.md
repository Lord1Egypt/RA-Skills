## Description:

Enhances OpenClaw agents with real-time Ollama streaming, Markdown tool-call recovery, and support for additional reasoning model families.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wd041216-bit](https://clawhub.ai/user/wd041216-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Manusilized to patch OpenClaw's Ollama integration for agents that need incremental response streaming, model metadata defaults, and fallback handling for Markdown-embedded tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This package patches core OpenClaw agent files rather than operating as an isolated skill.

Mitigation: Prefer a reviewed upstream PR when available, keep backups of replaced files, and test the patch in a disposable OpenClaw checkout before using it in production.

Risk: Markdown-embedded JSON can be recovered as tool calls, which may turn model text into tool invocations.

Mitigation: Use tool allowlisting, argument validation, and explicit approval for consequential tool calls before installing it in environments with sensitive credentials or powerful tools.

Risk: The server security verdict for this release is suspicious.

Mitigation: Review the TypeScript diff carefully and treat the scanner guidance as authoritative during deployment review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wd041216-bit/skills/manusilized)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline shell commands and TypeScript patch references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation guidance for a core OpenClaw patch; review and test before applying to a working agent environment.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
