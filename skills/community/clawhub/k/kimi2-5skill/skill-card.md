## Description: <br>
Troubleshoot and operate Kimi 2.5 / OpenClaw image understanding when image recognition fails, OCR/images cannot be analyzed, the image tool reports Unknown model, configured vision models are ignored at runtime, or a safe recovery workflow is needed for OpenClaw image-capable models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwill2023](https://clawhub.ai/user/jiangwill2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and recover OpenClaw image understanding or OCR failures, especially Unknown model errors caused by invalid agent-level model provider configuration. It guides runtime verification, targeted configuration inspection, gateway restart, regression testing, and recovery communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational edits to agent-level models.json can disrupt active workloads or expose provider secrets if handled carelessly. <br>
Mitigation: Identify the affected agent, back up models.json, avoid exposing provider secrets, validate the JSON after edits, and restart the gateway only when comfortable with possible impact to active workloads. <br>
Risk: Static configuration checks can create false confidence when the image runtime still fails. <br>
Mitigation: Confirm recovery with openclaw status and at least one real image or OCR regression test before declaring the issue fixed. <br>


## Reference(s): <br>
- [Recovery Playbook](artifact/references/recovery-playbook.md) <br>
- [Incident 2026-04-14](artifact/references/incident-2026-04-14.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operational runbook guidance with manual validation steps] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
