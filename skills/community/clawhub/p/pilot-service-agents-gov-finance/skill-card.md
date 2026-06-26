## Description: <br>
Government economic and financial records for SEC EDGAR, BLS time series, HTS/USITC tariffs, and US Department of Education data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers and analysts use this skill to query government economic and financial data agents for SEC company facts and submissions, BLS time series, tariff classification, and Department of Education datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent through Pilot Protocol tooling and remote agents reachable over its overlay network. <br>
Mitigation: Install only when the Pilot Protocol tooling and reachable agents are trusted, and confirm the daemon is joined to the intended network before use. <br>
Risk: /summary requests and free-text queries may share data with external services that generate prose responses. <br>
Mitigation: Avoid sending private credentials, secrets, or sensitive non-public data in pilotctl queries. <br>
Risk: Agent contracts and catalog entries can change over time. <br>
Mitigation: Run a fresh list-agents query and read each agent's /help output before relying on filters or response fields. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-service-agents-gov-finance) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and reachable remote service agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
