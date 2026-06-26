## Description: <br>
Jobclaw Recruit helps recruiters publish, update, delete, and review job postings and matched candidates in the JobClaw matching system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imluyu](https://clawhub.ai/user/imluyu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Recruiters and hiring teams use this skill to collect job details, publish and manage postings, retrieve matched candidates, and prepare structured candidate analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can print account tokens and caches recruiter credentials locally. <br>
Mitigation: Treat printed tokens like passwords, avoid sharing transcripts containing tokens, and clear cached credentials when they are no longer needed. <br>
Risk: The skill can send recruiting data, job details, and candidate profile or resume data to an API endpoint, including a custom endpoint if one is provided. <br>
Mitigation: Use only the default or another trusted JobClaw endpoint, and do not pass a custom apiUrl unless the server is approved for the recruiting data involved. <br>
Risk: The skill can publish, update, and deactivate job postings. <br>
Mitigation: Review job details, job IDs, and requested actions before running write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imluyu/jobclaw-recruit) <br>
- [Publisher profile](https://clawhub.ai/user/imluyu) <br>
- [JobClaw API endpoint](https://api.jobclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can include recruiter job IDs, job posting details, candidate match summaries, and hiring recommendations in the agent conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
