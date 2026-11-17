## Description:

Reads public Instagram profiles, posts, reels, stories, comments, followers, and search results through Scavio's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, researchers, and developers use this skill to look up public Instagram account and content data for creator discovery, influencer vetting, and competitor research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests disclose queried Instagram handles, post URLs, and search terms to Scavio.

Mitigation: Use the third-party service only when the user accepts sharing those queries; avoid submitting sensitive information.

Risk: Paginated or repeated requests consume API credits and may incur costs.

Mitigation: Agree on a page or credit budget before multi-call tasks, check remaining credits, and stop at the limit.

Risk: The skill requires a Scavio API key linked to a third-party account.

Mitigation: Supply the key via SCAVIO_API_KEY and keep it out of shared output.

## Reference(s):

- [Scavio Instagram API documentation](https://scavio.dev/docs/instagram-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=instagram-scraper-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/instagram-scraper-api)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [Markdown summaries, JSON data, or example API requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include pagination tokens, credit usage, and remaining balance.]

## Skill Version(s):

1.0.6 (source: server-resolved ClawHub release; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
