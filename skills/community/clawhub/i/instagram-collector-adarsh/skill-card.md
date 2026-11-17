## Description:

Collects Instagram profile metrics for a handle using Apify, including follower count, engagement rate, posting frequency, average likes and comments, and top hashtags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Marketing teams, auditors, and developers use this skill to gather public Instagram profile metrics for a marketing audit pipeline while preserving a typed fallback result when collection fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instagram handles are sent to Apify under the user's Apify account.

Mitigation: Confirm the handle data is appropriate to send to Apify and review Apify logging, cost, rate-limit, and data-retention terms before use.

Risk: The skill depends on an APIFY_API_TOKEN environment variable.

Mitigation: Store the token as an environment variable or managed secret and avoid placing it in prompts, source files, logs, or generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/instagram-collector-adarsh)
- [Apify Instagram Profile Scraper API endpoint](https://api.apify.com/v2/acts/apify~instagram-profile-scraper/runs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript examples, JSON-like data shapes, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for collecting Instagram metrics through Apify and returning a valid InstagramData object, including graceful error output.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
