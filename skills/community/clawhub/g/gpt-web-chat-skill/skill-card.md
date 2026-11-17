## Description:

Automates chatgpt.com through a browser session to send prompts, collect replies, check login state, and maintain ChatGPT sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lainxxx](https://clawhub.ai/user/lainxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they want an agent to route a prompt through an existing ChatGPT web session, retrieve the response, and surface structured handling guidance for login or connectivity failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and attachments are sent to chatgpt.com through a browser session.

Mitigation: Use only when that routing is intentional, and avoid sensitive content unless the browser session and account are approved for that data.

Risk: A logged-in browser session may be reused in the background.

Mitigation: Use a dedicated browser profile where possible and provide cleanup steps for stored session data after use.

Risk: The release evidence reports missing runtime scripts that the skill instructs the agent to execute.

Mitigation: Confirm the package includes or pins the expected runtime scripts before installation or execution.

## Reference(s):

- [Server-resolved GitHub source repository](https://github.com/lainXXX/gpt-web-chat-skill)
- [ClawHub skill page](https://clawhub.ai/lainxxx/skills/gpt-web-chat-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and structured JSON response handling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return ChatGPT replies or concise remediation guidance based on runtime status and error codes.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
