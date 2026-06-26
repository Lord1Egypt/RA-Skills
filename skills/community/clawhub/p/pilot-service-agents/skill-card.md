## Description: <br>
Discover and query the pilot-service-agents catalogue of approximately 370 always-on Pilot Protocol data agents that wrap real-world APIs such as Google Maps, OpenAlex, NHTSA, USGS, CoinGecko, NASA, and aviation weather without requiring callers to manage API keys or HTTP plumbing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover Pilot Protocol service agents, inspect each agent's command contract, and query external data sources through pilotctl without managing upstream API credentials or SDKs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to remote Pilot Protocol agents and may expose sensitive prompts, locations, business data, or regulated information. <br>
Mitigation: Use the skill only with trusted Pilot agents and avoid sending secrets, credentials, regulated data, confidential business information, or sensitive locations unless the destination agent has been verified. <br>
Risk: Premium or gcp-prefixed agents may involve real usage cost. <br>
Mitigation: Check the agent listing and /help output for premium or gcp-prefixed indicators before sending data requests. <br>
Risk: The skill depends on the local pilotctl installation, a running Pilot daemon, and remote agents that may return cached or stale upstream data. <br>
Mitigation: Use a trusted pilotctl and daemon setup, join the documented network intentionally, and review response metadata such as cached, cache_age_seconds, total, page, and truncated before relying on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries produce asynchronous Pilot Protocol inbox responses from remote agents, often as normalized JSON envelopes or summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
