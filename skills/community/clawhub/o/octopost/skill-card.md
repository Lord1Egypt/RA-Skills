## Description:

Post, schedule, queue, and thread social posts on X and other connected networks through Octopost, with a human approval queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakemarsh](https://clawhub.ai/user/jakemarsh)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use Octopost to draft and publish, schedule, queue, and manage social posts across connected accounts. The approval queue supports human review before publication when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Octopost can publish supplied content to connected social networks.

Mitigation: Confirm the destination accounts and post content; use the approval queue when publication is not explicitly authorized.

Risk: The service requires an API key, and the hosted service implementation was not independently verified.

Mitigation: Protect the API key and review the service's behavior and account access before connecting it.

Risk: Octopost plans may incur service fees.

Mitigation: Review current pricing before use.

## Reference(s):

- [MCP Setup Documentation](https://octopost.ink/docs/mcp.md)
- [Agent API Documentation](https://octopost.ink/docs/agents.md)
- [Pricing](https://octopost.ink/pricing)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Social media post text, thread segments, and publishing or queue status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be adapted to connected networks' formats and character limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
