## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[7revor](https://clawhub.ai/user/7revor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation builders use this skill to configure Notion API access and prepare curl-based requests for reading, creating, querying, and updating pages, data sources, and blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion integration key can grant access to shared pages and data sources. <br>
Mitigation: Scope the integration to only the pages or data sources needed and protect the local API key file. <br>
Risk: Create and update requests can change Notion workspace content. <br>
Mitigation: Review generated commands and request payloads before executing them. <br>
Risk: The API key could be exposed if copied into shared files, logs, or commits. <br>
Mitigation: Keep the key out of source control and shared transcripts, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Notion Developers](https://developers.notion.com) <br>
- [Notion Integrations](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Notion integration key and workspace permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
