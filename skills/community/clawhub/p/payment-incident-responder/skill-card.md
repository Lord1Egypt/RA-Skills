## Description: <br>
Coordinate payment incident response with structured triage, blast-radius assessment, mitigation actions, stakeholder communication, reconciliation recovery, and postmortem tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anugotta](https://clawhub.ai/user/anugotta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Payment operations, engineering, support, and incident response teams use this skill to triage payment incidents, coordinate containment and communications, recover correctness through reconciliation, and prepare postmortems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment-system changes may be harmful if treated as automatic authority. <br>
Mitigation: Use the skill as a checklist and communication aid with authorized incident responders and human review before pausing payment flows, rolling back systems, repairing data, or declaring resolution. <br>
Risk: Incorrect or premature customer communication can create confusion during payment incidents. <br>
Mitigation: Use approved customer messaging, timestamp decisions in the incident log, and confirm metrics plus correctness checks before communicating resolution. <br>


## Reference(s): <br>
- [Incident playbook](artifact/incident-playbook.md) <br>
- [Setup](artifact/setup.md) <br>
- [Validation checklist](artifact/validation-checklist.md) <br>
- [Communication templates](artifact/comms-templates.md) <br>
- [Postmortem template](artifact/postmortem-template.md) <br>
- [RBI Master Directions](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown checklist and incident update guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute payment actions or access payment systems.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
