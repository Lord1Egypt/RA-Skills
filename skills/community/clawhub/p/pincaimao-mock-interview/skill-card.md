## Description: <br>
聘才猫（Pincaimao）模拟面试 guides an agent through the Pincaimao Mock Interview API to run multi-turn text or video mock interviews with configurable questions, roles, and reference-answer options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect job and resume inputs, call Pincaimao's mock-interview service, and continue the same conversation across interview rounds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends job descriptions, resumes, interview answers, and optional video data to Pincaimao for processing. <br>
Mitigation: Submit only data needed for the mock interview and avoid unnecessary personal or sensitive information. <br>
Risk: API keys, cos_key file references, and conversation_id values can expose authenticated access or interview context. <br>
Mitigation: Store the API key only in PCM_MOCK_INTERVIEW_KEY and treat returned file and conversation identifiers as sensitive. <br>
Risk: The skill relies on pincaimao-basic for shared upload, authentication, response, and streaming behavior. <br>
Mitigation: Review and install pincaimao-basic from a trusted source before using this skill. <br>


## Reference(s): <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao API base endpoint](https://api.pincaimao.com) <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-mock-interview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can show raw API answer content when the user asks for raw output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
