## Description: <br>
Fetch Iberian day-ahead electricity prices for Portugal and Spain from OMIE via the OMIEData library, plan cheapest appliance or EV charging windows, compare PT vs ES prices, and trigger smart-home actions from price thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pmagnomuller](https://clawhub.ai/user/pmagnomuller) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Portugal and Spain OMIE day-ahead prices, compare markets, find low-cost appliance or EV charging windows, and optionally automate local device commands from price thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional control mode can execute user-supplied shell commands when --execute is enabled. <br>
Mitigation: Keep dry-run mode on until the exact on/off commands and threshold logic have been reviewed. <br>
Risk: Local automation commands may affect smart-home devices or other host resources. <br>
Mitigation: Use a dedicated low-privilege account and tightly allowlist any commands used for device control. <br>


## Reference(s): <br>
- [OMIE](https://www.omie.es) <br>
- [OMIEData Python package](https://pypi.org/project/OMIEData/) <br>
- [ClawHub skill page](https://clawhub.ai/pmagnomuller/omie-energy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price tables, optimized time windows, PT/ES comparison summaries, dry-run command previews, and local configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
