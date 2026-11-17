## Description:

Finds decision-makers and key contacts at exhibitor companies using the Lensmor API for pre-show LinkedIn outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

B2B sales and marketing teams use this skill to identify decision-makers, influencers, and buyer-function contacts at target exhibitor companies before a trade show, then plan LinkedIn outreach or booth meeting requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends target company names and role filters to Lensmor and uses returned professional contact data for outreach.

Mitigation: Use it only for lawful business outreach approved by the organization; do not submit confidential prospecting lists or regulated data unless that use has been approved.

Risk: Returned contact records, LinkedIn profile links, and source types may need verification before messaging.

Mitigation: Review contact records before outreach, do not fabricate missing contacts, and state clearly that email addresses are not available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/lensmor-contact-finder)
- [Lensmor API documentation](https://api.lensmor.com/)
- [Lensmor platform](https://platform.lensmor.com)
- [Lensmor website](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with contact tables, outreach priority notes, and short follow-up suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; does not return email addresses and treats LinkedIn profiles as the primary outreach channel.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
