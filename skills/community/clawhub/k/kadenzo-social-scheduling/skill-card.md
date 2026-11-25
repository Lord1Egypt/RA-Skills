## Description:

Schedule, review and change social media posts through the Kadenzo MCP server, and read post analytics and social listening. Use when the user asks to post, schedule, queue, reschedule or cancel content on Instagram, TikTok, X, LinkedIn, Facebook, YouTube, Pinterest, Threads, Bluesky, Telegram or Mastodon, or asks how their posts or brand mentions are doing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jors7](https://clawhub.ai/user/jors7)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media teams use this skill to draft, schedule, review, change, or cancel posts across supported networks and to review post performance and mentions through Kadenzo.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Choosing the wrong social account or time zone could schedule a post for the wrong audience or time.

Mitigation: Use the account IDs returned by list_accounts, clarify ambiguous account choices, confirm the user's time zone, and repeat the final local time.

Risk: Scheduling, updating, canceling, or commenting changes the user's social accounts.

Mitigation: Validate the post first, show the final content, accounts, and time, and get a clear confirmation before making the change.

## Reference(s):

- [Kadenzo Developer Documentation](https://studio.kadenzo.app/developers)
- [Kadenzo Plans](https://kadenzo.app/pricing)

## Skill Output:

**Output Type(s):** [Text, Guidance, Analysis]

**Output Format:** [Network-specific social post copy and text summaries of scheduling status, analytics, and social listening.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post content may be tailored per social network; summaries reflect selected accounts and available metrics.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
