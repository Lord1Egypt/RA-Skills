## Description: <br>
Liepin Assistant connects an agent to Liepin MCP so users can search jobs, view job descriptions, submit applications, and manage resume information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyapersonal](https://clawhub.ai/user/wangyapersonal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers use this skill to connect an agent to their Liepin account, search for roles, inspect job descriptions, update resume details, and submit applications after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a long-lived Liepin account token and can access account and resume data. <br>
Mitigation: Prefer the LIEPIN_TOKEN environment variable, avoid sharing tokens in chats, and revoke or clear the token when finished. <br>
Risk: The skill can update resume information or submit job applications through the connected Liepin account. <br>
Mitigation: Preview every resume change and job application, and proceed only after explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangyapersonal/liepin-assistant) <br>
- [Liepin MCP API reference](references/api.md) <br>
- [Liepin MCP credential page](https://www.liepin.com/mcp/server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Liepin token and is subject to Liepin token lifetime and rate limits.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
