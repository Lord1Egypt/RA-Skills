## Description:

Find high-intent leads on Hacker News via the free Algolia API, score posts, surface Ask HN threads, and identify technical founders actively seeking tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdbrain](https://clawhub.ai/user/3rdbrain)

### License/Terms of Use:

MIT

## Use Case:

Sales, marketing, founder, and developer-facing teams use this skill to find Hacker News posts and Ask HN threads that may indicate demand for B2B tools, then prioritize outreach with lead-quality scoring and suggested response timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to hn.algolia.com.

Mitigation: Use sanitized keywords and avoid secrets, customer names, private strategy terms, or other confidential business information.

Risk: Lead scores and response urgency are heuristic and may overstate prospect quality.

Mitigation: Review matched posts manually and tailor any outreach to the actual thread context before engaging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3rdbrain/skills/hn-prospecting)
- [Publisher profile](https://clawhub.ai/user/3rdbrain)
- [Hacker News Algolia API](https://hn.algolia.com/api)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [CLI text summaries and structured JavaScript result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key or environment variables are required; searches query the public Hacker News Algolia API.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
