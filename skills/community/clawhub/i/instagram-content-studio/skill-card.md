## Description:

Manage an Instagram account by viewing profile and post data, publishing images or videos, and reading or writing comments through Instagram and Facebook Graph API scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uyeong](https://clawhub.ai/user/uyeong)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent manage Instagram publishing and engagement workflows from scripted commands. It is suited for profile lookup, post listing, media publishing, and comment operations after the user configures Meta credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token refresh commands can print refreshed access tokens and write tokens to a plaintext .env file.

Mitigation: Use a dedicated Meta app with minimal permissions, keep .env files private and out of version control, and avoid running refresh commands in environments where stdout is logged.

Risk: Posting local media temporarily exposes selected files through a public Cloudflare tunnel.

Mitigation: Use hosted media URLs for sensitive or large files, and only provide local files that are acceptable to expose briefly during upload.

Risk: Publishing posts, comments, or replies can create public account activity.

Mitigation: Review captions, comment text, target media IDs, and account context before allowing the command to run.

## Reference(s):

- [Instagram skill on ClawHub](https://clawhub.ai/uyeong/skills/instagram-content-studio)
- [Meta for Developers](https://developers.facebook.com/)
- [Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/)
- [Agent Skills](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON command output with concise natural-language guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may publish media or comments to Instagram and may update local credential files during token refresh.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
