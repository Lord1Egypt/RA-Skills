## Description:

Layered Memory Sys provides a six-layer memory management system for AI agents, with TTL-based retention, scheduled consolidation, TF-IDF search, import/export, backup, Docker deployment, and a web/API management surface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[141553](https://clawhub.ai/user/141553)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent, searchable, tiered memory to AI agents, including automatic forgetting, consolidation, archival, backup, and memory import/export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive long-term memory can be exposed through unauthenticated local API or WebSocket services.

Mitigation: Install only in a trusted local environment and do not expose ports 3456 or 3457 without authentication, loopback binding, and CORS or origin restrictions.

Risk: Installer choices can create persistent background components with broad access to local session and memory data.

Mitigation: Avoid running the installer as root unless a persistent service is intentional, and review service configuration, data paths, and backup locations before deployment.

Risk: Cloud embedding or summarization settings may send memory and session text to third-party providers.

Mitigation: Review provider configuration and API key settings before use, and prefer local processing or disabled cloud providers for sensitive memory content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/141553/skills/layered-memory-sys)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, JavaScript entry points, and HTTP API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start local API and WebSocket services, create SQLite memory data, write backup files, and manage local memory records.]

## Skill Version(s):

2.4.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
