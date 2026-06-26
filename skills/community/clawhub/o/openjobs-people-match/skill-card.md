## Description: <br>
Evaluate candidate-job fit using OpenJobs AI. Grade a single CV against a job description or bulk-grade multiple candidates and rank them by match score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenJobsAI](https://clawhub.ai/user/OpenJobsAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and recruiting workflow agents use this skill to score candidate CVs or LinkedIn profiles against a specific job description and present ranked match results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate CVs, LinkedIn URLs, job descriptions, and the Mira API key are sensitive. <br>
Mitigation: Use the skill only when authorized to submit that data to OpenJobs AI/Mira, minimize unnecessary personal data, and avoid printing the full API key. <br>
Risk: Fit scores and descriptions are AI-generated match assessments, not absolute candidate quality determinations. <br>
Mitigation: Present scores as job-specific match signals and keep human review in the hiring decision process. <br>
Risk: The skill depends on a third-party API and user-provided API credentials. <br>
Mitigation: Install and run it only when the user trusts OpenJobs AI/Mira and has a valid Mira API key available in the environment. <br>


## Reference(s): <br>
- [Openjobs People Match on ClawHub](https://clawhub.ai/OpenJobsAI/openjobs-people-match) <br>
- [OpenJobs AI](https://www.openjobs-ai.com/?utm_source=people_match_skill) <br>
- [OpenJobs AI platform signup](https://platform.openjobs-ai.com/) <br>
- [OpenJobs AI version endpoint](https://mira-api.openjobs-ai.com/v1/version) <br>
- [OpenJobs AI people grade endpoint](https://mira-api.openjobs-ai.com/v1/people-grade) <br>
- [OpenJobs AI people bulk grade endpoint](https://mira-api.openjobs-ai.com/v1/people-bulk-grade) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results include match scores from 0 to 100, concise match descriptions, ranked bulk output, and OpenJobs AI attribution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
