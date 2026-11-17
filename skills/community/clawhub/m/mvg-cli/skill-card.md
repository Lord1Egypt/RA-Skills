## Description:

Munich public transport (MVG) CLI and S-Bahn live tracking for departure times, route planning, nearby stations, service alerts, and real-time S-Bahn positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lars147](https://clawhub.ai/user/lars147)

### License/Terms of Use:

MIT

## Use Case:

External transit users and developers use this skill to run Munich MVG terminal lookups for station search, departures, routes, nearby stops, service alerts, line lists, and optional S-Bahn live tracking.

### Deployment Geography for Use:

Global; the transit data and practical utility are focused on Munich, Germany.

## Known Risks and Mitigations:

Risk: Installation paths can run mutable or locally copied code, and the README includes a sudo copy option.

Mitigation: Install only from a reviewed, pinned commit or trusted versioned package, and avoid the sudo install option.

Risk: The live-tracking command executes Node.js and trusts local ws module resolution.

Mitigation: Treat live tracking as higher risk; run it only with reviewed dependencies in a controlled environment or disable it until the path is fixed.

Risk: The live-tracking implementation includes an exposed geOps key.

Mitigation: Replace the embedded key with a reviewed configuration mechanism or disable live tracking until the key handling is fixed.

## Reference(s):

- [MVG API base URL](https://www.mvg.de/api/bgw-pt/v3/)
- [S-Bahn München Live](https://s-bahn-muenchen-live.de)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands; command results may be terminal text tables or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only network lookups; live tracking requires Node.js and the ws module.]

## Skill Version(s):

0.1.0 (source: pyproject.toml and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
