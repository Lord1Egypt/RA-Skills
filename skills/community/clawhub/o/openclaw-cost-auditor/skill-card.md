## Description: <br>
OpenClaw Cost Auditor helps agents inspect local OpenClaw log files and estimate token usage and cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBlockChainNetwork](https://clawhub.ai/user/GBlockChainNetwork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators can use this skill to audit a chosen OpenClaw log directory, count token entries, and estimate spend from local log data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation advertises reporting, alerts, PDF output, and API integrations that are not supported by the provided artifact files. <br>
Mitigation: Treat those advertised capabilities as unverified unless the publisher supplies reviewed files that implement them. <br>
Risk: The script reads log files from the directory supplied by the user, defaulting to /var/log/openclaw. <br>
Mitigation: Run it only against the OpenClaw log directory intended for audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GBlockChainNetwork/openclaw-cost-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script prints total tokens and an estimated cost using a fixed per-token rate.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
