## Description: <br>
Notion API for creating and managing pages, databases, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to configure Notion API access and perform common page, data source, and block operations with curl request examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Notion API key can grant access to shared workspace content if it is exposed or reused broadly. <br>
Mitigation: Use a dedicated integration, store the API key with restrictive file permissions, and share only the specific pages or databases required. <br>
Risk: POST and PATCH examples can create or modify Notion pages, data sources, and blocks in a real workspace. <br>
Mitigation: Review write requests before running them and test against limited-scope pages or databases first. <br>


## Reference(s): <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [Notion integrations](https://notion.so/my-integrations) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/notion) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Notion API headers, endpoint patterns, credential setup steps, and request payload examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
