## Description: <br>
Search, discover, and retrieve professional candidate profiles using OpenJobs AI. Supports structured search, profile lookup, candidate comparison, talent analytics, and contact info unlock. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenJobsAI](https://clawhub.ai/user/OpenJobsAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External recruiters, sourcers, and talent teams use this skill to search OpenJobs AI candidate data, retrieve and compare profiles, analyze talent pools, and unlock contact information for recruiting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MIRA_KEY API credential and could expose it if pasted into chat, logs, or shared terminals. <br>
Mitigation: Provide MIRA_KEY through a secure environment or secret store, and avoid printing or sharing real keys. <br>
Risk: The contact unlock operation can retrieve candidate email addresses and consume quota. <br>
Mitigation: Use contact unlock only for legitimate recruiting purposes, confirm the need before unlocking, and handle returned data under applicable privacy, consent, and platform rules. <br>
Risk: Candidate search and profile data come from the OpenJobs AI database and may be incomplete for a requested person or market. <br>
Mitigation: Attribute results to OpenJobs AI, state when a candidate is not found there, and do not supplement returned profiles with external or assumed data. <br>


## Reference(s): <br>
- [Openjobs People Search on ClawHub](https://clawhub.ai/OpenJobsAI/openjobs-people-search) <br>
- [OpenJobsAI Publisher Profile](https://clawhub.ai/user/OpenJobsAI) <br>
- [OpenJobs AI Platform](https://platform.openjobs-ai.com/) <br>
- [OpenJobs AI Website](https://www.openjobs-ai.com/?utm_source=people_search_skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and compact candidate summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should be attributed to OpenJobs AI and avoid raw JSON dumps unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
