## Description: <br>
Monitor DigitalOcean VPS droplets by listing instances and fetching CPU, memory, disk, and bandwidth metrics with summaries using the DigitalOcean API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect DigitalOcean Droplet health, utilization, bandwidth, and short-window monitoring summaries from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a DigitalOcean API token and can expose Droplet names, identifiers, regions, status, and operational metrics in command output. <br>
Mitigation: Use the minimum required token permissions, store the token securely, and review output before sharing it outside the operating team. <br>
Risk: Computed CPU, memory, disk, and bandwidth summaries may be approximate or incomplete when Monitoring data is missing or delayed. <br>
Mitigation: Confirm important operational decisions against DigitalOcean Monitoring or another trusted observability source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elandivar/neomano-vps-monitoring) <br>
- [DigitalOcean API endpoint](https://api.digitalocean.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Analysis, Guidance] <br>
**Output Format:** [JSON metric data and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, DIGITALOCEAN_TOKEN, and DigitalOcean Monitoring enabled for the target Droplets.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
