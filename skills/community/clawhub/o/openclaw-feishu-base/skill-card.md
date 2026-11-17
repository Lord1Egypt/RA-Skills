## Description:

Unified Feishu Base/Bitable management for OpenClaw. Use when you need to inspect Base schema, manage tables/fields, or query/create/update/delete records in Feishu Base/Bitable with existing Feishu credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systransform88](https://clawhub.ai/user/systransform88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Feishu Base schema, discover bases and tables, and manage Feishu Base records, tables, fields, and attachments through the OpenClaw feishu_base tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Attachment actions can read local files or fetch arbitrary URLs and upload the contents to Feishu.

Mitigation: Use tightly scoped Feishu credentials and a runtime with filesystem and network limits; only pass local paths or URLs that the user explicitly selected.

Risk: Destructive actions can delete Feishu Base records, fields, or tables when deletion is enabled.

Mitigation: Keep allowDelete disabled by default and enable it only for a specific, confirmed deletion task with exact targets or filters.

Risk: Production use without dependency pinning or review may expose users to unreviewed dependency or runtime behavior.

Mitigation: Review before installation and pin dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/systransform88/skills/openclaw-feishu-base)
- [Artifact README](README.md)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, guidance]

**Output Format:** [Text containing JSON-serialized Feishu Base operation results or structured error details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses existing Feishu credentials; delete actions are blocked unless allowDelete is enabled.]

## Skill Version(s):

0.2.7 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
