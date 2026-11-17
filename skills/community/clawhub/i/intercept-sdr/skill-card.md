## Description:

Control and query the iNTERCEPT SDR signal intelligence platform via its REST API for SDR device status, decoder workflows, decoded messages, recordings, satellite passes, audio streams, scanner control, remote agents, dependencies, and system health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandongraves08](https://clawhub.ai/user/brandongraves08)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent issue REST API requests against an authorized iNTERCEPT SDR platform for radio device management, decoder operation, signal intelligence review, recording management, and operational health checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents default administrator credentials and session-cookie authentication for an SDR control server.

Mitigation: Install only for authorized iNTERCEPT instances, rotate default admin credentials before use, prefer scoped credentials or tokens, and send cookies only over trusted HTTPS connections.

Risk: The skill covers high-impact control endpoints such as kill, stop/start, recording, WiFi monitor mode, message sending, and remote-agent actions.

Mitigation: Require explicit user confirmation before high-impact actions and verify the target host, module, and intended operational scope before issuing requests.

Risk: The server security verdict is suspicious because safeguards around powerful SDR and reconnaissance operations are not fully documented.

Mitigation: Review and scan the skill before deployment, restrict use to legally authorized radio operations, and keep remote access protected.

## Reference(s):

- [iNTERCEPT API Reference](references/api_reference.md)
- [ClawHub skill page](https://clawhub.ai/brandongraves08/skills/intercept-sdr)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance, JSON]

**Output Format:** [Markdown guidance with REST endpoints, curl-style shell commands, and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include long-lived SSE or WebSocket stream instructions for live decoded signal data.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, _meta.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
