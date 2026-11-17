## Description:

A lightweight Python guard that helps LLM agents detect likely infinite loops and respond with healing, pause, or abort directives across common agent harnesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add loop detection, pre-flight plan checks, local loop fingerprinting, and corrective intervention directives to LLM agent workflows. It is aimed at agents that may repeat tool calls, drift from intent, or need a recoverable alternative to hard aborts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Healing mode can promote observed agent text into a system-message-style directive.

Mitigation: Treat healing output as advisory data, sanitize it before use, and preserve role separation when adding it to an agent context.

Risk: Loop samples and fingerprints are stored locally by default.

Mitigation: Avoid passing secrets in action strings, configure or isolate the Loop DNA storage path, and periodically delete retained loop history.

Risk: The security verdict recommends review before installation in tool-enabled agents.

Mitigation: Install only a pinned, reviewed package in a virtual environment and review the skill before deploying it with tool access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/morgana-anti-infinite-loop-v2-en)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown documentation with Python and shell snippets; runtime output is a directive dictionary for agent intervention.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Core package is documented as zero-dependency, with optional extras for numpy, torch, and multi-agent use.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
