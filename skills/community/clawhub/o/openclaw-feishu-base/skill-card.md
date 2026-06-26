## Description: <br>
Unified Feishu Base/Bitable management for OpenClaw. Use when you need to inspect Base schema, manage tables/fields, or query/create/update/delete records in Feishu Base/Bitable with existing Feishu credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systransform88](https://clawhub.ai/user/systransform88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to operate Feishu Base/Bitable resources through an agent, including schema inspection, table and field management, record reads and writes, and attachment handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Feishu credentials to read and modify Feishu Base business data. <br>
Mitigation: Use least-privileged Feishu credentials, specify the intended account, Base, and table for write actions, and inspect schema before changing records or fields. <br>
Risk: Destructive actions can delete records, fields, or tables when deletion is enabled. <br>
Mitigation: Keep allowDelete disabled unless deletion is required, and confirm exact record IDs, filters, table IDs, or field IDs before enabling destructive operations. <br>
Risk: Attachment actions can upload user-supplied local or remote files. <br>
Mitigation: Use attachment actions only with trusted file paths and URLs, and review the returned attachment metadata before writing it into records. <br>
Risk: Linked-record field creation and parallel field creation may fail because of Feishu-side limits or validation behavior. <br>
Mitigation: Treat linked-record field creation as best effort, create plain fields first when possible, and serialize field creation one-by-one. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/systransform88/openclaw-feishu-base) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON tool results and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Feishu Base records, schema details, table or field metadata, attachment metadata, or structured error details.] <br>

## Skill Version(s): <br>
0.2.7 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
