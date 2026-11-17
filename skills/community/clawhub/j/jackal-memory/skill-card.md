## Description:

Sovereign, recoverable memory for AI agents backed by Jackal decentralized storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regan-milne](https://clawhub.ai/user/regan-milne)

### License/Terms of Use:


## Use Case:

External developers and agent operators use Jackal Memory to persist and restore agent memory across sessions and machines using Jackal decentralized storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved agent memory can contain credentials, personal data, or sensitive operating context and is sent to a third-party Jackal Memory service.

Mitigation: Store only reviewed, non-sensitive memory unless separate controls such as local encryption and upload review are in place.

Risk: Remote memory is loaded back into the agent as text that can influence identity or behavior.

Mitigation: Treat loaded memory as untrusted context, review it before use, and avoid giving it higher priority than system or user instructions.

Risk: The skill depends on JACKAL_MEMORY_API_KEY for remote access.

Mitigation: Keep the API key in environment variables, avoid logging it, and rotate it if it is exposed.

## Reference(s):

- [Jackal Memory homepage](https://web-production-5cce7.up.railway.app)
- [Jackal Memory login](https://web-production-5cce7.up.railway.app/auth/login)
- [ClawHub skill listing](https://clawhub.ai/regan-milne/skills/jackal-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline shell commands, Python commands, and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JACKAL_MEMORY_API_KEY; first-time provisioning requires a Jackal address.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
