## Description:

Build a HubSpot workflow that auto-enriches and stages new contacts upon creation, sets lifecycle stage, copies company name and industry from the associated company, and branches on completeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

CRM operations teams and HubSpot administrators use this skill to build and verify a manual HubSpot workflow that standardizes newly created contacts, copies associated company data, and flags contacts still missing company information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs on all newly created contacts and may overwrite contact company and industry fields from the primary associated company.

Mitigation: Review enrollment criteria before activation, test with representative contacts, and add exclusions such as import lists when those contacts should not be overwritten.

Risk: The optional Chrome extension route interacts with an authenticated HubSpot UI session.

Mitigation: Use that route only in a trusted HubSpot account and browser profile, and review every workflow change before saving or turning it on.

Risk: AI-generated workflow drafts may use incorrect HubSpot trigger logic or omit unsupported branch and copy actions.

Mitigation: Manually verify trigger conditions, branch checks, copy-from-associated-company actions, and re-enrollment settings in the HubSpot UI before enabling the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomgranot/skills/new-contact-hygiene-workflow)
- [Publisher Profile](https://clawhub.ai/user/tomgranot)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown workflow instructions with verification and rollback steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual HubSpot UI workflow guidance; no automatic local execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
