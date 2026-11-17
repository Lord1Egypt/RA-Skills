## Description:

The Corbett Report — official WordPress RSS at corbettreport.com/feed/. Fetch only; answer in English; items strictly from XML; dated header, numbered list, title as link, optional teaser from <description>.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximedogawa](https://clawhub.ai/user/maximedogawa)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent for recent Corbett Report posts, episodes, interviews, or podcast headlines. The skill directs the agent to fetch the official RSS feed and summarize only item titles, links, dates, categories, and teasers present in the XML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RSS feed may be unavailable, empty, or fail to fetch.

Mitigation: The skill instructs the agent to report the fetch failure briefly and not invent content.

Risk: Current feed items may include opinionated third-party content.

Mitigation: The skill confines responses to titles, URLs, dates, categories, and teaser text from the official RSS XML so readers can evaluate the linked source.

## Reference(s):

- [The Corbett Report](https://corbettreport.com/)
- [The Corbett Report RSS Feed](https://corbettreport.com/feed/)
- [ClawHub Skill Page](https://clawhub.ai/maximedogawa/skills/news-corbett-report)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown with dated header, numbered linked titles, and optional RSS teaser text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to 3-5 newest feed items in English; content is limited to fields from each RSS item.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
