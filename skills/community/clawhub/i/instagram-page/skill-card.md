## Description: <br>
Instagram Page helps agents manage Instagram Business or Creator accounts by constructing Instagram Graph API calls for publishing photos, reels, stories, comments, account data, and insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seph1709](https://clawhub.ai/user/seph1709) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to manage an Instagram Business or Creator account linked to a Facebook Page. It guides credential setup and produces PowerShell or pwsh Graph API calls for publishing media, moderating comments, retrieving account data, and reading insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue delete requests for Instagram comments without an explicit confirmation safeguard in the artifact instructions. <br>
Mitigation: Require the agent to show the exact comment ID and text, get explicit confirmation before deletion, and prefer hiding or reviewing comments before permanent deletion. <br>
Risk: The skill uses long-lived Instagram credentials stored in a local credentials file, with IG_APP_SECRET needed only during setup. <br>
Mitigation: Restrict credentials file permissions, delete IG_APP_SECRET after setup, grant only required Meta permissions, refresh tokens before expiry, and rotate credentials immediately if the host is compromised. <br>
Risk: The skill can publish posts, reels, stories, and carousels to the connected Instagram account. <br>
Mitigation: Confirm the target account, media URLs, captions, and publish action before sending Graph API publish requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seph1709/instagram-page) <br>
- [Publisher profile](https://clawhub.ai/user/seph1709) <br>
- [Instagram Graph API v25.0 endpoint](https://graph.facebook.com/v25.0) <br>
- [Meta for Developers](https://developers.facebook.com/apps/) <br>
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline PowerShell and pwsh command snippets for Instagram Graph API requests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local credentials from ~/.config/instagram-page/credentials.json and calls graph.facebook.com only.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
