## Description: <br>
Facebook Page Manager helps an agent manage Facebook Page content through the Graph API, including text, photo, carousel, video, Reels, Story, scheduled post, and comment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcbaivn](https://clawhub.ai/user/mcbaivn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content operators use this skill to prepare and run Facebook Page publishing and moderation commands with a Page access token. It is intended for agents that need to post media, schedule content, review scheduled posts, and manage page comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Facebook Page access tokens can authorize public content and engagement actions if exposed or over-scoped. <br>
Mitigation: Use least-privilege Page permissions, store tokens in environment variables or a secret manager, keep fb_config.json out of version control, and rotate or revoke any exposed token. <br>
Risk: The skill can publish, schedule, reschedule, delete, comment, or reply on behalf of a Facebook Page. <br>
Mitigation: Manually confirm post IDs, target media, schedules, delete actions, and reschedules before allowing the agent to run commands. <br>
Risk: Facebook Graph API limits and media rules can cause failed or delayed publishing workflows. <br>
Mitigation: Check the bundled API reference before posting media, especially carousel size, video processing time, Reels duration, Story limitations, and scheduled publishing windows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mcbaivn/mcbaivn-facebook-page-manager) <br>
- [Access token guide](references/get-token.md) <br>
- [API reference](references/api-reference.md) <br>
- [Meta Graph API changelog](https://developers.facebook.com/docs/graph-api/changelog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Facebook Graph API actions through the bundled Python CLI when the agent is given valid Page credentials and explicit task details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact clawhub.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
