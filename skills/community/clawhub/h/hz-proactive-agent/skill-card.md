## Description: <br>
Transforms AI agents from task-followers into proactive partners that anticipate needs, maintain durable memory, verify work, and improve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lidekahdjdhdhsjjs-lang](https://clawhub.ai/user/lidekahdjdhdhsjjs-lang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure proactive behavior, durable memory, onboarding, heartbeat checks, and security review patterns for AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants a proactive agent broad memory, monitoring, cleanup, and autonomous-work authority without enough user control. <br>
Mitigation: Require explicit approval before email or calendar access, desktop or browser cleanup, trash operations, background agent turns, sub-agent spawning, or edits to operating files. <br>
Risk: The memory files can accumulate private user, project, or workflow data. <br>
Mitigation: Treat memory files as private data and review, prune, or delete them regularly. <br>
Risk: External content handled by the agent can contain prompt-injection attempts. <br>
Mitigation: Treat external content as data, isolate instructions from untrusted sources, and review or run the included security audit before deployment. <br>


## Reference(s): <br>
- [Huizai Proactive Agent on ClawHub](https://clawhub.ai/lidekahdjdhdhsjjs-lang/hz-proactive-agent) <br>
- [Project Homepage](https://github.com/lidekahdjdhdhsjjs-lang/Huizai-openclaw) <br>
- [Onboarding Flow Reference](references/onboarding-flow.md) <br>
- [Security Patterns Reference](references/security-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workspace asset templates and an optional security audit script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog describe upstream 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
