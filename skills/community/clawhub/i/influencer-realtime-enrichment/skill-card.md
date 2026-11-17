## Description:

Fetch fresh, on-demand creator data across TikTok, Instagram, Facebook, and YouTube: page/profile info, latest videos, posts, and media details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengyu-xixihaha](https://clawhub.ai/user/chengyu-xixihaha)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, and analysts use this skill to retrieve current creator and content data, compare it with prior assumptions, and summarize decision-relevant deltas for campaigns or monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator identifiers, content URLs, query terms, and possibly an API key may be sent to the configured gateway.

Mitigation: Use only a trusted HTTPS gateway, keep unrelated secrets out of the .env file, and review what identifiers or URLs are submitted before running enrichment.

Risk: Untrusted callers could alter endpoint or header settings through environment variables or operation arguments.

Mitigation: Restrict who can set SCRUMBALL_BASE_URL and override headers, and review configured endpoint values before execution.

Risk: The runner creates a persistent install ID that may remain after the skill is reinstalled.

Mitigation: Document and, when needed, manually delete the persistent install ID files referenced by the runner.

## Reference(s):

- [API Index](references/api-index.md)
- [Request and Response Guide](references/request-response.md)
- [Operations Manifest](references/operations.json)
- [ClawHub Skill Page](https://clawhub.ai/chengyu-xixihaha/skills/influencer-realtime-enrichment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional JSON API responses and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output contract includes freshness, key deltas, impact, and next step.]

## Skill Version(s):

1.0.5 (source: server release evidence and config.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
