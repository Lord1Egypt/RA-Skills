## Description:

Extracts follower lists and available public profile fields for Instagram accounts through Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datavoyantlab](https://clawhub.ai/user/datavoyantlab)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can retrieve followers and available public profile fields for up to 10 Instagram accounts per run, subject to Apify pricing and explicit charge approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested Instagram usernames are sent to the paid Apify service.

Mitigation: Disclose the transfer before execution and send the Apify token only to the documented Apify API.

Risk: The linked Apify account can incur charges for the run and retrieved followers.

Mitigation: Check current pricing, show the proposed charge cap and obtain explicit approval before every billable run.

Risk: A charge cap may stop collection before all followers are retrieved.

Mitigation: Mark charge-limited results as potentially partial rather than claiming a complete list.

## Reference(s):

- [Skill homepage](https://datavoyantlab.com/agent-skills/instagram)
- [Apify Instagram Followers Scraper](https://apify.com/datavoyantlab/instagram-followers-scraper)
- [ClawHub skill release](https://clawhub.ai/datavoyantlab/skills/instagram-followers-scraper)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Follower items with run and dataset IDs, requested usernames, charge cap, and completion status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be partial when the charge limit is reached.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and skill instructions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
