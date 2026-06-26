## Description: <br>
Provides offline access to a bundled Priority Pass lounge catalog for local lounge lookup, facility filtering, airport briefs, and lounge comparisons when network access is unavailable or disallowed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skylinehk](https://clawhub.ai/user/skylinehk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query and compare airport lounge records from a local, offline snapshot. It is intended for air-gapped or network-restricted environments where answers must stay grounded in bundled data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Offline lounge results may be stale because the bundled catalog snapshot was generated on 2026-03-11. <br>
Mitigation: Verify current lounge availability through another source when travel accuracy matters, and state when an answer is limited by the bundled snapshot. <br>
Risk: Users may expect the offline bundle to fetch live updates or use remote MCP endpoints. <br>
Mitigation: Keep runtime use local and read-only, avoid remote endpoints and secrets, and report missing or outdated data instead of guessing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/skylinehk/pp-lounge-map-offline) <br>
- [Offline MCP Setup](references/mcp.md) <br>
- [Offline Safety](references/safety.md) <br>
- [Offline Publishing Notes](references/publishing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON MCP configuration and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Grounded in the bundled offline catalog snapshot generated on 2026-03-11; no live availability lookup is performed.] <br>

## Skill Version(s): <br>
1.3.26 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
