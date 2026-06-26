## Description: <br>
Triage tenant maintenance requests by severity, assign priority, identify the right contractor type, estimate costs, and generate work orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AdamsJB](https://clawhub.ai/user/AdamsJB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Self-managing landlords and property managers use this skill to classify tenant maintenance issues, draft tenant and owner notifications, route work to the right trade, and create standardized work orders. <br>

### Deployment Geography for Use: <br>
Massachusetts, United States <br>

## Known Risks and Mitigations: <br>
Risk: Generated work orders can contain tenant, property, phone, and cost details. <br>
Mitigation: Install and run the skill only where tenant and property information is appropriate to store, and review or delete old work-order files according to retention needs. <br>
Risk: Draft messages, contractor dispatch recommendations, and cost estimates could be acted on before review. <br>
Mitigation: Require human approval before sending tenant or owner messages, dispatching contractors, or committing to repair costs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/AdamsJB/homestruk-maintenance-triage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown work orders and drafted tenant or owner messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save local work-order files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
