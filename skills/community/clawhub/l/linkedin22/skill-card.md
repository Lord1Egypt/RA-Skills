## Description: <br>
Mael helps draft and publish formal LinkedIn status updates with relevant hashtags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muhammad194494-pixel](https://clawhub.ai/user/muhammad194494-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare LinkedIn posts, confirm the content with the user, and invoke a local publisher script to post or report failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local Python script outside the artifact to authenticate and publish to LinkedIn. <br>
Mitigation: Review ~/.openclaw/workspace/linkedin_post.py and its authentication behavior before installation or use. <br>
Risk: The skill can publish content under the user's public LinkedIn account. <br>
Mitigation: Confirm the final post text with the user before running the publishing command. <br>


## Reference(s): <br>
- [Mael on ClawHub](https://clawhub.ai/muhammad194494-pixel/linkedin22) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and concise posting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts should stay within LinkedIn's 3000 character limit and use a formal, professional tone.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
