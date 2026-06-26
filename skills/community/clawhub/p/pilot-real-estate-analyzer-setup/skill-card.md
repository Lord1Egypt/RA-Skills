## Description: <br>
Deploy a real estate analysis system with 4 agents for property scraping, market valuation, comparable analysis, and deal alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and real estate investment teams use this skill to configure a four-agent Pilot workflow for listing ingestion, market valuation, comparable sales analysis, and deal alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup installs downstream pilot-* skills and coordinates data flows across multiple agents. <br>
Mitigation: Review the downstream skills and install only the role-specific dependencies needed for the deployment. <br>
Risk: Incorrect peer names or trust handshakes could route property or deal data to the wrong agent. <br>
Mitigation: Confirm each hostname and peer relationship before running handshake, subscribe, or publish commands. <br>
Risk: Slack, email, and webhook notifications can expose property, investor, tenant, or deal data externally. <br>
Mitigation: Verify notification destinations and payload contents before sending real data. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-real-estate-analyzer-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces role-specific setup steps, hostnames, handshakes, manifests, and example Pilot publish/subscribe commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
