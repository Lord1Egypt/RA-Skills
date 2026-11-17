## Description:

HR Recruiting Tracker helps an agent parse PDF, DOCX, TXT, and Markdown resumes into local Markdown and JSON bundles, draft candidate profiles, upload reviewed candidate records to Tencent Docs SmartSheet, and initialize or maintain job tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[surqing](https://clawhub.ai/user/surqing)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and recruiting operations staff use this skill to convert resumes into local review bundles, prepare structured candidate records, upload confirmed drafts into Tencent Docs, and maintain job information tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles candidate PII and Tencent Docs access, and the security evidence flags under-scoped defaults that users should review before installation.

Mitigation: Install only in a controlled Tencent Docs environment, treat generated resume bundles and uploaded records as confidential candidate data, and keep dry-run previews redacted unless local troubleshooting requires sensitive output.

Risk: Tencent Docs writes can target an ambiguous same-name SmartSheet when multiple fixed-title sheets exist.

Mitigation: Prefer an explicit --file-id for production candidate and job tables, and use dry-run or remote probing before write operations.

Risk: External authorization and upload flows depend on mcporter and an installed tencent-docs skill.

Mitigation: Pin or verify mcporter and tencent-docs before use, and review the external auth script path before running authorization commands.

Risk: Fallback resume parsing may produce incomplete or uncertain candidate fields.

Mitigation: Keep fallback outputs marked for HR review and require --confirmed-reviewed before uploading records where extraction_report.json indicates review_required.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/surqing/skills/hr-recruiting-tracker)
- [Resume ingestion workflow](references/workflow_resume_ingestion.md)
- [Candidate upload workflow](references/workflow_candidate_upload.md)
- [Job management workflow](references/workflow_job_management.md)
- [Dependency contracts](references/dependency_contracts.md)
- [Recruiting table schema](assets/schemas/recruiting_tables.json)
- [Candidate draft schema](assets/schemas/candidate_draft.schema.json)
- [Tencent Docs MCP OpenAPI](https://docs.qq.com/openapi/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with shell commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local resume bundles, candidate draft JSON, extraction reports, Tencent Docs SmartSheet record metadata, and job table operation summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
