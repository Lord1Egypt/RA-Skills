## Description: <br>
Generate AI images/videos and post to 30+ social media platforms with Postzee. Use when the user wants to create AI media, generate images or videos, optimize prompts, create HeyGen avatar videos, or schedule social media posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasfreitas](https://clawhub.ai/user/lucasfreitas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to generate AI images or videos, optimize creative prompts, create avatar videos, and draft, schedule, or publish posts through connected Postzee channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live posts to connected social accounts without consistently requiring final confirmation. <br>
Mitigation: Require the agent to show the exact content, media, target channels, timing, and credit cost before any live publish; use draft mode for uncertain posts. <br>
Risk: The skill requires credentials and access to connected Postzee social accounts. <br>
Mitigation: Configure credentials through a secret or MCP configuration mechanism rather than pasting raw keys into normal chat. <br>


## Reference(s): <br>
- [Postzee documentation](https://docs.postzee.app) <br>
- [Postzee app](https://postzee.app) <br>
- [ClawHub release page](https://clawhub.ai/lucasfreitas/postzee) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or schedule social media posts and generated media through Postzee MCP tools.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
