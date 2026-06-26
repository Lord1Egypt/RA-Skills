## Description: <br>
聘才猫 - 在线面试 Use when calling Pincaimao Online Interview API to conduct a multi-turn AI interview session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External recruiters, hiring teams, and their agents use this skill to run Pincaimao online interview sessions from a job description and resume, including text or video interview rounds, custom questions, and optional report callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends resumes, job descriptions, candidate answers, and interview reports to the Pincaimao service. <br>
Mitigation: Share only data needed for the interview workflow and confirm that use of the Pincaimao service is acceptable for the candidate and organization. <br>
Risk: Sensitive interview reports can be sent to a user-provided callback URL. <br>
Mitigation: Use callback URLs only for domains the user controls or explicitly trusts, and avoid callback delivery when it is not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-online-interview) <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao API endpoint](https://api.pincaimao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and optional raw API response excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the PCM_ONLINE_INTERVIEW_KEY environment variable and may summarize or relay interview responses returned by the Pincaimao API.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
