## Description: <br>
Search and discover job positions using OpenJobs AI. Find jobs by title, company, location, seniority, industry, and more with structured filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenJobsAI](https://clawhub.ai/user/OpenJobsAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search the OpenJobs AI job database with structured filters such as title, company, location, seniority, employment type, industry, and posting date. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API-key setup instructions can expose the user's MIRA_KEY if it is printed, pasted into chat, or logged. <br>
Mitigation: Configure MIRA_KEY through a secure secret or environment mechanism, avoid printing it, and rotate the key if it has already been exposed. <br>
Risk: Job-search filters are sent to the OpenJobs AI API. <br>
Mitigation: Install only if you trust OpenJobs AI and review search filters before sending sensitive or personal information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OpenJobsAI/openjobs-jobs-search) <br>
- [OpenJobs AI publisher profile](https://clawhub.ai/user/OpenJobsAI) <br>
- [OpenJobs AI API version endpoint](https://mira-api.openjobs-ai.com/v1/version) <br>
- [OpenJobs AI platform](https://platform.openjobs-ai.com/) <br>
- [OpenJobs AI website](https://www.openjobs-ai.com/?utm_source=jobs_search_skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown job summaries with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 20 active, non-deleted jobs per search request and requires a MIRA_KEY credential.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
