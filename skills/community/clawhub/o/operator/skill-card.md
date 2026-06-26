## Description: <br>
Manage your Operator fleet of AI agent instances: create, configure, monitor, message, and manage OpenClaw agents while handling authentication, instance lifecycle, secrets, automations, and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[promptrotator](https://clawhub.ai/user/promptrotator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Operator and OpenClaw agent fleets through authenticated CLI-style API requests, including instance lifecycle tasks, logs, agent messaging, secrets, automations, and webhooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evidence security summary reports suspicious behavior involving nested review tooling with full filesystem and command access by default. <br>
Mitigation: Install only after reviewing that authority, and prefer --no-yolo or AUTOREVIEW_YOLO=0 unless broader access is intentional. <br>
Risk: The skill guides authenticated API use and credential storage for Operator. <br>
Mitigation: Read credentials from the local config when needed, mask API keys in outputs, and reauthenticate on 401 responses instead of exposing raw tokens. <br>
Risk: The skill can guide actions that affect instances, files, secrets, automations, and webhooks. <br>
Mitigation: Review the requested operation and generated API command before execution, especially for destructive lifecycle changes or secret access changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/promptrotator/operator) <br>
- [Operator application](https://www.operator.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands, JSON snippets, SSE parsing examples, and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
