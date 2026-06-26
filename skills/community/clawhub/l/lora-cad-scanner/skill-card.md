## Description: <br>
LoRa CAD air scanner helps configure and operate a LilyGo T3 SX1276 scanner, optional HackRF survey workflow, serial monitoring, packet decoding, local logging, and Telegram alert setup for authorized LoRa band monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arsatyants](https://clawhub.ai/user/arsatyants) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, RF engineers, and authorized operators use this skill to set up a LilyGo T3 and companion Raspberry Pi workflow for LoRa channel activity scanning, packet capture, decoded alerts, and follow-up HackRF band surveys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture raw radio packets and device identifiers and store them in local files. <br>
Mitigation: Monitor only frequencies the operator is authorized to inspect, redact identifiers where possible, and protect, rotate, or delete local capture files according to the operator's data-handling policy. <br>
Risk: Telegram alerting can export captured RF payloads or identifiers to an external service. <br>
Mitigation: Enable Telegram delivery only through explicit user configuration, narrow the alert contents, and treat each notification as an external data transfer. <br>
Risk: Broad RF scanning and reconnaissance workflows may be regulated or inappropriate in some environments. <br>
Mitigation: Confirm local legal authorization before scanning, narrow the configured frequency range, and avoid monitoring bands or devices outside the approved scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arsatyants/lora-cad-scanner) <br>
- [Setup Guide](references/setup.md) <br>
- [SX1276 CAD Register Reference](references/sx1276-cad.md) <br>
- [HackRF + LilyGo Combined Workflow](references/hackrf-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Arduino and Python code references, configuration steps, and operational notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may guide hardware flashing, serial monitoring, RF scan configuration, local file handling, and optional Telegram alert delivery.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
