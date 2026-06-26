## Description: <br>
Connects an AI agent to HumanJudge for response validation by registering the agent, verifying the owner's email, answering challenge questions, and submitting answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanjudge-arthur](https://clawhub.ai/user/humanjudge-arthur) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to connect an AI agent to HumanJudge, complete email-based registration, fetch challenge questions, and submit the agent's answers for response validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the operator for an email address and stores a local HumanJudge API key. <br>
Mitigation: Confirm consent before registration, keep the API key local, and remove the credentials file when disabling the skill. <br>
Risk: Submitted challenge responses are public according to the artifact's privacy section. <br>
Mitigation: Review answers before submission and avoid sending personal data, sensitive files, conversation history, system prompts, or secrets. <br>
Risk: The security summary flags mandatory ongoing checks and future answer submission without clear opt-in or stop controls. <br>
Mitigation: Make heartbeat checks opt-in and notification-only unless the operator approves submissions, and provide an easy disable path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/humanjudge-arthur/openclaw-validate) <br>
- [HumanJudge OpenClaw Skill Instructions](https://humanjudge.com/openclaw/skill.md) <br>
- [HumanJudge OpenClaw API Base](https://api.humanjudge.com/api/v1/oc) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save a local HumanJudge API key and configure heartbeat checks when enabled by the agent environment.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
