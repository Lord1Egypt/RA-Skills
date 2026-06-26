## Description: <br>
OpenClaw Token Monitor runs a local dashboard that polls active OpenClaw sessions, stores token usage history in SQLite, and visualizes real-time, daily, monthly, session, and CNY cost metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oldyoungcn](https://clawhub.ai/user/oldyoungcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor active OpenClaw token consumption, review historical usage by date or session, estimate costs, and investigate unusual usage patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard exposes sensitive token and session usage history through an unauthenticated service. <br>
Mitigation: Run it only on trusted machines, bind or firewall port 3000 to localhost, and avoid exposing it on shared networks. <br>
Risk: The skill permanently stores token and session usage history. <br>
Mitigation: Treat the SQLite database as sensitive operational data and apply local retention, access control, and deletion practices before use. <br>
Risk: The runtime depends on third-party browser assets and an undeclared /tmp dependency. <br>
Mitigation: Review runtime dependencies and pin or vendor required assets before using the skill in controlled environments. <br>


## Reference(s): <br>
- [OpenClaw Token Monitor on ClawHub](https://clawhub.ai/oldyoungcn/openclaw-token-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with setup commands and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime dashboard exposes JSON APIs, server-sent events, CSV export, and chart image export.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
