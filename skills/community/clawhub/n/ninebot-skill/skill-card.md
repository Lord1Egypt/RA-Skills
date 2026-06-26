## Description: <br>
Ninebot Skill helps an agent guide interaction, diagnostics, configuration, and troubleshooting for Ninebot electric scooters, balance vehicles, and e-bikes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aNinebot](https://clawhub.ai/user/aNinebot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for help connecting Ninebot devices, reading battery and ride status, exporting ride statistics, changing vehicle settings, and troubleshooting common device issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Factory reset, speed-limit changes, firmware actions, and other vehicle parameter changes can affect vehicle behavior or erase settings. <br>
Mitigation: Require explicit user confirmation, perform changes only while the vehicle is safely parked, and back up important settings before firmware or reset operations. <br>
Risk: Diagnostic or configuration guidance may be incomplete for a specific Ninebot model or firmware version. <br>
Mitigation: Ask the user to confirm the exact device model and current state before applying guidance, and treat high-impact changes as review-before-action steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aNinebot/ninebot-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration guidance] <br>
**Output Format:** [Markdown with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only agent guidance; no API keys, MCP tools, or executable scripts were detected.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
