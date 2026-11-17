## Description:

Post and reply to X/Twitter and Farcaster with text, images, threads, account-aware limits, draft previews, and optional link shortening or text variation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teeclaw](https://clawhub.ai/user/teeclaw)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to draft, preview, post, reply, and thread social updates across X/Twitter and Farcaster while handling credentials, platform limits, images, and posting costs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post publicly to social accounts and spend Farcaster wallet funds when posting casts.

Mitigation: Use dry-run previews first, keep account permissions and wallet balances limited, and require human review before live posting.

Risk: Shell scripts use powerful social and wallet credentials and source local environment files.

Mitigation: Install only after reviewing the scripts and credential handling, and prefer safer secret storage before production use.

Risk: Tier detection and posting flows can call X/Twitter write-capable API endpoints.

Mitigation: Avoid refresh or live posting flows until the tier probe behavior is reviewed or fixed, and verify API billing expectations.

Risk: Image uploads and link shortening can disclose media or URLs to third-party destinations.

Mitigation: Do not send sensitive media or links through image upload or shortening features unless those destinations are disclosed and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teeclaw/skills/openclaw-social-post)
- [TeeClaw ClawHub profile](https://clawhub.ai/user/teeclaw)
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
- [X API pricing](https://developer.twitter.com/#pricing)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated social post text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke X/Twitter and Farcaster APIs, upload images to third-party hosts, shorten links, and spend account or wallet funds when run outside dry-run mode.]

## Skill Version(s):

1.5.0 (source: frontmatter, CHANGELOG released 2026-02-11, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
