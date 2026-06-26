## Description: <br>
Manages Instagram Business and Creator accounts through the Instagram Graph API for publishing, media retrieval, insights, comment moderation, direct messages, and story monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media operators, marketers, and developers use this skill to manage connected Instagram Business or Creator accounts, inspect account and post performance, publish content, moderate comments, and handle existing direct-message conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OAuth connection for a connected Instagram Business or Creator account, giving ClawLink access to sensitive account capabilities. <br>
Mitigation: Review the ClawLink permissions before connecting an account and use only the intended Business or Creator account. <br>
Risk: The skill can publish posts, moderate comments, send direct messages, delete content, mark messages as read, and change messaging configuration. <br>
Mitigation: Require a clear preview and explicit user approval before any write, delete, DM, mark-read, or messaging-configuration action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/instagram-posts) <br>
- [Instagram Graph API overview](https://developers.facebook.com/docs/instagram-api) <br>
- [Instagram Media Publishing API](https://developers.facebook.com/docs/instagram-api/reference/ig-media) <br>
- [Instagram Insights API](https://developers.facebook.com/docs/instagram-api/reference/ig-user/insights) <br>
- [Instagram Messaging API](https://developers.facebook.com/docs/instagram-api/reference/ig-user/conversations) <br>
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated ClawLink calls that read Instagram account data or perform user-approved write actions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
