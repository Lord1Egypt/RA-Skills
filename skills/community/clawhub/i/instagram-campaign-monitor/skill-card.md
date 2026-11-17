## Description:

Monitors recent public Instagram posts from campaign or branded hashtags through Apify, with optional brand-term filtering and webhook delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datavoyantlab](https://clawhub.ai/user/datavoyantlab)

### License/Terms of Use:

MIT-0

## Use Case:

Campaign managers and marketing teams use this skill to track recent public posts under branded hashtags, discover user-generated content, and receive scheduled campaign reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify scans incur charges to the linked account.

Mitigation: Confirm current pricing and obtain explicit approval for the search scope and charge cap before each billable run.

Risk: Hashtags and filters are processed by Apify; matching public post data may be forwarded to a webhook.

Mitigation: Disclose external processing and require approval of any user-supplied HTTPS webhook destination before sending results.

Risk: The Apify token could be exposed if sent to an unintended destination.

Mitigation: Keep the token private and send it only to the documented Apify API, never to a webhook.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/datavoyantlab/skills/instagram-campaign-monitor)
- [Instagram Campaign Hashtag Monitor on Apify](https://apify.com/datavoyantlab/instagram-campaign-hashtag-monitor)
- [DataVoyantLab skill homepage](https://datavoyantlab.com/agent-skills/instagram)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Markdown report with JSON dataset items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes matching posts, run and dataset IDs, search scope, and authorized charge; zero matches are distinguished from failed runs.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
