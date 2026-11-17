## Description:

Searches LinkedIn posts by keyword with the Apify harvestapi/linkedin-post-search actor, including optional author, company, date, sorting, pagination, reactions, and comments controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godefroy](https://clawhub.ai/user/godefroy)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to construct Apify actor requests for LinkedIn post searches, monitor runs, and retrieve JSON datasets for posts, comments, or reactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens passed in URL query strings may be exposed through process listings, shell history, logs, or copied command output.

Mitigation: Use a dedicated least-privileged Apify token, avoid logging tokenized URLs, and prefer bearer-token headers when adapting the commands.

Risk: Actor runs and optional reaction or comment scraping can incur usage costs.

Mitigation: Set bounded maxPosts, maxReactions, and maxComments values and monitor Apify usage during runs.

Risk: LinkedIn search results may be incomplete and each search query is limited to 85 characters.

Mitigation: Treat results as a non-exhaustive dataset, keep queries within the documented limit, and verify important findings before relying on them.

## Reference(s):

- [LinkedIn Search Posts ClawHub page](https://clawhub.ai/godefroy/skills/linkedin-search-posts)
- [Apify actor run endpoint](https://api.apify.com/v2/acts/harvestapi~linkedin-post-search/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with bash curl examples and JSON result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_API_TOKEN; retrieves Apify actor run and dataset JSON; optional comment and reaction scraping can increase result volume and cost.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
