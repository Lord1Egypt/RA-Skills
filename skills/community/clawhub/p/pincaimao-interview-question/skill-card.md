## Description: <br>
聘才猫（Pincaimao）面试出题大师 helps an agent call Pincaimao's Interview Question Master API to generate interview questions from a job description and candidate resume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and their agents use this skill to send a job description and candidate resume to Pincaimao and receive interview questions, with optional analysis or raw API output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate resumes and job descriptions may contain personal or confidential hiring information and are sent to Pincaimao for processing. <br>
Mitigation: Install and use the skill only when the user or organization is authorized to send that data to Pincaimao. <br>
Risk: The PCM_INTERVIEW_QUESTIONS_KEY and returned cos_key values are sensitive access materials. <br>
Mitigation: Keep the API key in environment variables, do not hardcode it, and avoid exposing cos_key values in shared logs or transcripts. <br>
Risk: The skill depends on a separate pincaimao-basic skill for shared upload, authentication, response, and streaming behavior. <br>
Mitigation: Review pincaimao-basic before allowing an agent to install or load it in the same environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-interview-question) <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao platform API](https://api.pincaimao.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown text with bash examples and optional raw API response excerpts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PCM_INTERVIEW_QUESTIONS_KEY and can return either a readable summary or raw answer content from the Pincaimao API.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
