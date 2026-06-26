## Description: <br>
Build a HubSpot workflow that auto-enriches and stages new contacts upon creation, sets lifecycle stage, copies company name and industry from the associated company, and branches on completeness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CRM administrators and revenue operations teams use this skill to build and verify a HubSpot workflow that stages and enriches every newly created contact before manual follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow changes HubSpot contact lifecycle, company, and industry fields, and copy actions can overwrite imported or existing values. <br>
Mitigation: Test with sample contacts, confirm overwrite behavior before activation, consider excluding imports, and review workflow history during the first 24 hours. <br>
Risk: AI-assisted setup can misconfigure triggers, branch conditions, copy actions, or re-enrollment settings. <br>
Mitigation: Prefer the manual UI build for production use, and verify trigger logic, copy-from-associated-company actions, branch conditions, and re-enrollment settings before enabling the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/new-contact-hygiene-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes manual workflow setup steps, verification checks, rollback guidance, and caveats for optional AI-assisted setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
