## Description: <br>
Manages HubSpot CRM contacts and deals for USC SYNERGY, including search, creation, updates, associations, pipeline tracking, notes, tasks, and cURL-based workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mibbou](https://clawhub.ai/user/mibbou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Operators or agents managing USC SYNERGY's HubSpot CRM use this skill to look up and maintain contacts and deals, advance pipeline stages, add notes and tasks, and prepare daily pipeline reports. It is intended for environments where the user controls the relevant HubSpot account and token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, associate, change stages for, or archive live customer CRM records. <br>
Mitigation: Use a least-privilege HubSpot token and require explicit confirmation before any create, update, association, note or task creation, stage change, or archive action. <br>
Risk: External n8n webhook flows are listed without complete scoping, payload, consent, retention, or access-control details. <br>
Mitigation: Do not enable or invoke webhook flows until the destination, payload contents, consent, retention, and access controls are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mibbou/hubspot-crm) <br>
- [Publisher profile](https://clawhub.ai/user/mibbou) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown with bash cURL command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HUBSPOT_ACCESS_TOKEN and explicit user confirmation before mutating CRM records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
