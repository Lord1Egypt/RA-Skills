## Description: <br>
Project Manager Pro lets an OpenClaw agent create, organize, prioritize, decompose, export, and review local tasks and projects through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals using OpenClaw agents use this skill to manage personal tasks and projects in natural language, including task creation, prioritization, project breakdowns, proactive check-ins, and exports. It is intended for local task management rather than team collaboration, calendar scheduling, or time tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-run setup can execute a shell script that may install jq and prompt for sudo through the system package manager. <br>
Mitigation: Review scripts/setup.sh before running it, install jq manually when preferred, and run setup only after accepting any package-manager or sudo prompts. <br>
Risk: Tasks, projects, exports, and check-in data are stored as local plaintext files and can include sensitive personal, financial, fitness, meal, or content-planning details. <br>
Mitigation: Use disk encryption, restrict workspace access, handle exported files carefully, and keep cross-tool integrations disabled unless those details are appropriate for local plaintext and agent-visible context. <br>
Risk: Task data is processed by the user's configured LLM provider during normal agent conversations. <br>
Mitigation: Review the configured LLM provider's data policy and avoid storing highly sensitive tasks unless that provider and deployment configuration are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-project-manager-pro) <br>
- [README](artifact/README.md) <br>
- [Security considerations](artifact/SECURITY.md) <br>
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational text and Markdown, with JSON task data and optional Markdown, CSV, or JSON exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores tasks, projects, check-in logs, and exports as local plaintext files under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
