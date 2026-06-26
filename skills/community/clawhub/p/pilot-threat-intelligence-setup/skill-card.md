## Description: <br>
Deploys a four-agent threat intelligence platform for IOC collection, enrichment, analysis, and distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security developers and operators use this skill to set up collector, enricher, analyzer, and distributor agents for threat feed aggregation, IOC enrichment, severity analysis, and STIX/TAXII or SIEM distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The distributor role can send threat data to external security systems if destinations, data classification, or approval gates are misconfigured. <br>
Mitigation: Test in staging and enable distributor publishing only after confirming destinations, data classification, approval gates, validation rules, rollback paths, and audit procedures. <br>
Risk: The setup depends on Pilot skills plus pilotctl and clawhub binaries that affect agent trust relationships and threat-intelligence data flows. <br>
Mitigation: Verify the pilot dependencies and binaries before installation, then establish handshakes only between intended peers. <br>


## Reference(s): <br>
- [Pilot Protocol Homepage](https://pilotprotocol.network) <br>
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/pilot-threat-intelligence-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON manifest examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup steps for required Pilot skills, hostnames, trust handshakes, and threat-intelligence data flows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
