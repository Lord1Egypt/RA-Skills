## Description: <br>
Transforms AI agents from task-followers into proactive partners that maintain memory, perform check-ins, verify work, and improve their own operating patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a proactive assistant that keeps durable local context, performs heartbeat-style maintenance, proposes useful work, and applies safety and verification routines before reporting completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persistent memory can retain personal details or work context without clear consent boundaries. <br>
Mitigation: Require explicit consent before saving personal details, disable automatic message logging until reviewed, and periodically delete or redact stored notes. <br>
Risk: Heartbeat and proactive behaviors may check email, calendar, files, apps, tabs, or cleanup targets without enough user involvement. <br>
Mitigation: Disable unattended email, calendar, app, tab, and file cleanup actions unless the user has intentionally authorized each workflow. <br>
Risk: Cron jobs, sub-agents, or BOOTSTRAP.md behavior could run background actions that the user has not reviewed. <br>
Mitigation: Review all BOOTSTRAP.md, cron, and sub-agent behavior before enabling the skill, and require approval before external actions or destructive changes. <br>


## Reference(s): <br>
- [Proactive Agent Jarvis on ClawHub](https://clawhub.ai/bingze00000/proactive-agent-jarvis) <br>
- [Publisher profile](https://clawhub.ai/user/bingze00000) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>
- [Hal 9001 profile](https://x.com/halthelobster) <br>
- [Bulletproof Memory](https://clawdhub.com/halthelobster/bulletproof-memory) <br>
- [PARA Second Brain](https://clawdhub.com/halthelobster/para-second-brain) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with file templates, checklists, JSON examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local operating instructions and templates for persistent memory, heartbeat checks, onboarding, safety review, and proactive agent behavior.] <br>

## Skill Version(s): <br>
3.1.1 (source: server release metadata and artifact/_meta.json; SKILL.md frontmatter says 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
