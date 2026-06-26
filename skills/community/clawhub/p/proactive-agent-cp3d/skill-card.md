## Description: <br>
Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a proactive assistant architecture with onboarding files, persistent memory practices, heartbeat checks, security guardrails, and self-improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and personal profiling can capture sensitive user context. <br>
Mitigation: Use a dedicated workspace, keep secrets and sensitive personal data out of memory files, and review USER.md, SOUL.md, MEMORY.md, and AGENTS.md changes. <br>
Risk: Proactive behavior and broad tool use can trigger actions beyond the user's intent. <br>
Mitigation: Require explicit approval before shell commands, browser automation, account access, crons, spawned agents, or external actions. <br>
Risk: Instruction and configuration files can alter future agent behavior. <br>
Mitigation: Review proposed updates to operating rules and memory files before relying on the modified agent behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/proactive-agent-cp3d) <br>
- [Onboarding Flow](references/onboarding-flow.md) <br>
- [Security Patterns](references/security-patterns.md) <br>
- [Author profile](https://x.com/halthelobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workspace file templates and a local security-audit shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter states 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
