## Description:

Fetches web pages from provided URLs and returns structured markdown summaries for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to fetch web pages and turn page content into concise markdown summaries for research, agent memory, and fact checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted URLs could be used to reach local files, localhost services, private networks, or cloud metadata endpoints.

Mitigation: Restrict inputs to parsed http and https URLs, block private and local address ranges, and validate redirects before fetching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmyclanker/skills/jimmy-web-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Structured markdown summary with key points, source URL, and generation timestamp]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required; accepts a URL and optional focus string.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
