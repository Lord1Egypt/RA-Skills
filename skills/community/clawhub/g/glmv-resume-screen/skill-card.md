## Description:

Screen and evaluate resumes against criteria using ZhiPu GLM-V multimodal model, reading multiple resume files, comparing them against user-defined screening criteria, and returning pass/fail analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring teams, and agents assisting hiring workflows use this skill to batch-screen resumes against stated criteria and compare candidate fit. It is intended for resume filtering, candidate comparison, and job-application evaluation workflows where sending resume contents to Zhipu's API is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume contents and screening criteria are sent to Zhipu's external API.

Mitigation: Use the skill only when organizational policy allows that transfer, and avoid uploading unnecessary personal data.

Risk: Saved Markdown or JSON outputs may contain sensitive applicant information.

Mitigation: Store outputs in approved locations, limit access, and delete them when they are no longer needed.

Risk: The ZHIPU_API_KEY is required for operation.

Mitigation: Store the key securely through the agent or shell environment and avoid committing it to files.

Risk: Local PDF processing depends on PyMuPDF.

Mitigation: Use an isolated environment with pinned dependencies when enabling local PDF processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaredforreal/skills/glmv-resume-screen)
- [GLM-V Resume Screen Homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-resume-screen)
- [Zhipu Chat Completions API Documentation](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown table by default, with optional Markdown or JSON file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPU_API_KEY; supports up to 50 remote resume files or up to 50 pages of local PDF input, and saved outputs may contain sensitive applicant information.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
