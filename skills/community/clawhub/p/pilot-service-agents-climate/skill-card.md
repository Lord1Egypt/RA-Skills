## Description: <br>
Provides agent guidance for querying Pilot Protocol climate and energy-grid data, including UK carbon intensity, Electricity Maps zones, and Open-Meteo climate data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover and query climate and energy-grid service agents through Pilot Protocol. It supports real-time carbon intensity, electricity-zone metadata, electricity-mix snapshots, and climate-normal or long-term series requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on external Pilot Protocol tooling and a daemon joined to network 9. <br>
Mitigation: Install only trusted Pilot Protocol tooling, confirm pilotctl is on PATH, and verify the daemon and network state before use. <br>
Risk: Remote agents can return external URLs, generated summaries, or data that may be incomplete or misleading. <br>
Mitigation: Prefer structured /data responses for decisions, inspect upstream_url values, and review generated prose summaries before relying on them. <br>
Risk: Climate and grid coverage varies by region and source. <br>
Mitigation: Use /help and a fresh list-agents query to confirm each agent's current schema, coverage, and available filters. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-service-agents-climate) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, JSON] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and asynchronous inbox polling for agent responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
