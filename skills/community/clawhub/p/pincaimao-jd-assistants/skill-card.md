## Description: <br>
聘才猫（Pincaimao）JD 助手 helps agents call the Pincaimao JD Assistant API to generate job postings from job descriptions and structured job tags from job titles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting teams and agents use this skill to generate readable job postings from role details and structured job tags from job titles through Pincaimao's authenticated API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hiring-related content, including job descriptions, resumes, or contract text, may be sent to Pincaimao for processing. <br>
Mitigation: Send only content your organization permits, avoid confidential or regulated data unless approved, and review Pincaimao's handling requirements before use. <br>
Risk: The skill depends on a dedicated PCM_JD_ASSISTANT_KEY and authenticated calls to the Pincaimao API. <br>
Mitigation: Use a dedicated key, keep it in the environment rather than source files, rotate it when needed, and verify requests target api.pincaimao.com. <br>
Risk: The skill requires the separate pincaimao-basic skill for shared API behavior such as authentication, response formats, and SSE parsing. <br>
Mitigation: Install and review pincaimao-basic before loading this skill so the agent applies the expected authentication and response-handling conventions. <br>


## Reference(s): <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao agent registration](https://www.pincaimao.com/agents/login?invite_code=uwqc) <br>
- [Pincaimao JD Assistant API endpoint](https://api.pincaimao.com/agents/v1/chat/chat-messages) <br>
- [ClawHub skill listing](https://clawhub.ai/pincaimao/pincaimao-jd-assistants) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bash examples, readable text responses, and JSON tag data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Raw API answers can be shown on request; job tag output requires parsing the answer field as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
