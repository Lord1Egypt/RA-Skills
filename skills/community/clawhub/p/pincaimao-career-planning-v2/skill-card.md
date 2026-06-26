## Description: <br>
聘才猫 - 职业规划助手 V2 Use when calling Pincaimao Career Planning Assistant V2 API to generate career advice based on a resume and advice type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to upload a resume to Pincaimao and request career advice for early-career planning, career transition, or promotion-path scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume contents and related user inputs are transmitted to api.pincaimao.com for processing. <br>
Mitigation: Use the skill only when that data sharing is acceptable, redact unnecessary personal details, and verify the resume path before invoking the API. <br>
Risk: The API key authorizes requests to the Pincaimao service. <br>
Mitigation: Use a dedicated PCM_CAREER_PLANNING_KEY and keep it in the environment rather than hardcoding or sharing it. <br>
Risk: Uploaded resume file references such as cos_key values may be sensitive. <br>
Mitigation: Treat returned file keys as sensitive and avoid exposing them in shared logs, prompts, or public output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-career-planning-v2) <br>
- [Pincaimao publisher profile](https://clawhub.ai/user/pincaimao) <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or raw API answer text, with bash examples for API invocation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PCM_CAREER_PLANNING_KEY, curl, python3, a resume file, and one advice type: 初入职场, 转型建议, or 晋升路径.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
