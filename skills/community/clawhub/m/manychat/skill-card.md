## Description: <br>
ManyChat API integration with managed authentication for managing subscribers, tags, custom fields, flows, and Facebook Messenger messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to ManyChat through Maton-managed authentication, inspect ManyChat page and subscriber data, manage tags and fields, and send approved messages or flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses MATON_API_KEY and Maton connection URLs to access a connected ManyChat account. <br>
Mitigation: Keep MATON_API_KEY and connection URLs private, scope them to the intended account, and rotate credentials if they are exposed. <br>
Risk: The skill can modify subscriber records, tags, custom fields, bot fields, and send messages or flows. <br>
Mitigation: Require explicit user approval before write or send operations and verify the account, recipient or subscriber IDs, message text, changed fields or tags, and consent basis. <br>
Risk: Multiple ManyChat connections can cause actions to target the wrong account. <br>
Mitigation: Use the Maton-Connection header when multiple connections exist and confirm the intended connection before approving account changes. <br>


## Reference(s): <br>
- [ClawHub ManyChat listing](https://clawhub.ai/byungkyu/manychat) <br>
- [ManyChat API Documentation](https://api.manychat.com/swagger) <br>
- [ManyChat API Key Generation Guide](https://help.manychat.com/hc/en-us/articles/14959510331420) <br>
- [ManyChat Dev Program](https://help.manychat.com/hc/en-us/articles/14281269835548) <br>
- [Maton](https://maton.ai) <br>
- [Related API Gateway skill](https://clawhub.ai/byungkyu/api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline HTTP paths, JSON examples, and Python or JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a configured ManyChat connection through Maton.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
