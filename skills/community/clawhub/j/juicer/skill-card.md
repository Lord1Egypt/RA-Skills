## Description:

Connect Juicer to OpenClaw. Juicer pulls public posts from Instagram, TikTok, X, Facebook, LinkedIn, YouTube, Reddit, Bluesky and more into one place: embed social feeds and walls on any website, track brand mentions, listen to topics and check competitors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicer](https://clawhub.ai/user/juicer)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and social media teams use Juicer to find public posts across supported networks and create or manage feeds, social walls, and embed codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email-based setup sends the user's email to Juicer, and the supplied security evidence notes that privacy disclosure is not explicit.

Mitigation: Explain the email sharing before requesting it and let the user choose OAuth or a developer API key instead.

Risk: The security scan was partial and did not fully inspect components.

Mitigation: Review the skill and its requested access before connecting a Juicer account.

## Reference(s):

- [Juicer MCP server documentation](https://developers.juicer.io/mcp-server)
- [Juicer developer API keys](https://www.juicer.io/developer)
- [Juicer API documentation](https://developers.juicer.io)
- [Juicer skill release on ClawHub](https://clawhub.ai/juicer/skills/juicer)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional commands, configuration details, social data summaries, and embed codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available social data and feed behavior depend on supported networks, account plan, and credit balance.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
