## Description: <br>
jef1test helps agents call 100+ external service APIs through Maton.ai managed OAuth connections and a passthrough API gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjcloud](https://clawhub.ai/user/hjcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent query or manage connected third-party services such as Google Workspace, Microsoft 365, Slack, GitHub, Notion, Airtable, HubSpot, and similar APIs. The skill is intended for accounts and services that the user has explicitly authorized through Maton connections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad write-capable access across connected third-party accounts. <br>
Mitigation: Connect only needed services with least-privilege scopes and require explicit confirmation before posting, editing, deleting, sending messages, changing business records, or accessing sensitive data. <br>
Risk: MATON_API_KEY can act like a delegated account key for Maton API access. <br>
Mitigation: Protect MATON_API_KEY as a sensitive credential and install the skill only when agent access to third-party APIs through Maton is intended. <br>
Risk: When multiple connections exist for the same service, the agent could act on the wrong account. <br>
Mitigation: Specify the intended connection whenever possible before making service API calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjcloud/jef1test) <br>
- [Maton homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized Maton service connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
