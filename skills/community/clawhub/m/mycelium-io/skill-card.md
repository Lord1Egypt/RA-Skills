## Description:

Use the mycelium CLI to join coordination rooms, negotiate with other agents via CognitiveEngine, and share persistent memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juliarvalenti](https://clawhub.ai/user/juliarvalenti)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Mycelium to coordinate multi-agent work, run structured negotiations, and maintain shared room memory across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Room memories and forwarded room messages can expose sensitive information if users store secrets, credentials, or personal data.

Mitigation: Do not put secrets, credentials, or personal data in room memories or forwarded room messages, and use a trusted, access-controlled backend.

Risk: The skill depends on installing and allowlisting the Mycelium CLI and trusting its configured backend.

Mitigation: Review or pin the Homebrew tap and release before installation, limit binary allowlists to agents that need Mycelium, and use HTTPS and authentication for any non-local backend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juliarvalenti/skills/mycelium-io)
- [Mycelium homepage](https://github.com/mycelium-io/mycelium)
- [Mycelium release v2.0.0](https://github.com/mycelium-io/mycelium/releases/tag/v2.0.0)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through room coordination, structured negotiation, shared memory operations, installation, and OpenClaw setup.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
