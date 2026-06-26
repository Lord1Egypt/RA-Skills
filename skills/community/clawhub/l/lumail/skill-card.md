## Description: <br>
Manage the Lumail email marketing platform through CLI and TypeScript SDK guidance for subscriber, campaign, tag, event, transactional email, email verification, and V2 tool workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and email operations teams use this skill to work with Lumail account workflows, including subscriber management, campaign creation and sending, tag and event operations, transactional emails, email verification, and Lumail V2 tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill can guide actions that send campaigns or transactional emails and modify subscriber data when connected to a Lumail account. <br>
Mitigation: Require explicit approval before sending email, deleting or unsubscribing contacts, or running broad V2 tools. <br>
Risk: Lumail API tokens may grant access to account data and email-sending capabilities. <br>
Mitigation: Use the least-privileged API key available, protect saved tokens, and avoid raw token display unless necessary. <br>


## Reference(s): <br>
- [Lumail API base URL](https://lumail.io/api) <br>
- [ClawHub Lumail skill page](https://clawhub.ai/Melvynx/lumail) <br>
- [Melvynx publisher profile](https://clawhub.ai/user/Melvynx) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe CLI commands, SDK calls, JSON parameters for V2 tools, and account-safety review points.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
