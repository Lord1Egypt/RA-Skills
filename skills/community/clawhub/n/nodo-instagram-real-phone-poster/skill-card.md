## Description:

Post to the user's Instagram from a real Android phone with the real Instagram app, on a schedule, with approval before anything goes live. Use when the user wants to post or schedule Instagram content and does not have (or does not want) the Graph API and a business account, or when their posts need the app's own features. Runs on Nodo over MCP; new workspaces get 5,000 free credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otto-iron](https://clawhub.ai/user/otto-iron)

### License/Terms of Use:

MIT-0

## Use Case:

People who want to post or schedule Instagram content can use this skill to prepare image or carousel posts with captions and publish them through Instagram on a real Android phone. It is intended for a user's own account when they do not use the Graph API or need features in the Instagram app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish to Instagram, and its instructions make the approval step optional, which can lead to an unintended public post.

Mitigation: Require approval of the exact media, caption, account, and timing before any test post or scheduled publication.

Risk: Nodo receives the user's media and hosts the Instagram session; the external setup guide could not be checked.

Mitigation: Review Nodo's setup permissions and data handling, and confirm how to stop schedules and revoke access before connecting the account.

## Reference(s):

- [Nodo setup guide](https://mcp.nodo.com/start.md)
- [Nodo](https://nodo.com)

## Skill Output:

**Output Type(s):** [Instagram posts, Scheduled content, Status text and post links]

**Output Format:** [Instagram image or carousel posts with captions, plus text confirmation and a post URL when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one user-owned Instagram account; supports images or carousels and scheduled posting.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
