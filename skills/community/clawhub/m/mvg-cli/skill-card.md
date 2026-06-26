## Description: <br>
Mvg helps agents use a Munich public transport CLI for departure times, route planning, nearby stations, service alerts, and real-time S-Bahn positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lars147](https://clawhub.ai/user/Lars147) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to look up Munich public transport departures, routes, nearby stations, service alerts, line information, and live S-Bahn positions from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MVG searches, route endpoints, addresses, or coordinates may be sent to MVG or geOps services. <br>
Mitigation: Use the skill only for transit queries that are acceptable to share with those external services, and avoid sensitive addresses or coordinates. <br>
Risk: Live S-Bahn tracking depends on a local Node.js runtime and ws module for the geOps WebSocket connection. <br>
Mitigation: Use live tracking only in environments where the local node binary and ws module are trusted; otherwise rely on non-live lookup commands. <br>
Risk: Unpinned GitHub or sudo-based installation can execute changing third-party code with elevated local impact. <br>
Mitigation: Install a reviewed, pinned release where possible and avoid sudo or PATH-wide installation unless the source is trusted. <br>


## Reference(s): <br>
- [MVG API](https://www.mvg.de/api/bgw-pt/v3/) <br>
- [S-Bahn München Live](https://s-bahn-muenchen-live.de) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON, with Markdown guidance and inline shell commands when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All commands support machine-readable JSON output.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
