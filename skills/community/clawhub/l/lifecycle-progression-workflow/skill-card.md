## Description: <br>
Build workflows to automate contact progression through the sales funnel: Lead to MQL to SQL to Opportunity to Customer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and marketing operations teams use this skill to create HubSpot contact-based workflows that move contacts forward through lifecycle stages when score, meeting, deal, and closed-won conditions are met. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect trigger logic could enroll contacts when only part of the intended lifecycle condition is true. <br>
Mitigation: Verify that each workflow uses AND logic between the event condition and the current lifecycle stage before publishing. <br>
Risk: Published workflows can automatically change many HubSpot contact lifecycle stages. <br>
Mitigation: Test with sample contacts or a limited segment and review workflow history before broad rollout. <br>
Risk: Browser-extension-driven workflow edits may make unintended UI changes. <br>
Mitigation: Supervise extension-driven edits and manually confirm triggers, actions, and re-enrollment settings before enabling workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tomgranot/lifecycle-progression-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown instructions with workflow trigger and action specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-facing setup guidance for HubSpot workflow configuration; it does not execute CRM changes directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
