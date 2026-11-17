## Description:

Retrieves current public Instagram Stories by username through a paid Apify service, returning media links and available story metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datavoyantlab](https://clawhub.ai/user/datavoyantlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers retrieve active Stories from public Instagram profiles, including media URLs, timestamps, mentions, links, music, locations, and partnership details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested account names are shared with Apify/DataVoyantLab.

Mitigation: Disclose the external lookup before execution and avoid private or sensitive account lists.

Risk: An Apify account may incur charges for the run and each submitted username.

Mitigation: Show current prices and the exact maximum charge; require explicit approval of that cap before each run.

Risk: The Apify token grants access to the connected paid account.

Mitigation: Keep the token secret and send it only to the documented Apify API.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/datavoyantlab/skills/instagram-stories-scraper)
- [Advanced Instagram Stories Scraper on Apify](https://apify.com/datavoyantlab/advanced-instagram-stories-scraper)
- [Publisher skill information](https://datavoyantlab.com/agent-skills/instagram)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Complete JSON story dataset with a short text count by username]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the authorized charge cap and, for asynchronous runs, run and dataset IDs; a successful lookup may return no active Stories.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata and skill instructions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
