## Description: <br>
Classify medical messages (emails, iMessages) as critical, urgent, or routine based on medical urgency indicators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binubmuse](https://clawhub.ai/user/binubmuse) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External healthcare support teams and developers can use this skill to prioritize inbound patient messages into critical, urgent, or routine categories for qualified human review. It should be used as non-authoritative triage support, not as a replacement for emergency services, clinical assessment, or licensed medical judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical urgency classifications may be incorrect or incomplete in a high-stakes healthcare context. <br>
Mitigation: Use the skill only as non-authoritative triage support and require qualified human review before acting on classifications. <br>
Risk: Safety boundaries are under-disclosed for emergency or clinical use. <br>
Mitigation: Deployments should add clear emergency escalation language and direct users to emergency services for life-threatening symptoms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binubmuse/medical-triage) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/binubmuse) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, guidance] <br>
**Output Format:** [JSON array of triage results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each result includes the message id, triage category, reason, and confidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
