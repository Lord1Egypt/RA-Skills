## Description:

聘才猫（Pincaimao）简历诊断 helps an agent upload a resume, call the Pincaimao Resume Diagnosis Assistant API, and summarize how the resume matches a job description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External hiring teams, recruiters, and agents use this skill to evaluate a candidate resume against a job description through Pincaimao's hosted resume diagnosis API. It is intended for workflows where the user can provide a resume file, a job description, and an approved Pincaimao API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that the skill requires installing and loading an unpinned helper skill before handling resumes, job descriptions, and an API key.

Mitigation: Before use, verify that pincaimao-basic comes from the expected publisher and version.

Risk: Candidate resumes, job descriptions, and API credentials are involved in external processing by Pincaimao.

Mitigation: Install only if you trust Pincaimao with this data and avoid sending confidential or regulated hiring data unless your organization has approved the processing and storage.

Risk: Uploaded resume files are stored on Pincaimao COS and returned cos_key paths are sensitive.

Mitigation: Treat cos_key values as sensitive and avoid sharing raw upload responses outside the authorized workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pincaimao/skills/pincaimao-resume-diagnosis)
- [Pincaimao homepage](https://www.pincaimao.com)
- [Pincaimao API endpoint](https://api.pincaimao.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional raw API output in code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can present a human-readable summary by default or raw API answer content when requested.]

## Skill Version(s):

1.0.1 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
