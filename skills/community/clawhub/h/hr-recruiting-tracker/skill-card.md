## Description: <br>
HR Recruiting Tracker helps agents turn local resumes into Markdown and JSON resume bundles, prepare candidate drafts, upload reviewed records to Tencent Docs smart sheets, and maintain recruiting job tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surqing](https://clawhub.ai/user/surqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams and recruiting operations agents use this skill to ingest confidential resumes, prepare reviewable candidate records, upload confirmed records to Tencent Docs, and maintain job tracking tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume bundles and candidate drafts can contain confidential recruiting data. <br>
Mitigation: Use the skill only in approved environments and keep generated bundles in private storage. <br>
Risk: Candidate records may be incomplete or low-confidence when fallback parsing is used. <br>
Mitigation: Review candidate drafts before upload and require explicit confirmation for review-required records. <br>
Risk: Uploading to the wrong Tencent Docs smart sheet could expose or misplace recruiting records. <br>
Mitigation: Run dry-run first and prefer an explicit Tencent Docs file_id in production. <br>
Risk: External Tencent Docs and mcporter dependencies affect upload and job-management workflows. <br>
Mitigation: Install mcporter and tencent-docs only from trusted sources and verify authorization before remote operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/surqing/hr-recruiting-tracker) <br>
- [Resume ingestion workflow](references/workflow_resume_ingestion.md) <br>
- [Candidate upload workflow](references/workflow_candidate_upload.md) <br>
- [Job management workflow](references/workflow_job_management.md) <br>
- [Dependency contracts](references/dependency_contracts.md) <br>
- [Tencent Docs MCP API](https://docs.qq.com/openapi/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, Markdown, and local file bundles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles confidential recruiting data; Tencent Docs upload workflows require authorized external dependencies and HR confirmation for review-required records.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
