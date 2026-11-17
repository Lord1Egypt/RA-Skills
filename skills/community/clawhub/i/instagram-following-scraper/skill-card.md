## Description:

Extracts accounts followed by public Instagram profiles through Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datavoyantlab](https://clawhub.ai/user/datavoyantlab)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to retrieve the accounts followed by public Instagram profiles, including usernames and public profile fields. It does not retrieve follower lists or posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested public Instagram usernames are shared with Apify for scraping.

Mitigation: Disclose the transfer to the user before execution.

Risk: Apify charges the linked account for a billable run.

Mitigation: Show current prices and the proposed charge cap, and obtain explicit approval for that cap before each run.

Risk: Exposure of the Apify API token could allow unauthorized use.

Mitigation: Keep APIFY_TOKEN private and send it only to the documented Apify API.

## Reference(s):

- [Skill page on ClawHub](https://clawhub.ai/datavoyantlab/skills/instagram-following-scraper)
- [DataVoyantLab Instagram agent skills](https://datavoyantlab.com/agent-skills/instagram)
- [Instagram Following Scraper on Apify](https://apify.com/datavoyantlab/instagram-following-scraper)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Following-list items with requested usernames, run and dataset IDs, charge cap, and partial-result status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be incomplete if the approved charge cap is reached.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
