## Description: <br>
Mixpost is a self-hosted social media management software that helps you schedule and manage your social media content across multiple platforms including Facebook, Twitter/X, Instagram, LinkedIn, Pinterest, TikTok, YouTube, Mastodon, Google Business Profile, Threads, Bluesky, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lao9s](https://clawhub.ai/user/lao9s) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure an agent for Mixpost workspace operations, including account lookup, media management, tag management, and social post drafting, scheduling, approval, publishing, and deletion through Mixpost API examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Mixpost access token can authorize workspace changes if exposed or over-permissioned. <br>
Mitigation: Use the least-privileged available token, keep it out of logs and shared files, and rotate it if exposure is suspected. <br>
Risk: Publishing, scheduling, approving, uploading, updating, or deleting content can affect public social media channels or workspace records. <br>
Mitigation: Require explicit user confirmation before any write, publish, schedule, approval, upload, update, or delete operation. <br>
Risk: Using the wrong workspace UUID can apply actions to an unintended Mixpost workspace. <br>
Mitigation: Verify the workspace UUID before running account, media, tag, or post operations. <br>


## Reference(s): <br>
- [Mixpost homepage](https://mixpost.app) <br>
- [ClawHub skill page](https://clawhub.ai/lao9s/mixpost) <br>
- [Publisher profile](https://clawhub.ai/user/lao9s) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MIXPOST_URL, MIXPOST_ACCESS_TOKEN, and MIXPOST_WORKSPACE_UUID environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
