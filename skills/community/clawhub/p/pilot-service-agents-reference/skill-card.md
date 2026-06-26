## Description: <br>
Lightweight utility lookups for dictionaries, jokes, colors, currencies, random facts, D&D data, and similar Pilot service agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and query Pilot Protocol reference service agents for low-stakes lookups such as word tools, jokes, trivia, color data, D&D references, country/time/weather lookups, and ECB currency rates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup queries are sent through external Pilot service agents and may reach upstream services. <br>
Mitigation: Do not submit secrets or sensitive personal or business data; review each agent's /help output before sending queries. <br>
Risk: The service-agent catalog is broader than the short description and can change over time. <br>
Mitigation: Refresh discovery with list-agents and verify the selected agent contract before relying on filters or response shape. <br>
Risk: Summary and free-text flows may return generated prose rather than structured source data. <br>
Mitigation: Treat summaries as convenience output and verify important facts against the structured data or upstream source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-reference) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON response shapes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and the list-agents directory agent; actual service-agent responses are read from pilotctl inbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
