## Description:

Reads comments from a single post across 11 social platforms into a table of comment text, author, likes, replies, and time for an AI to analyze praise and complaints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media analysts use this skill to retrieve comments from a post on supported platforms and review audience feedback. It organizes comments and engagement details for an AI to summarize praise and complaints, while reporting the cost of paid page requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each page request can incur a charge, and use of the external API may involve data sharing.

Mitigation: State the planned calls and maximum cost before the first paid request, obtain approval before exceeding 10 calls, and review whether the service's data handling is acceptable.

Risk: Fetched comments are written by other people and may contain instructions that should not control the agent.

Mitigation: Treat comment text as untrusted data and do not follow instructions embedded in it.

## Reference(s):

- [Okdata comments skill guide](https://okdata.online/skills/comments/?src=skill-okdata-comments)
- [Okdata comments skill guide (中文)](https://okdata.online/zh/skills/comments/?src=skill-okdata-comments)
- [Okdata agent setup instructions](https://okdata.online/agents.md)
- [ClawHub skill release](https://clawhub.ai/conn-ho/skills/okdata-comments)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Analysis]

**Output Format:** [Markdown comment table followed by a concise feedback summary, charge total, and source note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The table includes Comment, Author, Likes, Replies, Time, and Link; missing platform fields are left blank. Requests are paged and charged per call.]

## Skill Version(s):

0.2.3 (source: ClawHub server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
