## Description: <br>
Personal network intelligence: remember people, find connections, and draft introductions while storing contacts locally as plain Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ilyabelikin](https://clawhub.ai/user/ilyabelikin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Peeps to maintain a local personal-network knowledge base, retrieve relationship context, find useful connections, and draft introductions from their own contact notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal relationship notes, private notes, contact details, and sensitive context are stored as local plaintext files. <br>
Mitigation: Keep the mind/peeps folder in a private workspace, avoid recording details you would not want resurfaced, and review files before sharing or committing the workspace. <br>
Risk: The skill instructs the agent to search the web for people by default and can optionally fetch images. <br>
Mitigation: Change the instructions or local config to require confirmation before external searches or image fetching, especially for private individuals. <br>
Risk: Automatic housekeeping can silently alter action history when actions.md is read. <br>
Mitigation: Review the retention rules before use and require confirmation before cleanup if preserving historical action records matters. <br>
Risk: Connections to related skills may move information across local datasets or suggest outbound dispatch through Haah. <br>
Mitigation: Require explicit user approval before cross-skill sharing or outbound dispatch, and verify what context will be included. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ilyabelikin/peeps) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ilyabelikin) <br>
- [Supported agents](https://github.com/vercel-labs/skills#supported-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown contact files, organization files, action queues, concise guidance, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores personal relationship records as local plaintext under mind/peeps; optional image fetching and proactive checks depend on local configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
