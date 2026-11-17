## Description:

Manage and auto-post Facebook Page content through Meta Graph API, including text, photos, carousel posts, videos, Reels, Stories, scheduled posts, and comment management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to generate setup guidance, configuration, and Python CLI commands for publishing and managing Facebook Page content through Graph API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish, reschedule, delete, comment on, and reply to Facebook Page content using a powerful Page access token.

Mitigation: Manually confirm the target Page, post, comment, schedule, and command intent before running generated commands.

Risk: Page access tokens may grant long-lived publishing and management permissions.

Mitigation: Prefer environment variables or a secret manager, avoid never-expiring production tokens where possible, and rotate or revoke tokens if exposed.

Risk: A local fb_config.json file can expose Page tokens if it is committed or shared.

Mitigation: Keep fb_config.json out of source control and use least-privilege Page permissions for the required task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcbaivn/skills/mcbaivn-facebook-page-manager)
- [Access token setup guide](artifact/references/get-token.md)
- [Facebook Page Manager API reference](artifact/references/api-reference.md)
- [Meta for Developers](https://developers.facebook.com/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)
- [Graph API changelog](https://developers.facebook.com/docs/graph-api/changelog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, JSON, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that publish, schedule, reschedule, delete, comment on, or reply to Facebook Page content.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact clawhub.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
