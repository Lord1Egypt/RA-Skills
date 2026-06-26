## Description: <br>
LinkHut helps users manage LinkHut bookmarks from chat through ClawLink OAuth, including saving, organizing, searching, updating, and deleting bookmarks with tags, notes, and privacy settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect LinkHut through ClawLink OAuth and manage bookmark collections from an agent chat workflow. It supports saving bookmarks, searching by tag, listing tags, updating metadata, and deleting bookmarks by exact URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting LinkHut through the third-party ClawLink OAuth service. <br>
Mitigation: Install only if the user accepts that OAuth connection path and reconnect through the dashboard if authorization expires. <br>
Risk: Bookmark write operations can add or change saved bookmark metadata. <br>
Mitigation: Review write requests before execution, especially URL, tags, notes, privacy, and reading-list settings. <br>
Risk: Bookmark deletion is high impact and irreversible. <br>
Mitigation: Confirm the exact bookmark URL before calling the delete tool. <br>


## Reference(s): <br>
- [ClawHub LinkHut Skill Page](https://clawhub.ai/hith3sh/linkhut) <br>
- [LinkHut](https://linkhut.org/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=linkhut) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ClawLink tool-call examples for LinkHut bookmark and tag operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
