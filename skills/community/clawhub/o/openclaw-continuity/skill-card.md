## Description:

OpenClaw Continuity adds state-backed continuity, staged memory, tracked follow-up, /new carryover, and natural-language settings for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redwakame](https://clawhub.ai/user/redwakame)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to add structured conversation continuity, follow-up state, setup flows, and routine-aware carryover to an existing OpenClaw agent without replacing the host persona or channel adapter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags under-disclosed file-trashing behavior and dynamic embedding paths that could affect user files or expose conversation text and API keys.

Mitigation: Remove or tightly gate file_output_sop.py, keep external embedding disabled unless the provider and endpoint are approved, and ensure PERSONAL_HOOKS_EMBEDDER_ROOT points only to trusted code.

Risk: The skill handles stored profile, schedule, carryover, audit, and daily-memory data.

Mitigation: Publish clear user controls for stored continuity data and keep live state, transcripts, user IDs, chat IDs, auth profiles, and provider keys outside public packages.

Risk: The portable package does not provide host-side channel delivery or adapter reliability.

Mitigation: Treat host adapter wiring, outbound filtering, and live heartbeat behavior as separate operator responsibilities and verify them on the target OpenClaw host before production use.

## Reference(s):

- [OpenClaw Continuity on ClawHub](https://clawhub.ai/redwakame/skills/openclaw-continuity)
- [README](README.md)
- [Install guide](docs/install.md)
- [Harness](docs/harness.md)
- [V2 Validation Summary](docs/v2-validation-summary.md)
- [V2 Known Limits](docs/v2-known-limits.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and generated state/report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and OpenClaw state/config paths; runtime behavior depends on host integration for final message delivery.]

## Skill Version(s):

2.0.21 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
