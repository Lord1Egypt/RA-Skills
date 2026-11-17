## Description:

Coordinate payment incident response with structured triage, blast-radius assessment, mitigation actions, stakeholder communication, reconciliation recovery, and postmortem tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anugotta](https://clawhub.ai/user/anugotta)

### License/Terms of Use:

MIT-0

## Use Case:

Incident commanders, engineering leads, communications owners, and reconciliation owners use this skill to coordinate payment incident triage, containment, stakeholder updates, recovery checks, and postmortem follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operators may treat incident-response guidance as authority for payment, refund, legal, compliance, or public communication decisions.

Mitigation: Require an authorized incident commander and appropriate legal, compliance, or communications reviewers to approve containment actions and customer-facing messages before execution or publication.

Risk: Premature resolution messaging or unsafe retry behavior can worsen customer impact or create duplicate charges.

Mitigation: Verify payment metrics, customer-facing correctness, queue or webhook recovery, and reconciliation status before declaring resolution or retrying payment flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anugotta/skills/payment-incident-responder)
- [Publisher Profile](https://clawhub.ai/user/anugotta)
- [RBI Master Directions](https://www.rbi.org.in/scripts/BS_ViewMasDirections.aspx?id=12898)
- [Setup](artifact/setup.md)
- [Incident Playbook](artifact/incident-playbook.md)
- [Communication Templates](artifact/comms-templates.md)
- [Validation Checklist](artifact/validation-checklist.md)
- [Postmortem Template](artifact/postmortem-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Markdown checklist and incident update text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes severity and phase, top immediate actions, customer impact summary, next update owner and time, and reconciliation correctness checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
