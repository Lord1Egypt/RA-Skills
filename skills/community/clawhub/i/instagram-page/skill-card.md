## Description:

Instagram Business manager: post photos, reels, stories, and get insights using Instagram Graph API calls through PowerShell or pwsh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seph1709](https://clawhub.ai/user/seph1709)

### License/Terms of Use:


## Use Case:

External users and social media operators use this skill to prepare and run Instagram Business or Creator account API calls for publishing media, managing comments, and retrieving account or media insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local credentials file contains a long-lived Instagram access token and may temporarily contain a Meta app secret during setup.

Mitigation: Store only IG_ACCESS_TOKEN and IG_USER_ID after setup, delete IG_APP_SECRET immediately, restrict credentials.json to the local user account, and rotate the token if the file may have been exposed.

Risk: Generated publishing and comment-management calls can change public Instagram content when the token has those permissions.

Mitigation: Grant only the Meta permissions needed for the intended task and review each generated API call before execution.

Risk: A stale or exposed access token can cause failed requests or unauthorized account access.

Mitigation: Refresh the token before its 60-day expiry window and rotate it immediately if the host or credential file may be compromised.

## Reference(s):

- [ClawHub Instagram Page release](https://clawhub.ai/seph1709/skills/instagram-page)
- [Instagram Graph API v25.0 base URL](https://graph.facebook.com/v25.0)
- [Meta for Developers Apps](https://developers.facebook.com/apps/)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces inline Instagram Graph API request patterns and credential setup guidance; it does not include standalone scripts.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
