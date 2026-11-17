## Description:

Navigate job hunting with application tracking, company research, and interview preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and job seekers use this skill to organize a job search, track applications, research companies, tailor application materials, and prepare for interviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect sensitive job-search details such as salary targets, employment history, contacts, and application status in local Markdown files.

Mitigation: Store only necessary details and protect the $HOME/job-search directory like other private documents.

Risk: Job market signals such as salary ranges, remote restrictions, company stability, and posting age can become stale.

Mitigation: Verify current compensation, location, and company information before applying or making decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/job-search)
- [Memory Setup - Job Search](artifact/memory-template.md)
- [Research Patterns - Job Search](artifact/research.md)
- [Interview Preparation - Job Search](artifact/interviews.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-directed local Markdown notes under $HOME/job-search; no external binaries are required.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
