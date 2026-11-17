## Description:

Manage ProductBoard releases and roadmap planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robertoamoreno](https://clawhub.ai/user/robertoamoreno)

### License/Terms of Use:


## Use Case:

Product managers, product operations teams, and developers use this skill to review Productboard product hierarchy, organize features, assign owners, set planning dates, and update release status across sprint, release, and quarterly planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live Productboard roadmap records, including feature creation, status updates, owner assignment, date changes, and archiving.

Mitigation: Install only for users authorized to modify Productboard roadmap data and confirm the target workspace, product, record identifiers, and intended changes before write actions.

Risk: Planning actions may be applied to the wrong feature or product if the current roadmap state is not reviewed first.

Mitigation: Prefer read-only review with product hierarchy, feature listing, and feature detail tools before creating or updating records.

## Reference(s):

- [Productboard Release on ClawHub](https://clawhub.ai/robertoamoreno/skills/productboard-release)
- [openclaw-productboard homepage](https://github.com/robertoamoreno/openclaw-productboard)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning workflows and Productboard tool-use guidance; changes to live roadmap records should be confirmed before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
