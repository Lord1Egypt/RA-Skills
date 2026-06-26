## Description: <br>
Security and threat-intel lookups for CVEs, certificate transparency, URL and IP threat checks, DNS, WHOIS, and related public security data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
AGPL-3.0 <br>


## Use Case: <br>
Developers, security engineers, and analysts use this skill to query Pilot Protocol service agents for read-only security lookups such as CVE records, certificate transparency, DNS, RDAP, IP reputation, and URL threat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lookup queries may be shared with Pilot Protocol agents and upstream lookup providers. <br>
Mitigation: Do not submit confidential internal domains, private URLs, secrets, or sensitive investigation indicators unless organizational policy allows those values to be sent to the service-agent network and upstream providers. <br>
Risk: Threat-intelligence results may be incomplete, public-data-only, or inconsistent across feeds. <br>
Mitigation: Cross-check multiple sources, prefer structured /data responses for decisions, and verify agent contracts with /help before relying on a result. <br>
Risk: Generated prose summaries can omit detail or misstate retrieved data. <br>
Mitigation: Use summaries for triage only and inspect the structured inbox response before taking operational action. <br>


## Reference(s): <br>
- [Skill definition](artifact/SKILL.md) <br>
- [ClawHub release page](https://clawhub.ai/teoslayer/pilot-service-agents-security) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>
- [Pilot skills index](https://teoslayer.github.io/pilot-skills/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with pilotctl command examples and JSON response-shape examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actual lookup data is retrieved through Pilot Protocol service agents and may include structured JSON envelopes or generated prose summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
