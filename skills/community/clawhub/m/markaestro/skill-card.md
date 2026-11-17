## Description:

Schedule, publish, and review social posts through Markaestro (Facebook, Instagram, TikTok, Threads, Pinterest, LinkedIn, X, YouTube), read brand and per-post analytics, and manage Intelligent Evergreen queues using its MCP server or public API. Use when a task mentions Markaestro, posting or scheduling to a connected social account, uploading media for a post, checking whether a post published or how it performed, reporting on social performance, deciding what or when to post next, batch-scheduling or editing scheduled content, refreshing analytics, finding the best time to post, writing in a brand's voice, or managing proven recurring content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markaestro](https://clawhub.ai/user/markaestro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media teams use this skill to create, schedule, publish, and review posts across connected social channels, manage recurring content, and inspect brand and post analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posts and recurring content can be published to connected social accounts.

Mitigation: Review content, destinations, schedules, and recurring-post settings before approval, and confirm before immediate or recurring publication.

Risk: The local API fallback uses a bearer API key.

Mitigation: Prefer hosted browser sign-in and authorize only the needed brands; for local use, pin a reviewed package version and protect the API key.

## Reference(s):

- [Markaestro skill page](https://clawhub.ai/markaestro/skills/markaestro)
- [Markaestro API reference (OpenAPI)](https://markaestro.com/api/public/v1/openapi.json)
- [MCP tools reference](references/tools.md)
- [Delivery modes and channel settings](references/settings.md)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and structured API request and response data (JSON)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create drafts or scheduled posts and report on publishing status and analytics for connected accounts.]

## Skill Version(s):

0.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
