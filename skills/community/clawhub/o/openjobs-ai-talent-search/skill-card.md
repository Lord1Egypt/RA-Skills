## Description: <br>
Search and discover academic scholars using OpenJobs AI by name, affiliation, research areas, citations, h-index, publications, and other structured filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OpenJobsAI](https://clawhub.ai/user/OpenJobsAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, recruiters, and analysts use this skill to search the OpenJobs AI scholar database for academic talent by institution, field, publication record, citations, h-index, education, and location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance can expose a live Mira API key if the key is pasted into chat, echoed, or shared in terminal output. <br>
Mitigation: Configure MIRA_KEY through a secure environment or secret manager, avoid printing it, and review the skill before installation. <br>
Risk: Scholar searches send query criteria to OpenJobs AI. <br>
Mitigation: Use the skill only for searches you are comfortable sending to OpenJobs AI and present returned data as OpenJobs AI data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OpenJobsAI/openjobs-ai-talent-search) <br>
- [OpenJobs AI publisher profile](https://clawhub.ai/user/OpenJobsAI) <br>
- [OpenJobs AI](https://www.openjobs-ai.com/?utm_source=scholar_search_skill) <br>
- [OpenJobs AI platform](https://platform.openjobs-ai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and concise scholar result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results should be attributed to OpenJobs AI and kept compact; raw JSON and large tables are discouraged.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
