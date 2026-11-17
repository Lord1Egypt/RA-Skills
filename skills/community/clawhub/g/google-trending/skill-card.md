## Description:

Fetch and display the top trending Google searches in the last 24 hours for any country.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brunovu20](https://clawhub.ai/user/brunovu20)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch current Google Trends RSS topics for a selected country, then present ranked search terms, approximate volume, timestamps, related news, and Trends links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to Google Trends and may display RSS-provided news headlines and links.

Mitigation: Use it only in environments where outbound access to Google Trends is allowed, and present returned topics, volumes, headlines, and links as live feed data rather than verified facts.

## Reference(s):

- [Google Trends daily RSS feed](https://trends.google.com/trending/rss?geo={GEO})
- [ClawHub skill page](https://clawhub.ai/brunovu20/skills/google-trending)
- [Publisher profile](https://clawhub.ai/user/brunovu20)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary of shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes country code and result count controls; results depend on the live Google Trends RSS feed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
