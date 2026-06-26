## Description: <br>
Create and manage articles on the PANews platform, including authenticated draft, submission, image upload, tag search, column application, revision, and content polishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[medz](https://clawhub.ai/user/medz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External PANews contributors use this skill to prepare, create, update, submit, and manage platform articles through authenticated creator workflows. It is also useful for reviewing article drafts, searching tags, uploading cover images, and applying for a publishing column. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a PANews browser session token for account-changing actions such as creating, submitting, updating, or deleting creator content. <br>
Mitigation: Use an environment variable or credential store for PA-User-Session, validate the session before write actions, and avoid pasting tokens into chat or command history. <br>
Risk: Broad implicit triggers may lead an agent into publishing workflows before the intended column, article, or submission state is clear. <br>
Mitigation: Confirm the target column, article, and whether the user intends to submit for review before create, update, submit, or delete actions. <br>
Risk: Delete operations are sensitive because evidence notes no CLI-level second confirmation. <br>
Mitigation: Require explicit user confirmation for the exact article before invoking delete operations. <br>


## Reference(s): <br>
- [Publish a New Article](references/workflow-publish.md) <br>
- [Manage My Articles](references/workflow-manage.md) <br>
- [Revise and Resubmit](references/workflow-revise.md) <br>
- [Apply for a Column](references/workflow-apply-column.md) <br>
- [Polish an Article](references/workflow-polish.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/medz/panews-creator) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and structured workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated API-backed publishing actions when the user provides a valid PANews session.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
