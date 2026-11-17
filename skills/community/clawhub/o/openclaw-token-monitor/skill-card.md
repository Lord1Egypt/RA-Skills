## Description:

OpenClaw Token Monitor provides a local dashboard for tracking active OpenClaw token usage, SQLite-backed history, session summaries, token-rate trends, and CNY cost estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oldyoungcn](https://clawhub.ai/user/oldyoungcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect OpenClaw token consumption, review daily or hourly usage trends, and investigate unusual token spend across active sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose detailed session telemetry through an unauthenticated local network service.

Mitigation: Bind the service to localhost before use on shared or reachable networks and add authentication if remote access is required.

Risk: Wildcard CORS and insufficient API input validation can broaden access to telemetry endpoints.

Mitigation: Remove wildcard CORS and validate API inputs, including date and polling parameters.

Risk: Session-level token history is persisted locally and may retain sensitive usage metadata longer than intended.

Mitigation: Define a retention policy for the SQLite history database and clear or rotate stored telemetry when it is no longer needed.

Risk: Rendering session data with innerHTML can create web UI exposure if session fields contain unexpected content.

Mitigation: Render session data with text-safe DOM APIs or sanitize values before insertion into the page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oldyoungcn/skills/openclaw-token-monitor)
- [Publisher profile](https://clawhub.ai/user/oldyoungcn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and dashboard usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill starts or explains a local Node dashboard that serves token telemetry and stores history in SQLite.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
