## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landercortazarromero](https://clawhub.ai/user/landercortazarromero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to work with the Notion API for page, data source, and block operations, including searching, querying, creating, and updating workspace content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion API key stored locally could be exposed and used to access content shared with the integration. <br>
Mitigation: Use a least-privilege Notion integration, store the key in an OS secret store when possible, restrict any local key file with permissions such as chmod 600, and rotate the key if exposed. <br>
Risk: Sharing broad Notion pages or databases with the integration can give the agent more workspace access than intended. <br>
Mitigation: Share only the pages or databases needed for the task and review integration access before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/landercortazarromero/korta-notion) <br>
- [Notion Developers](https://developers.notion.com) <br>
- [Notion Integrations](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with cURL command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Notion API key and pages or databases shared with the integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
