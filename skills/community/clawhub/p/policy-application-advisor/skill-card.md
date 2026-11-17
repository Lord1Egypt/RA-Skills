## Description:

Policy Application Advisor supports an end-to-end policy application workflow for park-enterprise scenarios, including policy monitoring, project evaluation, material preparation, form-filling assistance, human confirmation, and delivery tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perrykono-debug](https://clawhub.ai/user/perrykono-debug)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, park operators, and policy-application advisors use this skill to assess policy eligibility, prepare application drafts and checklists, validate materials, and track application progress while preserving user confirmation before any submission or external action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise policy-application data may include sensitive financial, tax, qualification, or application-history information.

Mitigation: Confirm connected policy libraries, company profiles, and historical application records are appropriate for read access; avoid sending raw enterprise financial or tax data to third parties.

Risk: Policy eligibility, subsidy estimates, or deadlines may become outdated or misleading if source policy data is stale.

Mitigation: Use policy sources with publication and deadline metadata, refresh expired policy records before warnings or eligibility decisions, and label subsidy calculations as estimates subject to official rules.

Risk: Draft materials or form mappings could be mistaken for final submissions.

Mitigation: Keep the human confirmation gate before submissions, writes, external sends, or API calls; label generated application materials as pending user confirmation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text with checklists, tables, draft materials, validation notes, and progress updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; draft outputs are advisory and should be marked for user confirmation.]

## Skill Version(s):

1.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
