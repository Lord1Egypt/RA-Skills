## Description: <br>
Incident response process management following the NIST 800-61 lifecycle, covering severity classification, escalation matrices, role assignment, communication management, phased recovery coordination, blameless post-mortem facilitation, and 5-whys root cause analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Incident commanders, security teams, SREs, and operations teams use this skill to coordinate service-affecting incidents from detection through post-incident review. It supports severity assignment, escalation, stakeholder communication, recovery coordination, incident metrics, and root cause analysis without performing technical forensics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags this release as suspicious because an autoreview helper may grant nested reviewers full local access. <br>
Mitigation: Install only for trusted ClawHub maintainer workflows, review the helper before use, prefer --no-yolo or AUTOREVIEW_YOLO=0, scope credentials tightly, and confirm public or account-affecting actions before execution. <br>
Risk: Incident coordination guidance can produce incorrect severity, escalation, or notification recommendations if the responder supplies incomplete or stale incident facts. <br>
Mitigation: Require the incident commander to validate severity, impact, notification obligations, and recovery decisions against current organizational policy before acting. <br>
Risk: The skill is scoped to process coordination and may be misapplied as a forensic or containment procedure. <br>
Mitigation: Use dedicated technical incident response procedures for evidence collection, device forensics, and containment execution. <br>


## Reference(s): <br>
- [Communication Templates](references/communication-templates.md) <br>
- [RCA Framework](references/rca-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with incident templates, checklists, matrices, and report structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only process guidance; does not perform evidence collection, containment execution, or forensic analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
