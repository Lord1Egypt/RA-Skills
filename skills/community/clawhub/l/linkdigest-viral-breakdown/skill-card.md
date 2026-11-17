## Description:

Analyzes a public social media post into its hook, timed structure, title and cover ideas, call to action, and reusable template, while checking quoted text against the source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media analysts, and developers use the skill to study the structure of a public Douyin, Xiaohongshu, TikTok, YouTube, or Bilibili post and prepare a source-grounded breakdown or writing template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content may be processed by third parties, and cached results for a public link may be shared with other users.

Mitigation: Submit public links only and remove private details from share text.

Risk: LinkDigest API use consumes credits.

Mitigation: Set --max-credits to cap spending for a request and review the documented pricing.

Risk: The API key can grant access to a paid account.

Mitigation: Keep LINKDIGEST_API_KEY in an environment variable or client configuration; do not paste it into chats, source code, or commits.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-linkdigest-viral-breakdown)
- [LinkDigest privacy policy](https://linkdigest.dev/privacy)
- [LinkDigest OpenAPI specification](https://linkdigest.dev/openapi.json)
- [ClawHub skill release](https://clawhub.ai/jackchew7143/skills/linkdigest-viral-breakdown)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown or JSON containing a post breakdown and reusable content template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include source-checked quotations, platform engagement metrics, translations, and notes about missing content; it does not predict reach.]

## Skill Version(s):

1.2.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
