## Description: <br>
Turn your OpenClaw into an autonomous social media manager using Post Bridge API for scheduling, posting, and managing content across TikTok, Instagram Reels, YouTube Shorts, Twitter/X, LinkedIn, Pinterest, Facebook, Threads, and Bluesky. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackfriks](https://clawhub.ai/user/jackfriks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, marketers, and social media operators use this skill to help an agent upload media, create posts, schedule or queue publishing, manage scheduled posts, and check posting results through Post Bridge. It is intended for workflows where the user has connected social accounts and wants agent-assisted publishing with human approval controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to post, schedule, edit, sync analytics for, or delete content through connected Post Bridge social accounts. <br>
Mitigation: Require explicit user approval after the agent shows the target accounts, caption, media, timing, and action type before any posting, scheduling, editing, analytics sync, or deletion. <br>
Risk: The Post Bridge API key can grant access to connected social accounts if exposed. <br>
Mitigation: Keep POST_BRIDGE_API_KEY out of shared logs and rotate it immediately if it is exposed. <br>
Risk: Multi-platform posting can send content to unintended accounts or apply the wrong platform-specific settings. <br>
Mitigation: Review the selected account IDs and platform_configurations for each target platform before creating or updating a post. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackfriks/post-bridge-social-manager) <br>
- [Post Bridge](https://post-bridge.com) <br>
- [Post Bridge API reference](https://api.post-bridge.com/reference) <br>
- [Post Bridge API base URL](https://api.post-bridge.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline HTTP examples, shell commands, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request plans, captions, scheduling details, account selections, media upload steps, and status-checking instructions.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
