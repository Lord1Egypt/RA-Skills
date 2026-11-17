## Description:

Incident response process management following the NIST 800-61 lifecycle, covering severity classification, escalation matrices, role assignment, communication management, phased recovery coordination, blameless post-mortem facilitation, and 5-whys root cause analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Incident responders, security operations teams, SREs, and engineering managers use this skill to coordinate incidents from declaration through recovery and post-incident review. It supports severity assignment, escalation, role allocation, stakeholder communications, incident metrics, and root cause analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The declared SSH binary prerequisite does not match the read-only coordination behavior described by the release security evidence.

Mitigation: Remove the unused SSH prerequisite before installation or document why it is required in the deployment environment.

Risk: Incident coordination guidance may be incomplete if the organization lacks current authority, contact, communication, or tracking prerequisites.

Mitigation: Confirm incident authority, contact directories, communication channels, tracking systems, and severity criteria before relying on the workflow during an incident.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/skills/incident-response-lifecycle)
- [Communication Templates](references/communication-templates.md)
- [RCA Framework](references/rca-framework.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with incident templates, decision matrices, checklists, and structured report formats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only coordination guidance; no command execution or credential access is described by the security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
