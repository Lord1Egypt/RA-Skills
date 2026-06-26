## Description: <br>
Access the Monday.com API through Maton Gateway to manage boards, items, columns, groups, users, and workspaces with GraphQL and managed OAuth authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to prepare Monday.com GraphQL calls through Maton Gateway, including OAuth connection setup and common board, item, column, group, user, and workspace operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, delete, and connection-removal actions against Monday.com data. <br>
Mitigation: Require explicit approval before mutations, verify target board, item, and connection IDs, and test read-only queries first. <br>
Risk: Use depends on Maton as the OAuth and API intermediary. <br>
Mitigation: Install only where Maton is trusted for the workflow and use the least-privileged Monday.com connection practical. <br>
Risk: The MATON_API_KEY grants access to Maton-mediated operations. <br>
Mitigation: Store the key in a secret manager or protected environment variable and avoid exposing it in prompts, logs, or shared files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/otman-ai/monday-matan) <br>
- [Maton](https://maton.ai) <br>
- [Maton Connection Management](https://ctrl.maton.ai) <br>
- [Maton Monday Gateway Endpoint](https://gateway.maton.ai/monday/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with cURL and GraphQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MATON_API_KEY and may require a Maton Monday OAuth connection ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
