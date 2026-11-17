## Description:

Control Home Assistant smart home devices, lights, scenes, and automations via moltbot-ha CLI with configurable safety confirmations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamvaleriofantozzi](https://clawhub.ai/user/iamvaleriofantozzi)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent discover and control Home Assistant entities through the moltbot-ha CLI while preserving confirmation steps for higher-risk smart-home actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls physical smart-home devices, including critical domains such as locks, alarms, covers, and garage doors.

Mitigation: Keep safety level 3 or stronger, require explicit user confirmation before using --force, and configure blocked_entities for devices that should never be automated.

Risk: The skill requires a long-lived Home Assistant access token.

Mitigation: Use a dedicated least-privilege Home Assistant account or token, prefer HA_TOKEN over storing tokens in config files, and revoke or rotate the token if exposure is suspected.

Risk: Plaintext HTTP examples can expose Home Assistant traffic outside a trusted local boundary.

Mitigation: Prefer HTTPS or a trusted local-only network path, and avoid exposing Home Assistant control endpoints to untrusted networks.

Risk: The install flow uses an external moltbot-ha package without a pinned version in the artifact instructions.

Mitigation: Install only a reviewed and pinned release where possible, and review the package before granting access to Home Assistant credentials.

Risk: Broad entity access can let an agent operate devices beyond the intended scope.

Mitigation: Configure allowed_entities to limit access to approved Home Assistant entities and keep blocked_entities for high-impact devices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iamvaleriofantozzi/skills/moltbot-ha)
- [Project homepage](https://github.com/iamvaleriofantozzi/moltbot-ha)
- [Home Assistant REST API documentation](https://developers.home-assistant.io/docs/api/rest/)
- [Moltbot documentation](https://docs.molt.bot/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Home Assistant entity names, JSON-capable CLI output, and confirmation guidance for critical actions.]

## Skill Version(s):

0.1.1 (source: server release metadata and changelog, released 2026-02-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
