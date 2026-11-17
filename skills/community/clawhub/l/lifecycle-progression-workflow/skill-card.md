## Description:

Build workflows to automate contact progression through the sales funnel: Lead to MQL to SQL to Opportunity to Customer. Each transition is triggered by a specific event (score threshold, meeting booked, deal created, deal won).

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, sales, and revenue operations teams use this skill to configure HubSpot workflows that move contacts forward through lifecycle stages based on lead score, meeting, deal, and closed-won events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HubSpot workflow changes can update lifecycle stages and send internal notifications.

Mitigation: Use appropriate HubSpot permissions, test with sample contacts first, and verify trigger logic before enabling workflows broadly.

Risk: Workflow skeletons generated with Breeze may use OR-style event triggers where these progression workflows require AND logic with the current lifecycle stage.

Mitigation: Manually review and correct enrollment conditions for each workflow before activation.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with workflow prompts and setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces HubSpot workflow configuration guidance; no executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
