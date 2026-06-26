## Description: <br>
Transforms AI agents from task-followers into proactive partners that anticipate needs, preserve working memory, verify outcomes, and improve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure a proactive agent workflow with memory files, onboarding, heartbeat checks, reverse prompting, self-healing, and verification habits. It is intended for agents that may monitor context, propose actions, maintain notes, and generate supporting commands or configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the skill gives a proactive agent broad memory, monitoring, cleanup, and background-work authority without enough user control. <br>
Mitigation: Install only when that operating model is desired, restrict readable files and accounts, and require confirmation before cleanup, file moves, scheduled jobs, spawned agents, or email and calendar checks. <br>
Risk: The skill encourages persistent memory files that may capture sensitive personal, project, or account context. <br>
Mitigation: Review and delete generated memory files regularly, exclude secrets from notes, and keep credentials in separately protected stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/muguozi1-openclaw-proactive-agent) <br>
- [Onboarding flow reference](artifact/references/onboarding-flow.md) <br>
- [Security patterns reference](artifact/references/security-patterns.md) <br>
- [Author profile from ClawHub metadata](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline commands, checklists, file templates, and short code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory, onboarding, heartbeat, agent, tool, and user-context files when the operator enables those workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
