## Description:

Schedule videos and text posts to Instagram, TikTok, YouTube, Facebook, X, LinkedIn and Pinterest with Kreatix, move or cancel them, and read views and follower stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abrahimceylan](https://clawhub.ai/user/abrahimceylan)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and creators use Kreatix to schedule and manage posts across connected social accounts and review engagement and follower statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key grants access to the connected Kreatix service, and the security assessment advises considering whether that service is trusted.

Mitigation: Use a key only for the intended account, keep it private, and revoke it in Kreatix settings if exposed.

Risk: The security scan was partial, so its benign verdict does not cover all evidence.

Mitigation: Review the skill and confirm trust in the Kreatix service before providing an API key.

Risk: Scheduling, rescheduling, or canceling a post changes connected social accounts.

Mitigation: Show the user the channels, caption, and time, then wait for confirmation before making these changes.

## Reference(s):

- [Kreatix for AI agents](https://kreatix.cc/ai-agents/)
- [Kreatix MCP endpoint](https://api.kreatix.cc/mcp)
- [Kreatix agent key settings](https://kreatix.cc/settings/agent)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Guidance]

**Output Format:** [Markdown with JSON-RPC and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KREATIX_API_KEY. Scheduling, rescheduling, and cancellation require user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
