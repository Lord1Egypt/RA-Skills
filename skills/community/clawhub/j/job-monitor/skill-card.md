## Description: <br>
Analyze JD text and return structured match summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghong5233](https://clawhub.ai/user/wanghong5233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, candidates, and job-search assistants use this skill to analyze job description text for title, skills, match score, and gap analysis. It can also request a user-confirmed BOSS job search scan through a local service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job descriptions, search keywords, and related notes are sent to a local backend for processing. <br>
Mitigation: Use the skill only with a trusted local service on port 8010 and avoid submitting confidential hiring material or private annotations unless that processing is acceptable. <br>
Risk: The BOSS scan can interact with an external job-search workflow. <br>
Mitigation: Require user confirmation before any external platform action and do not submit applications automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghong5233/job-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown summary derived from JSON responses, with shell commands used for local API calls when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports API errors or invalid JSON and asks the user to retry or provide corrected job description text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
