## Description: <br>
Secure email gateway for AI agents - human-in-the-loop approval for reading and sending emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[casperaiassist](https://clawhub.ai/user/casperaiassist) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use PostWall to let agents read only human-approved emails, submit outbound email drafts for approval, and track draft status through the PostWall CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The PostWall CLI can access email content approved for agent use. <br>
Mitigation: Install only when comfortable granting CLI access to the intended mailbox or account, and confirm which account PostWall connects to before use. <br>
Risk: Outbound email drafts may contain incorrect recipients or content before human approval. <br>
Mitigation: Review drafts in PostWall before approving send actions, and use the draft update flow for requested changes. <br>
Risk: The skill requires a PostWall API key for authentication. <br>
Mitigation: Use the expected PostWall source for installation and keep POSTWALL_API_KEY scoped to the intended environment. <br>


## Reference(s): <br>
- [PostWall homepage](https://postwallapp.com) <br>
- [PostWall repository](https://github.com/postwallapp/postwall) <br>
- [PostWall ClawHub release](https://clawhub.ai/casperaiassist/postwall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [PostWall CLI commands can return structured JSON when called with --json.] <br>

## Skill Version(s): <br>
1.7.0 (source: SKILL.md frontmatter metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
