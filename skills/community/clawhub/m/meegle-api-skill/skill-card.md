## Description: <br>
Meegle API helps agents find and use Meegle Open API documentation for credentials, users, spaces, work items, settings, comments, views, and measurement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkycy](https://clawhub.ai/user/pkycy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide agents through authenticated Meegle Open API workflows, including project, work item, comment, user, settings, view, and measurement operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Meegle business-data read, write, update, and delete operations using plugin or user token permissions. <br>
Mitigation: Use least-privilege Meegle credentials, restrict plugin data scope, and install only where agent access to Meegle data is intended. <br>
Risk: Delete, replace, batch update, membership, workflow, template, and attachment operations can make disruptive changes. <br>
Mitigation: Require explicit user confirmation before those operations and scope each request to the intended space, work item type, and target records. <br>
Risk: Unscoped cross-space searches may expose more project data than the user intended. <br>
Mitigation: Prefer narrowly scoped project_key, user_key, and filter parameters, and avoid cross-space searches unless the user explicitly requests them. <br>


## Reference(s): <br>
- [Meegle API Skill on ClawHub](https://clawhub.ai/pkycy/meegle-api-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Meegle API Credentials Skill](artifact/meegle-api-credentials/SKILL.md) <br>
- [Meegle International API Host](https://project.larksuite.com) <br>
- [Meegle China API Host](https://project.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API request details, credential setup notes, and endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated API calls that read, write, update, or delete Meegle business data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
