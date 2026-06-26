## Description: <br>
Describes product collection task HTTP APIs for creating, picking, updating, and batch-updating collection tasks, including task types, statuses, success payload rules, and browser-extension versus dashboard roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rowin90](https://clawhub.ai/user/rowin90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to integrate product data collection workers, task queues, browser-extension collectors, and dashboard workflows with product REST task endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authorization values can be exposed through chats, logs, screenshots, or source files. <br>
Mitigation: Keep PRODUCT_TASK_AUTH in scoped environment or host configuration and avoid printing, sharing, or committing it. <br>
Risk: Create, update, and batch-update requests can change remote task records and product data. <br>
Mitigation: Verify the target environment, filters, taskVersionName, taskType, and status before issuing write operations. <br>
Risk: Connecting to an untrusted product-task API could expose credentials or alter the wrong dataset. <br>
Mitigation: Install only when the product-task API is trusted and PRODUCT_DATA_COLLECTION_BASE_URL points to the intended environment. <br>


## Reference(s): <br>
- [Product Data Collection on ClawHub](https://clawhub.ai/rowin90/product-data-collection) <br>
- [rowin90 publisher profile](https://clawhub.ai/user/rowin90) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with endpoint tables, JSON body descriptions, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRODUCT_TASK_AUTH and PRODUCT_DATA_COLLECTION_BASE_URL to be supplied from environment or host configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
