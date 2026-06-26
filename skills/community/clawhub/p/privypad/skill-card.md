## Description: <br>
Interact with the PrivyPad.com API to read, create, update, delete, and organize encrypted notes and groups on behalf of a user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIDidMyHomework](https://clawhub.ai/user/AIDidMyHomework) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent work with PrivyPad notes and groups through the PrivyPad API when the user supplies an API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can access private PrivyPad notes when the user provides a pp_ token. <br>
Mitigation: Treat the token like a password, provide it only for intended tasks, and ask the agent to fetch the minimum notes needed. <br>
Risk: An agent can update, delete, or permanently delete notes through the API. <br>
Mitigation: Require clear user confirmation before updates or deletes, especially permanent deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIDidMyHomework/privypad) <br>
- [PrivyPad API base URL](https://www.privypad.com/api/v1/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with API request examples and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JavaScript fetch or Python httpx examples for PrivyPad API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
