## Description:

Builds local companion applications that monitor user-selected sources from 127.0.0.1, provide starter scripts, PWA packaging, optional browser extension behavior, state-change notifications, and containerized long-running operation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build small local monitoring tools for livestreams, feeds, prices, build states, server availability, folders, queues, and similar status sources. It helps agents choose between a single HTML file, a localhost server, a PWA, an optional browser extension, and containerized operation based on the monitoring need.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated companions may use wildcard CORS on localhost APIs.

Mitigation: Prefer same-origin APIs or a strict Origin allowlist, and require authentication for POST or control endpoints.

Risk: Generated companions may run as durable background monitors.

Mitigation: Require explicit user approval for persistence, document how to stop the monitor, and bind exposed services to 127.0.0.1 unless the user deliberately requests controlled remote access.

Risk: Unauthenticated localhost APIs may expose secrets or sensitive internal status.

Mitigation: Do not store secrets or sensitive internal status in unauthenticated localhost APIs; use user-provided configuration and limit exposed status data.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/kikikari/skills/lokaler-companion)
- [Dauerbetrieb im Container](references/docker.md)
- [Browser-Erweiterung (Manifest V3)](references/erweiterung.md)
- [Fallstricke](references/fallstricke.md)
- [Installierbare Oberflaeche (PWA)](references/pwa.md)
- [Der Starter](references/starter.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and project files when applied by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local server, starter, PWA, browser extension, Docker, and validation artifacts depending on the requested companion.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
