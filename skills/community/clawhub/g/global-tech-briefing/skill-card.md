## Description:

Create a structured global tech news briefing by running web searches for top tech trends, company announcements, and AI/quantum headlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request concise global technology news briefings for today or a specified date. It summarizes live search findings into trends, company news, and key takeaways instead of returning raw search results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs live external web searches for broad technology news queries when invoked.

Mitigation: Install and use it only when live tech-news searches are acceptable; narrow invocation wording if stricter control is needed.

Risk: Briefings may summarize current search results into incomplete or time-sensitive takeaways.

Mitigation: Review important conclusions against primary sources before using them for decisions.

## Reference(s):

- [Brave Search API](https://brave.com/search/api)
- [Global Tech Briefing on ClawHub](https://clawhub.ai/terrycarter1985/skills/global-tech-briefing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured text briefing with Markdown-style section labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and web_search; accepts an optional YYYY-MM-DD date argument.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
