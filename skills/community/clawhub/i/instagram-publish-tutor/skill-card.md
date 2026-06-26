## Description: <br>
Use when publishing images to Instagram via the Graph API from a Creator or Business account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and social media operators use this skill to configure Instagram Graph API credentials and publish a single public image URL with a caption to a Creator or Business account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The access token can publish to the user's Instagram account if exposed or misused. <br>
Mitigation: Keep the token out of git, store it in a local .env file, use --dry-run before final publishing, and revoke the token immediately if it leaks. <br>
Risk: Publishing requires a public image URL that Meta can fetch, which can fail if the URL is private or unavailable. <br>
Mitigation: Use only intended public image URLs and verify the URL in a logged-out browser before publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mebusw/instagram-publish-tutor) <br>
- [Meta for Developers](https://developers.facebook.com/) <br>
- [Meta Developer Apps](https://developers.facebook.com/apps/) <br>
- [Instagram professional account settings](https://www.instagram.com/accounts/professional_account_settings/) <br>
- [Instagram Graph API endpoint](https://graph.instagram.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command-line examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Meta access token, an Instagram Creator or Business account, and a publicly reachable image URL; supports dry-run validation before final publish.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
