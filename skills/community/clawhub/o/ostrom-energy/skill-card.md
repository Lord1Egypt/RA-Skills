## Description: <br>
Fetch Ostrom hourly electricity spot prices, find cheapest appliance and EV charging windows, and optionally trigger trusted smart-home actions from price thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pmagnomuller](https://clawhub.ai/user/pmagnomuller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Ostrom electricity prices, identify lower-cost charging or appliance windows, and connect reviewed price-threshold decisions to smart-home automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ostrom API credentials and local configuration can contain sensitive access material. <br>
Mitigation: Provide credentials only through protected environment variables or trusted local config, and do not commit or publish files containing secrets. <br>
Risk: Control mode can run user-provided shell commands when execution is enabled. <br>
Mitigation: Keep control mode in dry-run until reviewed, use fixed trusted commands, and do not allow untrusted text to populate command arguments or credential files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pmagnomuller/ostrom-energy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ostrom API credentials; control mode remains dry-run unless execution is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
