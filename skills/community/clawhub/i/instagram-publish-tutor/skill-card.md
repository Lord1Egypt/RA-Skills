## Description:

Use when publishing images to Instagram via the Graph API from a Creator or Business account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, social media operators, and developers use this skill to set up Meta/Instagram API access and publish a public single-image Instagram post with a caption from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an Instagram access token that can publish posts for the user's account.

Mitigation: Keep the token out of git, store it in a local .env file or environment variable, and rotate it immediately if exposed.

Risk: Running the publish command can create a live Instagram post from the provided image URL and caption.

Mitigation: Review the exact image URL and caption before execution, and use dry-run mode when validating setup.

Risk: Meta must be able to fetch the image from the supplied URL.

Mitigation: Use a public HTTP or HTTPS image URL and confirm it opens from a logged-out browser before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mebusw/skills/instagram-publish-tutor)
- [Meta for Developers](https://developers.facebook.com/)
- [Meta app dashboard](https://developers.facebook.com/apps/)
- [Instagram Graph API endpoint](https://graph.instagram.com)
- [Instagram professional account settings](https://www.instagram.com/accounts/professional_account_settings/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-supplied public image URL, caption, Instagram access token, optional Instagram user ID, optional .env path, optional Graph API version, and optional dry-run mode.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
