## Description: <br>
Creates Jira issues and searches assignable users on a configured Jira server using a user-provided bearer token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UlanziCom](https://clawhub.ai/user/UlanziCom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Jira workspace operators use this skill to create Jira issues from structured or natural-language inputs and to look up assignable users for a project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Jira bearer token to create issues and search users. <br>
Mitigation: Use a least-privilege token limited to the intended Jira site and projects. <br>
Risk: Issue creation can send incorrect project, assignee, priority, or due-date values to Jira. <br>
Mitigation: Review issue details before calling create_issue. <br>
Risk: Advertised batch creation and analytics behavior may not be fully supported by the provided artifact source. <br>
Mitigation: Do not rely on batch or analytics features unless their source is obtained and inspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/UlanziCom/jira-task-creator) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Usage guide](artifact/README.md) <br>
- [Package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Markdown, Configuration guidance] <br>
**Output Format:** [JSON-like dictionaries for Jira operation results, with Markdown guidance and reports where supported] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Jira base URL and bearer token configuration supplied by the user.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
