## Description:

Helps agents manage LinkedIn organization posts, comments, reactions, and analytics through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Community managers and teams use this skill to review LinkedIn organization activity, publish or moderate posts and comments with approval, and retrieve follower, page, and post statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting LinkedIn through Maton grants an intermediary access to the authorized account.

Mitigation: Confirm trust in Maton before connecting, grant only needed LinkedIn permissions, and remove unused connections.

Risk: Posts, comments, reactions, and deletions can affect the wrong organization or publish unintended content.

Mitigation: Verify the connection, organization, and exact change; obtain explicit user approval before every write.

Risk: Hosted functions, triggers, and destinations can keep acting or forwarding events after setup.

Mitigation: Approve each automation and destination separately, review where events go, and remove them when no longer needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/byungkyu/skills/linkedin-community)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [LinkedIn Community Management overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Text or Markdown with CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account access requires a Maton connection; changes require user approval.]

## Skill Version(s):

1.2.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
