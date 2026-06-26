## Description: <br>
Connects agents to 100+ third-party APIs through Maton.ai managed OAuth, including Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjcloud](https://clawhub.ai/user/hjcloud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to make authenticated API calls to external business services after users authorize the relevant Maton connections. It is suited for workflows that need direct reads or writes against connected SaaS accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad live API gateway access can let an agent read, create, update, send, or delete data across connected services. <br>
Mitigation: Connect only least-privilege accounts, specify exact service connections where possible, and require explicit confirmation before destructive, public, billing, messaging, admin, webhook, crawl, or document-processing actions. <br>
Risk: MATON_API_KEY is a sensitive credential for the Maton gateway. <br>
Mitigation: Store the key in a secret manager or protected environment variable, avoid logging it, rotate it if exposed, and limit use to trusted runtimes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hjcloud/jeftest) <br>
- [Maton homepage](https://maton.ai) <br>
- [API Gateway skill documentation](artifact/SKILL.md) <br>
- [Provider routing guides](artifact/references/) <br>
- [License](artifact/LICENSE.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with API request examples and inline shell or code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized third-party service connections.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
