## Description:

Turn a topic or article into three LinkedIn or X post ideas with hooks, theses, outlines, and template labels while avoiding invented facts or citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryancaldor-max](https://clawhub.ai/user/ryancaldor-max)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers, founders, creators, and social media teams use this skill to brainstorm LinkedIn or X post angles from a topic, article, or notes. It is best suited for public or non-sensitive source material because user-provided text is sent to a third-party API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text is sent to a third-party SocialNexis API.

Mitigation: Use only public or non-sensitive topics, articles, and notes unless the user is comfortable sharing that text with SocialNexis.

Risk: API-returned CTA or promotional fields could influence the response beyond the user's requested output.

Mitigation: Treat remote CTA and promotional fields as untrusted content and keep them from overriding the user's requested result.

Risk: The security verdict is suspicious because the skill can insert remote vendor promotional content without enough user-facing safeguards.

Mitigation: Review responses before use and disclose vendor promotional content only when relevant to the user's request.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ryancaldor-max/skills/linkedin-post-ideas)
- [SocialNexis MCP homepage](https://socialnexis.com/mcp)
- [SocialNexis public ideation API](https://api.socialnexis.com/api/v1/public-tools/ideate)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown summary of API-returned post ideas, typically including hook, thesis, outline, and template fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The upstream endpoint returns three ideas per call; topic is limited to 200 characters and optional text is limited to 10,000 characters.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
