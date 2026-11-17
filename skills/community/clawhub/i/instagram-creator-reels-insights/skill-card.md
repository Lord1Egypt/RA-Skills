## Description:

Reviews public creators’ recent Instagram Reels and regular video posts and produces source-linked daily or weekly insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apismith-labs](https://clawhub.ai/user/apismith-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and researchers use the skill to review recent public videos from selected Instagram accounts, identify transcript-supported themes and hooks, and plan content with links back to source posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and medium confidence; it did not fully assess one component or some instruction text, and the skill’s network capability has no declared tool scope.

Mitigation: Before a run, confirm the host exposes authorized Apify tools and run/result access; use those tools only and never provide credentials in chat.

Risk: Reports may have incomplete or unknown coverage because they include only posts and transcripts actually returned.

Mitigation: Use the report’s stated coverage and base conclusions only on returned posts and transcript evidence.

Risk: More creators or videos can generate Apify usage on the user’s account.

Mitigation: Review actual usage in the Apify Console; the skill does not estimate or cap costs.

## Reference(s):

- [Workflow contract](references/workflow.md)
- [Instagram Profile Posts & Reels Scraper](https://apify.com/apple_yang/instagram-post-scraper)
- [Instagram Transcript API & Profile Scraper](https://apify.com/apple_yang/instagram-transcripts-scraper)
- [Apify OpenClaw requirements](https://docs.apify.com/integrations/openclaw)
- [Project usage examples](https://github.com/apismith-labs/instagram-ai-agent-skills#instagram-creator-video-insights)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with creator-specific sections, source links, and transcript-supported observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coverage may be partial or unknown; conclusions are limited to returned posts and transcripts.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
