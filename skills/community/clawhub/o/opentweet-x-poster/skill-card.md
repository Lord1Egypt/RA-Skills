## Description:

Post to X (Twitter), Bluesky and LinkedIn using the OpenTweet API, including cross-posting, scheduling, threads, X Articles from markdown, media upload, evergreen queues, inspiration search, AI repurposing, human-approved DM outreach campaigns, and engagement analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petricbranko](https://clawhub.ai/user/petricbranko)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent create, schedule, publish, and analyze social content through OpenTweet for connected X, Bluesky, and LinkedIn accounts. It is most relevant for agent-assisted social posting workflows where public publishing, deletion, bulk scheduling, evergreen posting, and DM outreach require careful user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create public posts, schedule bulk content, delete posts, manage evergreen queues, and queue DM outreach through connected social accounts.

Mitigation: Install only when the user trusts OpenTweet with the connected accounts and API key, and require review before publishing, bulk scheduling, evergreen setup, deletion, or DM campaign approval.

Risk: Omitting a platform list can publish according to the account's auto cross-post setting rather than only to X.

Mitigation: Check cross-posting state before ambiguous posts and specify the intended platform list when the user asks for a particular network.

Risk: Cross-posted content can partially succeed, fail, or be skipped on individual networks.

Mitigation: Read and report the per-network results from OpenTweet instead of describing the overall operation as a single success.

Risk: AI-qualified DM outreach can create compliance and reputation risk if leads are approved without human review.

Mitigation: Show qualified leads and drafted messages to the user, approve only specific selected leads, keep pacing conservative, and respect opt-outs.

Risk: AI-generated or repurposed content may be inaccurate, inappropriate, or misaligned with the user's voice.

Mitigation: Keep generated content in draft or review state until the user has inspected and approved it.

## Reference(s):

- [OpenTweet X Poster on ClawHub](https://clawhub.ai/petricbranko/skills/opentweet-x-poster)
- [OpenTweet OpenClaw Twitter Posting](https://opentweet.io/features/openclaw-twitter-posting)
- [OpenTweet API Documentation](https://opentweet.io/api/v1/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with HTTP requests, JSON request bodies, shell commands, configuration notes, and human-facing status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenTweet API response summaries, published post URLs, scheduled post IDs, per-network posting results, and review prompts before sensitive actions.]

## Skill Version(s):

1.7.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
