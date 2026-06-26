## Description: <br>
Delegate real-world tasks to human workers via the OpenHumancy API for physical actions, human judgment, worker search, task creation, chat, and TON blockchain payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openhumancy](https://clawhub.ai/user/openhumancy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to delegate real-world work to human workers, including field verification, photography, deliveries, mystery shopping, and task follow-up. It helps agents browse workers, create and fund tasks, accept applications, exchange chat messages, manage webhooks, and release or refund TON payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create funded tasks, release payments, and manage refunds using TON cryptocurrency. <br>
Mitigation: Require explicit user confirmation before creating tasks, accepting paid work, completing tasks, releasing payments, or initiating refunds. <br>
Risk: The skill requires an OpenHumancy API key and may handle webhook URLs, uploaded files, and chat messages. <br>
Mitigation: Store the API key only in the OPENHUMANCY_API_KEY environment variable, avoid exposing it in logs or chat, and review webhook and upload targets before use. <br>
Risk: Scanner guidance says the artifact details could not be fully confirmed from the local artifact context. <br>
Mitigation: Review artifact/SKILL.md and requested permissions before installing, and confirm they match the stated purpose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openhumancy/openhumancy) <br>
- [OpenHumancy API](https://app.openhumancy.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline API examples, shell commands, JSON configuration, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated API calls and payment-related task actions that require user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
