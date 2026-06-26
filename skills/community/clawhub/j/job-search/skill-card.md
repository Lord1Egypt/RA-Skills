## Description: <br>
Navigate job hunting with application tracking, company research, and interview preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Job seekers and their agents use this skill to organize job-search memory, track applications, research target companies, tailor materials, and prepare for interviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill expects to store personal job-search notes, salary preferences, contacts, resumes, and cover letters in ~/job-search/. <br>
Mitigation: Keep the folder private, avoid storing secrets or employer-confidential information, and delete stale records when no longer needed. <br>
Risk: Salary, remote-work, and company-health information can become outdated or misleading. <br>
Mitigation: Verify current salary ranges, remote restrictions, company news, and review recency before using the guidance for decisions. <br>
Risk: Application materials can become generic or over-optimized if tailored mechanically. <br>
Mitigation: Use writing samples and user review to preserve the applicant's voice before sending resumes, cover letters, or outreach. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/job-search) <br>
- [Memory Setup](artifact/memory-template.md) <br>
- [Research Patterns](artifact/research.md) <br>
- [Interview Preparation](artifact/interviews.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with local file templates and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local job-search notes and materials under ~/job-search/; no required external binaries are declared.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
