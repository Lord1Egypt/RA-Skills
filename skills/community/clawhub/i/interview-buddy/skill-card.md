## Description: <br>
AI-powered mock interview practice with real-time feedback for job interview preparation, behavioral questions, technical prep, mock interviews, and role-specific coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill through an OpenClaw agent to practice interviews, receive feedback on answers, and continue guided mock interview sessions for a chosen role, company, or interview type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends interview prompts and answers to ToolWeb's hosted interview-coaching service. <br>
Mitigation: Avoid sending confidential employer, customer, or highly personal details unless ToolWeb processing is acceptable for the use case. <br>
Risk: The skill requires a TOOLWEB_API_KEY and successful calls may count against quota or billing. <br>
Mitigation: Protect the API key, scope access to intended users, and monitor ToolWeb usage or billing limits. <br>
Risk: The skill depends on a third-party API and curl availability. <br>
Mitigation: Confirm TOOLWEB_API_KEY is configured, curl is installed, and ToolWeb service access is acceptable before relying on the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/interview-buddy) <br>
- [ToolWeb portal](https://portal.toolweb.in) <br>
- [Interview Buddy API endpoint](https://portal.toolweb.in/apis/tools/interview-buddy) <br>
- [ToolWeb platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with interview prompts, answer feedback, ratings, follow-up questions, configuration snippets, and curl command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may count against ToolWeb quota or billing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
