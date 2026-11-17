## Description:

mwcHorus helps agents build, maintain, and extend Horus, a local-first tech and event intelligence terminal configured for MWC 2026 Barcelona monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trungviet17](https://clawhub.ai/user/trungviet17)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to maintain Horus relay ingestion, source pipelines, UI behavior, local data storage, and OpenClaw chat bridge behavior for MWC 2026 monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Horus may maintain durable project memory and treat multiple chat channels as one shared context.

Mitigation: Install only when shared conversation continuity is intended, and avoid storing secrets, personal data, or raw chat content in MEMORY.md.

Risk: The relay may be network-exposed if configured to bind beyond localhost.

Mitigation: Bind the relay to 127.0.0.1 unless remote access is intentional, and protect any remote relay with authentication and firewall rules.

Risk: Environment files can contain upstream credentials or session keys.

Mitigation: Keep .env out of source control, use per-user credentials where applicable, and rotate credentials if they are accidentally exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trungviet17/skills/mwc-2026-horus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, environment snippets, code snippets, and concise user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide or modify Horus project files when requested; user-facing event summaries should avoid technical implementation detail unless requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
