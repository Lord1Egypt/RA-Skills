## Description: <br>
Helps an agent manage Meo Mai Moi pet-owner tasks through the documented API, including pet profiles, health records, helper profiles, placement workflows, authentication, and safe automation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[troioi-vn](https://clawhub.ai/user/troioi-vn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet owners and their agents use this skill to safely access and update Meo Mai Moi pet records through documented API endpoints. It supports read-first workflows for profiles, weights, vaccinations, medical records, microchips, helper profiles, and placement lifecycle questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive Meo Mai Moi API token to access user account and pet data. <br>
Mitigation: Store the token in a local secret or environment file, avoid exposing it in chats, logs, commits, or generated docs, and verify the Meo Mai Moi site and token page before use. <br>
Risk: Delete operations, ownership transfers, placement changes, and other pet-record writes can have important real-world consequences. <br>
Mitigation: Use read-first workflows, confirm destructive or state-changing actions, call only documented endpoints, and re-read resources after writes to verify the result. <br>


## Reference(s): <br>
- [Meo Mai Moi API Reference](references/api.md) <br>
- [Meo Mai Moi Domain Model](references/domain-model.md) <br>
- [Meo Mai Moi Workflows](references/workflows.md) <br>
- [Install and Example Prompts](references/examples.md) <br>
- [Meo Mai Moi App](https://meo-mai-moi.com) <br>
- [API Token Page](https://meo-mai-moi.com/developer) <br>
- [Meo Mai Moi Docs](https://meo-mai-moi.com/docs) <br>
- [API Integration Guide](https://meo-mai-moi.com/docs/api-integration.html) <br>
- [Project Page](https://project.meo-mai-moi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint names, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Meo Mai Moi personal access token for live account access.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
