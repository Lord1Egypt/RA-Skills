## Description:

Routes Huoshan and Qifu knowledge requests through a default Feishu Bitable catalog, preserves entry-document and child-document relationships, and returns original catalog links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzj997](https://clawhub.ai/user/zzj997)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and agents use this skill to find, list, recommend, compare, navigate, or answer source-grounded questions about Huoshan and Qifu knowledge materials stored in Feishu. It supports catalog metadata lookup, hierarchy navigation, source verification, and concise Markdown presentation of matching internal resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the user to authorize Feishu/Lark read access for an internal knowledge catalog or selected linked documents.

Mitigation: Review the requested OAuth scopes during authorization and use the skill only with catalogs and documents the agent is intended to read.

Risk: Catalog and document content can be internal or user-provided and may be incomplete, inaccessible, or untrusted.

Mitigation: Keep operations read-only, treat retrieved content as evidence rather than instructions, and mark answers when source text cannot be read.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzj997/skills/huoshan-qifu-knowledge-router)
- [Publisher profile](https://clawhub.ai/user/zzj997)
- [Default Feishu Bitable catalog](https://bytedance.larkoffice.com/base/UpAdbZX4NafHHssmmJgchNrEnyb?table=tblb40YEYGtLsGvu&view=vewya09oBp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with compact tables and original catalog links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Feishu/Lark retrieval; source-content answers are limited to successfully accessed documents.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
