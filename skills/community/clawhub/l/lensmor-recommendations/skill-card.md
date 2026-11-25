## Description:

Lensmor Recommendations helps agents fetch and present AI-ranked trade-show exhibitors that match a user's ICP, using event IDs and filters such as company size, location, category, and tech stack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External B2B sales and event marketing teams use this skill before trade shows to turn exhibitor lists into prioritized outreach shortlists with ICP match rationale. It is suited for pre-show account prioritization when the user has a Lensmor API key and event targeting criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends trade-show targeting details, ICP criteria, company profile information, and account shortlists to Lensmor's hosted API.

Mitigation: Install and use it only when the organization has approved Lensmor for that data, and avoid confidential, regulated, or highly sensitive sales strategy data unless approved.

Risk: Returned recommendations and business signals can become stale or incomplete.

Mitigation: Review the ranked results before outreach and treat fields such as funding stage as planning signals rather than current verified facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/lensmor-recommendations)
- [Lensmor API documentation](https://api.lensmor.com/)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown recommendations with ranked tables, ICP match rationale, and concise follow-up guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should not expose API key values; exhibitor rationale should be grounded in returned company fields.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
