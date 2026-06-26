## Description: <br>
Nex.ai shares real-time organizational context with an AI agent by letting it query a context graph, manage records, and receive live insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[najmuzzaman-mohammad](https://clawhub.ai/user/najmuzzaman-mohammad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers using OpenClaw use this skill to connect an agent to a Nex workspace, query organizational context about contacts and companies, process conversations into records and insights, and manage CRM-like records through the Nex developer API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send sensitive conversation content and CRM data to Nex. <br>
Mitigation: Install only if Nex is approved for the data involved, redact secrets and regulated data before ingestion, and avoid uploading sensitive transcripts without review. <br>
Risk: The skill can change or delete CRM data through write scopes and write-capable API methods. <br>
Mitigation: Use a dedicated least-privilege API key, prefer read-only scopes unless writes are required, and require manual confirmation before delete, schema change, bulk update, or transcript upload actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/najmuzzaman-mohammad/nex) <br>
- [Nex Skill Homepage](https://github.com/nex-crm/nex-as-a-skill) <br>
- [Nex Developer Settings](https://app.nex.ai/settings/developer) <br>
- [Nex API Documentation](https://docs.nex.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Nex API responses that may require jq filtering for large JSON payloads.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
